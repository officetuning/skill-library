"""Camada 3 do QA: todo campo usado em visual.json existe no modelo TMDL?

Uso:
    python check_visual_bindings.py <Projeto>.SemanticModel/definition <Projeto>.Report/definition

Sai com código 1 se houver referência quebrada (quebra o pipeline).
Percorre o JSON inteiro de cada visual.json atrás de dois tipos de nó:
{"Expression": {"SourceRef": {"Entity": <tabela>}}, "Property": <campo>}
(colunas, medidas e agregações) e
{"HierarchyLevel": {"Expression": {"Hierarchy": ...}, "Level": <nível>}}
(níveis de hierarquia do modelo, e também a hierarquia inteira, sem nível;
hierarquias automáticas de data ficam de fora).
"""
from __future__ import annotations

import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from tmdl_parser import model_fields, parse_model  # noqa: E402


def field_refs(node, found: list[tuple[str, str]]):
    if isinstance(node, dict):
        prop = node.get("Property")
        entity = (((node.get("Expression") or {}).get("SourceRef") or {}).get("Entity"))
        if isinstance(prop, str) and isinstance(entity, str):
            found.append((entity, prop))
        for v in node.values():
            field_refs(v, found)
    elif isinstance(node, list):
        for v in node:
            field_refs(v, found)


def _hierarquia(no) -> tuple:
    """(tabela, hierarquia) de um nó {"Expression": {"SourceRef": ...}, "Hierarchy": nome}."""
    entity = ((no.get("Expression") or {}).get("SourceRef") or {}).get("Entity")
    return entity, no.get("Hierarchy")


def hierarchy_refs(node, found: list[tuple[str, str, str | None]]):
    """(tabela, hierarquia, nível) de cada referência a hierarquia do modelo.

    Nível `None` = a hierarquia inteira. Referências por apelido (`SourceRef.Source`) e
    hierarquias automáticas de data (`PropertyVariationSource`) ficam de fora.
    """
    if isinstance(node, dict):
        hl = node.get("HierarchyLevel")
        if isinstance(hl, dict):
            ref = (*_hierarquia((hl.get("Expression") or {}).get("Hierarchy") or {}), hl.get("Level"))
            if all(isinstance(x, str) for x in ref):
                found.append(ref)
            return  # a hierarquia dentro do nível já foi conferida
        h = node.get("Hierarchy")
        if isinstance(h, dict):
            ref = _hierarquia(h)
            if all(isinstance(x, str) for x in ref):
                found.append((*ref, None))
        for v in node.values():
            hierarchy_refs(v, found)
    elif isinstance(node, list):
        for v in node:
            hierarchy_refs(v, found)


def model_levels(model) -> set[tuple[str, str, str | None]]:
    """Níveis do modelo; `(tabela, hierarquia, None)` representa a hierarquia inteira."""
    hierarquias = [(t["nome"], h) for t in model["tabelas"] for h in t["hierarquias"]]
    return {(t, h["nome"], n) for t, h in hierarquias for n in [*h["niveis"], None]}


def main(model_dir: str, report_dir: str) -> int:
    modelo = parse_model(model_dir)
    campos, niveis = model_fields(modelo), model_levels(modelo)
    pages = pathlib.Path(report_dir) / "pages"
    if not pages.is_dir():
        print(f"Pasta 'pages' não encontrada em {report_dir}. O relatório está em PBIR?", file=sys.stderr)
        return 2

    quebrados = []
    total = 0
    for vj in sorted(pages.rglob("visual.json")):
        visual = json.loads(vj.read_text(encoding="utf-8-sig"))
        refs: list[tuple[str, str]] = []
        field_refs(visual, refs)
        nivel_refs: list[tuple[str, str, str | None]] = []
        hierarchy_refs(visual, nivel_refs)
        for ref in sorted(set(refs)):
            total += 1
            if ref not in campos:
                quebrados.append((vj.relative_to(pages), f"'{ref[0]}'[{ref[1]}]"))
        for ref in sorted(set(nivel_refs), key=str):
            total += 1
            if ref not in niveis:
                nivel = f", nível {ref[2]}" if ref[2] else ""
                quebrados.append((vj.relative_to(pages), f"'{ref[0]}' hierarquia {ref[1]}{nivel}"))

    if quebrados:
        print(f"❗ {len(quebrados)} referência(s) sem correspondente no modelo:")
        for arquivo, descricao in quebrados:
            print(f"  {arquivo}: {descricao}")
        return 1
    print(f"✔️ {total} referência(s) conferidas; todas existem no modelo.")
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(2)
    sys.exit(main(sys.argv[1], sys.argv[2]))
