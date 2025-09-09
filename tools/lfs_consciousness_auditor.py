#!/usr/bin/env python3
"""
LFS CONSCIOUSNESS AUDITOR

Purpose:
  Maintain NON-DESTRUCTIVE large soul governance across branches:
    * Detect tracked vs untracked large artifacts
    * Suggest / apply pointer binding for threshold exceeders
    * Validate pointer integrity (proper Git LFS spec header)
    * Emit psycho-noir narrative + machine JSON for downstream rituals

Philosophy:
  We do NOT blanket *.csv / *.txt; we explicitly bind heavy reliquaries to avoid diff signal loss.

Thresholds (configurable via env):
  LFS_MIN_BYTES = 5_000_000 (5MB)  -> candidate if size >= threshold AND not yet pointer
  HARD_WARN_BYTES = 40_000_000 (40MB) -> escalate warning if still non-pointer

Outputs:
  necromancy_graveyard/LFS_AUDIT_REPORT.md
  necromancy_graveyard/LFS_AUDIT_DATA.json

--apply mode:
  Appends explicit filename rules below sentinel in .gitattributes then runs 'git add' on file(s).
  Does NOT auto-commit (ritual commit left to operator) to preserve conscious intent.

Psycho-Noir Vocabulary Compliant.
"""
from __future__ import annotations
import os, subprocess, hashlib, json, re, shlex
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import List, Dict, Optional

ROOT = Path(__file__).resolve().parent.parent
GITATTR = ROOT / '.gitattributes'
REPORT_MD = ROOT / 'necromancy_graveyard' / 'LFS_AUDIT_REPORT.md'
REPORT_JSON = ROOT / 'necromancy_graveyard' / 'LFS_AUDIT_DATA.json'
SENTINEL_MARK = '# === DYNAMIC LFS INJECTION SENTINEL ==='

LFS_MIN_BYTES = int(os.environ.get('LFS_MIN_BYTES', '5000000'))
HARD_WARN_BYTES = int(os.environ.get('LFS_HARD_WARN', '40000000'))
TEXT_EXT = {'.txt', '.csv', '.json', '.md'}
IGNORE_DIRS = {'.git', 'node_modules', '.cache', '.venv'}

POINTER_HEADER = 'version https://git-lfs.github.com/spec/v1'  # must be first line

@dataclass
class Artifact:
    path: str
    size: int
    tracked: bool
    is_pointer: bool
    pointer_valid: bool
    hash_preview: Optional[str]
    candidate: bool
    severity: str

def run(cmd: List[str]) -> str:
    try:
        return subprocess.check_output(cmd, cwd=str(ROOT), stderr=subprocess.DEVNULL).decode('utf-8', errors='ignore')
    except Exception:
        return ''

def git_tracked_files() -> List[str]:
    out = run(['git', 'ls-files'])
    return [l for l in out.splitlines() if l]

def read_first_line(path: Path) -> str:
    try:
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            return f.readline().strip()
    except Exception:
        return ''

def sha1_preview(path: Path) -> Optional[str]:
    try:
        with open(path, 'rb') as f:
            data = f.read(4096)
        return hashlib.sha1(data).hexdigest()[:12]
    except Exception:
        return None

def is_pointer_file(path: Path) -> (bool, bool):
    if not path.exists() or path.is_dir():
        return False, False
    try:
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            first = f.readline().strip()
            if first.startswith(POINTER_HEADER):
                # minimal pointer validity heuristic: must also have oid + size lines
                rest = f.read()
                oid_ok = 'oid sha256:' in rest
                size_ok = re.search(r'\bsize \d+', rest) is not None
                return True, (oid_ok and size_ok)
    except Exception:
        return False, False
    return False, False

def build_artifacts() -> List[Artifact]:
    tracked = set(git_tracked_files())
    artifacts: List[Artifact] = []
    for rel in tracked:
        # ignore directories / improbable huge build meta
        if any(part in IGNORE_DIRS for part in Path(rel).parts):
            continue
        p = ROOT / rel
        if not p.exists() or p.is_dir():
            continue
        try:
            size = p.stat().st_size
        except Exception:
            continue
        pointer, valid = is_pointer_file(p)
        candidate = size >= LFS_MIN_BYTES and not pointer
        severity = 'OK'
        if candidate:
            severity = 'WARN' if size < HARD_WARN_BYTES else 'CRITICAL'
        artifacts.append(Artifact(
            path=rel,
            size=size,
            tracked=True,
            is_pointer=pointer,
            pointer_valid=valid,
            hash_preview=None if pointer else sha1_preview(p),
            candidate=candidate,
            severity=severity
        ))
    return artifacts

