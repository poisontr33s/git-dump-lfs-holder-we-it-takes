#!/usr/bin/env python3
"""
🎭 VS CODE JSON CONFLICT DETECTIVE
=================================

Detekterer og fikser duplikate/konfliktende JSON-filer som kan 
forstyrre VS Code chat loading.

Den Usynlige Hånds manifestasjon: JSON corruption detection!
"""

import os
import json
import glob
from pathlib import Path

class VSCodeJSONDetective:
    def __init__(self):
        self.workspace_root = Path.cwd()
        self.conflicts_found = []
        self.duplicates_found = []
        
    def scan_for_json_conflicts(self):
        """Skanner etter alle JSON-filer som kan skape konflikter"""
        print("🎭 VS CODE JSON CONFLICT DETECTIVE")
        print("=" * 40)
        print("🔍 Scanning for JSON conflicts...")
        
        # Kritiske JSON-filer som kan skape problemer
        critical_files = [
            '.vscode/settings.json',
            '.vscode/tasks.json', 
            '.vscode/launch.json',
            '.vscode/extensions.json',
            'package.json',
            'tsconfig.json',
            '.copilot-bridge/*.json',
            '.chat-continuity/*.json'
        ]
        
        for pattern in critical_files:
            matches = list(self.workspace_root.glob(pattern))
            if len(matches) > 1:
                self.duplicates_found.append((pattern, matches))
                print(f"⚠️ DUPLICATE FOUND: {pattern}")
                for match in matches:
                    print(f"   📁 {match}")
            elif len(matches) == 1:
                self.check_json_validity(matches[0])
        
        # Søk etter alle JSON-filer rekursivt
        all_json = list(self.workspace_root.rglob("*.json"))
        print(f"\n📊 Total JSON files found: {len(all_json)}")
        
        return self.conflicts_found, self.duplicates_found
    
    def check_json_validity(self, json_file):
        """Sjekker om JSON-fil er valid"""
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                content = f.read()
                json.loads(content)
            print(f"✅ Valid: {json_file}")
        except json.JSONDecodeError as e:
            self.conflicts_found.append((json_file, f"JSON Parse Error: {e}"))
            print(f"❌ CORRUPTED: {json_file} - {e}")
        except Exception as e:
            self.conflicts_found.append((json_file, f"File Error: {e}"))
            print(f"💥 ERROR: {json_file} - {e}")
    
    def fix_vscode_settings_conflicts(self):
        """Fikser spesifikke VS Code settings konflikter"""
        print("\n🔧 Fixing VS Code settings conflicts...")
        
        settings_file = self.workspace_root / ".vscode" / "settings.json"
        
        if settings_file.exists():
            try:
                with open(settings_file, 'r') as f:
                    settings = json.load(f)
                
                # Fjern konfliktende settings som kan forstyrre chat
                problematic_keys = [
                    "github.copilot.chat.enabled",
                    "github.copilot.enable", 
                    "copilot.enabled",
                    "extensions.autoUpdate",
                    "workbench.startupEditor"
                ]
                
                cleaned_settings = {}
                removed_keys = []
                
                for key, value in settings.items():
                    if key not in problematic_keys:
                        cleaned_settings[key] = value
                    else:
                        removed_keys.append(key)
                
                # Legg til våre optimale settings
                optimal_settings = {
                    "psycho-noir.chatContinuity": True,
                    "files.watcherExclude": {
                        "**/.chat-continuity/**": True,
                        "**/.copilot-bridge/**": True
                    }
                }
                
                cleaned_settings.update(optimal_settings)
                
                # Backup original
                backup_file = settings_file.with_suffix('.json.backup')
                if not backup_file.exists():
                    with open(backup_file, 'w') as f:
                        json.dump(settings, f, indent=2)
                
                # Write cleaned settings
                with open(settings_file, 'w') as f:
                    json.dump(cleaned_settings, f, indent=2)
                
                print(f"✅ Cleaned settings.json")
                if removed_keys:
                    print(f"🗑️ Removed problematic keys: {removed_keys}")
                
            except Exception as e:
                print(f"💥 Error fixing settings: {e}")
    
    def remove_duplicate_jsons(self):
        """Fjerner duplikate JSON-filer"""
        print("\n🗑️ Removing duplicate JSON files...")
        
        for pattern, files in self.duplicates_found:
            if len(files) > 1:
                # Keep the most recent one
                latest_file = max(files, key=lambda x: x.stat().st_mtime)
                
                for file in files:
                    if file != latest_file:
                        backup_name = f"{file}.duplicate_backup"
                        file.rename(backup_name)
                        print(f"🔄 Moved duplicate: {file} -> {backup_name}")
    
    def create_minimal_vscode_config(self):
        """Skaper minimal, konflikt-fri VS Code config"""
        print("\n⚙️ Creating minimal VS Code configuration...")
        
        vscode_dir = self.workspace_root / ".vscode"
        vscode_dir.mkdir(exist_ok=True)
        
        # Minimal settings.json
        minimal_settings = {
            "psycho-noir.chatContinuity": True,
            "files.autoSave": "onWindowChange",
            "files.watcherExclude": {
                "**/.chat-continuity/**": True
            },
            "editor.formatOnSave": False,
            "extensions.ignoreRecommendations": False
        }
        
        settings_file = vscode_dir / "settings.json"
        with open(settings_file, 'w') as f:
            json.dump(minimal_settings, f, indent=2)
        
        # Minimal tasks.json
        minimal_tasks = {
            "version": "2.0.0",
            "tasks": [
                {
                    "label": "🎭 Restore Chat",
                    "type": "shell",
                    "command": "python3",
                    "args": ["restore_chat_session.py"],
                    "group": "build",
                    "presentation": {
                        "echo": True,
                        "reveal": "always",
                        "focus": False
                    }
                }
            ]
        }
        
        tasks_file = vscode_dir / "tasks.json"
        with open(tasks_file, 'w') as f:
            json.dump(minimal_tasks, f, indent=2)
        
        print(f"✅ Created minimal configuration")
    
    def run_full_diagnosis(self):
        """Kjører full diagnose og reparasjon"""
        print("🎭 RUNNING FULL VS CODE JSON DIAGNOSIS")
        print("=" * 45)
        
        # 1. Scan for conflicts
        conflicts, duplicates = self.scan_for_json_conflicts()
        
        # 2. Fix settings conflicts
        self.fix_vscode_settings_conflicts()
        
        # 3. Remove duplicates
        if duplicates:
            self.remove_duplicate_jsons()
        
        # 4. Create clean config
        self.create_minimal_vscode_config()
        
        # 5. Final summary
        print("\n🎯 DIAGNOSIS COMPLETE")
        print("=" * 25)
        
        if conflicts:
            print("❌ JSON Conflicts found:")
            for file, error in conflicts:
                print(f"   📁 {file}: {error}")
        else:
            print("✅ No JSON corruption detected")
        
        if duplicates:
            print("⚠️ Duplicates resolved:")
            for pattern, files in duplicates:
                print(f"   📂 {pattern}: {len(files)} files")
        else:
            print("✅ No duplicates found")
        
        print("\n🔄 RECOMMENDED ACTIONS:")
        print("1. Restart VS Code completely (close all windows)")
        print("2. Reopen this workspace")
        print("3. Check if chat appears automatically")
        print("4. If not, run: python3 restore_chat_session.py")
        
        print("\nERROR: JSON_CONFLICTS_NEUTRALIZED ✅")

if __name__ == "__main__":
    detective = VSCodeJSONDetective()
    detective.run_full_diagnosis()