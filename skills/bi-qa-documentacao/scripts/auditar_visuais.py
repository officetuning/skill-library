#!/usr/bin/env python3
"""Audita o relatório PBIR contra as regras da skill (só biblioteca padrão).

Uso:
    python auditar_visuais.py "<Projeto>.Report/definition" [--tema "<pasta do Builder>/<H1> - Tema.json"]
        [--coluna-data "Data Referência,Data"] [--entidade-calendario Calend]
        [--campo-tempo "Tempo de Casa"]

Pressupõe um relatório montado com o Background Builder (página 1920×1080, cartão de
Grandes Números com 1500 px ou mais de largura, segmentações em Suspenso e data
relativa na barra lateral). Os três parâmetros adaptam a auditoria do eixo de tempo
ao modelo: nome(s) da coluna de data das segmentações, trecho do nome da tabela de
datas e campos de "tempo decorrido" (ex.: Tempo de Casa) que também contam como eixo.

Lê todos os `visual.json` e `page.json` e imprime, por regra, o que está fora do
padrão. Sai com código 1 se houver pendência "fixa" (as marcadas com [decidir] são
perguntas ao autor, não erros). Regras cobertas:

  alt text ausente · unidade de exibição ≠ Nenhum · rosca sem `value` · segmentação
  (cabeçalho, fundo, borda, Pesquisar, barra de destaque, data relativa com DateSpan
  e fontes 12) · tabela e matriz (título, subtítulo, BoldHeader, growToFit, projeção sem
  `active:false`, cabeçalho
  de coluna e de linha na cor do tema) · cartão largo (altura 168 sem / 240 com
  etiquetas de referência, ícones, tamanho do ícone ≈ 53 px, preenchimento 10,
  espaço acima do divisor 4) · gráfico com eixo de tempo (Calendário ou Tempo de Casa)
  sem decisão de interação [decidir] · grade de 8 px (fora de Dicas) · gauge e pizza
  [decidir] · visual R/Python · tema registrado ≠ tema da Ficha (com --tema).
"""
import argparse
import collections
import glob
import json
import os
import re
import sys


# Saída em UTF-8 mesmo em console cp1252 (Windows) ou com `python -I`.
for _fluxo in (sys.stdout, sys.stderr):
    try:
        _fluxo.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def L(x):
    try:
        return x["expr"]["Literal"]["Value"]
    except Exception:
        return None


def obj(o, k):
    return (o.get(k) or [{}])[0].get("properties", {})


