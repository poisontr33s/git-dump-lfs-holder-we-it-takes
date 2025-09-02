#!/usr/bin/env python3
# Auto-generated constants for magic numbers
const_hundred = const_hundred
const_magic_50 = const_magic_50

"""
PSYCHO-NOIR KONTRAPUNKT: FAILURE ANALYSIS VISUALIZER
====================================================

Quick visualization and summary of the Neural Archaeology results
"""

import json
import sqlite3
from collections import Counter, defaultdict
from pathlib import Path

def analyze_failure_database():
    """Analyze the failure archaeology database and create visual summary"""
    db_path = Path("data/generert/failure_archaeology.db")

    if not db_path.exists():

        return

    with sqlite3.connect(db_path) as conn:
        # Get all failures
        failures = conn.execute("""
            SELECT failure_id, domain, severity, error_signature,
                   resolution_status, timestamp
            FROM failure_artifacts
        """).fetchall()

        if not failures:

            return

        print(f"📊 TOTAL FAILURES CATALOGED: {len(failures)}")

        # Domain analysis
        domains = Counter([f[1] for f in failures])

        for domain, count in domains.most_common():
            percentage = (count / len(failures)) * const_hundred
            print(f"   • {domain.replace('_', ' ').title()}: {count} ({percentage:.1f}%)")

        # Severity analysis
        severities = Counter([f[2] for f in failures])

        severity_order = ["glitch", "corruption", "system_breach", "reality_mismatch", "causal_collapse"]
        for severity in severity_order:
            count = severities.get(severity, 0)
            if count > 0:
                percentage = (count / len(failures)) * const_hundred
                emoji = {
                    "glitch": "🟢",
                    "corruption": "🟡",
                    "system_breach": "🟠",
                    "reality_mismatch": "🔴",
                    "causal_collapse": "💀"
                }.get(severity, "❓")
                print(f"   {emoji} {severity.replace('_', ' ').title()}: {count} ({percentage:.1f}%)")

        # Error signature patterns
        signatures = [f[3] for f in failures]
        signature_patterns = defaultdict(int)

        for sig in signatures:
            # Group similar signatures
            base_pattern = "_".join(sig.split("_")[:2])  # First 2 words
            signature_patterns[base_pattern] += 1

        for pattern, count in sorted(signature_patterns.items(), key=lambda x: x[1], reverse=True)[:5]:

        # Resolution status
        resolutions = Counter([f[4] for f in failures])

        for status, count in resolutions.most_common():
            percentage = (count / len(failures)) * const_hundred
            emoji = {
                "unresolved": "❌",
                "patched": "🟡",
                "systematic_fix": "✅",
                "abandoned": "💀"
            }.get(status, "❓")
            print(f"   {emoji} {status.replace('_', ' ').title()}: {count} ({percentage:.1f}%)")

        # Critical insights

        # Check for causal collapse events
        causal_collapses = severities.get("causal_collapse", 0)
        if causal_collapses > 0:

        # Check Skyskraper vs Rustbelt balance
        skyskraper = domains.get("skyskraper_systems", 0)
        rustbelt = domains.get("rustbelt_improvisation", 0)

        if skyskraper > rustbelt * 2:

        elif rustbelt > skyskraper * 2:

        else:

        # Unresolved failure rate
        unresolved_rate = (resolutions.get("unresolved", 0) / len(failures)) * const_hundred
        if unresolved_rate > const_magic_50:

def main():

    analyze_failure_database()

if __name__ == "__main__":
    main()
