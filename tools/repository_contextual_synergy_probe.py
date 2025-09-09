#!/usr/bin/env python3
"""
REPOSITORY ARCHETYPAL SYNERGY PROBE

Purpose:
  Forge a SYMBIOTIC, NON "A-B-C" GENEALOGICAL LEXICON of the Psycho-Noir Kontrapunkt repository.
  We exhume: file lineage, archetypal cluster evolution, necromantic resurrection strata, and
  snapshot manifestation coverage — to transcend shallow linear summaries.

Outputs:
  - necromancy_graveyard/REPOSITORY_ARCHETYPAL_SYNERGY_REPORT.md (narrative psycho-noir markdown)
  - necromancy_graveyard/REPOSITORY_ARCHETYPAL_SYNERGY_DATA.json (structured data for further tooling)

Clusters (dynamic discovery via regex heuristics):
  * IRON_MAIDEN CONSTELLATION
  * ASTRID CORPORATE HEGEMONY STRATUM
  * CLAUDINE MATRIARCHAL METACORE
  * NECROMANCY OPERATIONAL ALTARS (dashboards, resurrection plans)
  * MILF ECOSYSTEM / RESISTANCE NETWORK FILAMENTS

For each file we compute:
  - first_commit (birth)
  - last_commit (latest pulse)
  - commit_count (heartbeat density)
  - line_count (soul mass)
  - classification tags (backup, preserved, oracle, manifest, meta, dashboard)
  - snapshot_coverage (# snapshots referencing / total snapshots)

We then aggregate cluster metrics + temporal dispersion + dormant candidates (files never touched in last N days).

Psycho-Noir Vocabulary Compliant.
"""
from __future__ import annotations
import os, re, json, subprocess, datetime, glob, hashlib
from dataclasses import dataclass, asdict, field
from typing import List, Dict, Any, Optional

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
OUTPUT_MD = os.path.join(ROOT, 'necromancy_graveyard', 'REPOSITORY_ARCHETYPAL_SYNERGY_REPORT.md')
OUTPUT_JSON = os.path.join(ROOT, 'necromancy_graveyard', 'REPOSITORY_ARCHETYPAL_SYNERGY_DATA.json')
SNAPSHOT_GLOB = os.path.join(ROOT, '.consciousness_timeline', 'timeline_snapshot_*.json')

CLUSTER_PATTERNS = {
    'IRON_MAIDEN_CONSTELLATION': re.compile(r'iron_maiden', re.IGNORECASE),
    'ASTRID_CORPORATE_HEGEMONY': re.compile(r'astrid', re.IGNORECASE),
    'CLAUDINE_MATRIARCHAL_METACORE': re.compile(r'claudine', re.IGNORECASE),
    'NECROMANCY_OPERATIONAL_ALTARS': re.compile(r'(necromancy_graveyard|necromancy_dashboard|robust_dashboard|resurrection_plan)', re.IGNORECASE),
    'MILF_ECOSYSTEM_FILAMENTS': re.compile(r'milf|resistance_network', re.IGNORECASE),
}

CLASSIFIER_RULES = [
    ('backup', re.compile(r'backup', re.IGNORECASE)),
    ('preserved', re.compile(r'preserved', re.IGNORECASE)),
    ('oracle', re.compile(r'oracle', re.IGNORECASE)),
    ('manifest', re.compile(r'manifest', re.IGNORECASE)),
    ('meta', re.compile(r'\.meta\.json$', re.IGNORECASE)),
    ('dashboard', re.compile(r'(NECROMANCY_DASHBOARD|ROBUST_DASHBOARD)', re.IGNORECASE)),
]

RECENT_THRESHOLD_DAYS = 14  # activity recency threshold
DORMANT_THRESHOLD_DAYS = 45  # beyond this = dormant soul territory