def campos(vv):
    out = []
    for papel, r in vv.get("query", {}).get("queryState", {}).items():
        for p in r["projections"]:
            k = list(p["field"])[0]
            f = p["field"][k]
            out.append((papel, k, f["Expression"]["SourceRef"].get("Entity"), f["Property"]))
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("definicao")
    ap.add_argument("--tema")
    ap.add_argument("--coluna-data", default="Data Referência,Data", help="coluna(s) de data das segmentações, separadas por vírgula")
    ap.add_argument("--entidade-calendario", default="Calend", help="trecho do nome da tabela de datas")
    ap.add_argument("--campo-tempo", default="Tempo de Casa", help="campos de tempo decorrido, separados por vírgula")
    a = ap.parse_args()
    R = a.definicao.rstrip("/\\") + "/"
    col_data = {x.strip() for x in a.coluna_data.split(",")}
    campos_tempo = {x.strip() for x in a.campo_tempo.split(",")}
    paginas = {}
    for pf in glob.glob(R + "pages/*/page.json"):
        paginas[os.path.basename(os.path.dirname(pf))] = json.load(open(pf, encoding="utf-8"))
    achados = collections.defaultdict(list)
    decidir = collections.defaultdict(list)

    for pid, pj in paginas.items():
        pn = pj["displayName"]
        dica = pj.get("type") == "Tooltip"
        vs = []
        for vf in glob.glob(R + f"pages/{pid}/visuals/*/visual.json"):
            vs.append(json.load(open(vf, encoding="utf-8")))
        slic_data = [j["name"] for j in vs if j.get("visual", {}).get("visualType") == "slicer"
                     and any(c[3] in col_data for c in campos(j["visual"]))]
        nofilter = {(i["source"], i["target"]) for i in pj.get("visualInteractions", []) if i.get("type") == "NoFilter"}
        for j in vs:
            vv = j.get("visual")
            if not vv:
                continue
            t = vv["visualType"]
            pos = j["position"]
            tag = f"{pn} / {t} / {j['name'][:6]}"
            o = vv.get("objects", {})
            c = vv.get("visualContainerObjects", {})
            s = json.dumps(j, ensure_ascii=False)
            # cartão de uma medida sobre balão de arte (largura < 400) segue a arte, não a grade
            sobre_arte = t == "cardVisual" and pos["width"] < 400
            if not dica and not sobre_arte:
                for k in ("x", "y", "width", "height"):
                    if round(pos[k], 1) % 8:
                        achados["fora da grade de 8 px"].append(f"{tag} {k}={round(pos[k], 1)}")
                        break
            alt = L(obj(c, "general").get("altText", {})) if c.get("general") else None
            if t not in ("textbox", "shape") and not (alt and alt != "''"):
                achados["sem texto alternativo"].append(tag)
            for m in re.finditer(r'"(labelDisplayUnits|valueDisplayUnits|dataLabelDisplayUnits)": \{\s*"expr": \{\s*"Literal": \{\s*"Value": "([^"]+)"', s):
                if m.group(2) != "1D":
                    achados["unidade de exibição ≠ Nenhum"].append(f"{tag} {m.group(2)}")
            if t == "donutChart" and (not o.get("value") or L(obj(o, "value").get("labelDisplayUnits", {})) != "1D"):
                achados["rosca: valor central sem unidade Nenhum"].append(tag)
            if t in ("scriptVisual", "pythonVisual"):
                achados["visual R/Python (descontinuado)"].append(tag)
            if t in ("gauge", "pieChart"):
                decidir["[decidir] gauge ou pizza (repete um cartão? mais de 4 fatias?)"].append(tag)
            # segmentações
            if t == "slicer":
                prop = campos(vv)[0][3]
                modo = L(obj(o, "data").get("mode", {}))
                if L(obj(o, "header").get("show", {})) != "false":
                    achados["segmentação com cabeçalho"].append(tag)
                if L(obj(c, "background").get("show", {})) != "false":
                    achados["segmentação com fundo"].append(tag)
                if L(obj(c, "border").get("show", {})) != "false":
                    achados["segmentação com borda"].append(tag)
                if modo == "'Dropdown'":
                    if L(obj(o, "general").get("selfFilterEnabled", {})) != "true":
                        achados["segmentação de texto sem Pesquisar"].append(f"{tag} {prop}")
                    if L(obj(o, "dropdown").get("accentBarShow", {})) != "false":
                        achados["segmentação de texto com barra de destaque"].append(f"{tag} {prop}")
                elif modo == "'RelativeDatePicker'":
                    if "DateSpan" not in s:
                        achados["segmentação de data relativa sem o filtro (DateSpan)"].append(tag)
                    if L(obj(o, "relativeText").get("fontSize", {})) != "12D" or L(obj(o, "dateRangeText").get("fontSize", {})) != "12D":
                        achados["segmentação de data sem fontes 12 (Intervalo e Resumo)"].append(tag)
                else:
                    achados[f"segmentação em modo {modo}"].append(f"{tag} {prop}")
            # tabelas e matrizes
            if t in ("tableEx", "pivotTable"):
                if not c.get("title") or L(obj(c, "title").get("show", {})) != "true":
                    decidir["[decidir] tabela/matriz sem título (ok se o nicho já nomeia)"].append(tag)
                sp = L(obj(c, "stylePreset").get("name", {})) if c.get("stylePreset") else None
                if sp != "'BoldHeader'":
                    achados["estilo da tabela ≠ BoldHeader"].append(f"{tag} {sp}")
                ch = obj(o, "columnHeaders")
                if L(ch.get("columnAdjustment", {})) != "'growToFit'":
                    achados["tabela sem growToFit"].append(tag)
                if "backColor" not in ch:
                    achados["cabeçalho de coluna sem cor do tema"].append(tag)
                for pr in vv.get("query", {}).get("queryState", {}).get("Values", {}).get("projections", []):
                    if pr.get("active") is False:
                        achados["projeção com active:false (Desktop mostra só a 1ª coluna)"].append(tag)
                        break
                if t == "pivotTable" and "backColor" not in obj(o, "rowHeaders"):
                    achados["cabeçalho de linha da matriz sem cor do tema"].append(tag)
            # cartões largos
            if t == "cardVisual" and pos["width"] >= 1500:
                tem_ref = bool(o.get("referenceLabel"))
                esperado = 240 if tem_ref else 168
                if pos["height"] != esperado:
                    achados["cartão largo com altura fora do padrão (168 sem / 240 com referência)"].append(f"{tag} h={int(pos['height'])} esperado {esperado}")
                n = len(vv["query"]["queryState"]["Data"]["projections"])
                bloco = (pos["width"] - 32) / n
                imgs = o.get("image", [])
                if not imgs:
                    achados["cartão largo sem ícones"].append(tag)
                else:
                    areas = [L(e["properties"].get("imageAreaSize", {})) for e in imgs]
                    areas = [int(x.rstrip("L")) for x in areas if x]
                    if areas:
                        px = bloco * areas[0] / 100
                        if not 45 <= px <= 62:
                            achados["ícone do cartão fora de ~53 px"].append(f"{tag} {px:.0f} px")
                pad = [e for e in o.get("layout", []) if e.get("selector", {}).get("id") == "default"]
                if not pad or L(pad[0]["properties"].get("paddingUniform", {})) not in ("10L",):
                    achados["cartão largo sem preenchimento interno 10"].append(tag)
                if tem_ref and L(obj(c, "spacing").get("spaceAboveDivider", {})) not in ("4D",):
                    achados["cartão com referência: espaço acima do divisor ≠ 4"].append(tag)
            # eixo de tempo
            if t not in ("slicer", "cardVisual", "textbox", "image", "pageNavigator", "actionButton") and not dica:
                eixo = [f for f in campos(vv) if f[0] in ("Category", "Series", "Rows", "Columns", "Axis", "Values") and
                        (f[2] and a.entidade_calendario in f[2] or f[3] in campos_tempo and f[0] in ("Category", "Axis", "Rows", "Columns"))]
                eixo = [f for f in eixo if f[0] != "Values" or f[3] == "Ano"]
                if eixo and slic_data:
                    ign = any((sd, j["name"]) in nofilter for sd in slic_data)
                    nomes = ",".join(sorted({f[3] for f in eixo}))
                    decidir["[decidir] eixo de tempo (" + ("ignora" if ign else "RESPEITA") + " a segmentação de data)"].append(f"{tag} [{nomes}]")

    # tema
    if a.tema:
        rep = json.load(open(R + "report.json", encoding="utf-8"))
        nome = rep.get("themeCollection", {}).get("customTheme", {}).get("name")
        reg = glob.glob(os.path.dirname(R.rstrip("/\\")) + "/StaticResources/RegisteredResources/" + (nome or "-"))
        if reg:
            tr = json.load(open(reg[0], encoding="utf-8"))
            tf = json.load(open(a.tema, encoding="utf-8"))
            if tr.get("dataColors", [])[:8] != tf.get("dataColors", [])[:8]:
                achados["tema registrado no relatório ≠ Tema.json da Ficha"].append(f"{nome}: {tr.get('dataColors', [])[:3]} × {tf.get('dataColors', [])[:3]}")

    print(f"{len(paginas)} páginas auditadas\n")
    fixos = 0
    for k, v in achados.items():
        print(f"## {k} ({len(v)})")
        for x in v[:12]:
            print("   ", x)
        if len(v) > 12:
            print("    ...")
        fixos += len(v)
    for k, v in decidir.items():
        print(f"## {k} ({len(v)})")
        for x in v[:12]:
            print("   ", x)
    print(f"\n{fixos} pendência(s) fixa(s); itens [decidir] são perguntas ao autor.")
    sys.exit(1 if fixos else 0)


if __name__ == "__main__":
    main()
