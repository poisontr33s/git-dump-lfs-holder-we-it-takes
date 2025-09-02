#!/usr/bin/env python3
"""
🎭 SIMPLE CHAT FIX
================

SUPER ENKEL løsning: Fjerner alt som kan forstyrre chat,
lager minimal config som BARE fokuserer på chat continuity.
"""

import os
import json
import shutil
from pathlib import Path

def nuclear_chat_fix():
    """Nuclear option: Fjern alt, start på nytt med minimal config"""

    workspace = Path.cwd()

    # 1. Backup existing .vscode
    vscode_dir = workspace / ".vscode"
    if vscode_dir.exists():
        backup_dir = workspace / ".vscode.backup"
        if backup_dir.exists():
            shutil.rmtree(backup_dir)
        shutil.copytree(vscode_dir, backup_dir)

    # 2. Remove .vscode entirely
    if vscode_dir.exists():
        shutil.rmtree(vscode_dir)

    # 3. Create fresh, minimal .vscode
    vscode_dir.mkdir()

    # Ultra-minimal settings - ONLY chat continuity
    ultra_minimal_settings = {
        "psycho-noir.active": True
    }

    with open(vscode_dir / "settings.json", 'w') as f:
        json.dump(ultra_minimal_settings, f, indent=2)

    # 4. Remove any conflicting JSON files that might interfere
    potentially_conflicting = [
        ".copilot-bridge",
        ".chat-continuity",
        "node_modules",
        ".vscode-server"
    ]

    for item in potentially_conflicting:
        item_path = workspace / item
        if item_path.exists():
            if item_path.is_dir():
                shutil.rmtree(item_path)
            else:
                item_path.unlink()

    # 5. Create ONLY the essential chat restore file
    chat_restore = '''#!/usr/bin/env python3
"""MINIMAL CHAT RESTORE"""
import json
from datetime import datetime

'''

    with open(workspace / "restore_chat_session.py", 'w') as f:
        f.write(chat_restore)

if __name__ == "__main__":
    nuclear_chat_fix()