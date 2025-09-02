#!/usr/bin/env python3
"""
🎭 OFFLINE SESSION JSON MANAGER 🎭
==================================

Programmeringsspråk-agnostisk session manager
som arbeider direkte med JSON filer.
Ingen backend API nødvendig.
"""

import json
import os
import shutil
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any

class OfflineSessionManager:
    """
    🎭 Offline Session JSON Manager
    
    Arbeider direkte med JSON filer - 100% programmeringsspråk-agnostisk
    Lik Google AI Studio's <> knapp for session export/import
    """

    def __init__(self, sessions_dir: str = None):
        self.project_root = Path(__file__).parent.parent.parent
        self.sessions_dir = Path(sessions_dir) if sessions_dir else self.project_root / "data" / "sessions"
        self.sessions_dir.mkdir(parents=True, exist_ok=True)
        
        print(f"🎭 Offline Session Manager initialized")
        print(f"📁 Sessions directory: {self.sessions_dir}")

    def list_all_sessions(self) -> List[Dict[str, Any]]:
        """List alle tilgjengelige session JSON filer"""
        
        sessions = []
        
        for json_file in self.sessions_dir.glob("*.json"):
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    session_data = json.load(f)
                
                # Extract summary info
                metadata = session_data.get("session_metadata", {})
                completion = session_data.get("completion_metrics", {})
                
                summary = {
                    "file_path": str(json_file),
                    "file_name": json_file.name,
                    "session_id": metadata.get("session_id", json_file.stem),
                    "title": metadata.get("title", "Unknown Session"),
                    "timestamp": metadata.get("timestamp", "Unknown"),
                    "completion_percentage": completion.get("latest_completion_percentage", 0),
                    "file_size": json_file.stat().st_size,
                    "technical_achievements_count": len(session_data.get("technical_achievements", [])),
                    "hook_points_count": len(session_data.get("hook_points", []))
                }
                
                sessions.append(summary)
                
            except Exception as e:
                print(f"⚠️ Error reading {json_file}: {e}")
        
        # Sort by timestamp (newest first)
        sessions.sort(key=lambda s: s["timestamp"], reverse=True)
        return sessions

    def load_session(self, session_id_or_file: str) -> Optional[Dict[str, Any]]:
        """Last session fra ID eller fil-path"""
        
        # Try as file path first
        session_file = Path(session_id_or_file)
        if not session_file.exists():
            # Try as session ID
            session_file = self.sessions_dir / f"{session_id_or_file}.json"
        
        if not session_file.exists():
            print(f"❌ Session ikke funnet: {session_id_or_file}")
            return None
        
        try:
            with open(session_file, 'r', encoding='utf-8') as f:
                session_data = json.load(f)
            
            print(f"📀 Session lastet: {session_file.name}")
            return session_data
            
        except Exception as e:
            print(f"❌ Error loading session: {e}")
            return None

    def save_session(self, session_data: Dict[str, Any], file_name: str = None) -> str:
        """Lagre session til JSON fil"""
        
        if not file_name:
            session_id = session_data.get("session_metadata", {}).get("session_id", "unknown")
            file_name = f"{session_id}.json"
        
        session_file = self.sessions_dir / file_name
        
        try:
            with open(session_file, 'w', encoding='utf-8') as f:
                json.dump(session_data, f, indent=2, ensure_ascii=False)
            
            print(f"💾 Session lagret: {session_file}")
            return str(session_file)
            
        except Exception as e:
            print(f"❌ Error saving session: {e}")
            return ""

    def export_session(self, session_id_or_file: str, export_path: str) -> bool:
        """Eksporter session til spesifisert path"""
        
        session_data = self.load_session(session_id_or_file)
        if not session_data:
            return False
        
        try:
            export_file = Path(export_path)
            export_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(export_file, 'w', encoding='utf-8') as f:
                json.dump(session_data, f, indent=2, ensure_ascii=False)
            
            print(f"📤 Session eksportert: {export_file}")
            return True
            
        except Exception as e:
            print(f"❌ Export error: {e}")
            return False

    def import_session(self, import_path: str) -> Optional[str]:
        """Importer session fra fil"""
        
        import_file = Path(import_path)
        if not import_file.exists():
            print(f"❌ Import fil ikke funnet: {import_path}")
            return None
        
        try:
            with open(import_file, 'r', encoding='utf-8') as f:
                session_data = json.load(f)
            
            # Validate basic structure
            if not session_data.get("session_metadata", {}).get("session_id"):
                print("❌ Invalid session format - missing session_id")
                return None
            
            # Save to sessions directory
            session_file = self.save_session(session_data)
            
            print(f"📥 Session importert: {import_file.name}")
            return session_file
            
        except Exception as e:
            print(f"❌ Import error: {e}")
            return None

    def create_new_session(self, title: str, conversation_text: str = "") -> Dict[str, Any]:
        """Opprett ny session"""
        
        session_id = f"session_{int(datetime.now().timestamp())}_{hash(title) % 0xFFFF:04x}"
        
        session_data = {
            "session_metadata": {
                "session_id": session_id,
                "timestamp": datetime.now().isoformat(),
                "title": title,
                "conversation_length": len(conversation_text),
                "session_type": "manual_creation"
            },
            "technical_achievements": [],
            "decision_points": [],
            "code_implementations": [],
            "completion_metrics": {
                "latest_completion_percentage": 0,
                "success_indicators": 0,
                "error_indicators": 0,
                "success_ratio": 0,
                "progress_momentum": "new"
            },
            "hook_points": [],
            "learning_patterns": [],
            "conversation_summary": f"New session: {title}",
            "raw_conversation": conversation_text[:1000] if conversation_text else ""
        }
        
        session_file = self.save_session(session_data)
        
        print(f"➕ Ny session opprettet: {session_id}")
        return session_data

    def duplicate_session(self, session_id_or_file: str, new_title: str = None) -> Optional[Dict[str, Any]]:
        """Dupliser session som ny"""
        
        original = self.load_session(session_id_or_file)
        if not original:
            return None
        
        # Create new session based on original
        new_session_id = f"session_{int(datetime.now().timestamp())}_{hash(str(original)) % 0xFFFF:04x}"
        
        new_session = original.copy()
        new_session["session_metadata"] = original["session_metadata"].copy()
        new_session["session_metadata"]["session_id"] = new_session_id
        new_session["session_metadata"]["timestamp"] = datetime.now().isoformat()
        
        if new_title:
            new_session["session_metadata"]["title"] = new_title
        else:
            original_title = original["session_metadata"].get("title", "Unknown")
            new_session["session_metadata"]["title"] = f"Copy of {original_title}"
        
        session_file = self.save_session(new_session)
        
        print(f"📋 Session duplisert: {new_session_id}")
        return new_session

    def delete_session(self, session_id_or_file: str) -> bool:
        """Slett session"""
        
        # Try as file path first
        session_file = Path(session_id_or_file)
        if not session_file.exists():
            # Try as session ID
            session_file = self.sessions_dir / f"{session_id_or_file}.json"
        
        if not session_file.exists():
            print(f"❌ Session ikke funnet: {session_id_or_file}")
            return False
        
        try:
            # Create backup before deletion
            backup_dir = self.sessions_dir / "deleted"
            backup_dir.mkdir(exist_ok=True)
            
            backup_file = backup_dir / f"{session_file.name}.backup"
            shutil.move(str(session_file), str(backup_file))
            
            print(f"🗑️ Session slettet (backup: {backup_file})")
            return True
            
        except Exception as e:
            print(f"❌ Delete error: {e}")
            return False

    def search_sessions(self, query: str) -> List[Dict[str, Any]]:
        """Søk i sessions basert på innhold"""
        
        all_sessions = self.list_all_sessions()
        matching_sessions = []
        
        query_lower = query.lower()
        
        for session_summary in all_sessions:
            try:
                session_data = self.load_session(session_summary["session_id"])
                if not session_data:
                    continue
                
                # Search in title, summary, and achievements
                search_text = f"{session_summary['title']} {session_data.get('conversation_summary', '')}"
                
                # Add technical achievements text
                for achievement in session_data.get("technical_achievements", []):
                    search_text += f" {achievement.get('description', '')}"
                
                # Add hook points
                for hook in session_data.get("hook_points", []):
                    search_text += f" {hook.get('concept', '')}"
                
                if query_lower in search_text.lower():
                    matching_sessions.append(session_summary)
                    
            except Exception as e:
                print(f"⚠️ Error searching session {session_summary['session_id']}: {e}")
        
        return matching_sessions

    def display_session_summary(self, session_id_or_file: str):
        """Vis session sammendrag"""
        
        session_data = self.load_session(session_id_or_file)
        if not session_data:
            return
        
        metadata = session_data.get("session_metadata", {})
        completion = session_data.get("completion_metrics", {})
        
        print("\n🎭 SESSION SUMMARY")
        print("=" * 50)
        print(f"📀 Title: {metadata.get('title', 'Unknown')}")
        print(f"🆔 ID: {metadata.get('session_id', 'Unknown')}")
        print(f"📅 Timestamp: {metadata.get('timestamp', 'Unknown')}")
        print(f"🎯 Completion: {completion.get('latest_completion_percentage', 0)}%")
        print(f"🏆 Achievements: {len(session_data.get('technical_achievements', []))}")
        print(f"🔗 Hook Points: {len(session_data.get('hook_points', []))}")
        print(f"📝 Summary: {session_data.get('conversation_summary', 'No summary')}")
        print("=" * 50)

