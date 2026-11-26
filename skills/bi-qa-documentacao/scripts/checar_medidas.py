#!/usr/bin/env python3
"""Acusa medidas concentradas em tabela só de medidas (só biblioteca padrão).

Uso:
    python checar_medidas.py "<Projeto>.SemanticModel/definition" [--minimo 5]

A orientação de modelagem é distribuir as medidas pelas tabelas a que pertencem e
organizá-las por pasta de exibição ("Distribute measures across relevant tables",
microsoft/skills-for-fabric, semantic-model-authoring). Uma tabela é tratada como
"só de medidas" quando guarda pelo menos --minimo medidas e não tem coluna visível.
Sai com código 1 se encontrar alguma. Para mover, use `mover_medidas.py`.
"""
import argparse
import collections
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import tmdl_parser as tp  # noqa: E402

for _fluxo in (sys.stdout, sys.stderr):
    try:
        _fluxo.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def oculta(coluna):
    return "isHidden" in coluna.get("props", {}) or coluna.get("oculta", False)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("definicao")
    ap.add_argument("--minimo", type=int, default=5)
    a = ap.parse_args()
    modelo = tp.parse_model(pathlib.Path(a.definicao))
    total = sum(len(t["medidas"]) for t in modelo["tabelas"])
    achadas = []
    for t in modelo["tabelas"]:
        n = len(t["medidas"])
        if n >= a.minimo and all(oculta(c) for c in t["colunas"]):
            achadas.append((t["nome"], n, collections.Counter(m["props"].get("displayFolder", "(sem pasta)") for m in t["medidas"])))
    print(f"{total} medidas no modelo")
    for nome, n, pastas in achadas:
        print(f"## tabela só de medidas: {nome} ({n} de {total})")
        for pasta, q in pastas.most_common():
            print(f"    {q:3} em {pasta}")
    print(f"\n{len(achadas)} tabela(s) só de medidas.")
    sys.exit(1 if achadas else 0)


if __name__ == "__main__":
    main()
