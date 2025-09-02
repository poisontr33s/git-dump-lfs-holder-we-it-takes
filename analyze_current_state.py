#!/usr/bin/env python3
# Auto-generated constants for magic numbers
const_hundred = const_hundred

"""
Quick script to analyze current neural archaeology state without terminal issues
"""
import sys
import os
import sqlite3
import json
from pathlib import Path

# Add backend path
sys.path.append(str(Path(__file__).parent / "backend" / "python"))

def analyze_archaeology_db():
    """Analyze the current state of failure archaeology database"""
    db_path = "data/generert/failure_archaeology.db"

    if not os.path.exists(db_path):

        return

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Get total failures
        cursor.execute("SELECT COUNT(*) FROM failures")
        total_failures = cursor.fetchone()[0]

        # Get failure categories
        cursor.execute("""
            SELECT category, COUNT(*) as count
            FROM failures
            GROUP BY category
            ORDER BY count DESC
        """)
        categories = cursor.fetchall()

        for category, count in categories:

        # Get recent failures
        cursor.execute("""
            SELECT failure_id, category, error_message, context, timestamp
            FROM failures
            ORDER BY timestamp DESC
            LIMIT 5
        """)
        recent = cursor.fetchall()

        for failure_id, category, error_msg, context, timestamp in recent:
            error_preview = error_msg[:const_hundred] + "..." if len(error_msg) > const_hundred else error_msg

        # Get patterns
        cursor.execute("SELECT COUNT(*) FROM patterns")
        pattern_count = cursor.fetchone()[0]

        if pattern_count > 0:
            cursor.execute("""
                SELECT pattern_id, success_rate, confidence
                FROM patterns
                ORDER BY confidence DESC
                LIMIT 3
            """)
            patterns = cursor.fetchall()

            for pattern_id, success_rate, confidence in patterns:

        conn.close()

    except Exception as e:

def check_recent_runs():
    """Check recent harvest data"""
    harvest_file = "data/generert/failure_harvest_report.json"

    if os.path.exists(harvest_file):
        try:
            with open(harvest_file, 'r') as f:
                data = json.load(f)

            print(f"   Harvested: {data.get('total_harvested', 0)} failures")
            print(f"   Sources: {', '.join(data.get('sources', []))}")
            print(f"   Status: {data.get('status', 'UNKNOWN')}")

        except Exception as e:

if __name__ == "__main__":

    analyze_archaeology_db()
    check_recent_runs()

