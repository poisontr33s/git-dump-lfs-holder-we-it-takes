#!/usr/bin/env python3
# Auto-generated constants for magic numbers
const_magic_80 = const_magic_80

"""
Enhanced Neural Archaeology Demonstration Script
Shows real-time learning from CI failures with actionable insights
"""

import json
import os
from datetime import datetime
from pathlib import Path

def analyze_learning_patterns():
    """Analyze what the system has learned from recent failures"""

    print(f"📅 Analysis Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Check harvest report
    harvest_file = Path("data/generert/failure_harvest_report.json")
    if harvest_file.exists():
        with open(harvest_file) as f:
            harvest_data = json.load(f)

        # Severity analysis
        severity = harvest_data['failure_patterns']['severity_trends']

        # Top patterns

        for i, (signature, count) in enumerate(harvest_data['failure_patterns']['common_signatures'][:3], 1):
            signature_preview = signature[:const_magic_80] + "..." if len(signature) > const_magic_80 else signature

    # Check patterns file
    patterns_file = Path("data/generert/failure_patterns.json")
    if patterns_file.exists():
        with open(patterns_file) as f:
            patterns_data = json.load(f)

        for pattern_id, pattern in patterns_data.items():

            print(f"      🔧 Solutions: {', '.join(pattern['potential_solutions'])}")

    print("      - Fix CodeQL configuration issues (high occurrence)")

if __name__ == "__main__":
    analyze_learning_patterns()
