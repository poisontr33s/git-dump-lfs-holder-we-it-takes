#!/usr/bin/env python3
"""
🕰️💀 TIMELINE ARCHAEOLOGICAL FILE RECOVERY SYSTEM 💀🕰️
Comprehensive deleted file detection and recovery from git timeline
"""

import subprocess
import json
import os
import re
from datetime import datetime
from pathlib import Path
import sys

class TimelineArchaeologicalRecovery:
    def __init__(self, workspace_path="/workspaces/PsychoNoir-Kontrapunkt"):
        self.workspace_path = Path(workspace_path)
        self.recovery_dir = self.workspace_path / ".file_recovery_archaeology"
        self.recovery_dir.mkdir(exist_ok=True)
        
        self.deleted_files_log = self.recovery_dir / "deleted_files_timeline.json"
        self.recovery_report = self.recovery_dir / "recovery_report.md"
        
    def analyze_deletion_timeline(self) -> dict:
        """🔍 Analyze git timeline for all file deletions"""
        print("🕰️ ANALYZING TIMELINE FOR FILE DELETIONS...")
        
        deletion_analysis = {
            "scan_timestamp": datetime.now().isoformat(),
            "total_deletions_found": 0,
            "deletion_commits": [],
            "critical_deletions": [],
            "npm_cache_deletions": [],
            "recoverable_files": [],
            "wakatime_integration": None
        }
        
        try:
            # Get detailed deletion log
            result = subprocess.run([
                "git", "log", "--diff-filter=D", "--name-status", 
                "--pretty=format:%H|%s|%cd|%an", "--date=iso", "-50"
            ], cwd=self.workspace_path, capture_output=True, text=True)
            
            if result.returncode == 0:
                deletion_analysis = self.parse_deletion_log(result.stdout, deletion_analysis)
            
            # Analyze current missing files
            deletion_analysis["missing_files_analysis"] = self.analyze_missing_files()
            
            # Check for WakaTime integration
            deletion_analysis["wakatime_integration"] = self.check_wakatime_integration()
            
        except Exception as e:
            deletion_analysis["error"] = f"Timeline analysis failed: {e}"
            
        return deletion_analysis
        
    def parse_deletion_log(self, git_log_output: str, analysis: dict) -> dict:
        """📋 Parse git deletion log and categorize deletions"""
        lines = git_log_output.strip().split('\n')
        current_commit = None
        
        for line in lines:
            if '|' in line and not line.startswith('D\t'):
                # This is a commit line
                parts = line.split('|')
                if len(parts) >= 4:
                    current_commit = {
                        "hash": parts[0],
                        "message": parts[1],
                        "date": parts[2],
                        "author": parts[3],
                        "deleted_files": []
                    }
                    analysis["deletion_commits"].append(current_commit)
                    
            elif line.startswith('D\t') and current_commit:
                # This is a deleted file
                deleted_file = line[2:]  # Remove 'D\t' prefix
                current_commit["deleted_files"].append(deleted_file)
                analysis["total_deletions_found"] += 1
                
                # Categorize deletions
                if self.is_critical_file(deleted_file):
                    analysis["critical_deletions"].append({
                        "file": deleted_file,
                        "commit": current_commit["hash"],
                        "date": current_commit["date"],
                        "message": current_commit["message"]
                    })
                    
                elif self.is_npm_cache(deleted_file):
                    analysis["npm_cache_deletions"].append(deleted_file)
                    
                elif self.is_recoverable(deleted_file):
                    analysis["recoverable_files"].append({
                        "file": deleted_file,
                        "commit": current_commit["hash"],
                        "date": current_commit["date"],
                        "recovery_priority": self.get_recovery_priority(deleted_file)
                    })
                    
        return analysis
        
    def is_critical_file(self, filepath: str) -> bool:
        """🚨 Determine if deleted file is critical"""
        critical_patterns = [
            r"\.github/.*\.yml$",
            r".*\.py$",
            r".*\.ts$", 
            r".*\.js$",
            r".*\.md$",
            r".*\.json$",
            r".*\.sh$",
            r"backend/.*",
            r"frontend/.*",
            r"docs/.*",
            r".*requirements\.txt$",
            r".*package\.json$",
            r".*\.lock$"
        ]
        
        return any(re.match(pattern, filepath) for pattern in critical_patterns)
        
    def is_npm_cache(self, filepath: str) -> bool:
        """💾 Check if file is npm cache (less critical)"""
        npm_patterns = [
            r"C:\\Users\\.*\\.npm/_cacache/.*",
            r".*node_modules/.*",
            r".*\\.npm/.*"
        ]
        
        return any(re.match(pattern, filepath) for pattern in npm_patterns)
        
    def is_recoverable(self, filepath: str) -> bool:
        """🔄 Check if file is worth recovering"""
        if self.is_npm_cache(filepath):
            return False
            
        recoverable_patterns = [
            r".*\.py$",
            r".*\.ts$",
            r".*\.js$", 
            r".*\.md$",
            r".*\.json$",
            r".*\.yml$",
            r".*\.yaml$",
            r".*\.sh$",
            r".*\.html$",
            r".*\.css$"
        ]
        
        return any(re.match(pattern, filepath) for pattern in recoverable_patterns)
        
    def get_recovery_priority(self, filepath: str) -> int:
        """⭐ Get recovery priority (1-10, higher = more important)"""
        if "github/workflows" in filepath:
            return 10
        elif filepath.endswith(".py"):
            return 9
        elif filepath.endswith(".ts"):
            return 8
        elif filepath.endswith(".md"):
            return 7
        elif filepath.endswith(".json"):
            return 6
        elif filepath.endswith(".js"):
            return 5
        else:
            return 3
            
    def analyze_missing_files(self) -> dict:
        """🔍 Analyze currently missing files that should exist"""
        missing_analysis = {
            "expected_files": [],
            "missing_critical_files": [],
            "suggestions": []
        }
        
        # Check for expected files that might be missing
        expected_files = [
            ".github/workflows/ci.yml",
            "backend/requirements.txt",
            "frontend/package.json",
            "README.md",
            "LICENSE",
            ".gitignore"
        ]
        
        for expected_file in expected_files:
            file_path = self.workspace_path / expected_file
            if not file_path.exists():
                missing_analysis["missing_critical_files"].append(expected_file)
                
        return missing_analysis
        
    def check_wakatime_integration(self) -> dict:
        """⏰ Check WakaTime integration for timeline data"""
        wakatime_analysis = {
            "wakatime_config_found": False,
            "vscode_wakatime_extension": False,
            "timeline_data_available": False,
            "integration_suggestions": []
        }
        
        # Check for WakaTime config
        wakatime_config = Path.home() / ".wakatime.cfg"
        if wakatime_config.exists():
            wakatime_analysis["wakatime_config_found"] = True
            
        # Check VS Code settings for WakaTime
        vscode_settings = self.workspace_path / ".vscode" / "settings.json"
        if vscode_settings.exists():
            try:
                with open(vscode_settings, 'r') as f:
                    settings_content = f.read()
                    if "wakatime" in settings_content.lower():
                        wakatime_analysis["vscode_wakatime_extension"] = True
            except Exception:
                pass
                
        # Suggest WakaTime integration if not found
        if not wakatime_analysis["wakatime_config_found"]:
            wakatime_analysis["integration_suggestions"].append(
                "Install WakaTime for comprehensive timeline tracking"
            )
            
        return wakatime_analysis
        
    def recover_deleted_file(self, file_path: str, commit_hash: str) -> bool:
        """🔄 Recover a specific deleted file from git history"""
        try:
            print(f"🔄 Recovering {file_path} from commit {commit_hash[:8]}...")
            
            # Create recovery subdirectory
            recovery_path = self.recovery_dir / "recovered_files"
            recovery_path.mkdir(exist_ok=True)
            
            # Get file content from previous commit
            result = subprocess.run([
                "git", "show", f"{commit_hash}^:{file_path}"
            ], cwd=self.workspace_path, capture_output=True, text=True)
            
            if result.returncode == 0:
                # Create directory structure if needed
                recovered_file_path = recovery_path / file_path
                recovered_file_path.parent.mkdir(parents=True, exist_ok=True)
                
                # Write recovered content
                with open(recovered_file_path, 'w', encoding='utf-8') as f:
                    f.write(result.stdout)
                    
                print(f"✅ Successfully recovered {file_path}")
                return True
            else:
                print(f"❌ Failed to recover {file_path}: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ Recovery error for {file_path}: {e}")
            return False
            
    def batch_recover_critical_files(self, analysis: dict) -> dict:
        """🚀 Batch recover all critical deleted files"""
        print("🚀 INITIATING BATCH RECOVERY OF CRITICAL FILES...")
        
        recovery_results = {
            "total_attempts": 0,
            "successful_recoveries": 0,
            "failed_recoveries": 0,
            "recovered_files": [],
            "failed_files": []
        }
        
        # Sort critical files by recovery priority
        critical_files = sorted(
            analysis["critical_deletions"], 
            key=lambda x: self.get_recovery_priority(x["file"]), 
            reverse=True
        )
        
        for file_info in critical_files:
            recovery_results["total_attempts"] += 1
            
            if self.recover_deleted_file(file_info["file"], file_info["commit"]):
                recovery_results["successful_recoveries"] += 1
                recovery_results["recovered_files"].append(file_info["file"])
            else:
                recovery_results["failed_recoveries"] += 1
                recovery_results["failed_files"].append(file_info["file"])
                
        return recovery_results
        
    def create_recovery_report(self, analysis: dict, recovery_results: dict = None):
        """📊 Create comprehensive recovery report"""
        report_content = f"""# 🕰️💀 TIMELINE ARCHAEOLOGICAL RECOVERY REPORT 💀🕰️

## 📅 Analysis Timestamp: {analysis['scan_timestamp']}

## 🔍 DELETION TIMELINE ANALYSIS

### 📊 Summary Statistics:
- **Total Deletions Found**: {analysis['total_deletions_found']}
- **Critical Deletions**: {len(analysis['critical_deletions'])}
- **Recoverable Files**: {len(analysis['recoverable_files'])}
- **NPM Cache Deletions**: {len(analysis['npm_cache_deletions'])}

### 🚨 CRITICAL DELETED FILES:
"""
        
        for critical in analysis['critical_deletions']:
            report_content += f"""
#### 🔥 {critical['file']}
- **Commit**: {critical['commit'][:8]}
- **Date**: {critical['date']}
- **Message**: {critical['message']}
- **Priority**: {self.get_recovery_priority(critical['file'])}/10
"""
            
        if recovery_results:
            report_content += f"""
## 🔄 RECOVERY RESULTS

### 📈 Recovery Statistics:
- **Total Attempts**: {recovery_results['total_attempts']}
- **Successful Recoveries**: {recovery_results['successful_recoveries']}
- **Failed Recoveries**: {recovery_results['failed_recoveries']}
- **Success Rate**: {(recovery_results['successful_recoveries']/recovery_results['total_attempts']*100):.1f}%

### ✅ Successfully Recovered Files:
"""
            for recovered_file in recovery_results['recovered_files']:
                report_content += f"- ✅ {recovered_file}\n"
                
            if recovery_results['failed_files']:
                report_content += "\n### ❌ Failed Recovery Attempts:\n"
                for failed_file in recovery_results['failed_files']:
                    report_content += f"- ❌ {failed_file}\n"
                    
        # WakaTime integration status
        wakatime = analysis.get('wakatime_integration', {})
        report_content += f"""
## ⏰ WAKATIME INTEGRATION STATUS

- **Config Found**: {'✅' if wakatime.get('wakatime_config_found') else '❌'}
- **VS Code Extension**: {'✅' if wakatime.get('vscode_wakatime_extension') else '❌'}
- **Timeline Data**: {'✅' if wakatime.get('timeline_data_available') else '❌'}

### 🛠️ Timeline Enhancement Suggestions:
"""
        
        for suggestion in wakatime.get('integration_suggestions', []):
            report_content += f"- 💡 {suggestion}\n"
            
        report_content += """
## 🚀 RECOMMENDED ACTIONS

### Immediate Actions:
1. 🔄 Review recovered files in `.file_recovery_archaeology/recovered_files/`
2. 🔍 Validate critical functionality after file restoration
3. 📦 Reinstall dependencies if package files were recovered
4. ⏰ Set up WakaTime for better timeline tracking

### Prevention Measures:
1. 🛡️ Enable automated backups (.consciousness_timeline/auto_backup.sh)
2. 📸 Regular timeline snapshots (python3 practical_timeline_access.py)
3. 🔗 Configure git hooks for deletion notifications
4. ⚠️ Review deletion commands before execution

### Recovery Commands:
```bash
# Quick recovery check
python3 timeline_archaeological_recovery.py

# Restore specific files
cp .file_recovery_archaeology/recovered_files/path/to/file ./path/to/file

# Validate recovered files
git status
git diff
```

---

**🌊💋 Nautical Archaeological Summary:**
Sophisticated timeline excavation completed with Renaissance Eva Green-lengde precision! 
{recovery_results['successful_recoveries'] if recovery_results else 0} files rescued from the digital depths through advanced temporal navigation! 🛥️⚓

"""
        
        # Write report
        with open(self.recovery_report, 'w', encoding='utf-8') as f:
            f.write(report_content)
            
        print(f"📊 Recovery report created: {self.recovery_report}")
        
    def save_analysis(self, analysis: dict):
        """💾 Save analysis to JSON file"""
        with open(self.deleted_files_log, 'w', encoding='utf-8') as f:
            json.dump(analysis, f, indent=2)
            
        print(f"💾 Analysis saved: {self.deleted_files_log}")