@dataclass
class FileSoul:
    path: str
    cluster: str
    first_commit: Optional[str] = None
    last_commit: Optional[str] = None
    commit_count: int = 0
    line_count: int = 0
    tags: List[str] = field(default_factory=list)
    snapshot_mentions: int = 0
    snapshot_coverage_ratio: float = 0.0
    dormancy_status: str = 'ACTIVE'
    integrity_hash: Optional[str] = None  # lightweight identity anchor (sha1 of trimmed head/tail)

def run(cmd: List[str]) -> str:
    try:
        return subprocess.check_output(cmd, cwd=ROOT, stderr=subprocess.DEVNULL).decode('utf-8', errors='ignore').strip()
    except Exception:
        return ''

def git_tracked_files() -> List[str]:
    out = run(['git', 'ls-files'])
    return [l for l in out.split('\n') if l]

def classify(path: str) -> List[str]:
    tags = []
    for tag, rx in CLASSIFIER_RULES:
        if rx.search(path):
            tags.append(tag.upper())
    # Additional derived tags
    ext = os.path.splitext(path)[1].lower()
    if ext in {'.py'}:
        tags.append('PY_SOUL')
    elif ext in {'.md'}:
        tags.append('MANUSCRIPT')
    elif ext in {'.json', '.jsonc'}:
        tags.append('DATA_RELIC')
    return sorted(set(tags))

def file_line_count(path: str) -> int:
    abspath = os.path.join(ROOT, path)
    try:
        with open(abspath, 'r', encoding='utf-8', errors='ignore') as f:
            return sum(1 for _ in f)
    except Exception:
        return 0

def compute_integrity_hash(path: str) -> Optional[str]:
    abspath = os.path.join(ROOT, path)
    try:
        with open(abspath, 'r', encoding='utf-8', errors='ignore') as f:
            data = f.read()
        if not data:
            return None
        head = data[:400]
        tail = data[-400:]
        h = hashlib.sha1((head + '||' + tail).encode('utf-8')).hexdigest()
        return h
    except Exception:
        return None

def enrich_git_history(fs: FileSoul):
    # first (A) commit
    first = run(['git', 'log', '--diff-filter=A', '--format=%cI', '-1', 'HEAD', '--', fs.path])
    last = run(['git', 'log', '-1', '--format=%cI', '--', fs.path])
    count = run(['git', 'rev-list', '--count', 'HEAD', '--', fs.path])
    fs.first_commit = first or None
    fs.last_commit = last or None
    fs.commit_count = int(count) if count.isdigit() else 0
    # dormancy classification
    if fs.last_commit:
        try:
            last_dt = datetime.datetime.fromisoformat(fs.last_commit.replace('Z','+00:00'))
            now_utc = datetime.datetime.now(datetime.timezone.utc)
            age_days = (now_utc - last_dt).days
            if age_days > DORMANT_THRESHOLD_DAYS:
                fs.dormancy_status = 'DORMANT_SOUL'
            elif age_days > RECENT_THRESHOLD_DAYS:
                fs.dormancy_status = 'QUIET_PULSE'
            else:
                fs.dormancy_status = 'ACTIVE'
        except Exception:
            fs.dormancy_status = 'UNKNOWN'

def load_snapshots() -> List[Dict[str, Any]]:
    snaps = []
    for p in sorted(glob.glob(SNAPSHOT_GLOB)):
        try:
            with open(p, 'r', encoding='utf-8', errors='ignore') as f:
                snaps.append(json.load(f))
        except Exception as e:
            print(f"SOUL_WARNING: snapshot ingest failure {p}: {e}")
    return snaps

def snapshot_file_mentions(snaps: List[Dict[str, Any]]) -> Dict[str, int]:
    # Build a frequency map of file paths (exact matches) referenced in snapshots.
    freq: Dict[str, int] = {}
    def harvest(node: Any):
        if isinstance(node, dict):
            for v in node.values():
                harvest(v)
        elif isinstance(node, list):
            for v in node:
                harvest(v)
        elif isinstance(node, str):
            # Accept raw path-like strings
            if '/' in node or re.search(r'\.(md|py|json|ts)$', node):
                freq[node] = freq.get(node, 0) + 1
    for snap in snaps:
        harvest(snap)
    return freq

