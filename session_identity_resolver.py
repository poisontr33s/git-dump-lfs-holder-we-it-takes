#!/usr/bin/env python3
# Auto-generated constants for magic numbers
const_magic_50 = const_magic_50
const_ten = const_ten

"""
🎭 PSYCHO-NOIR SESSION IDENTITY RESOLVER
=======================================

PROBLEMET: VS Code starter "clean" og vet ikke at DENNE SPESIFIKKE CHATEN
eksisterer et annet sted (GitHub Codespaces, annen VS Code instance, etc.)

LØSNINGEN: Automatisk session detection og tilbud om å fortsette
existing conversation fra der den faktisk er.
"""

import os
import json
import sys
import subprocess
import requests
import time
from pathlib import Path
from datetime import datetime

class SessionIdentityResolver:
    def __init__(self):
        self.workspace_root = Path.cwd()
        self.session_identity_file = self.workspace_root / ".session-identity.json"
        self.copilot_bridge_dir = self.workspace_root / ".copilot-bridge"

        # GitHub API for finding active Codespaces
        self.github_api = "https://api.github.com"
        self.repo_owner = "poisontr33s"
        self.repo_name = "PsychoNoir-Kontrapunkt"

    def detect_current_environment(self):
        """Detect hvor VS Code kjører nå"""
        env_info = {
            "environment_type": "local",
            "is_codespaces": os.environ.get("CODESPACES") == "true",
            "is_remote": os.environ.get("VSCODE_REMOTE_USER") is not None,
            "machine_id": self.get_machine_id(),
            "session_start_time": datetime.now().isoformat(),
            "workspace_path": str(self.workspace_root)
        }

        if env_info["is_codespaces"]:
            env_info["environment_type"] = "codespaces"
            env_info["codespace_name"] = os.environ.get("CODESPACE_NAME")
        elif env_info["is_remote"]:
            env_info["environment_type"] = "remote"

        return env_info

    def get_machine_id(self):
        """Unique machine identifier"""
        try:
            # Try different methods to get unique ID
            if os.path.exists("/etc/machine-id"):
                with open("/etc/machine-id") as f:
                    return f.read().strip()
            elif os.path.exists("/var/lib/dbus/machine-id"):
                with open("/var/lib/dbus/machine-id") as f:
                    return f.read().strip()
            else:
                # Fallback to hostname + user
                import socket
                import getpass
                return f"{socket.gethostname()}-{getpass.getuser()}"
        except:
            return "unknown-machine"

    def register_session_start(self):
        """Registrer at en session startet HER"""
        env_info = self.detect_current_environment()

        # Legg til session info
        session_info = {
            **env_info,
            "session_id": f"psycho_noir_{env_info['machine_id']}_{int(time.time())}",
            "last_activity": datetime.now().isoformat(),
            "chat_active": True,
            "registration_time": datetime.now().isoformat()
        }

        with open(self.session_identity_file, 'w') as f:
            json.dump(session_info, f, indent=2)

        return session_info

    def find_other_active_sessions(self):
        """Finn andre aktive sessions for dette workspace"""
        active_sessions = []

        # 1. Check for existing bridge exports
        if self.copilot_bridge_dir.exists():
            for export_file in self.copilot_bridge_dir.glob("session_export_*.json"):
                try:
                    with open(export_file) as f:
                        session_data = json.load(f)

                    # Analyze session to see if it's "recent" and "substantial"
                    conversation_count = len(session_data.get("conversations", []))
                    if conversation_count > const_magic_50:  # Substantial session
                        active_sessions.append({
                            "source": "local_export",
                            "file": str(export_file),
                            "conversations": conversation_count,
                            "export_time": session_data.get("export_time"),
                            "environment": session_data.get("environment", "unknown")
                        })
                except:
                    continue

        # 2. Check for GitHub Codespaces (if we have access)
        codespaces_sessions = self.check_github_codespaces()
        active_sessions.extend(codespaces_sessions)

        # 3. Check for git references to session files
        git_sessions = self.check_git_session_references()
        active_sessions.extend(git_sessions)

        return active_sessions

    def check_github_codespaces(self):
        """Check if there are active Codespaces with our session"""
        sessions = []

        # This would require GitHub token - for now, just detect patterns

        return sessions

    def check_git_session_references(self):
        """Check git history for session file references"""
        sessions = []

        try:
            # Look for recent commits that mention session exports
            result = subprocess.run(
                ["git", "log", "--oneline", "-const_ten", "--grep=session"],
                capture_output=True, text=True, cwd=self.workspace_root
            )

            if result.returncode == 0:
                for line in result.stdout.strip().split('\n'):
                    if line and ('session' in line.lower() or 'chat' in line.lower()):
                        sessions.append({
                            "source": "git_history",
                            "commit": line.split()[0],
                            "message": line,
                            "type": "potential_session_reference"
                        })
        except:
            pass

        return sessions

    def offer_session_continuation(self):
        """Main function: Offer user to continue existing session"""
        current_env = self.detect_current_environment()
        other_sessions = self.find_other_active_sessions()

        if not other_sessions:

            self.register_session_start()
            return

        print(f"\n🔍 FOUND {len(other_sessions)} EXISTING SESSION(S):")

        for i, session in enumerate(other_sessions, 1):
            if session["source"] == "local_export":

                print(f"   📄 File: {Path(session['file']).name}")
            elif session["source"] == "git_history":

        # Interactive choice
        try:
            choice = input("🎯 Continue existing session? (number/n for new): ").strip()

            if choice.lower() == 'n':

                self.register_session_start()
                return

            session_num = int(choice) - 1
            if 0 <= session_num < len(other_sessions):
                self.import_and_continue_session(other_sessions[session_num])
            else:

                self.register_session_start()

        except (ValueError, KeyboardInterrupt):

            self.register_session_start()

    def import_and_continue_session(self, session_info):
        """Import selected session and set up continuity"""

        if session_info["source"] == "local_export":
            # Run the existing bridge import
            import_file = session_info["file"]

            try:
                subprocess.run([
                    sys.executable,
                    "tools/copilot_session_bridge.py",
                    "--import", import_file
                ], cwd=self.workspace_root)

                # Update session identity to reflect import
                current_env = self.detect_current_environment()
                current_env.update({
                    "imported_from": session_info,
                    "session_continuation": True,
                    "original_conversations": session_info['conversations']
                })

                with open(self.session_identity_file, 'w') as f:
                    json.dump(current_env, f, indent=2)

                # Show where to continue
                self.show_continuation_guide(session_info)

            except Exception as e:

                self.register_session_start()
        else:

            self.register_session_start()

    def show_continuation_guide(self, session_info):
        """Show user how to continue the imported session"""

        print("1. Åpne GitHub Copilot Chat panel (Ctrl+Shift+I)")

        print(f"   • {session_info.get('conversations', 0)} conversations imported")
        print(f"   • From: {session_info.get('environment', 'unknown')} environment")
        print(f"   • Export time: {session_info.get('export_time', 'unknown')}")

def main():
    resolver = SessionIdentityResolver()
    resolver.offer_session_continuation()

if __name__ == "__main__":
    main()
