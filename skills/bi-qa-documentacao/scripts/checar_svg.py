#!/usr/bin/env python3
"""Checa medidas que desenham cena em SVG (só biblioteca padrão).

Uso:
    python checar_svg.py "<Projeto>.SemanticModel/definition" ["<Projeto>.Report/definition"]

Medida SVG é a que tem `data:image/svg+xml` ou `<svg` numa cadeia, ou chama uma função
DAX do modelo que desenha SVG (`definition/functions.tmdl`) ou a `DaxLib.SVG.*`. O corpo das
funções próprias passa pelas mesmas regras; o das bibliotecas `DaxLib.*` não é auditado.
HTML com `<svg>` embutido (visual de HTML, sem data URI) não precisa de escape e fica de fora.
Um SUBSTITUTE só isenta o texto que passa por ele. Achados:

  erro      sem-imageurl  devolve data URI e não tem `dataCategory: ImageUrl`
  erro      cerquilha     `#` de cor ou `url(#` sem virar `%23`
  erro      porcento      `%` sem virar `%25`
  conferir  virgula       FORMAT com casas decimais sem trocar a vírgula (em pt-BR quebra
                          o atributo do SVG; em texto visível pode ser intencional)
  erro      sem-alt       visual que usa a medida sem texto alternativo (pede a pasta do relatório)

Não detecta número convertido em texto sem FORMAT, nem cor vinda de outra medida: abra o
relatório em pt-BR. Data URI em base64 não precisa de escape. Sai com código 1 se houver
"erro"; itens a conferir não reprovam.
"""
import argparse
import json
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import tmdl_parser as tp  # noqa: E402
from auditar_visuais import obj, texto_ligado  # noqa: E402

for _fluxo in (sys.stdout, sys.stderr):
    try:
        _fluxo.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# comentário | cadeia | 'tabela' | [campo]: a ordem decide o que "esconde" o quê
TOKEN = re.compile(
    r"""(?P<com>--[^\n]*|//[^\n]*|/\*.*?\*/)|(?P<cad>"(?:[^"]|"")*")|(?P<nome>'(?:[^']|'')*'|\[(?:[^\]]|\]\])*\])""",
    re.S,
)
MARCA = re.compile(r"§(\d+)§")
HEX = re.compile(r"#[0-9A-Fa-f]{3,8}(?![0-9A-Za-z])|url\(#")
PORCENTO = re.compile(r"%(?![0-9A-Fa-f]{2})")
HTML = re.compile(r"<(div|span|br|p|table)\b", re.I)
FUNCAO = re.compile(r"^\s*function\s+(?P<nome>'(?:[^']|'')+'|[^\s=]+)\s*=\s*(?P<corpo>.*?)\s*$")


def separar(expressao):
    """Devolve (código sem comentários nem nomes, com §i§ no lugar das cadeias; cadeias)."""
    cadeias = []

    def troca(m):
        if m["com"]:
            return " "
        if m["nome"]:
            return " _ "
        cadeias.append(m["cad"][1:-1].replace('""', '"'))
        return f"§{len(cadeias) - 1}§"

    return TOKEN.sub(troca, expressao or ""), cadeias


def chamadas(codigo, funcao):
    """(início, [argumentos]) de cada chamada de `funcao`."""
    for m in re.finditer(r"(?<![\w.])" + funcao + r"\s*\(", codigo, re.I):
        nivel, argumentos, ini = 0, [], m.end()
        for i in range(m.end(), len(codigo)):
            ch = codigo[i]
            if ch in "({":
                nivel += 1
            elif ch in ")}" and nivel:
                nivel -= 1
            elif ch == ")":
                argumentos.append(codigo[ini:i].strip())
                break
            elif ch == "," and not nivel:
                argumentos.append(codigo[ini:i].strip())
                ini = i + 1
        yield m.start(), argumentos


def literal(argumento, cadeias):
    m = MARCA.fullmatch(argumento)
    return cadeias[int(m[1])] if m else None


def e_svg(cadeias):
    """SVG próprio ou data URI. HTML com `<svg>` embutido (visual de HTML) fica de fora."""
    if any("data:image/svg+xml" in c for c in cadeias):
        return True
    if any(HTML.search(c) for c in cadeias):
        return False
    return any("<svg" in c.lower() for c in cadeias)


