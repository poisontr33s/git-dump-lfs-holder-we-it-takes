#!/usr/bin/env python3
"""
🎭 NECROMANCY DASHBOARD
Comprehensive overview of code optimization and resurrection efforts
"""

import os
import json
import re
from datetime import datetime
from collections import defaultdict

class NecromancyDashboard:
    def __init__(self):
        self.dashboard_data = {}
        self.load_all_reports()

    def load_all_reports(self):
        """Load all necromancy reports and data"""
        reports_dir = 'necromancy_graveyard'

        if not os.path.exists(reports_dir):

            return

        # Load pattern detection results
        pattern_file = os.path.join(reports_dir, 'pattern_detection_results.json')
        if os.path.exists(pattern_file):
            with open(pattern_file, 'r', encoding='utf-8') as f:
                self.dashboard_data['pattern_results'] = json.load(f)

        # Load resurrection plan
        plan_file = os.path.join(reports_dir, 'resurrection_plan.json')
        if os.path.exists(plan_file):
            with open(plan_file, 'r', encoding='utf-8') as f:
                self.dashboard_data['resurrection_plan'] = json.load(f)

        # Load optimization stats
        self._load_optimization_stats()

    def _load_optimization_stats(self):
        """Load optimization statistics from backup directory"""
        backup_dir = 'necromancy_graveyard/backups'
        if os.path.exists(backup_dir):
            backup_files = [f for f in os.listdir(backup_dir) if f.endswith('.backup')]
            self.dashboard_data['optimization_stats'] = {
                'backups_created': len(backup_files),
                'last_optimization': max([os.path.getmtime(os.path.join(backup_dir, f)) for f in backup_files]) if backup_files else None
            }
        else:
            self.dashboard_data['optimization_stats'] = {'backups_created': 0, 'last_optimization': None}

    def generate_dashboard_report(self):
        """Generate comprehensive dashboard report"""
        if not self.dashboard_data:
            return "❌ No necromancy data available. Run necromancy tools first."

        report = f"""# 🎭 NECROMANCY DASHBOARD
# Code Optimization & Resurrection Center
# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

"""

        # Repository Overview
        if 'resurrection_plan' in self.dashboard_data:
            plan = self.dashboard_data['resurrection_plan']
            report += f"""## 📊 REPOSITORY STATUS

### 📈 Key Metrics
- **Files Analyzed:** {plan['repository_overview']['total_files']}
- **Total Patterns Found:** {plan['repository_overview']['total_patterns']}
- **Average Patterns/File:** {plan['repository_overview']['average_patterns_per_file']}
- **Estimated Optimization Time:** {plan['estimated_timeline']['total_estimated_time']}

### 🎯 Priority Distribution
"""
            for priority, count in plan['repository_overview']['optimization_priority_distribution'].items():
                priority_icon = {'critical': '🔴', 'high': '🟠', 'medium': '🟡', 'low': '🟢'}[priority]
                report += f"- {priority_icon} **{priority.title()}:** {count} files\n"

        # Current Optimization Status
        if 'optimization_stats' in self.dashboard_data:
            stats = self.dashboard_data['optimization_stats']
            report += f"""

### ⚡ Optimization Status
- **Backups Created:** {stats['backups_created']}
- **Last Optimization:** {datetime.fromtimestamp(stats['last_optimization']).strftime('%Y-%m-%d %H:%M:%S') if stats['last_optimization'] else 'Never'}
"""

        # Top Priority Files
        if 'resurrection_plan' in self.dashboard_data:
            plan = self.dashboard_data['resurrection_plan']
            report += f"""

## 🎯 TOP PRIORITY FILES

"""
            for i, file_plan in enumerate(plan['file_plans'][:5], 1):
                priority_icon = {'critical': '🔴', 'high': '🟠', 'medium': '🟡', 'low': '🟢'}[file_plan['priority_level']]
                report += f"""### {i}. {priority_icon} {os.path.basename(file_plan['file'])}
**Priority:** {file_plan['priority_level'].title()} | **Score:** {file_plan['optimization_score']} | **Time:** {file_plan['estimated_total_time']}
**Key Issues:** {', '.join([opt['pattern'].replace('_', ' ').title() for opt in file_plan['optimizations'][:3]])}

"""

        # Global Patterns
        if 'resurrection_plan' in self.dashboard_data and self.dashboard_data['resurrection_plan']['global_optimizations']:
            global_opts = self.dashboard_data['resurrection_plan']['global_optimizations']
            report += f"""

## 🌍 GLOBAL OPTIMIZATION PATTERNS

"""
            for i, pattern in enumerate(global_opts[:5], 1):
                severity_breakdown = pattern['severity_breakdown']
                max_severity = max(severity_breakdown.keys(), key=lambda x: {'critical': 3, 'high': 2, 'medium': 1, 'low': 0}[x])
                severity_icon = {'critical': '🔴', 'high': '🟠', 'medium': '🟡', 'low': '🟢'}[max_severity]

                report += f"""### {i}. {severity_icon} {pattern['pattern'].replace('_', ' ').title()}
**Affected Files:** {pattern['affected_files']} | **Total:** {pattern['total_occurrences']}
**Severity:** {', '.join(f'{k}: {v}' for k, v in severity_breakdown.items())}

"""

        # Implementation Roadmap
        if 'resurrection_plan' in self.dashboard_data:
            phases = self.dashboard_data['resurrection_plan']['implementation_phases']
            report += f"""

## 📅 IMPLEMENTATION ROADMAP

"""
            for phase in phases:
                report += f"""### {phase['phase']}
**Files:** {len(phase['files'])} | **Time:** {phase['estimated_time']}
*{phase['description']}*

"""

        # Success Metrics
        if 'resurrection_plan' in self.dashboard_data:
            metrics = self.dashboard_data['resurrection_plan']['success_metrics']
            report += f"""

## 📈 SUCCESS METRICS

"""
            for metric in metrics:
                report += f"""### {metric['metric']}
**Target:** {metric['target']}
*Measured by: {metric['measurement']}*

"""

        # Quick Actions
        report += f"""

## 🚀 QUICK ACTIONS

### Immediate (Today)
- [ ] Review automated optimizations in `necromancy_graveyard/AUTOMATED_OPTIMIZATION_REPORT.md`
- [ ] Run test suite to verify functionality
- [ ] Commit optimization changes with descriptive message

### Short-term (This Week)
- [ ] Start with critical priority files from resurrection plan
- [ ] Implement high-impact optimizations
- [ ] Update documentation for modified code

### Long-term (Next Sprint)
- [ ] Complete systematic optimization phases
- [ ] Monitor success metrics
- [ ] Plan next optimization cycle

## 📋 AVAILABLE REPORTS

- **Pattern Detection:** `necromancy_graveyard/PATTERN_DETECTION_REPORT.md`
- **Resurrection Plan:** `necromancy_graveyard/RESURRECTION_PLAN.md`
- **Automated Optimization:** `necromancy_graveyard/AUTOMATED_OPTIMIZATION_REPORT.md`
- **Backup Files:** `necromancy_graveyard/backups/`

## 🛠️ NECROMANCY TOOLS

- **Graveyard Scanner:** `tools/necromancy_graveyard.py`
- **Pattern Detector:** `tools/necromancy_pattern_detector.py`
- **Resurrection Planner:** `tools/resurrection_plan_generator.py`
- **Auto Optimizer:** `tools/automated_code_optimizer.py`

---

*Dashboard automatically updated with latest optimization data.*
*Run necromancy tools to refresh data and reports.*
"""

        return report

    def generate_progress_summary(self):
        """Generate progress summary for quick overview"""
        if not self.dashboard_data:
            return "No data available"

        summary = []

        if 'resurrection_plan' in self.dashboard_data:
            plan = self.dashboard_data['resurrection_plan']
            summary.append(f"📁 {plan['repository_overview']['total_files']} files analyzed")
            summary.append(f"🎯 {plan['repository_overview']['total_patterns']} patterns found")
            summary.append(f"⏱️  {plan['estimated_timeline']['total_estimated_time']} estimated")

        if 'optimization_stats' in self.dashboard_data:
            stats = self.dashboard_data['optimization_stats']
            summary.append(f"📦 {stats['backups_created']} backups created")

        return " | ".join(summary)

    def save_dashboard(self):
        """Save dashboard to file"""
        os.makedirs('necromancy_graveyard', exist_ok=True)

        dashboard_report = self.generate_dashboard_report()

        with open('necromancy_graveyard/NECROMANCY_DASHBOARD.md', 'w', encoding='utf-8') as f:
            f.write(dashboard_report)

        # Also save as README in graveyard directory
        with open('necromancy_graveyard/README.md', 'w', encoding='utf-8') as f:
            f.write(dashboard_report)

    def run_dashboard_generation(self):
        """Run complete dashboard generation"""

        self.load_all_reports()

        if not self.dashboard_data:

            return None

        self.save_dashboard()

        progress_summary = self.generate_progress_summary()

        return {
            'dashboard_generated': True,
            'progress_summary': progress_summary
        }

def main():
    dashboard = NecromancyDashboard()
    result = dashboard.run_dashboard_generation()
    return result

if __name__ == "__main__":
    main()
