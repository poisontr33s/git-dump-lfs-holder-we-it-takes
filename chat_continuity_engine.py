#!/usr/bin/env python3
"""
🎭 PSYCHO-NOIR CHAT CONTINUITY ENGINE
===================================

ENKEL LØSNING: Sørger for at DENNE SPESIFIKKE CHATEN fortsetter
når du åpner repoet, uavhengig av miljø.

Den Usynlige Hånds manifestasjon mot chat fragmentering!
"""

import os
import json
import glob
import shutil
from datetime import datetime
from pathlib import Path

class ChatContinuityEngine:
    def __init__(self):
        self.workspace_root = Path.cwd()
        self.chat_archive = self.workspace_root / ".chat-continuity"
        self.chat_archive.mkdir(exist_ok=True)

    def save_current_chat_context(self):
        """Lagrer kontekst for denne spesifikke chaten"""

        # Lag en context fil som beskriver hvor vi er i samtalen
        context = {
            "timestamp": datetime.now().isoformat(),
            "session_id": "psycho_noir_main_session",
            "workspace": str(self.workspace_root),
            "last_activity": "Chat continuity implementation",
            "status": "ACTIVE_DEVELOPMENT",
            "key_topics": [
                "PSYCHO-NOIR KONTRAPUNKT framework",
                "ROGBIV Liberation Protocol",
                "Chat session fragmentation solutions",
                "VS Code extension development",
                "Anti-gatekeeping methodology"
            ],
            "current_context": {
                "problem": "Chat sessions fragment when opening repo in different VS Code environments",
                "solution": "Simple continuity engine that preserves THIS chat when repo opens",
                "goal": "Seamless chat continuation regardless of where repo is opened"
            },
            "files_created_this_session": [
                ".vscode/extensions/psycho-noir-kontrapunkt/",
                "ROGBIV_LIBERATION_PROTOCOL.md",
                "emergency_session_restore.py",
                "tools/rogbiv_liberation_engine.py"
            ],
            "next_steps": [
                "Ensure this chat continues when repo reopens",
                "Test continuity across different VS Code environments",
                "Verify session bridge functionality"
            ]
        }

        # Lagre context
        context_file = self.chat_archive / "current_session_context.json"
        with open(context_file, 'w', encoding='utf-8') as f:
            json.dump(context, f, indent=2, ensure_ascii=False)

        return context

    def create_chat_launcher(self):
        """Lager en launcher som automatisk gjenoppretter chat context"""
        launcher_script = self.workspace_root / "restore_chat_session.py"

        launcher_code = '''#!/usr/bin/env python3
"""
🎭 AUTOMATIC CHAT SESSION LAUNCHER
================================

Kjøres automatisk når repoet åpnes for å gjenopprette chat context.
"""

import json
import os
from pathlib import Path

def restore_chat_session():
    """Gjenoppretter chat session når repoet åpnes"""
    workspace = Path.cwd()
    context_file = workspace / ".chat-continuity" / "current_session_context.json"

    if not context_file.exists():

        return False

    try:
        with open(context_file, 'r', encoding='utf-8') as f:
            context = json.load(f)

        for topic in context['key_topics']:

        for step in context['next_steps']:

        return True

    except Exception as e:

        return False

if __name__ == "__main__":
    restore_chat_session()
'''

        with open(launcher_script, 'w', encoding='utf-8') as f:
            f.write(launcher_code)

        # Make executable
        os.chmod(launcher_script, 0o755)

        return launcher_script

    def create_vscode_settings(self):
        """Lager VS Code settings som automatisk kjører chat restore"""
        vscode_dir = self.workspace_root / ".vscode"
        vscode_dir.mkdir(exist_ok=True)

        # Settings for automatic chat restore
        settings = {
            "psycho-noir.chatContinuity": True,
            "psycho-noir.autoRestore": True,
            "files.watcherExclude": {
                "**/.chat-continuity/**": True
            }
        }

        settings_file = vscode_dir / "settings.json"

        # Merge with existing settings if they exist
        if settings_file.exists():
            try:
                with open(settings_file, 'r') as f:
                    existing = json.load(f)
                existing.update(settings)
                settings = existing
            except:
                pass

        with open(settings_file, 'w') as f:
            json.dump(settings, f, indent=2)

        # Create tasks.json for automatic restore
        tasks = {
            "version": "2.0.0",
            "tasks": [
                {
                    "label": "🎭 Restore Chat Session",
                    "type": "shell",
                    "command": "python3",
                    "args": ["restore_chat_session.py"],
                    "group": "build",
                    "presentation": {
                        "echo": True,
                        "reveal": "always",
                        "focus": False,
                        "panel": "shared"
                    },
                    "problemMatcher": []
                }
            ]
        }

        tasks_file = vscode_dir / "tasks.json"
        with open(tasks_file, 'w') as f:
            json.dump(tasks, f, indent=2)

    def create_git_hooks(self):
        """Lager git hooks som kjører chat restore på checkout"""
        git_dir = self.workspace_root / ".git" / "hooks"

        if not git_dir.exists():

            return

        # Post-checkout hook
        hook_file = git_dir / "post-checkout"
        hook_content = '''#!/bin/bash
# 🎭 PSYCHO-NOIR Auto Chat Restore
echo "🎭 Restoring chat session..."
cd "$(git rev-parse --show-toplevel)"
if [ -f "restore_chat_session.py" ]; then
    python3 restore_chat_session.py
fi
'''

        with open(hook_file, 'w') as f:
            f.write(hook_content)

        os.chmod(hook_file, 0o755)

    def test_continuity(self):
        """Tester at continuity systemet fungerer"""

        # Test save
        context = self.save_current_chat_context()

        # Test restore
        os.system("python3 restore_chat_session.py")

    def deploy_full_solution(self):
        """Deployer komplett chat continuity løsning"""

        # 1. Save current context
        self.save_current_chat_context()

        # 2. Create launcher
        self.create_chat_launcher()

        # 3. Setup VS Code integration
        self.create_vscode_settings()

        # 4. Setup git hooks
        self.create_git_hooks()

        # 5. Test the system
        self.test_continuity()

if __name__ == "__main__":
    engine = ChatContinuityEngine()
    engine.deploy_full_solution()