def ler_funcoes(definicao) -> dict[str, str]:
    """{nome: corpo} das funções DAX do usuário em `definition/functions.tmdl`."""
    arquivo = pathlib.Path(definicao) / "functions.tmdl"
    funcoes, nome, nivel, cerca = {}, None, 0, False
    if not arquivo.exists():
        return funcoes
    for linha in arquivo.read_text(encoding="utf-8-sig").splitlines():
        limpa = linha.strip()
        if cerca:
            if limpa == "```":
                cerca, nome = False, None
            else:
                funcoes[nome] += linha + "\n"
            continue
        m = FUNCAO.match(linha)
        if m:
            nome, nivel = m["nome"].strip("'").replace("''", "'"), tp._indent(linha)
            cerca = m["corpo"] == "```"
            funcoes[nome] = "" if cerca else m["corpo"] + "\n"
        elif nome and (not limpa or tp._indent(linha) > nivel + 1):
            funcoes[nome] += linha + "\n"
        else:
            nome = None
    return funcoes


def chamadas_de_funcao(codigo, funcoes):
    """Nomes de função (do modelo ou da DaxLib.SVG) chamados no código mascarado."""
    achadas = {m[1] for m in re.finditer(r"(?<![\w.])(DaxLib\.SVG\.[\w.]+)\s*\(", codigo)}
    return achadas | {f for f in funcoes if re.search(r"(?<![\w.])" + re.escape(f) + r"\s*\(", codigo)}


def classificar_funcoes(funcoes):
    """(funções que desenham SVG, funções que devolvem data URI), seguindo as chamadas."""
    partes = {f: separar(corpo) for f, corpo in funcoes.items()}
    desenham = {f for f, (_, cad) in partes.items() if e_svg(cad)}
    uri = {f for f, (_, cad) in partes.items() if any("data:image/svg+xml" in c for c in cad)}
    uri.add("DaxLib.SVG.SVG")
    for _ in range(len(funcoes)):
        for f, (codigo, _c) in partes.items():
            usadas = chamadas_de_funcao(codigo, funcoes)
            if usadas & uri:
                uri.add(f)
            if usadas & desenham or any(u.startswith("DaxLib.SVG.") for u in usadas):
                desenham.add(f)
    return desenham | uri, uri


def alcancadas(inicio, funcoes):
    """Funções do modelo chamadas, direta ou indiretamente, a partir de `inicio`."""
    vistas, fila = set(), list(inicio)
    while fila:
        f = fila.pop()
        if f in funcoes and f not in vistas:
            vistas.add(f)
            fila += chamadas_de_funcao(separar(funcoes[f])[0], funcoes)
    return vistas


def cobertas(codigo, procurado, novo):
    """Índices das cadeias que passam por SUBSTITUTE(..., procurado, novo), inclusive via VAR."""
    blocos = re.split(r"\b(?=VAR\s|RETURN\b)", codigo)
    variaveis = {m[1]: b[m.end():] for b in blocos if (m := re.match(r"VAR\s+(\w+)\s*=", b))}
    fila = []
    for _, args in chamadas(codigo, "SUBSTITUTE"):
        if len(args) > 2 and args[2] in novo and args[1] in procurado:
            fila.append(args[0])
    indices, vistas = set(), set()
    while fila:
        trecho = fila.pop()
        indices |= {int(i) for i in MARCA.findall(trecho)}
        for nome in set(re.findall(r"\w+", trecho)) & set(variaveis) - vistas:
            vistas.add(nome)
            fila.append(variaveis[nome])
    return indices


def analisar_medida(expressao: str, props: dict, pedaco: bool = False) -> list[tuple[str, str]]:
    """`pedaco`: corpo de função chamada por uma cena, mesmo sem `<svg` próprio."""
    codigo, cadeias = separar(expressao)
    if not (pedaco or e_svg(cadeias)):
        return []
    achados = []
    if any("data:image/svg+xml" in c for c in cadeias) and props.get("dataCategory") != "ImageUrl":
        achados.append(("erro", "sem-imageurl"))
    if any(";base64," in c for c in cadeias):
        return achados
    substituicoes = [args for _, args in chamadas(codigo, "SUBSTITUTE") if len(args) > 2]
    procuradas = {int(i) for args in substituicoes for i in MARCA.findall(args[1])}
    for nome, padrao, de, para in (("cerquilha", HEX, "#", "%23"), ("porcento", PORCENTO, "%", "%25")):
        marcas = lambda texto: {f"§{i}§" for i, c in enumerate(cadeias) if c == texto}  # noqa: E731
        isentas = procuradas | cobertas(codigo, marcas(de), marcas(para))
        if any(padrao.search(c) for i, c in enumerate(cadeias) if i not in isentas):
            achados.append(("erro", nome))
    for inicio, args in chamadas(codigo, "FORMAT"):
        formato = literal(args[1], cadeias) if len(args) > 1 else None
        if not formato or not re.search(r"\.[0#]", formato):
            continue
        if len(args) > 2 and (literal(args[2], cadeias) or "").lower() == "en-us":
            continue
        if re.search(r"SUBSTITUTE\s*\(\s*$", codigo[:inicio], re.I):
            continue
        achados.append(("conferir", "virgula"))
        break
    return achados


