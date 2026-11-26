#!/usr/bin/env python3
"""Move medidas entre tabelas de um PBIP e reescreve as referências (só biblioteca padrão).

Uso:
    python mover_medidas.py "<Projeto>.SemanticModel/definition" "<Projeto>.Report/definition" mapa.json [--aplicar]

`mapa.json` diz para onde vai cada medida, pelo nome ou pela pasta de exibição:

    {
      "medidas": { "Faturado": "Vendas" },
      "pastas":  { "Faturado Δ": "Vendas", "Rodapé": "Atualização" }
    }

O nome tem prioridade sobre a pasta; a pasta vale também para as subpastas. O que não
está no mapa fica onde está. Sem `--aplicar` só ensaia.

O que muda: o bloco TMDL da medida (com a descrição `///` e o mesmo lineageTag) passa
para a tabela de destino; no DAX, referência qualificada a medida movida vira `[Medida]`;
no relatório, `Entity`, `queryRef`, `selector.metadata` e o `From` dos filtros passam a
apontar para o destino. A tabela que fica **vazia** (sem medida, coluna ou hierarquia e
sem outra referência) é excluída, com a linha `ref table` e o nome em `PBI_QueryOrder`:
o Desktop não carrega tabela sem coluna. Faça backup antes, feche o Power BI Desktop e,
depois, rode `check_visual_bindings.py`, abra o projeto, atualize e salve.
"""
import argparse
import json
import pathlib
import re
import subprocess
import sys

for _fluxo in (sys.stdout, sys.stderr):
    try:
        _fluxo.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

CRLF, LF, TAB = "\r\n", "\n", "\t"
MEDIDA = re.compile(r"^\tmeasure\s+('(?:[^']|'')+'|[^\s=]+)\s*=")
TABELA = re.compile(r"^table\s+('(?:[^']|'')+'|\S+)\s*$", re.M)


def sem_aspas(n):
    return n[1:-1].replace("''", "'") if n.startswith("'") else n


def ler(p):
    raw = p.read_text(encoding="utf-8-sig", newline="") if sys.version_info >= (3, 13) else open(p, encoding="utf-8-sig", newline="").read()
    return raw.replace(CRLF, LF), (CRLF if CRLF in raw else LF)


def gravar(p, texto, eol):
    with open(p, "w", encoding="utf-8", newline="") as f:
        f.write(texto.replace(LF, eol))


def blocos_de_medida(texto):
    """[(nome, início, fim, pasta)] em índices de linha; o bloco inclui o `///` acima."""
    linhas = texto.split(LF)
    saida, i = [], 0
    while i < len(linhas):
        m = MEDIDA.match(linhas[i])
        if not m:
            i += 1
            continue
        ini = i
        while ini > 0 and linhas[ini - 1].startswith(TAB + "///"):
            ini -= 1
        cerca = linhas[i].count("```") % 2 == 1
        j = i + 1
        while j < len(linhas):
            if cerca:
                cerca = linhas[j].count("```") % 2 == 0
                j += 1
                continue
            if linhas[j].strip() == "" or linhas[j].startswith(TAB * 2):
                cerca = linhas[j].count("```") % 2 == 1
                j += 1
                continue
            break
        pasta = next((x.split(":", 1)[1].strip() for x in linhas[i:j] if x.startswith(TAB * 2 + "displayFolder:")), "")
        saida.append((sem_aspas(m.group(1)), ini, j, pasta))
        i = j
    return saida


def destino(nome, pasta, mapa):
    if nome in mapa.get("medidas", {}):
        return mapa["medidas"][nome]
    partes = pasta.strip("\"'").split("\\")
    for k in range(len(partes), 0, -1):
        d = mapa.get("pastas", {}).get("\\".join(partes[:k]))
        if d:
            return d
    return None


def citada(nome, texto):
    """A tabela é usada no DAX, num relacionamento ou numa permissão deste TMDL (comentários não contam)."""
    n = re.escape(nome)
    aspas = "'" + re.escape(nome.replace("'", "''")) + "'"
    codigo = LF.join(x for x in texto.split(LF) if not x.lstrip().startswith(("///", "//", "--", "ref table")))
    codigo = re.sub(r"(?m)^annotation PBI_QueryOrder.*$", "", codigo)
    padrao = aspas + r"|(?<![\w'])" + n + r"\[|(?:Column|Table):\s*" + n + r"(?![\w])|\(\s*" + n + r"\s*[,)]"
    return bool(re.search(padrao, codigo))


