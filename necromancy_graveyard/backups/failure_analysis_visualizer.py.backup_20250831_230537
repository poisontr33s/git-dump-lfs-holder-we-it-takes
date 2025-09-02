#!/usr/bin/env python3
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
        print("❌ Database not found. Run the neural archaeology system first.")
        return
    
    print("🔍 ANALYZING FAILURE ARCHAEOLOGY DATABASE...")
    print("=" * 50)
    
    with sqlite3.connect(db_path) as conn:
        # Get all failures
        failures = conn.execute("""
            SELECT failure_id, domain, severity, error_signature, 
                   resolution_status, timestamp 
            FROM failure_artifacts
        """).fetchall()
        
        if not failures:
            print("❌ No failures found in database.")
            return
        
        print(f"📊 TOTAL FAILURES CATALOGED: {len(failures)}")
        print()
        
        # Domain analysis
        domains = Counter([f[1] for f in failures])
        print("🏗️  FAILURE DOMAINS:")
        for domain, count in domains.most_common():
            percentage = (count / len(failures)) * 100
            print(f"   • {domain.replace('_', ' ').title()}: {count} ({percentage:.1f}%)")
        print()
        
        # Severity analysis
        severities = Counter([f[2] for f in failures])
        print("⚠️  SEVERITY DISTRIBUTION:")
        severity_order = ["glitch", "corruption", "system_breach", "reality_mismatch", "causal_collapse"]
        for severity in severity_order:
            count = severities.get(severity, 0)
            if count > 0:
                percentage = (count / len(failures)) * 100
                emoji = {
                    "glitch": "🟢",
                    "corruption": "🟡", 
                    "system_breach": "🟠",
                    "reality_mismatch": "🔴",
                    "causal_collapse": "💀"
                }.get(severity, "❓")
                print(f"   {emoji} {severity.replace('_', ' ').title()}: {count} ({percentage:.1f}%)")
        print()
        
        # Error signature patterns
        signatures = [f[3] for f in failures]
        signature_patterns = defaultdict(int)
        
        for sig in signatures:
            # Group similar signatures
            base_pattern = "_".join(sig.split("_")[:2])  # First 2 words
            signature_patterns[base_pattern] += 1
        
        print("🔍 TOP ERROR PATTERNS:")
        for pattern, count in sorted(signature_patterns.items(), key=lambda x: x[1], reverse=True)[:5]:
            print(f"   • {pattern}: {count} occurrences")
        print()
        
        # Resolution status
        resolutions = Counter([f[4] for f in failures])
        print("🔧 RESOLUTION STATUS:")
        for status, count in resolutions.most_common():
            percentage = (count / len(failures)) * 100
            emoji = {
                "unresolved": "❌",
                "patched": "🟡",
                "systematic_fix": "✅",
                "abandoned": "💀"
            }.get(status, "❓")
            print(f"   {emoji} {status.replace('_', ' ').title()}: {count} ({percentage:.1f}%)")
        print()
        
        # Critical insights
        print("🚨 CRITICAL INSIGHTS:")
        
        # Check for causal collapse events
        causal_collapses = severities.get("causal_collapse", 0)
        if causal_collapses > 0:
            print(f"   💀 {causal_collapses} CAUSAL COLLAPSE events detected - IMMEDIATE ACTION REQUIRED")
        
        # Check Skyskraper vs Rustbelt balance
        skyskraper = domains.get("skyskraper_systems", 0)
        rustbelt = domains.get("rustbelt_improvisation", 0)
        
        if skyskraper > rustbelt * 2:
            print("   🏢 HIGH SKYSKRAPER FAILURE RATE - Automation systems need attention")
        elif rustbelt > skyskraper * 2:
            print("   🔧 HIGH RUSTBELT ACTIVITY - Manual interventions increasing")
        else:
            print("   ⚖️  Balanced failure distribution across domains")
        
        # Unresolved failure rate
        unresolved_rate = (resolutions.get("unresolved", 0) / len(failures)) * 100
        if unresolved_rate > 50:
            print(f"   ⚠️  {unresolved_rate:.1f}% failures remain UNRESOLVED - Learning opportunity")
        
        print()
        print("🎯 NEXT STEPS:")
        print("   1. Add resolution data to unresolved failures")
        print("   2. Document successful fix strategies")
        print("   3. Run system again to extract learning patterns")
        print("   4. Implement predictive alerts for high-risk patterns")

def main():
    print("🧠 PSYCHO-NOIR KONTRAPUNKT: FAILURE ANALYSIS VISUALIZER")
    print()
    analyze_failure_database()

if __name__ == "__main__":
    main()
