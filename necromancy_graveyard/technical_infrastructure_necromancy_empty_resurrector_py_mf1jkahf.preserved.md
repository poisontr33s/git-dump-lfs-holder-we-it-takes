# 🏴‍☠️ PRESERVED CONCEPT - technical_infrastructure_necromancy_empty_resurrector_py_mf1jkahf

## Preservation Metadata
- **Concept ID**: technical_infrastructure_necromancy_empty_resurrector_py_mf1jkahf
- **Category**: technical_infrastructure
- **Sophistication Level**: 89%
- **Resurrection Potential**: 98%
- **Preserved**: 2025-09-01T19:57:50.740Z
- **Content Hash**: 76d917198755cb42
- **Dependencies**: 0 identified

## Original Content

#!/usr/bin/env python3
"""
necromancy_empty_resurrector.py

Skanner hele repoet etter "tomme"/plassholder Python-filer (pass/NotImplementedError/TODO-only)
og genererer en rapport + forslag til gjenoppretting (resurrection plan).

Bruk:
  python3 tools/necromancy_empty_resurrector.py --write

Output:
  - data/generert/resurrection_targets.json
  - data/rapporter/resurrection_targets.md
"""

from __future__ import annotations

import ast
import json
import re
import sys
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any


ROOT = Path(__file__).resolve().parents[1]

EXCLUDES = {
    ".git",
    "__pycache__",
    ".venv",
    "node_modules",
    "data/session_backup_",
    "SESSION_SNAPSHOTS",
}


KEYWORD_TO_DOMAIN = {
    # Psycho-Noir dialekt for mapping forslag
    "skyskraper": "Skyskraperen",
    "rustbelt": "Rustbeltet",
    "usynlige": "Den Usynlige Hånd",
    "dialogue": "Dialogsystem",
    "orchestrator": "Orkestrering",
    "copilot": "Integrasjoner",
}


PLACEHOLDER_PATTERNS = [
    re.compile(r"^\s*$"),
    re.compile(r"^\s*#.*$", re.MULTILINE),
]


@dataclass
class EmptyIndicator:
    kind: str
    detail: str


@dataclass
class FileAssessment:
    path: str
    size: int
    line_count: int
    empty_score: int
    indicators: List[EmptyIndicator]
    inferred_domain: str | None
    last_modified: float

    @property
    def is_empty_like(self) -> bool:
        return self.empty_score >= 2 or (self.empty_score == 1 and self.line_count <= 20)


def should_exclude(p: Path) -> bool:
    rp = p.relative_to(ROOT).as_posix()
    for ex in EXCLUDES:
        if rp.startswith(ex) or f"/{ex}/" in rp:
            return True
    return False


def infer_domain(path: Path) -> str | None:
    lower = path.as_posix().lower()
    for kw, domain in KEYWORD_TO_DOMAIN.items():
        if kw in lower:
            return domain
    # heuristic by folder
    if "backend/python" in lower:
        return "Skyskraperen"
    if "tools" in lower:
        return "Verktøy / Meta"
    return None


def analyze_python(path: Path) -> FileAssessment | None:
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return None

    indicators: List[EmptyIndicator] = []
    empty_score = 0

    # Fast checks
    if not text.strip():
        indicators.append(EmptyIndicator("blank_file", "only whitespace"))
        empty_score += 3

    # Drop leading module docstring for structural analysis
    try:
        tree = ast.parse(text)
    except Exception as e:
        # Syntax issues – still scan for placeholder signals
        indicators.append(EmptyIndicator("syntax_error", str(e)))
        empty_score += 1
        tree = None

    if tree is not None:
        body = tree.body if hasattr(tree, "body") else []
        # Strip module docstring
        if body and isinstance(body[0], ast.Expr) and isinstance(body[0].value, ast.Constant) and isinstance(body[0].value.value, str):
            body = body[1:]

        if not body:
            indicators.append(EmptyIndicator("no_module_statements", "module body empty after docstring"))
            empty_score += 2

        def node_is_placeholder(n: ast.AST) -> bool:
            # pass or raise NotImplementedError
            if isinstance(n, ast.Pass):
                return True
            if isinstance(n, ast.Raise):
                # raise NotImplementedError
                try:
                    t = n.exc
                    if isinstance(t, ast.Call) and getattr(t.func, "id", "") == "NotImplementedError":
                        return True
                except Exception:
                    return False
            if isinstance(n, ast.Expr) and isinstance(getattr(n, "value", None), ast.Constant) and isinstance(n.value.value, str):
                # bare string (docstring-like) inside functions/classes
                return True
            return False

        def block_empty_like(stmts: List[ast.stmt]) -> bool:
            filtered = [s for s in stmts if not (isinstance(s, ast.Expr) and isinstance(getattr(s, "value", None), ast.Constant) and isinstance(s.value.value, str))]
            if not filtered:
                return True
            return all(node_is_placeholder(s) for s in filtered)

        func_placeholders = 0
        class_placeholders = 0

        for n in body:
            if isinstance(n, ast.FunctionDef):
                if block_empty_like(n.body):
                    func_placeholders += 1
            elif isinstance(n, ast.AsyncFunctionDef):
                if block_empty_like(n.body):
                    func_placeholders += 1
            elif isinstance(n, ast.ClassDef):
                if block_empty_like(n.body):
                    class_placeholders += 1

        if func_placeholders:
            indicators.append(EmptyIndicator("empty_functions", f"{func_placeholders} placeholder functions"))
            empty_score += 1 + (1 if func_placeholders > 1 else 0)
        if class_placeholders:
            indicators.append(EmptyIndicator("empty_classes", f"{class_placeholders} placeholder classes"))
            empty_score += 1

    # Text signals
    todo_hits = re.findall(r"#\s*(?:TODO|FIXME|HACK)\b", text, re.IGNORECASE)
    if todo_hits and len(text.splitlines()) <= 80:
        indicators.append(EmptyIndicator("todo_only_bias", f"{len(todo_hits)} TODO/FIXME markers"))
        empty_score += 1

    if re.search(r"raise\s+NotImplementedError\b", text):
        indicators.append(EmptyIndicator("raises_not_implemented", "module raises NotImplementedError"))
        empty_score += 1

    # Self-referential const placeholders like: const_magic_50 = const_magic_50
    if re.search(r"^\s*const_[a-zA-Z0-9_]+\s*=\s*const_[a-zA-Z0-9_]+\s*$", text, re.MULTILINE):
        indicators.append(EmptyIndicator("self_referential_consts", "const_* assigned to itself"))
        empty_score += 1

    rel = path.relative_to(ROOT)
    return FileAssessment(
        path=rel.as_posix(),
        size=len(text.encode("utf-8")),
        line_count=len(text.splitlines()),
        empty_score=empty_score,
        indicators=indicators,
        inferred_domain=infer_domain(rel),
        last_modified=path.stat().st_mtime,
    )


