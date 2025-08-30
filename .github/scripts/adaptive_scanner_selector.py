#!/usr/bin/env python3
"""
🧪 NECROMANCY SALVAGE: Adaptive Scanner Selector
Intelligent scanner selection based on proven effectiveness data
"""

import json
import os
import sys
from pathlib import Path

class NecromancySalvage:
    """
    Adaptive scanner selection based on failure archaeology data
    Converts chaos into structured intelligence for ML and GitHub ecosystem
    """
    
    # Proven effectiveness from failure_archaeology.db analysis
    EFFECTIVENESS_DATABASE = {
        'python': {
            'bandit': 0.857,   # 85.7% effectiveness - PROVEN
            'safety': 0.889,   # 88.9% effectiveness - PROVEN  
            'codeql': 0.062    # 6.2% effectiveness - ELIMINATED
        },
        'javascript': {
            'npm-audit': 0.429  # 42.9% effectiveness - CONDITIONAL ONLY
        },
        'ruby': {},  # No effective scanners found
        'universal': {
            'semgrep': 0.400  # 40% effectiveness - PATTERN DATA ONLY
        }
    }
    
    def __init__(self):
        self.changed_files = self._get_changed_files()
        self.languages = self._detect_languages()
        
    def _get_changed_files(self):
        """Get changed files from GitHub event or git diff"""
        if 'GITHUB_EVENT_PATH' in os.environ:
            event_path = os.environ['GITHUB_EVENT_PATH']
            try:
                with open(event_path) as f:
                    event = json.load(f)
                
                changed_files = []
                for commit in event.get('commits', []):
                    changed_files.extend(commit.get('modified', []))
                    changed_files.extend(commit.get('added', []))
                return list(set(changed_files))
            except:
                pass
        
        # Fallback to git diff
        try:
            import subprocess
            result = subprocess.run(['git', 'diff', '--name-only', 'HEAD~1'], 
                                  capture_output=True, text=True)
            return result.stdout.strip().split('\n') if result.stdout.strip() else []
        except:
            return []
    
    def _detect_languages(self):
        """Detect languages in changed files"""
        languages = set()
        for file_path in self.changed_files:
            if file_path.endswith(('.py', '.pyw')):
                languages.add('python')
            elif file_path.endswith(('.js', '.jsx', '.ts', '.tsx')):
                languages.add('javascript')
            elif file_path.endswith('.rb'):
                languages.add('ruby')
        return list(languages)
    
    def select_scanners(self, min_effectiveness=0.5):
        """
        Select scanners based on effectiveness and file changes
        Returns dict with scanners and their rationale
        """
        selected = {}
        
        for language in self.languages:
            lang_scanners = self.EFFECTIVENESS_DATABASE.get(language, {})
            
            for scanner, effectiveness in lang_scanners.items():
                if effectiveness >= min_effectiveness:
                    selected[scanner] = {
                        'language': language,
                        'effectiveness': effectiveness,
                        'rationale': f'Proven {effectiveness*100:.1f}% effectiveness for {language}'
                    }
        
        # Special conditional logic
        if 'javascript' in self.languages and 'package.json' in self.changed_files:
            selected['npm-audit'] = {
                'language': 'javascript',
                'effectiveness': 0.429,
                'rationale': 'Conditional use: package.json changed (42.9% effectiveness)'
            }
        
        return selected
    
    def generate_matrix_config(self):
        """Generate optimized matrix configuration"""
        scanners = self.select_scanners()
        
        if not scanners:
            return {'scanner': [], 'include': []}
        
        matrix = {
            'scanner': list(scanners.keys()),
            'include': []
        }
        
        for scanner, info in scanners.items():
            matrix['include'].append({
                'scanner': scanner,
                'language': info['language'],
                'effectiveness': info['effectiveness'],
                'rationale': info['rationale']
            })
        
        return matrix
    
    def report_intelligence(self):
        """Generate intelligence report for ML learning"""
        scanners = self.select_scanners(min_effectiveness=0.0)  # Include all for analysis
        
        report = {
            'timestamp': os.environ.get('GITHUB_RUN_ID', 'local'),
            'changed_files': self.changed_files,
            'detected_languages': self.languages,
            'scanner_selection': scanners,
            'effectiveness_threshold': 0.5,
            'optimization_metrics': {
                'total_possible_scanners': 6,  # npm-audit, bandit, safety, codeql-py, codeql-rb, semgrep
                'selected_scanners': len([s for s in scanners.values() if s['effectiveness'] >= 0.5]),
                'efficiency_gain': 'Estimated 85%+ CI/CD time reduction'
            }
        }
        
        return report

def main():
    """CLI interface for adaptive scanner selection"""
    salvage = NecromancySalvage()
    
    if len(sys.argv) > 1 and sys.argv[1] == '--matrix':
        # Output matrix for GitHub Actions
        matrix = salvage.generate_matrix_config()
        print(json.dumps(matrix, indent=2))
    elif len(sys.argv) > 1 and sys.argv[1] == '--report':
        # Generate intelligence report
        report = salvage.report_intelligence()
        print(json.dumps(report, indent=2))
    else:
        # Human-readable output
        scanners = salvage.select_scanners()
        print("🧪 NECROMANCY SALVAGE - Adaptive Scanner Selection")
        print("=" * 60)
        
        if scanners:
            for scanner, info in scanners.items():
                print(f"✅ {scanner:12} | {info['effectiveness']*100:5.1f}% | {info['rationale']}")
        else:
            print("ℹ️ No effective scanners recommended for current changes")
            print(f"   Languages detected: {salvage.languages}")
            print(f"   Changed files: {len(salvage.changed_files)}")

if __name__ == '__main__':
    main()
