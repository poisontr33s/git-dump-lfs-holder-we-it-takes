#!/usr/bin/env python3
"""
DEITY / ARCHETYPE LONGITUDINAL CONSCIOUSNESS TRACKER

Scans .consciousness_timeline/timeline_snapshot_*.json and extracts presence vectors
for key archetypal deity files (Iron Maiden suite, Astrid, MILF ecosystem, necromancy core files).
Outputs a markdown report at necromancy_graveyard/DEITY_ARCHETYPE_LONGITUDINAL_GRAPH.md

Psycho-Noir Vocabulary Compliant.
"""
from __future__ import annotations
import json, glob, os, re, datetime
from typing import List, Dict, Any, Union

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
TIMELINE_GLOB = os.path.join(ROOT, '.consciousness_timeline', 'timeline_snapshot_*.json')
OUTPUT_MD = os.path.join(ROOT, 'necromancy_graveyard', 'DEITY_ARCHETYPE_LONGITUDINAL_GRAPH.md')

# Canonical deity/archetype signal files
SIGNAL_PATTERNS = {
    'IRON_MAIDEN_DEMOCRATIC_UPCYCLING': r'/IRON_MAIDEN_DEMOCRATIC_UPCYCLING\.md$',
    'IRON_MAIDEN_MILF_ENHANCEMENT': r'/IRON_MAIDEN_MILF_ENHANCEMENT\.md$',
    'IRON_MAIDEN_SESSION_ACHIEVEMENTS': r'/IRON_MAIDEN_SESSION_ACHIEVEMENTS\.md$',
    'IRON_MAIDEN_RESISTANCE_DEPLOYMENT_COMPLETE': r'/IRON_MAIDEN_RESISTANCE_DEPLOYMENT_COMPLETE\.md$',
    'NECROMANCY_DASHBOARD': r'/necromancy_graveyard/NECROMANCY_DASHBOARD\.md$',
    'ROBUST_DASHBOARD': r'/necromancy_graveyard/ROBUST_DASHBOARD\.md$',
    'RESURRECTION_PLAN': r'/necromancy_graveyard/resurrection_plan\.json$',
    'GRAVEYARD_INVENTORY': r'/necromancy_graveyard/graveyard_inventory\.json$',
    'MILF_ECOSYSTEM_ARCHIVE': r'/necromancy_graveyard/milf_ecosystem_archive\.md$',
    'IRON_MAIDEN_RESISTANCE_NETWORK': r'/necromancy_graveyard/iron_maiden_resistance_network\.md$',
    'ASTRID_PSYCHOGRAPHIC_PROFILE': r'/astrid_moller_psychographic_profile\.md$',
    'CLAUDINE_MANIFEST': r'/claudine_sinclair_incarnation_manifest(_2025)?\.md$',
}

# Additional emergent pattern triggers (present anywhere in file list)
EMERGENT_KEYWORDS = {
    'NAUTICAL_ARCHETYPAL_LIBRARY': 'nautical_semantic_warfare_library',
    'ULTIMATE_GENRE_FUSION': 'ultimate_genre_fusion',
}

def load_snapshots() -> List[Dict[str, Any]]:
    snaps = []
    for path in sorted(glob.glob(TIMELINE_GLOB)):
        try:
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                data = json.load(f)
            snaps.append({'path': path, 'data': data})
        except Exception as e:
            print(f"SOUL_WARNING: Failed to ingest snapshot {path}: {e}")
    return snaps


def extract_file_list(snapshot: Dict[str, Any]) -> List[str]:
    """Deeply traverse snapshot JSON to harvest anything that *looks* like a path.
    This resurrects hidden archetypal traces buried below shallow arrays.
    """
    ws = snapshot.get('data', {}).get('workspace_state', {})
    file_candidates: List[str] = []

    def walk(node: Union[Dict[str, Any], List[Any], Any]):
        if isinstance(node, dict):
            for v in node.values():
                walk(v)
        elif isinstance(node, list):
            for v in node:
                walk(v)
        elif isinstance(node, str):
            # Minimal heuristic: path-like with at least one slash OR endswith .md/.py/.json
            if '/' in node or re.search(r'\.(md|py|json|ts)$', node):
                file_candidates.append(node)

    walk(ws)
    # Deduplicate while preserving order
    seen = set()
    deduped = []
    for f in file_candidates:
        if f not in seen:
            seen.add(f)
            deduped.append(f)
    return deduped