def _usa(no, nomes):
    """Nomes de medida (entre `nomes`) referenciados em qualquer ponto do JSON."""
    achados = set()
    if isinstance(no, dict):
        medida = no.get("Measure")
        if isinstance(medida, dict) and medida.get("Property") in nomes:
            achados.add(medida["Property"])
        for v in no.values():
            achados |= _usa(v, nomes)
    elif isinstance(no, list):
        for v in no:
            achados |= _usa(v, nomes)
    return achados


def visuais_sem_alt(relatorio: pathlib.Path, nomes: set[str]) -> list[str]:
    saida = []
    for arquivo in sorted(pathlib.Path(relatorio).glob("pages/*/visuals/*/visual.json")):
        j = json.loads(arquivo.read_text(encoding="utf-8-sig"))
        vv = j.get("visual") or {}
        usadas = _usa(j, nomes)
        if not usadas or texto_ligado(obj(vv.get("visualContainerObjects") or {}, "general").get("altText")):
            continue
        pagina = arquivo.parents[2] / "page.json"
        titulo = (json.loads(pagina.read_text(encoding="utf-8-sig")).get("displayName") if pagina.exists()
                  else arquivo.parents[2].name)
        saida.append(f"{titulo} / {vv.get('visualType')} / {j.get('name', '')[:6]} ({', '.join(sorted(usadas))})")
    return saida


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("modelo")
    ap.add_argument("relatorio", nargs="?")
    a = ap.parse_args()
    if a.relatorio and not (pathlib.Path(a.relatorio) / "pages").is_dir():
        raise SystemExit(f"Pasta 'pages' não encontrada em {a.relatorio}. Aponte para <Projeto>.Report/definition.")
    modelo = tp.parse_model(pathlib.Path(a.modelo))
    funcoes = ler_funcoes(a.modelo)
    desenham, devolvem_uri = classificar_funcoes(funcoes)
    nomes, achados, usadas = set(), [], set()
    for tabela in modelo["tabelas"]:
        for medida in tabela["medidas"]:
            codigo, cadeias = separar(medida["expressao"])
            chama = chamadas_de_funcao(codigo, funcoes)
            via_funcao = {f for f in chama if f in desenham or f.startswith("DaxLib.SVG.")}
            if not (e_svg(cadeias) or via_funcao):
                continue
            nomes.add(medida["nome"])
            usadas |= chama
            proprios = analisar_medida(medida["expressao"], medida["props"])
            if chama & devolvem_uri and medida["props"].get("dataCategory") != "ImageUrl":
                proprios = [("erro", "sem-imageurl")] + [x for x in proprios if x[1] != "sem-imageurl"]
            achados += [(n, c, medida["nome"]) for n, c in proprios]
    # as bibliotecas de terceiros (DaxLib) não são auditadas
    for f in sorted((alcancadas(usadas, funcoes) | (desenham & set(funcoes)))):
        if not f.startswith("DaxLib."):
            achados += [(n, c, f"função {f}") for n, c in
                        analisar_medida(funcoes[f], {"dataCategory": "ImageUrl"}, pedaco=True)]
    if a.relatorio:
        achados += [("erro", "sem-alt", v) for v in visuais_sem_alt(pathlib.Path(a.relatorio), nomes)]
    else:
        print("sem a pasta do relatório: texto alternativo não conferido")
    for nivel, codigo, onde in achados:
        print(f"## {nivel} {codigo}: {onde}")
    erros = sum(n == "erro" for n, _, _ in achados)
    print(f"\n{len(nomes)} medida(s) SVG; {erros} erro(s); {len(achados) - erros} a conferir.")
    sys.exit(1 if erros else 0)


if __name__ == "__main__":
    main()
