#!/usr/bin/env python3

import os
import json
import re
import ast
import subprocess
from datetime import datetime
from pathlib import Path
from collections import defaultdict

const_magic_50 = 50
const_magic_30 = 30
const_ten = 10

"""
🎭 NECROMANCY GRAVEYARD SYSTEM
Identifies sub-optimal code, dead patterns, and repurposable elements for resurrection
"""

class NecromancyGraveyard:
    def __init__(self):
        self.graveyard_dir = "necromancy_graveyard"
        self.scan_results = {}
        self.graveyard_inventory = {}
        self.resurrection_candidates = []

        # Sub-optimal patterns to detect
        self.suboptimal_patterns = {
            'python': {
                'dead_imports': r'^import\s+\w+(?:\s*,\s*\w+)*$',
                'unused_variables': r'^\s*[a-zA-Z_][a-zA-Z0-9_]*\s*=\s*.*$',
                'empty_functions': r'def\s+\w+\([^)]*\):\s*\n\s*pass',
                'redundant_code': r'if\s+.*:\s*\n\s*return\s+True\s*\n\s*else:\s*\n\s*return\s+False',
                'hardcoded_values': r'["\'][^"\']*["\']',
                'long_functions': r'def\s+\w+\([^)]*\):(?:\n\s+.*){const_magic_30,}',
                'nested_conditionals': r'if\s+.*:\s*\n\s+if\s+.*:\s*\n\s+if\s+.*:',
                'global_variables': r'^\s*[A-Z][A-Z_]*\s*=',
                'print_statements': r'print\s*\(',
                'todo_comments': r'#\s*TODO|#\s*FIXME|#\s*HACK',
                'deprecated_patterns': r'except\s+.*:\s*pass'
            },
            'javascript': {
                'console_logs': r'console\.log\s*\(',
                'var_declarations': r'\bvar\s+\w+',
                'global_variables': r'window\.\w+|global\.\w+',
                'hardcoded_values': r'["\'][^"\']*["\']',
                'empty_functions': r'function\s+\w+\([^)]*\)\s*\{\s*\}',
                'nested_callbacks': r'\}\s*\)\s*\(',
                'deprecated_methods': r'\.innerHTML\s*=|\.outerHTML',
                'unused_variables': r'let\s+\w+|const\s+\w+|var\s+\w+'
            },
            'markdown': {
                'broken_links': r'\[.*\]\([^)]*\)',
                'empty_sections': r'^##\s+.*\n\n(?=\n|$)',
                'redundant_headers': r'^#\s+.*\n=+\n',
                'inconsistent_formatting': r'^\s*[-*+]\s+.*\n\s*[-*+]\s+.*',
                'orphaned_code_blocks': r'```\w*\n.*?\n```'
            }
        }

        # Resurrection potential scores
        self.resurrection_potential = {
            'high': ['authentication', 'database', 'api', 'framework', 'architecture'],
            'medium': ['utility', 'helper', 'parser', 'validator', 'formatter'],
            'low': ['debug', 'test', 'temporary', 'prototype', 'experimental']
        }

    def scan_codebase(self):
        """Comprehensive scan of entire codebase"""

        # Scan Python files
        python_files = self.scan_python_files()

        # Scan JavaScript files
        js_files = self.scan_javascript_files()

        # Scan Markdown files
        md_files = self.scan_markdown_files()

        dead_files = self.scan_for_dead_files()

        # Analyze dependencies
        dependency_analysis = self.analyze_dependencies()

        self.scan_results = {
            'python_files': python_files,
            'javascript_files': js_files,
            'markdown_files': md_files,
            'dead_files': dead_files,
            'dependency_analysis': dependency_analysis,
            'scan_timestamp': datetime.now().isoformat(),
            'total_files_scanned': len(python_files) + len(js_files) + len(md_files)
        }

        return self.scan_results

    def scan_python_files(self):
        """Scan Python files for sub-optimal patterns"""
        python_files = []

        for root, dirs, files in os.walk('.'):
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['__pycache__', 'node_modules']]

            for file in files:
                if file.endswith('.py'):
                    filepath = os.path.join(root, file)
                    try:
                        with open(filepath, 'r', encoding='utf-8') as f:
                            content = f.read()

                        analysis = self.analyze_python_file(content, filepath)
                        if analysis['issues_found'] > 0:
                            python_files.append(analysis)
                    except Exception:
                        pass

        return python_files

    def analyze_python_file(self, content, filepath):
        """Analyze individual Python file"""
        issues = []
        resurrection_potential = 'low'

        for pattern_name, pattern in self.suboptimal_patterns['python'].items():
            matches = re.findall(pattern, content, re.MULTILINE)
            if matches:
                issues.append({
                    'type': pattern_name,
                    'count': len(matches),
                    'examples': matches[:3]  # First 3 examples
                })

        # Calculate resurrection potential
        filename_lower = os.path.basename(filepath).lower()
        for potential, keywords in self.resurrection_potential.items():
            if any(keyword in filename_lower for keyword in keywords):
                resurrection_potential = potential
                break

        try:
            tree = ast.parse(content)
            functions = [node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
            classes = [node for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]

            complexity_score = len(functions) + len(classes) * 2
        except:
            complexity_score = 0

        return {
            'issues_found': len(issues),
            'issues': issues,
            'resurrection_potential': resurrection_potential,
            'complexity_score': complexity_score,
            'line_count': len(content.split('\n')),
            'last_modified': os.path.getmtime(filepath)
        }

    def scan_javascript_files(self):
        """Scan JavaScript files for sub-optimal patterns"""
        js_files = []

        for root, dirs, files in os.walk('.'):
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules']]

            for file in files:
                if file.endswith('.js') or file.endswith('.ts'):
                    filepath = os.path.join(root, file)
                    try:
                        with open(filepath, 'r', encoding='utf-8') as f:
                            content = f.read()

                        analysis = self.analyze_javascript_file(content, filepath)
                        if analysis['issues_found'] > 0:
                            js_files.append(analysis)
                    except Exception:
                        pass

        return js_files

    def analyze_javascript_file(self, content, filepath):
        """Analyze individual JavaScript file"""
        issues = []
        resurrection_potential = 'low'

        for pattern_name, pattern in self.suboptimal_patterns['javascript'].items():
            matches = re.findall(pattern, content, re.MULTILINE)
            if matches:
                issues.append({
                    'type': pattern_name,
                    'count': len(matches),
                    'examples': matches[:3]
                })

        # Calculate resurrection potential
        filename_lower = os.path.basename(filepath).lower()
        for potential, keywords in self.resurrection_potential.items():
            if any(keyword in filename_lower for keyword in keywords):
                resurrection_potential = potential
                break

        return {
            'issues_found': len(issues),
            'issues': issues,
            'resurrection_potential': resurrection_potential,
            'line_count': len(content.split('\n')),
            'last_modified': os.path.getmtime(filepath)
        }

    def scan_markdown_files(self):
        """Scan Markdown files for sub-optimal patterns"""
        md_files = []

        for root, dirs, files in os.walk('.'):
            dirs[:] = [d for d in dirs if not d.startswith('.')]

            for file in files:
                if file.endswith('.md'):
                    filepath = os.path.join(root, file)
                    try:
                        with open(filepath, 'r', encoding='utf-8') as f:
                            content = f.read()

                        analysis = self.analyze_markdown_file(content, filepath)
                        if analysis['issues_found'] > 0:
                            md_files.append(analysis)
                    except Exception:
                        pass

        return md_files

    def analyze_markdown_file(self, content, filepath):
        """Analyze individual Markdown file"""
        issues = []

        for pattern_name, pattern in self.suboptimal_patterns['markdown'].items():
            matches = re.findall(pattern, content, re.MULTILINE | re.DOTALL)
            if matches:
                issues.append({
                    'type': pattern_name,
                    'count': len(matches),
                    'examples': [match[:const_magic_50] + '...' for match in matches[:3]]
                })

        return {
            'issues_found': len(issues),
            'issues': issues,
            'line_count': len(content.split('\n')),
            'last_modified': os.path.getmtime(filepath)
        }

    def scan_for_dead_files(self):
        """Scan for potentially dead/unused files"""
        dead_candidates = []

        all_files = []
        for root, dirs, files in os.walk('.'):
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['__pycache__', 'node_modules']]
            for file in files:
                if file.endswith(('.py', '.js', '.ts', '.md', '.json')):
                    all_files.append(os.path.join(root, file))

        for filepath in all_files:
            filename = os.path.basename(filepath)
            references_found = 0

            for other_file in all_files:
                if other_file != filepath:
                    try:
                        with open(other_file, 'r', encoding='utf-8') as f:
                            content = f.read()
                            if filename in content:
                                references_found += 1
                    except:
                        pass

            if references_found == 0:
                dead_candidates.append({
                    'filepath': filepath,
                    'references_found': references_found,
                    'file_size': os.path.getsize(filepath),
                    'last_modified': os.path.getmtime(filepath)
                })

        return dead_candidates

    def analyze_dependencies(self):
        """Analyze project dependencies for optimization opportunities"""
        analysis = {
            'python_packages': {},
            'node_packages': {},
            'unused_dependencies': [],
            'outdated_packages': []
        }

        # Check Python dependencies
        if os.path.exists('requirements.txt'):
            try:
                with open('requirements.txt', 'r') as f:
                    packages = f.read().split('\n')
                    analysis['python_packages'] = {pkg.split('==')[0]: pkg for pkg in packages if pkg.strip()}
            except:
                pass

        # Check Node dependencies
        if os.path.exists('package.json'):
            try:
                with open('package.json', 'r') as f:
                    package_data = json.load(f)
                    analysis['node_packages'] = package_data.get('dependencies', {})
            except:
                pass

        return analysis

    def create_graveyard_inventory(self):
        """Create comprehensive graveyard inventory"""

        os.makedirs(self.graveyard_dir, exist_ok=True)

        # Categorize by resurrection potential
        high_potential = []
        medium_potential = []
        low_potential = []

        # Process Python files
        for file_analysis in self.scan_results['python_files']:
            if file_analysis['resurrection_potential'] == 'high':
                high_potential.append(file_analysis)
            elif file_analysis['resurrection_potential'] == 'medium':
                medium_potential.append(file_analysis)
            else:
                low_potential.append(file_analysis)

        # Process JavaScript files
        for file_analysis in self.scan_results['javascript_files']:
            if file_analysis['resurrection_potential'] == 'high':
                high_potential.append(file_analysis)
            elif file_analysis['resurrection_potential'] == 'medium':
                medium_potential.append(file_analysis)
            else:
                low_potential.append(file_analysis)

        self.graveyard_inventory = {
            'high_resurrection_potential': high_potential,
            'medium_resurrection_potential': medium_potential,
            'low_resurrection_potential': low_potential,
            'dead_files': self.scan_results['dead_files'],
            'dependency_analysis': self.scan_results['dependency_analysis'],
            'created_at': datetime.now().isoformat()
        }

        # Save inventory
        inventory_path = os.path.join(self.graveyard_dir, 'graveyard_inventory.json')
        with open(inventory_path, 'w', encoding='utf-8') as f:
            json.dump(self.graveyard_inventory, f, indent=2, ensure_ascii=False)

        return self.graveyard_inventory

    def generate_resurrection_plan(self):
        """Generate resurrection plan for repurposing sub-optimal code"""

        resurrection_plan = {
            'immediate_actions': [],
            'short_term_goals': [],
            'long_term_vision': [],
            'resurrection_candidates': []
        }

        # Immediate actions (low-hanging fruit)
        for file_analysis in self.graveyard_inventory['low_resurrection_potential']:
            for issue in file_analysis['issues']:
                if issue['type'] in ['print_statements', 'console_logs', 'todo_comments']:
                    resurrection_plan['immediate_actions'].append({
                        'action': f"Remove {issue['count']} {issue['type']} from {os.path.basename(file_analysis['filepath'])}",
                        'file': file_analysis['filepath'],
                        'impact': 'code_cleanup',
                        'effort': 'low'
                    })

        # Short-term goals (medium impact)
        for file_analysis in self.graveyard_inventory['medium_resurrection_potential']:
            resurrection_plan['short_term_goals'].append({
                'goal': f"Refactor {os.path.basename(file_analysis['filepath'])} for better maintainability",
                'issues_count': file_analysis['issues_found'],
                'complexity_score': file_analysis.get('complexity_score', 0),
                'effort': 'medium'
            })

        # Long-term vision (high impact)
        for file_analysis in self.graveyard_inventory['high_resurrection_potential']:
            resurrection_plan['long_term_vision'].append({
                'vision': f"Transform {os.path.basename(file_analysis['filepath'])} into reusable framework component",
                'potential_value': 'high',
                'current_issues': file_analysis['issues_found'],
                'effort': 'high'
            })

        # Resurrection candidates
        for file_analysis in self.graveyard_inventory['high_resurrection_potential'] + self.graveyard_inventory['medium_resurrection_potential']:
            resurrection_plan['resurrection_candidates'].append({
                'file': file_analysis['filepath'],
                'resurrection_potential': file_analysis.get('resurrection_potential', 'unknown'),
                'issues_to_address': [issue['type'] for issue in file_analysis['issues']],
                'estimated_effort': self.estimate_resurrection_effort(file_analysis)
            })

        # Save resurrection plan
        plan_path = os.path.join(self.graveyard_dir, 'resurrection_plan.json')
        with open(plan_path, 'w', encoding='utf-8') as f:
            json.dump(resurrection_plan, f, indent=2, ensure_ascii=False)

        return resurrection_plan

    def estimate_resurrection_effort(self, file_analysis):
        """Estimate effort required for resurrection"""
        base_effort = file_analysis['issues_found'] * const_ten  # const_ten minutes per issue

        if 'complexity_score' in file_analysis:
            base_effort += file_analysis['complexity_score'] * 5

        if file_analysis.get('resurrection_potential') == 'high':
            base_effort *= 1.5
        elif file_analysis.get('resurrection_potential') == 'medium':
            base_effort *= 1.2

        return f"{int(base_effort)} minutes"

    def create_graveyard_report(self):
        """Create comprehensive graveyard report"""

        report = f"""# 🎭 NECROMANCY GRAVEYARD REPORT
# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 📈 SCAN SUMMARY
- **Total Files Scanned:** {self.scan_results['total_files_scanned']}
- **Python Files with Issues:** {len(self.scan_results['python_files'])}
- **JavaScript Files with Issues:** {len(self.scan_results['javascript_files'])}
- **Markdown Files with Issues:** {len(self.scan_results['markdown_files'])}
- **Potentially Dead Files:** {len(self.scan_results['dead_files'])}

## ⚰️ HIGH RESURRECTION POTENTIAL ({len(self.graveyard_inventory['high_resurrection_potential'])} files)

"""

        for file_analysis in self.graveyard_inventory['high_resurrection_potential']:
            report += f"### {os.path.basename(file_analysis['filepath'])}\n"
            report += f"- **Issues Found:** {file_analysis['issues_found']}\n"
            report += f"- **Lines:** {file_analysis['line_count']}\n"
            report += f"- **Key Issues:** {', '.join([issue['type'] for issue in file_analysis['issues'][:3]])}\n\n"

        report += f"""## 🔄 MEDIUM RESURRECTION POTENTIAL ({len(self.graveyard_inventory['medium_resurrection_potential'])} files)

"""

        for file_analysis in self.graveyard_inventory['medium_resurrection_potential']:
            report += f"### {os.path.basename(file_analysis['filepath'])}\n"
            report += f"- **Issues Found:** {file_analysis['issues_found']}\n"
            report += f"- **Lines:** {file_analysis['line_count']}\n\n"

        report += f"""## 🪦 DEAD FILES CANDIDATES ({len(self.graveyard_inventory['dead_files'])} files)

"""

        for dead_file in self.graveyard_inventory['dead_files'][:const_ten]:  # Show first const_ten
            report += f"- `{os.path.basename(dead_file['filepath'])}` ({dead_file['file_size']} bytes)\n"

        if len(self.graveyard_inventory['dead_files']) > const_ten:
            report += f"- ... and {len(self.graveyard_inventory['dead_files']) - const_ten} more\n"

        report += f"""
## 🎯 RESURRECTION ROADMAP

### Immediate Actions (Low Effort, High Impact)
- Clean up debug statements and TODO comments
- Remove unused imports and variables
- Standardize code formatting

### Short-term Goals (Medium Effort, Medium Impact)
- Refactor complex functions into smaller, focused functions
- Implement proper error handling
- Add comprehensive documentation

### Long-term Vision (High Effort, High Value)
- Transform high-potential code into reusable framework components
- Implement proper testing and validation
- Create modular, maintainable architecture

---

*Generated by Necromancy Graveyard System - Ready for code resurrection and optimization*
"""

        # Save report
        report_path = os.path.join(self.graveyard_dir, 'GRAVEYARD_REPORT.md')
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)

        return report_path

    def run_necromancy_scan(self):
        """Run complete necromancy scan"""

        # Scan codebase
        scan_results = self.scan_codebase()

        # Create inventory
        inventory = self.create_graveyard_inventory()

        # Generate resurrection plan
        resurrection_plan = self.generate_resurrection_plan()

        # Create report
        report_path = self.create_graveyard_report()

        return {
            'inventory': inventory,
            'resurrection_plan': resurrection_plan,
            'report_path': report_path
        }

def main():
    graveyard = NecromancyGraveyard()
    results = graveyard.run_necromancy_scan()

    print(f"⚰️ High Potential Candidates: {len(results['inventory']['high_resurrection_potential'])}")
    print(f"🔄 Medium Potential Candidates: {len(results['inventory']['medium_resurrection_potential'])}")
    print(f"🪦 Dead Files: {len(results['inventory']['dead_files'])}")

    return results

if __name__ == "__main__":
    main()