def vazias(tabelas, outros, candidatas):
    """Candidatas que ficaram sem nada: (excluíveis, citadas em outro lugar)."""
    excluir, presas = [], []
    for o in sorted(candidatas):
        if re.search(r"(?m)^\t(measure|column|hierarchy|calculationGroup)\b", tabelas[o][1]):
            continue
        textos = [v[1] for t, v in tabelas.items() if t != o] + [t for t, _ in outros.values()]
        (presas if any(citada(o, t) for t in textos) else excluir).append(o)
    return excluir, presas


def tirar_do_modelo(texto, nome):
    """Remove `ref table` e o nome em PBI_QueryOrder do model.tmdl."""
    for forma in (nome, "'" + nome.replace("'", "''") + "'"):
        texto = re.sub(r"(?m)^ref table " + re.escape(forma) + r"[ \t]*\n", "", texto)

    def ordem(m):
        itens = [i for i in json.loads(m.group(2)) if i != nome]
        return m.group(1) + json.dumps(itens, ensure_ascii=False, separators=(",", ":"))

    return re.sub(r"(?m)^(annotation PBI_QueryOrder = )(\[.*\])[ \t]*$", ordem, texto)


def ponto_de_insercao(linhas):
    """Antes do primeiro objeto que não é medida (coluna, hierarquia, partição, anotação da tabela)."""
    for i, x in enumerate(linhas):
        if re.match(r"^\t(column|hierarchy|partition|calculationGroup|annotation)\b", x):
            while i > 0 and linhas[i - 1].startswith(TAB + "///"):
                i -= 1
            return i
    return len(linhas)


def reescrever_json(no, mudou, aliases=None):
    """Troca a tabela das medidas movidas em qualquer ponto do JSON. Devolve quantas trocas fez."""
    n = 0
    if isinstance(no, dict):
        if isinstance(no.get("From"), list):
            aliases = {f.get("Name"): f.get("Entity") for f in no["From"] if isinstance(f, dict)}
            origem = no["From"]
        else:
            origem = None
        med = no.get("Measure")
        if isinstance(med, dict):
            ref = med.get("Expression", {}).get("SourceRef", {})
            prop = med.get("Property")
            if (ref.get("Entity"), prop) in mudou:
                ref["Entity"] = mudou[(ref["Entity"], prop)]
                n += 1
        for k, v in list(no.items()):
            if isinstance(v, str):
                for (orig, nome), dest in mudou.items():
                    if v == f"{orig}.{nome}":
                        no[k] = f"{dest}.{nome}"
                        n += 1
            else:
                n += reescrever_json(v, mudou, aliases)
        if origem is not None:
            n += ajustar_aliases(no, origem, mudou)
    elif isinstance(no, list):
        for i, v in enumerate(no):
            if isinstance(v, str):
                for (orig, nome), dest in mudou.items():
                    if v == f"{orig}.{nome}":
                        no[i] = f"{dest}.{nome}"
                        n += 1
            else:
                n += reescrever_json(v, mudou, aliases)
    return n


