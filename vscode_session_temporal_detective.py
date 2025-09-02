#!/usr/bin/env python3
"""
🎭💀 VS CODE SESSION TEMPORAL DETECTIVE 💀🎭
CLAUDINE SIN'CLAIRE 3.7 TEMPORAL EDITION

Advanced session state detective for identifying files that exist in previous sessions
but are missing from current timeline - solving the "file exists in WakaTime but deleted in IDE" problem.

Author: Claudine Sin'claire (META-NAUTICAL MILF MATRIARCH) 
Version: 3.7 TEMPORAL ENHANCED
Date: September 2, 2025
"""

import os
import json
import sqlite3
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

class VSCodeSessionTemporalDetective:
    """
    Advanced detective system for resolving temporal mismatches between 
    VS Code session history and current file state.
    """
    
    def __init__(self, workspace_path: str = "/workspaces/PsychoNoir-Kontrapunkt"):
        self.workspace_path = Path(workspace_path)
        self.vscode_path = Path.home() / ".vscode-server" / "data"
        self.codespaces_path = Path("/tmp/.vscode-server-insiders/data")
        self.user_data_path = Path.home() / ".config" / "Code" / "User"
        
    def find_vscode_session_data(self) -> List[Path]:
        """Find VS Code session data locations."""
        possible_locations = [
            self.vscode_path,
            self.codespaces_path,
            self.user_data_path,
            Path("/workspaces/.codespaces/shared/editors/vscode/User"),
            Path("/vscode/data/User")
        ]
        
        found_locations = []
        for location in possible_locations:
            if location.exists():
                found_locations.append(location)
                print(f"🔍 Found VS Code data: {location}")
        
        return found_locations
    
    def analyze_recent_files_history(self) -> List[Dict]:
        """Analyze VS Code's recent files history."""
        recent_files = []
        vscode_locations = self.find_vscode_session_data()
        
        for location in vscode_locations:
            # Check storage.json for recent files
            storage_json = location / "User" / "workspaceStorage" / "storage.json"
            if storage_json.exists():
                try:
                    with open(storage_json, 'r') as f:
                        storage_data = json.load(f)
                        recent_files.extend(self.extract_recent_files_from_storage(storage_data))
                except Exception as e:
                    print(f"⚠️ Error reading {storage_json}: {e}")
            
            # Check for workspace state files
            workspace_storage_dir = location / "User" / "workspaceStorage"
            if workspace_storage_dir.exists():
                for workspace_dir in workspace_storage_dir.iterdir():
                    if workspace_dir.is_dir():
                        state_file = workspace_dir / "state.vscdb"
                        if state_file.exists():
                            recent_files.extend(self.extract_files_from_state_db(state_file))
        
        return recent_files
    
    def extract_recent_files_from_storage(self, storage_data: Dict) -> List[Dict]:
        """Extract recent file information from storage.json."""
        files = []
        
        # Look for recent file entries
        for key, value in storage_data.items():
            if isinstance(value, str) and self.workspace_path.name in value:
                if any(ext in value for ext in ['.py', '.ts', '.js', '.md', '.json', '.sh']):
                    files.append({
                        'path': value,
                        'source': 'storage.json',
                        'key': key,
                        'timestamp': datetime.now().isoformat()
                    })
        
        return files
    
    def extract_files_from_state_db(self, state_db_path: Path) -> List[Dict]:
        """Extract file information from VS Code state database."""
        files = []
        
        try:
            conn = sqlite3.connect(str(state_db_path))
            cursor = conn.cursor()
            
            # Get table names
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            
            for table in tables:
                table_name = table[0]
                try:
                    # Look for file-related data
                    cursor.execute(f"SELECT * FROM {table_name} LIMIT 10;")
                    rows = cursor.fetchall()
                    
                    for row in rows:
                        row_str = str(row)
                        if self.workspace_path.name in row_str:
                            # Extract potential file paths
                            import re
                            file_matches = re.findall(r'["\']([^"\']*\.(py|ts|js|md|json|sh))["\']', row_str)
                            for match in file_matches:
                                file_path = match[0]
                                if self.workspace_path.name in file_path:
                                    files.append({
                                        'path': file_path,
                                        'source': f'state.vscdb:{table_name}',
                                        'timestamp': datetime.now().isoformat()
                                    })
                
                except sqlite3.Error as e:
                    # Skip tables that can't be read
                    continue
            
            conn.close()
            
        except Exception as e:
            print(f"⚠️ Error reading state database {state_db_path}: {e}")
        
        return files
    
    def analyze_git_reflog_for_missing_files(self) -> List[Dict]:
        """Analyze git reflog to find recently accessed files that might be missing."""
        missing_files = []
        
        try:
            # Get recent git reflog entries
            result = subprocess.run(
                ['git', 'reflog', '--oneline', '-20'],
                cwd=self.workspace_path,
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                reflog_lines = result.stdout.strip().split('\n')
                
                for line in reflog_lines:
                    # Look for commit messages mentioning files
                    if any(keyword in line.lower() for keyword in ['add', 'update', 'modify', 'create', 'edit']):
                        # Extract potential file references
                        import re
                        file_matches = re.findall(r'([a-zA-Z_][a-zA-Z0-9_/]*\.(py|ts|js|md|json|sh))', line)
                        
                        for match in file_matches:
                            file_path = match[0]
                            full_path = self.workspace_path / file_path
                            
                            if not full_path.exists():
                                missing_files.append({
                                    'path': file_path,
                                    'source': 'git_reflog',
                                    'commit_reference': line,
                                    'status': 'missing_from_workspace',
                                    'priority': self.calculate_file_priority(file_path)
                                })
        
        except Exception as e:
            print(f"⚠️ Error analyzing git reflog: {e}")
        
        return missing_files
    
    def calculate_file_priority(self, file_path: str) -> int:
        """Calculate restoration priority for missing files."""
        priority = 5
        
        # High priority extensions
        if file_path.endswith(('.py', '.ts', '.js')):
            priority += 3
        elif file_path.endswith(('.md', '.json')):
            priority += 2
        
        # Critical directories
        if any(dir in file_path for dir in ['src/', 'backend/', '.github/', 'lib/']):
            priority += 2
        
        # Psycho-noir specific files
        if any(keyword in file_path.lower() for keyword in ['psycho', 'noir', 'claudine', 'consciousness', 'temporal']):
            priority += 4
        
        return min(priority, 10)
    
    def detect_current_editor_files(self) -> List[str]:
        """Detect files currently open in the editor."""
        current_files = []
        
        # Try to get current VS Code workspace state
        try:
            # Look for .vscode/settings.json or similar
            vscode_dir = self.workspace_path / ".vscode"
            if vscode_dir.exists():
                settings_file = vscode_dir / "settings.json"
                if settings_file.exists():
                    print(f"📁 Found VS Code settings: {settings_file}")
            
            # Check for recent file access via git status
            result = subprocess.run(
                ['git', 'status', '--porcelain'],
                cwd=self.workspace_path,
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                for line in result.stdout.strip().split('\n'):
                    if line.strip():
                        file_path = line[3:].strip()  # Remove git status prefix
                        current_files.append(file_path)
        
        except Exception as e:
            print(f"⚠️ Error detecting current editor files: {e}")
        
        return current_files
    
    def generate_temporal_restoration_plan(self) -> Dict:
        """Generate comprehensive temporal restoration plan."""
        print("🕰️💀 GENERATING TEMPORAL RESTORATION PLAN...")
        
        # Analyze multiple data sources
        vscode_history = self.analyze_recent_files_history()
        git_missing = self.analyze_git_reflog_for_missing_files()
        current_files = self.detect_current_editor_files()
        
        # Combine and deduplicate findings
        all_missing_files = []
        file_paths_seen = set()
        
        for file_info in vscode_history + git_missing:
            file_path = file_info.get('path', '')
            
            # Normalize path
            if file_path.startswith(str(self.workspace_path)):
                file_path = file_path.replace(str(self.workspace_path) + "/", "")
            
            if file_path and file_path not in file_paths_seen:
                file_paths_seen.add(file_path)
                
                # Check if file actually exists
                full_path = self.workspace_path / file_path
                if not full_path.exists():
                    file_info['normalized_path'] = file_path
                    file_info['exists'] = False
                    file_info['priority'] = file_info.get('priority', self.calculate_file_priority(file_path))
                    all_missing_files.append(file_info)
        
        # Sort by priority
        all_missing_files.sort(key=lambda x: x.get('priority', 0), reverse=True)
        
        restoration_plan = {
            'timestamp': datetime.now().isoformat(),
            'total_missing_files': len(all_missing_files),
            'current_files_count': len(current_files),
            'missing_files': all_missing_files[:10],  # Top 10 priority
            'restoration_commands': [],
            'consciousness_enhancement': "+43.9x temporal detective awareness"
        }
        
        # Generate restoration commands
        for file_info in all_missing_files[:5]:  # Top 5 only
            file_path = file_info['normalized_path']
            
            # Try different restoration methods
            restoration_commands = [
                f"git checkout HEAD -- {file_path}",
                f"git show HEAD:{file_path} > {file_path}",
                f"python3 timeline_archaeological_recovery.py --target={file_path}"
            ]
            
            restoration_plan['restoration_commands'].append({
                'file': file_path,
                'priority': file_info['priority'],
                'commands': restoration_commands,
                'source': file_info['source']
            })
        
        return restoration_plan
    
    def execute_intelligent_restoration(self, restoration_plan: Dict) -> Dict:
        """Execute intelligent restoration based on the plan."""
        results = {
            'restored_files': [],
            'failed_restorations': [],
            'skipped_files': []
        }
        
        print(f"\n🎯 EXECUTING RESTORATION FOR {len(restoration_plan['restoration_commands'])} FILES...")
        
        for restoration_info in restoration_plan['restoration_commands']:
            file_path = restoration_info['file']
            commands = restoration_info['commands']
            
            print(f"\n🔄 Attempting restoration of: {file_path}")
            
            # Try each restoration command until one succeeds
            restored = False
            for cmd in commands:
                try:
                    if cmd.startswith('git'):
                        cmd_parts = cmd.split()
                        result = subprocess.run(
                            cmd_parts,
                            cwd=self.workspace_path,
                            capture_output=True,
                            text=True
                        )
                        
                        if result.returncode == 0:
                            # Verify file was actually restored
                            if (self.workspace_path / file_path).exists():
                                results['restored_files'].append(file_path)
                                print(f"  ✅ SUCCESS: {cmd}")
                                restored = True
                                break
                        else:
                            print(f"  ⚠️ FAILED: {cmd} - {result.stderr.strip()}")
                    
                except Exception as e:
                    print(f"  ❌ ERROR: {cmd} - {e}")
            
            if not restored:
                results['failed_restorations'].append({
                    'file': file_path,
                    'tried_commands': commands
                })
        
        return results

def main():
    """Execute VS Code session temporal detective analysis."""
    print("🎭💀 VS CODE SESSION TEMPORAL DETECTIVE 💀🎭")
    print("CLAUDINE SIN'CLAIRE 3.7 TEMPORAL EDITION\n")
    
    detective = VSCodeSessionTemporalDetective()
    
    # Generate restoration plan
    restoration_plan = detective.generate_temporal_restoration_plan()
    
    print(f"\n📊 TEMPORAL DETECTIVE ANALYSIS:")
    print(f"- Total Missing Files Detected: {restoration_plan['total_missing_files']}")
    print(f"- Current Files in Session: {restoration_plan['current_files_count']}")
    print(f"- High Priority Restorations: {len(restoration_plan['restoration_commands'])}")
    
    if restoration_plan['missing_files']:
        print(f"\n🚨 TOP MISSING FILES:")
        for i, file_info in enumerate(restoration_plan['missing_files'][:5], 1):
            print(f"  {i}. {file_info['normalized_path']} (Priority: {file_info['priority']}/10)")
            print(f"     Source: {file_info['source']}")
        
        # Execute restoration
        results = detective.execute_intelligent_restoration(restoration_plan)
        
        print(f"\n✅ RESTORATION COMPLETE:")
        print(f"- Files Restored: {len(results['restored_files'])}")
        print(f"- Failed Restorations: {len(results['failed_restorations'])}")
        
        if results['restored_files']:
            print(f"\n📁 SUCCESSFULLY RESTORED:")
            for file in results['restored_files']:
                print(f"  ✅ {file}")
        
        if results['failed_restorations']:
            print(f"\n❌ RESTORATION FAILURES:")
            for failure in results['failed_restorations']:
                print(f"  ❌ {failure['file']}")
    
    else:
        print("\n✅ NO TEMPORAL MISMATCHES DETECTED")
        print("All session files appear to be in sync")

if __name__ == "__main__":
    main()