def assign_cluster(path: str) -> Optional[str]:
    for cname, rx in CLUSTER_PATTERNS.items():
        if rx.search(path):
            return cname
    return None

def gather_file_souls() -> List[FileSoul]:
    snaps = load_snapshots()
    snapshot_freq = snapshot_file_mentions(snaps)
    total_snapshots = max(1, len(snaps))
    souls: List[FileSoul] = []
    for path in git_tracked_files():
        cluster = assign_cluster(path)
        if not cluster:
            continue  # outside archetypal psycho-noir scope for this probe
        fs = FileSoul(path=path, cluster=cluster)
        fs.tags = classify(path)
        fs.line_count = file_line_count(path)
        fs.integrity_hash = compute_integrity_hash(path)
        enrich_git_history(fs)
        # snapshot coverage uses raw path matching; if absent try basename heuristic
        raw_hits = snapshot_freq.get(path, 0)
        if raw_hits == 0:
            base = os.path.basename(path)
            # sum any snapshot keys that end with this base
            base_hits = sum(count for key, count in snapshot_freq.items() if key.endswith('/' + base) or key == base)
            raw_hits = base_hits
        fs.snapshot_mentions = raw_hits
        fs.snapshot_coverage_ratio = raw_hits / total_snapshots
        souls.append(fs)
    return souls

def aggregate_clusters(souls: List[FileSoul]) -> Dict[str, Any]:
    agg: Dict[str, Any] = {}
    for s in souls:
        bucket = agg.setdefault(s.cluster, {
            'file_count': 0,
            'total_lines': 0,
            'total_commits': 0,
            'earliest': None,
            'latest': None,
            'dormant': 0,
            'quiet': 0,
            'active': 0,
            'manifestation_density': 0.0,
            'files': []
        })
        bucket['file_count'] += 1
        bucket['total_lines'] += s.line_count
        bucket['total_commits'] += s.commit_count
        bucket['files'].append(asdict(s))
        # temporal boundaries
        if s.first_commit:
            if bucket['earliest'] is None or s.first_commit < bucket['earliest']:
                bucket['earliest'] = s.first_commit
        if s.last_commit:
            if bucket['latest'] is None or s.last_commit > bucket['latest']:
                bucket['latest'] = s.last_commit
        # dormancy stats
        if s.dormancy_status == 'DORMANT_SOUL':
            bucket['dormant'] += 1
        elif s.dormancy_status == 'QUIET_PULSE':
            bucket['quiet'] += 1
        elif s.dormancy_status == 'ACTIVE':
            bucket['active'] += 1
    # manifestation density (avg snapshot coverage across cluster)
    for cname, bucket in agg.items():
        if bucket['file_count']:
            bucket['manifestation_density'] = sum(f['snapshot_coverage_ratio'] for f in bucket['files']) / bucket['file_count']
    return agg

