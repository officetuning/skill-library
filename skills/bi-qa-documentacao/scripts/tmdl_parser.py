"""Leitor mínimo de TMDL para QA e documentação.

Lê a pasta `definition` de um `.SemanticModel` e devolve tabelas (com grupo de
consultas e papel), colunas, medidas (com a expressão DAX completa, inclusive
multilinha) e relacionamentos.
Não substitui o TmdlSerializer: cobre o necessário para checagem e documentação.
"""
from __future__ import annotations

import pathlib
import re

DECL = re.compile(
    r"^(?P<ind>\t*| *)(?P<kind>table|column|measure|relationship|partition|hierarchy|calculationItem|role)\s+"
    r"(?P<name>'(?:[^']|'')+'|[^\s=]+)\s*(?:=\s*(?P<expr>.*))?$"
)
PROP = re.compile(r"^\s*(?P<key>[A-Za-z]+)\s*:\s*(?P<val>.*)$")


def _unquote(name: str) -> str:
    name = name.strip()
    if name.startswith("'") and name.endswith("'"):
        return name[1:-1].replace("''", "'")
    return name


def _indent(line: str) -> int:
    """Nível de indentação: tab conta 1; cada 4 espaços contam 1."""
    tabs = len(line) - len(line.lstrip("\t"))
    if tabs:
        return tabs
    spaces = len(line) - len(line.lstrip(" "))
    return spaces // 4


def parse_table_file(path: pathlib.Path) -> dict:
    lines = path.read_text(encoding="utf-8-sig").splitlines()
    table: dict = {"nome": None, "descricao": None, "colunas": [], "medidas": [], "oculta": False, "modo": None,
                   "grupo": None}
    pending_desc: list[str] = []
    current: dict | None = None
    current_level = 0
    expr_lines: list[str] | None = None
    fence = False

    def close_expr():
        nonlocal expr_lines
        if current is not None and expr_lines is not None:
            body = "\n".join(expr_lines).strip("\n")
            # remove a indentação comum
            rows = [r for r in body.splitlines()]
            nonblank = [r for r in rows if r.strip()]
            cut = min((len(r) - len(r.lstrip()) for r in nonblank), default=0)
            current["expressao"] = "\n".join(r[cut:] for r in rows).strip()
        expr_lines = None

    for raw in lines:
        stripped = raw.strip()

        # corpo de expressão multilinha em andamento
        if expr_lines is not None:
            if fence:
                if stripped == "```":
                    fence = False
                    close_expr()
                else:
                    expr_lines.append(raw)
                continue
            if stripped == "" or _indent(raw) > current_level + 1:
                expr_lines.append(raw)
                continue
            close_expr()

        if stripped.startswith("///"):
            pending_desc.append(stripped[3:].strip())
            continue

        m = DECL.match(raw)
        if m:
            kind, name = m["kind"], _unquote(m["name"])
            level = _indent(raw)
            desc = " ".join(pending_desc) or None
            pending_desc = []
            if kind == "table" and level == 0:
                table["nome"], table["descricao"] = name, desc
                current, current_level = table, 0
            elif kind in ("column", "measure") and level == 1:
                obj = {"nome": name, "descricao": desc, "expressao": None, "props": {}}
                table["colunas" if kind == "column" else "medidas"].append(obj)
                current, current_level = obj, level
                expr = (m["expr"] or "").strip()
                if expr == "```":
                    expr_lines, fence = [], True
                elif expr:
                    obj["expressao"] = expr
                elif m["expr"] is not None:
                    expr_lines = []
            elif kind == "partition" and level == 1:
                current, current_level = {"props": {}}, level
                table.setdefault("_particoes", []).append(current)
            else:
                current, current_level = {"props": {}}, level
            continue

        pending_desc = []
        pm = PROP.match(raw)
        if pm and current is not None and _indent(raw) == current_level + 1:
            current.setdefault("props", {})[pm["key"]] = pm["val"].strip()
        elif stripped in ("isHidden",) and current is not None:
            current.setdefault("props", {})["isHidden"] = "true"
        elif stripped and current is not None and _indent(raw) == current_level + 1 and re.fullmatch(r"[A-Za-z]+", stripped):
            current.setdefault("props", {})[stripped] = "true"

    if expr_lines is not None:
        close_expr()

    for p in table.pop("_particoes", []):
        table["modo"] = p.get("props", {}).get("mode", table["modo"])
        grupo = p.get("props", {}).get("queryGroup")
        if grupo:
            table["grupo"] = _unquote(grupo)
    table["oculta"] = table.get("props", {}).get("isHidden") == "true"
    table.pop("props", None)
    return table