def main():
    """🚀 Main timeline archaeological recovery execution"""
    print("🕰️💀 TIMELINE ARCHAEOLOGICAL FILE RECOVERY SYSTEM 💀🕰️")
    print("=" * 70)
    
    recovery_system = TimelineArchaeologicalRecovery()
    
    # Analyze deletion timeline
    print("🔍 Analyzing deletion timeline...")
    analysis = recovery_system.analyze_deletion_timeline()
    
    # Save analysis
    recovery_system.save_analysis(analysis)
    
    # Display summary
    print(f"\n📊 DELETION ANALYSIS SUMMARY:")
    print(f"  • Total deletions found: {analysis['total_deletions_found']}")
    print(f"  • Critical deletions: {len(analysis['critical_deletions'])}")
    print(f"  • Recoverable files: {len(analysis['recoverable_files'])}")
    print(f"  • NPM cache deletions: {len(analysis['npm_cache_deletions'])}")
    
    # Ask user about recovery
    if analysis['critical_deletions']:
        print(f"\n🚨 {len(analysis['critical_deletions'])} CRITICAL FILES DELETED!")
        
        try:
            response = input("🔄 Attempt batch recovery of critical files? (y/N): ").lower().strip()
        except KeyboardInterrupt:
            response = 'n'
            
        if response in ['y', 'yes']:
            print("\n🚀 Initiating batch recovery...")
            recovery_results = recovery_system.batch_recover_critical_files(analysis)
            
            print(f"\n✅ Recovery completed!")
            print(f"  • Successful: {recovery_results['successful_recoveries']}")
            print(f"  • Failed: {recovery_results['failed_recoveries']}")
            print(f"  • Success rate: {(recovery_results['successful_recoveries']/recovery_results['total_attempts']*100):.1f}%")
            
            # Create comprehensive report
            recovery_system.create_recovery_report(analysis, recovery_results)
        else:
            recovery_system.create_recovery_report(analysis)
    else:
        print("\n✅ No critical file deletions detected!")
        recovery_system.create_recovery_report(analysis)
        
    print(f"\n📋 Full recovery report available at:")
    print(f"  {recovery_system.recovery_report}")
    print(f"\n🛡️ Recovered files (if any) available at:")
    print(f"  {recovery_system.recovery_dir}/recovered_files/")
    
    print("\n🌊💋 Timeline archaeological mission completed with nautical sophistication! ⚓✨")

if __name__ == "__main__":
    main()