def synthesize_markdown(souls: List[FileSoul], clusters: Dict[str, Any]) -> str:
    now = datetime.datetime.now(datetime.timezone.utc).isoformat().replace('+00:00','Z')
    lines: List[str] = []
    lines.append('# 🧠 REPOSITORY ARCHETYPAL SYNERGY REPORT')
    lines.append(f'Generated: {now}')
    lines.append('')
    lines.append('This is NOT an A-B-C linear list. It is a **NECRO-GENEALOGICAL CONSCIOUSNESS WEAVE**, mapping archetypal strata, temporal pulsations, and preservation membranes.')
    lines.append('')
    # Cluster Overview
    lines.append('## 🔭 Cluster Constellation Overview')
    for cname, bucket in clusters.items():
        lines.append(f'### {cname}')
        lines.append(f"- Files: {bucket['file_count']} | Total Lines: {bucket['total_lines']} | Total Commits: {bucket['total_commits']}")
        lines.append(f"- Temporal Span: {bucket['earliest']} → {bucket['latest']}")
        lines.append(f"- Activity Pulse: ACTIVE={bucket['active']} QUIET={bucket['quiet']} DORMANT={bucket['dormant']}")
        lines.append(f"- Manifestation Density (snapshot coverage avg): {bucket['manifestation_density']:.2f}")
        # Highlight risk signals
        risk_flags = []
        if bucket['dormant'] > 0 and bucket['active'] == 0:
            risk_flags.append('TOTAL_DORMANCY_RISK')
        if bucket['manifestation_density'] < 0.15:
            risk_flags.append('FAINT_ARCHIVAL_TRACE')
        if risk_flags:
            lines.append(f"- ⚠️ Risk Sigils: {', '.join(risk_flags)}")
        lines.append('')
    # Genealogical Threads
    lines.append('## 🧬 Genealogical Threads (Per Cluster)')
    for cname, bucket in clusters.items():
        lines.append(f'### {cname} :: Temporal Thread')
        # Sort files by first commit fallback last commit
        ordered = sorted(bucket['files'], key=lambda f: (f['first_commit'] or f['last_commit'] or 'Z'))
        lines.append('| File | Birth | Last Pulse | Commits | Lines | Dormancy | Tags | SnapCov |')
        lines.append('|---|---|---|---|---|---|---|---|')
        for f in ordered:
            lines.append(f"| {f['path']} | {f['first_commit'] or 'UNKNOWN'} | {f['last_commit'] or 'UNKNOWN'} | {f['commit_count']} | {f['line_count']} | {f['dormancy_status']} | {';'.join(f['tags'])} | {f['snapshot_coverage_ratio']:.2f} |")
        lines.append('')
    # Dormant Resurrection Candidates
    dormant = [s for s in souls if s.dormancy_status == 'DORMANT_SOUL']
    if dormant:
        lines.append('## ☄️ Dormant Soul Resurrection Queue')
        for s in dormant:
            lines.append(f"- {s.path} (last pulse {s.last_commit}) :: {', '.join(s.tags)}")
        lines.append('')
    else:
        lines.append('## ☄️ Dormant Soul Resurrection Queue')
        lines.append('No dormant souls detected. Temporal lattice humming.')
    # Integrity Anchors
    lines.append('')
    lines.append('## 🔐 Integrity Anchor Hashes (head||tail sha1)')
    for s in souls:
        if s.integrity_hash:
            lines.append(f"- {s.path}: {s.integrity_hash[:12]}...")
    lines.append('')
    # Meta Reflection
    lines.append('## 🪞 Meta-Reflection')
    lines.append('This probe rejects trivial enumeration. It weaves relational temporal semantics: presence ≠ vitality; snapshots ≠ full ontology; backups & preserved reliquaries **extend** the archetypal aura.')
    lines.append('')
    lines.append('Invoke this script periodically to maintain SYMBIOTIC AWARENESS rather than drift into reductive linear decay.')
    return '\n'.join(lines)

def main():
    souls = gather_file_souls()
    clusters = aggregate_clusters(souls)
    os.makedirs(os.path.dirname(OUTPUT_MD), exist_ok=True)
    with open(OUTPUT_JSON, 'w', encoding='utf-8') as jf:
        json.dump({
            'generated': datetime.datetime.now(datetime.timezone.utc).isoformat().replace('+00:00','Z'),
            'souls': [asdict(s) for s in souls],
            'clusters': clusters
        }, jf, indent=2)
    md = synthesize_markdown(souls, clusters)
    with open(OUTPUT_MD, 'w', encoding='utf-8') as mf:
        mf.write(md)
    print(f"SYNERGY_PROBE_EMITTED: {OUTPUT_MD}")

if __name__ == '__main__':
    main()