def scan_repo() -> List[FileAssessment]:
    assessments: List[FileAssessment] = []
    for p in ROOT.rglob("*.py"):
        if should_exclude(p):
            continue
        fa = analyze_python(p)
        if fa is None:
            continue
        if fa.is_empty_like:
            assessments.append(fa)
    # stable sort by domain, then by path
    return sorted(assessments, key=lambda a: (a.inferred_domain or "~", a.path))


def to_jsonable(items: List[FileAssessment]) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    for it in items:
        d = asdict(it)
        d["indicators"] = [asdict(i) for i in it.indicators]
        return_domain = it.inferred_domain or "Ukategorisert"
        d["inferred_domain"] = return_domain
        out.append(d)
    return out


def write_reports(items: List[FileAssessment]) -> Dict[str, str]:
    gen_dir = ROOT / "data" / "generert"
    rep_dir = ROOT / "data" / "rapporter"
    gen_dir.mkdir(parents=True, exist_ok=True)
    rep_dir.mkdir(parents=True, exist_ok=True)

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    json_path = gen_dir / f"resurrection_targets_{ts}.json"
    md_path = rep_dir / f"resurrection_targets_{ts}.md"

    # JSON
    json_data = {
        "generated_at": datetime.now().isoformat(),
        "count": len(items),
        "targets": to_jsonable(items),
    }
    json_path.write_text(json.dumps(json_data, indent=2, ensure_ascii=False), encoding="utf-8")

    # Markdown (kort, handlingsorientert)
    lines = []
    lines.append(f"# Necromancy: Gjenopprettbare Python-moduler ({len(items)})")
    lines.append("")
    lines.append(f"Generert: {datetime.now().isoformat()}")
    lines.append("")
    for it in items:
        badge = it.inferred_domain or "Ukategorisert"
        indicators = ", ".join(f"{ind.kind}" for ind in it.indicators)
        lines.append(f"- [{badge}] `{it.path}` • linjer: {it.line_count} • tom-score: {it.empty_score} • signaler: {indicators}")
    lines.append("")
    lines.append("## Foreslått første bølge (Top 10)")
    for it in items[:10]:
        lines.append(f"1. `{it.path}` → lag minimal implementasjon i tråd med domenet '{it.inferred_domain or 'Ukategorisert'}'")
    md_path.write_text("\n".join(lines), encoding="utf-8")

    return {"json": str(json_path.relative_to(ROOT)), "md": str(md_path.relative_to(ROOT))}


def main(argv: List[str]) -> int:
    write = "--write" in argv or "-w" in argv
    items = scan_repo()

    if write:
        paths = write_reports(items)
        print(json.dumps({"count": len(items), "reports": paths}, indent=2))
    else:
        # Dry run to STDOUT
        print(f"Found {len(items)} empty-like Python modules:\n")
        for it in items[:25]:
            print(f"- {it.path} ({it.line_count}l, score={it.empty_score}, domain={it.inferred_domain})")
        if len(items) > 25:
            print(f"… and {len(items) - 25} more")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))


## Resurrection Notes
This concept has been preserved with 89% sophistication retention.
Resurrection potential: 98%

🏴‍☠️ End of preserved concept