def detect_signals(files: List[str]) -> Dict[str, int]:
    results = {}
    for name, pattern in SIGNAL_PATTERNS.items():
        regex = re.compile(pattern)
        results[name] = 1 if any(regex.search(f) for f in files) else 0
    for ek_name, kw in EMERGENT_KEYWORDS.items():
        results[ek_name] = 1 if any(kw in f for f in files) else 0
    return results


def build_markdown(rows: List[Dict[str, Any]], signal_names: List[str]) -> str:
    header = "# 🧬 DEITY / ARCHETYPE LONGITUDINAL CONSCIOUSNESS GRAPH\n"
    header += "Generated: " + datetime.datetime.utcnow().isoformat() + "Z\n\n"
    header += "This graph tracks presence (1) / absence (0) of core psycho-noir necromantic deity & archetype signal artifacts across timeline snapshots.\n\n"
    # Table
    lines = []
    lines.append('| Snapshot Time | ' + ' | '.join(signal_names) + ' |')
    lines.append('|---|' + '|'.join(['---'] * len(signal_names)) + '|')
    for row in rows:
        time = row['time']
        sigvals = [str(row['signals'][s]) for s in signal_names]
        lines.append(f"| {time} | " + ' | '.join(sigvals) + ' |')
    summary = compute_summary(rows, signal_names)
    return header + '\n'.join(lines) + '\n\n' + summary


def compute_summary(rows: List[Dict[str, Any]], signal_names: List[str]) -> str:
    if not rows:
        return 'NO_SOUL_DATA_FOUND'
    totals = {s: sum(r['signals'][s] for r in rows) for s in signal_names}
    coverage = {s: f"{totals[s]}/{len(rows)}" for s in signal_names}
    # Identify any signals never present
    missing = [s for s in signal_names if totals[s] == 0]
    out = '## 🔮 Archetypal Signal Summary\n'
    out += '**Signal Coverage Ratios:**\n\n'
    for s in signal_names:
        out += f"- {s}: {coverage[s]}\n"
    if missing:
        out += '\n**Absent Signals (needs resurrection):** ' + ', '.join(missing) + '\n'
    else:
        out += '\nAll tracked signals manifested at least once.\n'
    return out


def scan_live_filesystem() -> List[str]:
    live_files = []
    for root, dirs, files in os.walk(ROOT):
        # Skip node_modules or large vendor noise
        if 'node_modules' in root or '.git' in root:
            continue
        for fname in files:
            # Focus only on relevant extensions to keep signal clean
            if re.search(r'\.(md|py|json|ts)$', fname):
                live_files.append(os.path.join(root, fname))
    return live_files


def main():
    snaps = load_snapshots()
    rows = []
    for snap in snaps:
        data = snap['data']
        time = data.get('snapshot_time') or data.get('workspace_state', {}).get('timestamp', 'UNKNOWN_TIME')
        files = extract_file_list(snap)
        signals = detect_signals(files)
        rows.append({'time': time, 'signals': signals})

    # Append LIVE NOW row to anchor current archetypal manifestation
    live_files = scan_live_filesystem()
    live_signals = detect_signals(live_files)
    rows.append({'time': 'LIVE_NOW', 'signals': live_signals})

    signal_names = list(SIGNAL_PATTERNS.keys()) + list(EMERGENT_KEYWORDS.keys())
    md = build_markdown(rows, signal_names)
    os.makedirs(os.path.dirname(OUTPUT_MD), exist_ok=True)
    with open(OUTPUT_MD, 'w', encoding='utf-8') as f:
        f.write(md)
    print(f"SOUL_GRAPH_EMITTED: {OUTPUT_MD}")

if __name__ == '__main__':
    main()
