#!/usr/bin/env python3
"""
🎭 SESSION DISK BROWSER & HOOK NAVIGATOR 🎭
==========================================

Interactive browser for session disks med "CD-player" interface.
Browse, search, and hook between sessions.
"""

import json
import sqlite3
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any
import sys

# Add backend to path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

from session_archaeology_engine import SessionArchaeologyEngine

class SessionDiskBrowser:
    """
    🎭 Interactive session disk browser
    
    CD-player-inspired interface for navigating sessions
    """

    def __init__(self):
        self.engine = SessionArchaeologyEngine()
        self.project_root = Path(__file__).parent.parent.parent
        self.current_session = None
        
    def list_all_sessions(self) -> List[Dict[str, Any]]:
        """List all available session disks"""
        
        with sqlite3.connect(self.engine.session_db) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT session_id, title, timestamp, completion_percentage, 
                       progress_level, file_path
                FROM session_disks
                ORDER BY timestamp DESC
            """)
            
            sessions = []
            for row in cursor.fetchall():
                sessions.append({
                    "session_id": row[0],
                    "title": row[1],
                    "timestamp": row[2],
                    "completion_percentage": row[3],
                    "progress_level": row[4],
                    "file_path": row[5]
                })
            
            return sessions

    def display_session_catalog(self):
        """Display session catalog like CD collection"""
        
        sessions = self.list_all_sessions()
        
        print("🎭 PSYCHO-NOIR SESSION DISK CATALOG")
        print("=" * 60)
        print(f"📀 Total Sessions: {len(sessions)}")
        print("-" * 60)
        
        for i, session in enumerate(sessions, 1):
            timestamp = datetime.fromisoformat(session['timestamp']).strftime("%Y-%m-%d %H:%M")
            completion = session['completion_percentage']
            level = session['progress_level']
            
            # Progress bar
            progress_bar = "█" * int(completion / 10) + "░" * (10 - int(completion / 10))
            
            print(f"💿 {i:2d}. {session['title'][:40]:<40}")
            print(f"     📅 {timestamp} | 🎯 {completion:3.0f}% [{progress_bar}] | 📊 L{level}")
            print(f"     🆔 {session['session_id']}")
            print()

    def load_and_display_session(self, session_id: str):
        """Load and display detailed session information"""
        
        session_disk = self.engine.load_session_disk(session_id)
        if not session_disk:
            print(f"❌ Session not found: {session_id}")
            return
        
        self.current_session = session_disk
        
        print("🎭 SESSION DISK VIEWER")
        print("=" * 60)
        
        metadata = session_disk["session_metadata"]
        print(f"📀 Session: {metadata['title']}")
        print(f"🆔 ID: {metadata['session_id']}")
        print(f"📅 Timestamp: {metadata['timestamp']}")
        print(f"💾 Size: {metadata.get('conversation_length', 0):,} chars")
        print()
        
        # Summary
        print("📋 SUMMARY:")
        print(f"   {session_disk['conversation_summary']}")
        print()
        
        # Completion metrics
        metrics = session_disk["completion_metrics"]
        print("📊 COMPLETION METRICS:")
        print(f"   🎯 Progress: {metrics['latest_completion_percentage']}%")
        print(f"   ✅ Success Indicators: {metrics['success_indicators']}")
        print(f"   ❌ Error Indicators: {metrics['error_indicators']}")
        print(f"   📈 Success Ratio: {metrics['success_ratio']:.2f}")
        print(f"   🚀 Momentum: {metrics['progress_momentum']}")
        print()
        
        # Technical achievements
        achievements = session_disk["technical_achievements"]
        print(f"🏆 TECHNICAL ACHIEVEMENTS ({len(achievements)}):")
        for i, achievement in enumerate(achievements[:10], 1):  # Show first 10
            ach_type = achievement.get('type', 'unknown')
            if ach_type == 'level_implementation':
                print(f"   {i:2d}. 🎯 Level {achievement.get('level', '?')}: {achievement.get('description', 'N/A')}")
            elif ach_type == 'file_creation':
                print(f"   {i:2d}. 📄 File: {achievement.get('file_path', 'N/A')}")
            elif ach_type == 'validation_success':
                print(f"   {i:2d}. ✅ Success: {achievement.get('description', 'N/A')[:50]}")
        if len(achievements) > 10:
            print(f"   ... and {len(achievements) - 10} more achievements")
        print()
        
        # Hook points
        hooks = session_disk["hook_points"]
        print(f"🔗 HOOK POINTS ({len(hooks)}):")
        for i, hook in enumerate(hooks[:8], 1):  # Show first 8
            concept = hook.get('concept', 'N/A')
            relevance = hook.get('relevance_score', 0)
            hook_type = hook.get('hook_type', 'unknown')
            print(f"   {i:2d}. 🎯 {concept} (relevance: {relevance:.2f}, type: {hook_type})")
        if len(hooks) > 8:
            print(f"   ... and {len(hooks) - 8} more hook points")
        print()
        
        # Learning patterns
        patterns = session_disk["learning_patterns"]
        if patterns:
            print(f"🧠 LEARNING PATTERNS ({len(patterns)}):")
            for i, pattern in enumerate(patterns, 1):
                name = pattern.get('pattern_name', 'N/A')
                pattern_type = pattern.get('pattern_type', 'unknown')
                effectiveness = pattern.get('effectiveness', 'unknown')
                print(f"   {i:2d}. 🎓 {name} ({pattern_type}, effectiveness: {effectiveness})")
            print()

    def find_hookable_sessions_for_current(self):
        """Find sessions that can hook to current session"""
        
        if not self.current_session:
            print("❌ No current session loaded")
            return
        
        print("🔍 FINDING HOOKABLE SESSIONS...")
        print("-" * 40)
        
        hooks = self.current_session["hook_points"]
        all_hookable = {}
        
        for hook in hooks[:5]:  # Check top 5 hook points
            concept = hook["concept"]
            print(f"🎯 Searching for concept: '{concept}'")
            
            hookable_sessions = self.engine.find_hookable_sessions(concept, limit=3)
            if hookable_sessions:
                all_hookable[concept] = hookable_sessions
                print(f"   Found {len(hookable_sessions)} compatible sessions")
                
                for session in hookable_sessions:
                    print(f"   📀 {session['session_id'][:20]}... - {session['title'][:30]} ({session['completion_percentage']}%)")
            else:
                print(f"   No compatible sessions found")
            print()
        
        if all_hookable:
            print("🔗 HOOK CREATION SUGGESTIONS:")
            for concept, sessions in all_hookable.items():
                print(f"   💡 Create continuation hook for '{concept}' with:")
                for session in sessions[:2]:  # Top 2 suggestions
                    print(f"      • {session['session_id']} ({session['completion_percentage']}%)")
            print()

    def create_session_hook_interactive(self, target_session_id: str, concept: str):
        """Create hook between current and target session"""
        
        if not self.current_session:
            print("❌ No current session loaded")
            return
        
        current_id = self.current_session["session_metadata"]["session_id"]
        
        hook_id = self.engine.create_session_hook(
            current_id, 
            target_session_id, 
            concept, 
            "continuation"
        )
        
        print(f"✅ Session hook created!")
        print(f"   🔗 Hook ID: {hook_id}")
        print(f"   📀 Source: {current_id}")
        print(f"   📀 Target: {target_session_id}")
        print(f"   🎯 Concept: {concept}")

    def interactive_menu(self):
        """Interactive session browser menu"""
        
        while True:
            print("\n🎭 SESSION DISK BROWSER")
            print("=" * 30)
            print("1. 📀 View Session Catalog")
            print("2. 🔍 Load Session")
            print("3. 🔗 Find Hookable Sessions")
            print("4. ⚡ Create Session Hook")
            print("5. 📊 Current Session Info")
            print("0. 🚪 Exit")
            print()
            
            choice = input("Choose option: ").strip()
            
            if choice == "1":
                self.display_session_catalog()
                
            elif choice == "2":
                session_id = input("Enter Session ID: ").strip()
                self.load_and_display_session(session_id)
                
            elif choice == "3":
                self.find_hookable_sessions_for_current()
                
            elif choice == "4":
                if not self.current_session:
                    print("❌ Load a session first")
                    continue
                target_id = input("Target Session ID: ").strip()
                concept = input("Hook Concept: ").strip()
                self.create_session_hook_interactive(target_id, concept)
                
            elif choice == "5":
                if self.current_session:
                    session_id = self.current_session["session_metadata"]["session_id"]
                    self.load_and_display_session(session_id)
                else:
                    print("❌ No session currently loaded")
                    
            elif choice == "0":
                print("👋 Exiting session browser...")
                break
                
            else:
                print("❌ Invalid option")

def main():
    """Main session browser interface"""
    
    browser = SessionDiskBrowser()
    
    # Auto-load latest session if available
    sessions = browser.list_all_sessions()
    if sessions:
        latest_session = sessions[0]
        print(f"🎯 Auto-loading latest session: {latest_session['session_id']}")
        browser.load_and_display_session(latest_session['session_id'])
    
    # Start interactive browser
    browser.interactive_menu()

if __name__ == "__main__":
    main()