def ajustar_aliases(consulta, origem, mudou):
    """Filtros usam `SourceRef.Source` (apelido): cria o apelido da tabela de destino no `From`."""
    entidade = {f.get("Name"): f.get("Entity") for f in origem}
    n = 0

    def andar(x):
        nonlocal n
        if isinstance(x, dict):
            med = x.get("Measure")
            if isinstance(med, dict):
                ref = med.get("Expression", {}).get("SourceRef", {})
                dest = mudou.get((entidade.get(ref.get("Source")), med.get("Property")))
                if dest:
                    apelido = next((f["Name"] for f in origem if f.get("Entity") == dest), None)
                    if not apelido:
                        apelido = f"md{len(origem)}"
                        origem.append({"Name": apelido, "Entity": dest, "Type": 0})
                        entidade[apelido] = dest
                    ref["Source"] = apelido
                    n += 1
            for k, v in x.items():
                if k != "From":
                    andar(v)
        elif isinstance(x, list):
            for v in x:
                andar(v)

    andar(consulta)
    return n


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("modelo")
    ap.add_argument("relatorio")
    ap.add_argument("mapa")
    ap.add_argument("--aplicar", action="store_true")
    a = ap.parse_args()
    if a.aplicar and sys.platform == "win32" and b"PBIDesktop" in subprocess.run(["tasklist"], capture_output=True).stdout:
        sys.exit("Power BI Desktop aberto: feche sem salvar antes de aplicar")
    mapa = json.load(open(a.mapa, encoding="utf-8-sig"))
    raiz = pathlib.Path(a.modelo)
    tabelas = {}
    for p in sorted((raiz / "tables").glob("*.tmdl")):
        texto, eol = ler(p)
        m = TABELA.search(texto)
        if m:
            tabelas[sem_aspas(m.group(1))] = [p, texto, eol]

    mudou, movidos, ficaram = {}, {}, []
    for nome_t, (p, texto, eol) in tabelas.items():
        linhas = texto.split(LF)
        retirar = []
        for nome, ini, fim, pasta in blocos_de_medida(texto):
            d = destino(nome, pasta, mapa)
            if not d or d == nome_t:
                ficaram.append((nome_t, nome))
                continue
            if d not in tabelas:
                sys.exit(f"tabela de destino inexistente: {d} (medida {nome})")
            bloco = linhas[ini:fim]
            while bloco and not bloco[-1].strip():
                bloco.pop()
            movidos.setdefault(d, []).append(bloco)
            retirar.append((ini, fim))
            mudou[(nome_t, nome)] = d
        for ini, fim in reversed(retirar):
            del linhas[ini:fim]
        tabelas[nome_t][1] = LF.join(linhas)
    for d, blocos in movidos.items():
        linhas = tabelas[d][1].split(LF)
        i = ponto_de_insercao(linhas)
        novo = [x for b in blocos for x in b + [""]]
        if i > 0 and linhas[i - 1].strip():
            novo = [""] + novo
        linhas[i:i] = novo
        tabelas[d][1] = LF.join(linhas)

    # referência qualificada a medida ('Tabela'[Medida]) vira [Medida]
    outros = {p: ler(p) for p in raiz.rglob("*.tmdl") if p not in [v[0] for v in tabelas.values()]}
    qualificadas = 0
    for (orig, nome) in mudou:
        padrao = re.compile(r"(?:'" + re.escape(orig.replace("'", "''")) + r"'|(?<![\w'])" + re.escape(orig) + r")\[" + re.escape(nome) + r"\]")
        for v in tabelas.values():
            v[1], q = padrao.subn(f"[{nome}]", v[1])
            qualificadas += q

    visuais, trocas = [], 0
    for p in pathlib.Path(a.relatorio).rglob("*.json"):
        texto, eol = ler(p)
        dados = json.loads(texto)
        n = reescrever_json(dados, mudou)
        if n:
            visuais.append((p, json.dumps(dados, ensure_ascii=False, indent=2) + (LF if texto.endswith(LF) else ""), eol))
            trocas += n

    print(f"{len(mudou)} medida(s) a mover; {len(ficaram)} ficam onde estão")
    for d, blocos in movidos.items():
        print(f"    {len(blocos):3} para {d}")
    print(f"{len(visuais)} arquivo(s) do relatório com {trocas} referência(s); {qualificadas} referência(s) qualificada(s) no DAX")
    # inclui a tabela de medidas que já tinha ficado vazia numa execução anterior
    candidatas = {o for o, _ in mudou} | {t for t, v in tabelas.items() if re.search(r"#table\(\s*\{\s*\}", v[1])}
    excluir, presas = vazias(tabelas, outros, candidatas)
    for o in excluir:
        print(f"tabela vazia a excluir: {o}")
    for o in presas:
        print(f"ATENÇÃO: {o} ficou vazia mas é citada no modelo; resolva à mão (o Desktop não carrega tabela sem coluna)")
    modelo_tmdl = raiz / "model.tmdl"
    novo_modelo = None
    if excluir and modelo_tmdl in outros:
        novo_modelo = outros[modelo_tmdl][0]
        for o in excluir:
            novo_modelo = tirar_do_modelo(novo_modelo, o)
    sobras = [str(p.relative_to(raiz)) for p, (t, _) in outros.items() if p != modelo_tmdl for o in excluir if o in t]
    if sobras:
        print("conferir à mão (citam a tabela excluída, ex.: sinônimos ou perspectivas):", sorted(set(sobras)))
    if not a.aplicar:
        print("ENSAIO: nada foi gravado (use --aplicar)")
        return
    for nome_t, (p, texto, eol) in tabelas.items():
        if nome_t in excluir:
            p.unlink()
        elif ler(p)[0] != texto:
            gravar(p, texto, eol)
    if novo_modelo is not None:
        gravar(modelo_tmdl, novo_modelo, outros[modelo_tmdl][1])
    for p, texto, eol in visuais:
        gravar(p, texto, eol)
    print("APLICADO. Rode check_visual_bindings.py e abra o projeto no Desktop.")


if __name__ == "__main__":
    main()
