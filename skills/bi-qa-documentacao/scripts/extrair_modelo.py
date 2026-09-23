"""Extrai o modelo TMDL (e, opcionalmente, as páginas PBIR) para um JSON
intermediário que alimenta a geração da documentação .docx.

Uso:
    python extrair_modelo.py <Projeto>.SemanticModel/definition [<Projeto>.Report/definition] > modelo.json
"""
from __future__ import annotations

import json
import pathlib
import subprocess
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from check_visual_bindings import field_refs  # noqa: E402
from tmdl_parser import parse_model  # noqa: E402


def git_info(path: str) -> dict:
    try:
        commit = subprocess.run(["git", "-C", path, "rev-parse", "--short", "HEAD"],
                                capture_output=True, text=True, check=True).stdout.strip()
        data = subprocess.run(["git", "-C", path, "log", "-1", "--format=%cI"],
                              capture_output=True, text=True, check=True).stdout.strip()
        return {"commit": commit, "data": data}
    except (OSError, subprocess.CalledProcessError):
        return {"commit": None, "data": None}


def paginas(report_dir: str) -> list[dict]:
    pages_dir = pathlib.Path(report_dir) / "pages"
    ordem = []
    meta = pages_dir / "pages.json"
    if meta.exists():
        ordem = json.loads(meta.read_text(encoding="utf-8-sig")).get("pageOrder", [])
    saida = []
    for pj in sorted(pages_dir.glob("*/page.json")):
        page = json.loads(pj.read_text(encoding="utf-8-sig"))
        visuais = []
        for vj in sorted(pj.parent.glob("visuals/*/visual.json")):
            v = json.loads(vj.read_text(encoding="utf-8-sig"))
            refs: list = []
            field_refs(v, refs)
            visuais.append({
                "nome": v.get("name", vj.parent.name),
                "tipo": (v.get("visual") or {}).get("visualType"),
                "campos": [f"'{t}'[{c}]" for t, c in sorted(set(refs))],
            })
        saida.append({"id": pj.parent.name, "nome": page.get("displayName", pj.parent.name), "visuais": visuais})
    pos = {pid: i for i, pid in enumerate(ordem)}
    saida.sort(key=lambda p: pos.get(p["id"], len(pos)))
    return saida


def main() -> None:
    if len(sys.argv) not in (2, 3):
        print(__doc__)
        sys.exit(2)
    modelo = parse_model(sys.argv[1])
    modelo["origem"] = git_info(sys.argv[1])
    if len(sys.argv) == 3:
        modelo["paginas"] = paginas(sys.argv[2])
    json.dump(modelo, sys.stdout, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
