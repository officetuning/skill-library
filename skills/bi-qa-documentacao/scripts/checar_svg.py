#!/usr/bin/env python3
"""Checa medidas que desenham cena em SVG (só biblioteca padrão).

Uso:
    python checar_svg.py "<Projeto>.SemanticModel/definition" ["<Projeto>.Report/definition"]

Medida SVG é a que tem `data:image/svg+xml` ou `<svg` numa cadeia. Achados:

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
    return any("data:image/svg+xml" in c or "<svg" in c.lower() for c in cadeias)


def analisar_medida(expressao: str, props: dict) -> list[tuple[str, str]]:
    codigo, cadeias = separar(expressao)
    if not e_svg(cadeias):
        return []
    achados = []
    if any("data:image/svg+xml" in c for c in cadeias) and props.get("dataCategory") != "ImageUrl":
        achados.append(("erro", "sem-imageurl"))
    if any(";base64," in c for c in cadeias):
        return achados
    trocas = [[literal(a, cadeias) for a in args[1:3]] for _, args in chamadas(codigo, "SUBSTITUTE")]
    if any(HEX.search(c) for c in cadeias) and ["#", "%23"] not in trocas:
        achados.append(("erro", "cerquilha"))
    if any(PORCENTO.search(c) for c in cadeias) and not any(t[-1:] == ["%25"] for t in trocas):
        achados.append(("erro", "porcento"))
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
    nomes, achados = set(), []
    for tabela in modelo["tabelas"]:
        for medida in tabela["medidas"]:
            if e_svg(separar(medida["expressao"])[1]):
                nomes.add(medida["nome"])
                achados += [(n, c, medida["nome"]) for n, c in analisar_medida(medida["expressao"], medida["props"])]
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
