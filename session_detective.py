#!/usr/bin/env python3
"""
🎭 PSYCHO-NOIR SESSION DETECTIVE
==============================

Den Usynlige Hånds øyne som ser alle avbrutte GitHub chat-sesjoner.
Jager fragmenterte samtaler med psykologisk presisjon.
"""

import os
import json
import glob
from datetime import datetime, timedelta
from pathlib import Path

class SessionDetective:
    def __init__(self):
        self.workspace_root = Path.cwd()
        self.vscode_logs = Path("/home/codespace/.vscode-remote/data/logs")
        self.current_time = datetime.now()
        
    def find_recent_interrupted_sessions(self, hours_back=24):
        """Jakter på nylig avbrutte GitHub chat-sesjoner"""
        
        print(f"🎭 PSYCHO-NOIR SESSION DETECTIVE - Jakt på avbrutte sesjoner")
        print(f"⏰ Tidsramme: Siste {hours_back} timer")
        print("=" * 60)
        
        cutoff_time = self.current_time - timedelta(hours=hours_back)
        interrupted_sessions = []
        
        # 1. Søk i VS Code Copilot logs
        copilot_sessions = self._scan_copilot_logs(cutoff_time)
        interrupted_sessions.extend(copilot_sessions)
        
        # 2. Søk i workspace session-filer
        workspace_sessions = self._scan_workspace_sessions(cutoff_time)
        interrupted_sessions.extend(workspace_sessions)
        
        # 3. Søk i copilot-bridge filer
        bridge_sessions = self._scan_bridge_sessions(cutoff_time)
        interrupted_sessions.extend(bridge_sessions)
        
        return interrupted_sessions
    
    def _scan_copilot_logs(self, cutoff_time):
        """Skanner VS Code Copilot chat logger"""
        sessions = []
        
        if not self.vscode_logs.exists():
            print("⚠️  VS Code logs ikke funnet")
            return sessions
            
        # Finn alle GitHub Copilot Chat logg-mapper
        chat_log_pattern = self.vscode_logs / "**/GitHub.copilot-chat"
        chat_dirs = glob.glob(str(chat_log_pattern), recursive=True)
        
        for chat_dir in chat_dirs:
            chat_path = Path(chat_dir)
            log_file = chat_path / "GitHub Copilot Chat.log"
            
            if log_file.exists():
                mod_time = datetime.fromtimestamp(log_file.stat().st_mtime)
                if mod_time > cutoff_time:
                    
                    # Les siste linjer for å se aktivitet
                    try:
                        with open(log_file, 'r', encoding='utf-8', errors='ignore') as f:
                            lines = f.readlines()
                            
                        if lines:
                            last_activity = self._parse_last_activity(lines)
                            
                            sessions.append({
                                'type': 'vscode_copilot_chat',
                                'path': str(log_file),
                                'last_modified': mod_time.isoformat(),
                                'last_activity': last_activity,
                                'session_dir': str(chat_path.parent.name),
                                'status': self._determine_session_status(lines)
                            })
                            
                    except Exception as e:
                        print(f"⚠️  Kunne ikke lese {log_file}: {e}")
        
        return sessions
    
    def _scan_workspace_sessions(self, cutoff_time):
        """Skanner workspace for session-filer"""
        sessions = []
        
        # Søk etter session-filer i workspace
        session_patterns = [
            "**/current_session_context.json",
            "**/session_*.json",
            "**/*session*.json",
            "**/live_session*.json"
        ]
        
        for pattern in session_patterns:
            files = glob.glob(str(self.workspace_root / pattern), recursive=True)
            
            for file_path in files:
                file_obj = Path(file_path)
                mod_time = datetime.fromtimestamp(file_obj.stat().st_mtime)
                
                if mod_time > cutoff_time:
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                            
                        sessions.append({
                            'type': 'workspace_session',
                            'path': file_path,
                            'last_modified': mod_time.isoformat(),
                            'session_data': self._extract_session_summary(data),
                            'status': 'potentially_interrupted'
                        })
                        
                    except Exception as e:
                        print(f"⚠️  Kunne ikke lese {file_path}: {e}")
        
        return sessions
    
    def _scan_bridge_sessions(self, cutoff_time):
        """Skanner copilot-bridge for session-eksporter"""
        sessions = []
        bridge_dir = self.workspace_root / ".copilot-bridge"
        
        if not bridge_dir.exists():
            return sessions
            
        # Finn session export filer
        session_files = list(bridge_dir.glob("session_export_*.json"))
        session_files.extend(bridge_dir.glob("session_export_*.md"))
        
        for file_path in session_files:
            mod_time = datetime.fromtimestamp(file_path.stat().st_mtime)
            
            if mod_time > cutoff_time:
                sessions.append({
                    'type': 'bridge_session_export',
                    'path': str(file_path),
                    'last_modified': mod_time.isoformat(),
                    'status': 'exported_session'
                })
        
        return sessions
    
    def _parse_last_activity(self, lines):
        """Parser siste aktivitet fra logglinjer"""
        if not lines:
            return "No activity"
            
        # Ta de siste 5 linjene og se etter timestamps
        recent_lines = lines[-5:]
        for line in reversed(recent_lines):
            if '[info]' in line or '[warning]' in line or '[error]' in line:
                return line.strip()
                
        return lines[-1].strip() if lines else "Unknown"
    
    def _determine_session_status(self, lines):
        """Bestemmer session-status basert på logginnhold"""
        recent_content = '\n'.join(lines[-20:]) if lines else ""
        
        if 'Invalid remote agent response' in recent_content:
            return 'interrupted_by_remote_error'
        elif 'Logged in as' in recent_content:
            return 'recently_active'
        elif 'Successfully activated' in recent_content:
            return 'initialization_complete'
        else:
            return 'status_unclear'
    
    def _extract_session_summary(self, data):
        """Ekstraherer sammendrag fra session data"""
        summary = {}
        
        if isinstance(data, dict):
            # Prøv å finne nøkkelinformasjon
            for key in ['session_id', 'timestamp', 'title', 'session_type', 'last_activity']:
                if key in data:
                    summary[key] = data[key]
                elif 'current_session' in data and key in data['current_session']:
                    summary[key] = data['current_session'][key]
                elif 'session_metadata' in data and key in data['session_metadata']:
                    summary[key] = data['session_metadata'][key]
        
        return summary
    
    def generate_recovery_report(self, sessions):
        """Genererer rapport om avbrutte sesjoner"""
        if not sessions:
            print("✅ Ingen avbrutte sesjoner funnet")
            return
            
        print(f"\n🚨 FUNNET {len(sessions)} POTENSIELT AVBRUTTE SESJONER:")
        print("=" * 60)
        
        for i, session in enumerate(sessions, 1):
            print(f"\n📋 SESJON #{i}")
            print(f"   Type: {session['type']}")
            print(f"   Sist endret: {session['last_modified']}")
            print(f"   Status: {session.get('status', 'ukjent')}")
            print(f"   Sti: {session['path']}")
            
            if 'last_activity' in session:
                print(f"   Siste aktivitet: {session['last_activity']}")
                
            if 'session_data' in session:
                data = session['session_data']
                if data:
                    print(f"   Session ID: {data.get('session_id', 'N/A')}")
                    print(f"   Tittel: {data.get('title', 'N/A')}")
        
        print("\n" + "=" * 60)
        print("🎭 Den Usynlige Hånds analyse komplett")

def main():
    detective = SessionDetective()
    
    # Søk etter avbrutte sesjoner i siste 24 timer
    sessions = detective.find_recent_interrupted_sessions(hours_back=24)
    
    # Generer rapport
    detective.generate_recovery_report(sessions)
    
    # Søk også etter eldre sesjoner (siste uke)
    print("\n" + "="*60)
    print("🔍 UTVIDET SØKK - SISTE UKE")
    older_sessions = detective.find_recent_interrupted_sessions(hours_back=168)  # 7 dager
    detective.generate_recovery_report(older_sessions)

if __name__ == "__main__":
    main()