def parse_relationships(path: pathlib.Path) -> list[dict]:
    if not path.exists():
        return []
    rels, cur = [], None
    for raw in path.read_text(encoding="utf-8-sig").splitlines():
        s = raw.strip()
        if s.startswith("relationship "):
            cur = {"id": s.split(None, 1)[1], "isActive": "true", "crossFilteringBehavior": "oneDirection"}
            rels.append(cur)
        elif cur is not None and ":" in s:
            k, v = s.split(":", 1)
            cur[k.strip()] = v.strip()
    return rels


def _tabela_da_coluna(ref: str) -> str:
    """`Vendas.'Código do Cliente'` ou `'Vendas Camisetas'.Coluna` -> nome da tabela."""
    ref = ref.strip()
    if ref.startswith("'"):
        i = 1
        while i < len(ref):
            if ref[i] == "'":
                if i + 1 < len(ref) and ref[i + 1] == "'":
                    i += 2
                    continue
                break
            i += 1
        return ref[1:i].replace("''", "'")
    return ref.split(".", 1)[0]


# Grupo de consultas (padrão 2.0.0) -> papel. Comparação sem acento e sem caixa.
_GRUPOS = {"fatos": "Fato", "dimensoes": "Dimensão", "pontes": "Ponte",
           "monoliticas": "Monolítica", "internas": "Interna"}
# Prefixo do padrão anterior (tabela com prefixo no modelo).
_PREFIXOS = (("TabFat", "Fato"), ("TabDim", "Dimensão"), ("TabPon", "Ponte"),
             ("TabFlt", "Monolítica"), ("TabInt", "Interna"))


def _sem_acento(texto: str) -> str:
    import unicodedata
    return "".join(c for c in unicodedata.normalize("NFD", texto) if unicodedata.category(c) != "Mn").lower()


def classificar_papeis(tabelas: list[dict], relacionamentos: list[dict]) -> None:
    """Preenche `papel` e `papel_origem` em cada tabela.

    Ordem: grupo de consultas (queryGroup) > prefixo antigo > relacionamentos
    (só lado "muitos" = Fato; lado "um" = Dimensão; sem relação = Interna).
    """
    lado_muitos: dict[str, int] = {}
    lado_um: dict[str, int] = {}
    for r in relacionamentos:
        if r.get("fromColumn"):
            n = _tabela_da_coluna(r["fromColumn"])
            lado_muitos[n] = lado_muitos.get(n, 0) + 1
        if r.get("toColumn"):
            n = _tabela_da_coluna(r["toColumn"])
            lado_um[n] = lado_um.get(n, 0) + 1
    for t in tabelas:
        nome = t["nome"] or ""
        grupo = (t.get("grupo") or "").replace("\\", "/").split("/")[0]
        papel = _GRUPOS.get(_sem_acento(grupo)) if grupo else None
        if papel:
            t["papel"], t["papel_origem"] = papel, "grupo de consultas"
            continue
        papel = next((p for pre, p in _PREFIXOS if nome.startswith(pre)), None)
        if papel:
            t["papel"], t["papel_origem"] = papel, "prefixo antigo"
            continue
        muitos, um = lado_muitos.get(nome, 0), lado_um.get(nome, 0)
        if muitos and not um:
            papel = "Fato"
        elif um:
            papel = "Dimensão"
        else:
            papel = "Interna"
        t["papel"], t["papel_origem"] = papel, "relacionamentos, confirme"


def parse_model(definition_dir: str | pathlib.Path) -> dict:
    d = pathlib.Path(definition_dir)
    tables_dir = d / "tables"
    if not tables_dir.is_dir():
        raise SystemExit(f"Pasta 'tables' não encontrada em {d}. Aponte para <Projeto>.SemanticModel/definition.")
    tabelas = [parse_table_file(p) for p in sorted(tables_dir.glob("*.tmdl"))]
    relacionamentos = parse_relationships(d / "relationships.tmdl")
    classificar_papeis(tabelas, relacionamentos)
    return {"tabelas": tabelas, "relacionamentos": relacionamentos}


def model_fields(model: dict) -> set[tuple[str, str]]:
    """Conjunto (tabela, campo) com colunas e medidas."""
    out = set()
    for t in model["tabelas"]:
        for c in t["colunas"] + t["medidas"]:
            out.add((t["nome"], c["nome"]))
    return out