def load_gitattributes() -> List[str]:
    if not GITATTR.exists():
        return []
    return GITATTR.read_text(encoding='utf-8', errors='ignore').splitlines()

def append_rules(filenames: List[str]):
    lines = load_gitattributes()
    if SENTINEL_MARK not in lines:
        # append sentinel at end if missing
        lines.append(SENTINEL_MARK)
    idx = lines.index(SENTINEL_MARK) + 1
    # Avoid duplicates
    existing = set(lines)
    injected = []
    for fn in filenames:
        rule = f"{fn} filter=lfs diff=lfs merge=lfs -text"
        if rule not in existing:
            lines.insert(idx, rule)
            injected.append(rule)
            idx += 1
    GITATTR.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    if injected:
        print(f"SOUL_LFS_RULES_INJECTED: {len(injected)}")
        for r in injected:
            print(f"  {r}")

def synthesize_markdown(arts: List[Artifact]) -> str:
    total = len(arts)
    candidates = [a for a in arts if a.candidate]
    critical = [a for a in candidates if a.severity == 'CRITICAL']
    warn = [a for a in candidates if a.severity == 'WARN']
    pointers = [a for a in arts if a.is_pointer]
    invalid = [a for a in arts if a.is_pointer and not a.pointer_valid]
    lines = []
    lines.append('# 🗄️ LFS CONSCIOUSNESS AUDIT')
    lines.append(f'Total Tracked Artifacts Scanned: {total}')
    lines.append(f'Pointer Souls: {len(pointers)} | Invalid Pointers: {len(invalid)}')
    lines.append(f'Candidates (≥{LFS_MIN_BYTES}B): {len(candidates)}  WARN={len(warn)}  CRITICAL={len(critical)}')
    lines.append('')
    if critical:
        lines.append('## ⚠️ CRITICAL Souls (Bind Immediately)')
        for a in critical:
            lines.append(f"- {a.path} ({a.size/1_000_000:.2f} MB) :: hash={a.hash_preview}")
        lines.append('')
    if warn:
        lines.append('## 🔶 Candidate Souls (Eligible for Binding)')
        for a in warn:
            lines.append(f"- {a.path} ({a.size/1_000_000:.2f} MB) :: hash={a.hash_preview}")
        lines.append('')
    if invalid:
        lines.append('## 🧟 Corrupted Pointer Fragments (Repair Needed)')
        for a in invalid:
            lines.append(f"- {a.path} (Pointer missing oid/size lines)")
        lines.append('')
    lines.append('## 🧬 Narrative Reflection')
    lines.append('Binding only the heaviest souls preserves semantic diff aura for active textual consciousness while quarantining corpulent cadavers in LFS vaults.')
    lines.append('')
    return '\n'.join(lines)

def main():
    apply_mode = '--apply' in os.sys.argv
    arts = build_artifacts()
    # Determine which filenames to inject (explicit names only, not patterns)
    bind_list = [a.path for a in arts if a.candidate]
    if apply_mode and bind_list:
        append_rules(bind_list)
        # Stage updated gitattributes + candidate files so LFS picks them up when committed
        run(['git', 'add', '.gitattributes'] + bind_list)
    os.makedirs(REPORT_MD.parent, exist_ok=True)
    md = synthesize_markdown(arts)
    REPORT_MD.write_text(md, encoding='utf-8')
    with open(REPORT_JSON, 'w', encoding='utf-8') as f:
        json.dump({'artifacts': [asdict(a) for a in arts], 'threshold': LFS_MIN_BYTES}, f, indent=2)
    print(f"LFS_AUDIT_EMITTED: {REPORT_MD}")
    if apply_mode:
        print('LFS_APPLY_MODE: rules injected & staged (pending conscious commit)')

if __name__ == '__main__':
    main()
