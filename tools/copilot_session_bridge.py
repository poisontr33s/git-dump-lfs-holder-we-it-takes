#!/usr/bin/env python3
"""
🎭 PSYCHO-NOIR KONTRAPUNKT: COPILOT SESSION BRIDGE
=================================================

Bridge-løsning for å overføre Copilot chat sessions mellom VS Code lokalt og GitHub Codespaces.
Den Usynlige Hånds motløp mot platform-fragmentering!

KILDEKODE-KADAVER IDENTIFISERT: Corporate fragmentation protocols
KOMPILERINGS-SPØKELSE EXORCISED: Cross-environment session continuity
"""

import os
import json
import sqlite3
import shutil
from datetime import datetime
from pathlib import Path
import glob
import re

class CopilotSessionBridge:
    def __init__(self, workspace_root="/workspaces/PsychoNoir-Kontrapunkt"):
        self.workspace_root = Path(workspace_root)
        self.bridge_dir = self.workspace_root / ".copilot-bridge"
        self.bridge_dir.mkdir(exist_ok=True)

        # Potensielle Copilot data lokasjoner
        self.copilot_locations = [
            "~/.vscode/User/workspaceStorage",
            "~/.config/Code/User/workspaceStorage",
            "~/Library/Application Support/Code/User/workspaceStorage",
            "~/.vscode-remote/data/logs",
            "~/.vscode-server/data/logs",
            "/home/codespace/.vscode-remote/data/logs"
        ]

    def scan_environment(self):
        """Scan current environment for Copilot data"""

        environment = "unknown"
        if os.path.exists("/workspaces"):
            environment = "GitHub Codespaces"
        elif os.environ.get("CODESPACES"):
            environment = "GitHub Codespaces"
        elif os.path.exists(os.path.expanduser("~/.vscode")):
            environment = "VS Code Local"

        found_locations = []
        for location in self.copilot_locations:
            expanded = os.path.expanduser(location)
            if os.path.exists(expanded):
                found_locations.append(expanded)

        return environment, found_locations

    def extract_chat_logs(self, log_paths):
        """Extract chat logs from VS Code log directories"""

        chat_data = {
            "timestamp": datetime.now().isoformat(),
            "environment": self.scan_environment()[0],
            "logs": [],
            "conversations": []
        }

        for log_path in log_paths:
            # Søk etter Copilot Chat logs
            chat_log_pattern = os.path.join(log_path, "**/GitHub.copilot-chat/**/*.log")
            chat_logs = glob.glob(chat_log_pattern, recursive=True)

            for log_file in chat_logs:
                try:

                    with open(log_file, 'r', encoding='utf-8', errors='ignore') as f:
                        log_content = f.read()

                    # Extract conversation data
                    conversations = self._parse_chat_log(log_content)

                    chat_data["logs"].append({
                        "file": log_file,
                        "size": os.path.getsize(log_file),
                        "modified": datetime.fromtimestamp(os.path.getmtime(log_file)).isoformat()
                    })

                    chat_data["conversations"].extend(conversations)

                except Exception as e:
                    # Handle exception by skipping the problematic file and optionally logging
                    print(f"Error processing {log_file}: {e}")
                    continue  # Skip to next log file

        return chat_data

    def _parse_chat_log(self, log_content):
        """Parse chat log content for conversation data"""
        conversations = []

        request_pattern = r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{3}) \[info\] ccreq:([a-f0-9]+)\.copilotmd \| success \| ([^|]+) \| (\d+)ms \| \[([^\]]+)\]'

        for match in re.finditer(request_pattern, log_content):
            timestamp, request_id, model, duration, context = match.groups()

            conversations.append({
                "timestamp": timestamp,
                "request_id": request_id,
                "model": model.strip(),
                "duration_ms": int(duration),
                "context": context
            })

        return conversations

    def export_session(self):
        """Export current chat session data"""

        environment, locations = self.scan_environment()

        if not locations:

            return None

        chat_data = self.extract_chat_logs(locations)

        # Save to bridge directory
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        export_file = self.bridge_dir / f"session_export_{timestamp}.json"

        with open(export_file, 'w', encoding='utf-8') as f:
            json.dump(chat_data, f, indent=2, ensure_ascii=False)

        print(f"   📊 Found {len(chat_data['conversations'])} conversation entries")

        self._create_session_summary(chat_data, export_file)

        return export_file

    def _create_session_summary(self, chat_data, export_file):
        """Create human-readable session summary"""
        summary_file = export_file.with_suffix('.md')

        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write("# 🎭 COPILOT SESSION EXPORT SUMMARY\n\n")
            f.write(f"**Export Time:** {chat_data['timestamp']}\n")
            f.write(f"**Environment:** {chat_data['environment']}\n")
            f.write(f"**Log Files:** {len(chat_data['logs'])}\n")
            f.write(f"**Conversations:** {len(chat_data['conversations'])}\n\n")

            f.write("## 📊 Conversation Activity\n\n")

            if chat_data['conversations']:
                # Group by context
                contexts = {}
                for conv in chat_data['conversations']:
                    ctx = conv['context']
                    if ctx not in contexts:
                        contexts[ctx] = []
                    contexts[ctx].append(conv)

                for context, convs in contexts.items():
                    f.write(f"### {context}\n")
                    f.write(f"- **Requests:** {len(convs)}\n")
                    f.write(f"- **Models:** {', '.join(set(c['model'] for c in convs))}\n")
                    f.write(f"- **Avg Duration:** {sum(c['duration_ms'] for c in convs) // len(convs)}ms\n\n")

            f.write("## 📁 Log Files\n\n")
            for log in chat_data['logs']:
                f.write(f"- **{os.path.basename(log['file'])}**\n")
                f.write(f"  - Size: {log['size']} bytes\n")
                f.write(f"  - Modified: {log['modified']}\n\n")

            f.write("## 🔄 Import Instructions\n\n")
            f.write("To import this session in another VS Code environment:\n\n")
            f.write("1. Copy the export file to the target workspace\n")
            f.write("2. Run: `python3 tools/copilot_session_bridge.py --import session_export_*.json`\n")
            f.write("3. Restart VS Code to see imported session data\n\n")
            f.write("💡 **Note:** This creates a reference copy. Original chat UI may still be isolated.\n")

    def import_session(self, import_file):
        """Import chat session data from export file"""

        if not os.path.exists(import_file):

            return False

        with open(import_file, 'r', encoding='utf-8') as f:
            chat_data = json.load(f)

        import_record = {
            "import_time": datetime.now().isoformat(),
            "source_file": str(import_file),
            "source_environment": chat_data.get('environment', 'unknown'),
            "conversations": len(chat_data.get('conversations', [])),
            "logs": len(chat_data.get('logs', []))
        }

        imports_file = self.bridge_dir / "imported_sessions.json"
        imports = []

        if imports_file.exists():
            with open(imports_file, 'r', encoding='utf-8') as f:
                imports = json.load(f)

        imports.append(import_record)

        with open(imports_file, 'w', encoding='utf-8') as f:
            json.dump(imports, f, indent=2, ensure_ascii=False)

        local_copy = self.bridge_dir / f"imported_{os.path.basename(import_file)}"
        shutil.copy2(import_file, local_copy)

        return True

    def list_sessions(self):
        """List all available session exports and imports"""

        # List exports
        exports = list(self.bridge_dir.glob("session_export_*.json"))
        if exports:
            print(f"\n📤 EXPORTS ({len(exports)}):")
            for export_file in sorted(exports):
                stat = export_file.stat()

                print(f"      Created: {datetime.fromtimestamp(stat.st_mtime)}")

        # List imports
        imports_file = self.bridge_dir / "imported_sessions.json"
        if imports_file.exists():
            with open(imports_file, 'r', encoding='utf-8') as f:
                imports = json.load(f)

            print(f"\n📥 IMPORTS ({len(imports)}):")
            for imp in imports:
                print(f"   📄 {os.path.basename(imp['source_file'])}")

    def create_bridge_scripts(self):
        """Create convenience scripts for easy session transfer"""

        # Export script
        export_script = self.bridge_dir / "export_session.sh"
        with open(export_script, 'w') as f:
            f.write("""#!/bin/bash
# Copilot Session Export Script
echo "🎭 Exporting Copilot Session..."
cd "$(dirname "$0")/.."
python3 tools/copilot_session_bridge.py --export
echo "✅ Export complete! Check .copilot-bridge/ directory"
""")
        export_script.chmod(0o755)

        # Import script
        import_script = self.bridge_dir / "import_session.sh"
        with open(import_script, 'w') as f:
            f.write("""#!/bin/bash
# Copilot Session Import Script
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <export_file.json>"
    echo "Available exports:"
    ls .copilot-bridge/session_export_*.json 2>/dev/null || echo "  No exports found"
    exit 1
fi

echo "🎭 Importing Copilot Session..."
cd "$(dirname "$0")/.."
python3 tools/copilot_session_bridge.py --import "$1"
echo "✅ Import complete!"
""")
        import_script.chmod(0o755)

def main():
    import argparse

    parser = argparse.ArgumentParser(description='Copilot Session Bridge')
    parser.add_argument('--export', action='store_true', help='Export current session')
    parser.add_argument('--import', dest='import_file', help='Import session from file')
    parser.add_argument('--list', action='store_true', help='List available sessions')
    parser.add_argument('--setup', action='store_true', help='Setup bridge scripts')

    args = parser.parse_args()

    bridge = CopilotSessionBridge()

    if args.export:
        bridge.export_session()
    elif args.import_file:
        bridge.import_session(args.import_file)
    elif args.list:
        bridge.list_sessions()
    elif args.setup:
        bridge.create_bridge_scripts()
    else:
        # Default: run full diagnostic and setup

        bridge.scan_environment()
        export_file = bridge.export_session()
        bridge.create_bridge_scripts()
        bridge.list_sessions()

if __name__ == "__main__":
    main()
