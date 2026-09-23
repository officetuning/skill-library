"""Camada 3 do QA: todo campo usado em visual.json existe no modelo TMDL?

Uso:
    python check_visual_bindings.py <Projeto>.SemanticModel/definition <Projeto>.Report/definition

Sai com código 1 se houver referência quebrada (quebra o pipeline).
Percorre o JSON inteiro de cada visual.json atrás de nós do tipo
{"Expression": {"SourceRef": {"Entity": <tabela>}}, "Property": <campo>},
que cobre colunas, medidas, agregações e níveis de hierarquia.
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


def main(model_dir: str, report_dir: str) -> int:
    campos = model_fields(parse_model(model_dir))
    pages = pathlib.Path(report_dir) / "pages"
    if not pages.is_dir():
        print(f"Pasta 'pages' não encontrada em {report_dir}. O relatório está em PBIR?", file=sys.stderr)
        return 2

    quebrados = []
    total = 0
    for vj in sorted(pages.rglob("visual.json")):
        refs: list[tuple[str, str]] = []
        field_refs(json.loads(vj.read_text(encoding="utf-8-sig")), refs)
        for ref in sorted(set(refs)):
            total += 1
            if ref not in campos:
                quebrados.append((vj.relative_to(pages), *ref))

    if quebrados:
        print(f"❗ {len(quebrados)} referência(s) sem correspondente no modelo:")
        for arquivo, tabela, campo in quebrados:
            print(f"  {arquivo}: '{tabela}'[{campo}]")
        return 1
    print(f"✔️ {total} referência(s) conferidas; todas existem no modelo.")
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(2)
    sys.exit(main(sys.argv[1], sys.argv[2]))