def main():
    """Interactive session manager"""
    
    manager = OfflineSessionManager()
    
    while True:
        print("\n🎭 OFFLINE SESSION JSON MANAGER")
        print("=" * 40)
        print("1. 📋 List all sessions")
        print("2. 📀 Load session")
        print("3. ➕ Create new session")
        print("4. 📤 Export session")
        print("5. 📥 Import session")
        print("6. 📋 Duplicate session")
        print("7. 🗑️ Delete session")
        print("8. 🔍 Search sessions")
        print("9. 📊 Session summary")
        print("0. 🚪 Exit")
        print()
        
        choice = input("Choose option: ").strip()
        
        if choice == "1":
            sessions = manager.list_all_sessions()
            print(f"\n📀 Found {len(sessions)} sessions:")
            for i, session in enumerate(sessions, 1):
                print(f"{i:2d}. {session['title'][:40]:<40} ({session['completion_percentage']:3.0f}%)")
                print(f"     🆔 {session['session_id']}")
                print(f"     📅 {session['timestamp'][:19]}")
                print()
        
        elif choice == "2":
            session_id = input("Session ID or file path: ").strip()
            session_data = manager.load_session(session_id)
            if session_data:
                print("\n📄 SESSION LOADED - JSON Content:")
                print(json.dumps(session_data, indent=2, ensure_ascii=False)[:1000] + "...")
        
        elif choice == "3":
            title = input("Session title: ").strip()
            conversation = input("Initial conversation (optional): ").strip()
            session_data = manager.create_new_session(title, conversation)
            manager.display_session_summary(session_data["session_metadata"]["session_id"])
        
        elif choice == "4":
            session_id = input("Session ID to export: ").strip()
            export_path = input("Export path (e.g., /tmp/my_session.json): ").strip()
            manager.export_session(session_id, export_path)
        
        elif choice == "5":
            import_path = input("Import file path: ").strip()
            manager.import_session(import_path)
        
        elif choice == "6":
            session_id = input("Session ID to duplicate: ").strip()
            new_title = input("New title (optional): ").strip() or None
            manager.duplicate_session(session_id, new_title)
        
        elif choice == "7":
            session_id = input("Session ID to delete: ").strip()
            if input(f"Confirm delete '{session_id}'? (y/N): ").lower() == 'y':
                manager.delete_session(session_id)
        
        elif choice == "8":
            query = input("Search query: ").strip()
            results = manager.search_sessions(query)
            print(f"\n🔍 Found {len(results)} matching sessions:")
            for result in results:
                print(f"📀 {result['title']} ({result['session_id'][:20]}...)")
        
        elif choice == "9":
            session_id = input("Session ID: ").strip()
            manager.display_session_summary(session_id)
        
        elif choice == "0":
            print("👋 Exiting session manager...")
            break
        
        else:
            print("❌ Invalid option")

if __name__ == "__main__":
    main()
