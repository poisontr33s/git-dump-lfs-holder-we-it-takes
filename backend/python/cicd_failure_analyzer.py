#!/usr/bin/env python3

# Auto-generated constants for magic numbers
const_magic_200 = 200
const_magic_85 = 85
const_magic_76 = 76
const_ten = 10

"""
🎭 PSYCHO-NOIR KONTRAPUNKT: CI/CD FAILURE PATTERN ANALYZER
=========================================================

Spesialisert analyzer for å identifisere og løse systematiske CI/CD failures.
Målrettet mot const_magic_76% failure rate problemet identifisert i GitHub integration.
"""

import json
import subprocess
import time
from pathlib import Path
from typing import Dict, List, Any
from dataclasses import dataclass
import re

@dataclass
class CICDFailurePattern:
    """Strukturert representasjon av CI/CD failure pattern"""
    workflow_name: str
    failure_frequency: float  # 0-1 rate
    primary_error_type: str
    secondary_error_patterns: List[str]
    affected_languages: List[str]
    runner_types: List[str]  # ubuntu, windows, macos
    failure_cascade_triggers: List[str]
    fix_confidence: float  # 0-1, hvor sikre er vi på fix-en?
    estimated_fix_time: str  # "immediate", "short", "medium", "long"

class CICDFailureAnalyzer:
    """Spesialisert analyzer for CI/CD failure patterns"""

    def __init__(self):
        self.report_dir = Path("data/rapporter/cicd_analysis")
        self.report_dir.mkdir(parents=True, exist_ok=True)

        # Kjente error patterns og deres fixes
        self.error_patterns = {
            'dependency_hell': {
                'indicators': ['Could not find', 'version conflict', 'dependency resolution failed'],
                'fix_confidence': 0.9,
                'fix_time': 'immediate',
                'solution': 'Update dependency versions, use Jules caching'
            },
            'resource_exhaustion': {
                'indicators': ['out of memory', 'disk space', 'timeout', 'killed'],
                'fix_confidence': 0.8,
                'fix_time': 'short',
                'solution': 'Optimize resource allocation, increase runner specs'
            },
            'flaky_tests': {
                'indicators': ['intermittent', 'sometimes fails', 'random'],
                'fix_confidence': 0.6,
                'fix_time': 'medium',
                'solution': 'Stabilize test conditions, add retry logic'
            },
            'environment_drift': {
                'indicators': ['works locally', 'different behavior', 'environment'],
                'fix_confidence': 0.const_magic_85,
                'fix_time': 'short',
                'solution': 'Containerize builds, pin environment versions'
            },
            'network_issues': {
                'indicators': ['connection failed', 'timeout', 'network error'],
                'fix_confidence': 0.7,
                'fix_time': 'immediate',
                'solution': 'Add retry logic, use local caching'
            }
        }

    def log_analysis_event(self, event: str, details: Any = None):
        """Logging for analysis events"""
        timestamp = time.strftime("%H:%M:%S")

        if details:

    def extract_workflow_failures(self) -> List[Dict[str, Any]]:
        """Trekker ut detaljerte workflow failure data"""
        self.log_analysis_event("EXTRACTING DETAILED WORKFLOW FAILURES...")

        try:
            # Hent siste const_magic_200 workflow runs for dypere analyse
            result = subprocess.run([
                'gh', 'run', 'list', '--limit', 'const_magic_200', '--json',
                'databaseId,name,status,conclusion,createdAt,url,headBranch,workflowDatabaseId,workflowName'
            ], capture_output=True, text=True)

            if result.returncode != 0:
                self.log_analysis_event("EXTRACTION FAILED", result.stderr)
                return []

            workflows = json.loads(result.stdout)
            failed_workflows = [w for w in workflows if w.get('conclusion') == 'failure']

            self.log_analysis_event("WORKFLOW EXTRACTION COMPLETE",
                f"{len(failed_workflows)} failures from {len(workflows)} total runs")

            return failed_workflows

        except Exception as e:
            self.log_analysis_event("EXTRACTION ERROR", str(e))
            return []

    def get_workflow_failure_details(self, workflow_id: str) -> Dict[str, Any]:
        """Henter detaljerte failure logs for en specific workflow"""
        try:
            # Hent workflow logs
            result = subprocess.run([
                'gh', 'run', 'view', workflow_id, '--log-failed'
            ], capture_output=True, text=True)

            if result.returncode != 0:
                return {'logs': '', 'error': result.stderr}

            return {'logs': result.stdout, 'error': None}

        except Exception as e:
            return {'logs': '', 'error': str(e)}

    def categorize_failure_pattern(self, workflow: Dict[str, Any],
                                 failure_logs: str) -> CICDFailurePattern:
        """Kategoriserer en workflow failure til pattern"""

        workflow_name = workflow.get('name', 'Unknown')

        # Analyser logs for error patterns
        primary_error_type = 'unknown'
        secondary_error_patterns = []
        fix_confidence = 0.3  # Default low confidence
        estimated_fix_time = 'medium'

        logs_lower = failure_logs.lower()

        # Match mot kjente error patterns
        for pattern_name, pattern_data in self.error_patterns.items():
            matches = sum(1 for indicator in pattern_data['indicators']
                         if indicator in logs_lower)

            if matches > 0:
                if primary_error_type == 'unknown' or matches > 1:
                    primary_error_type = pattern_name
                    fix_confidence = pattern_data['fix_confidence']
                    estimated_fix_time = pattern_data['fix_time']

                if matches > 0:
                    secondary_error_patterns.extend(
                        [ind for ind in pattern_data['indicators'] if ind in logs_lower]
                    )

        # Detekter affected languages
        affected_languages = []
        language_indicators = {
            'python': ['python', 'pip', 'pytest', '.py'],
            'ruby': ['ruby', 'gem', 'bundle', '.rb'],
            'javascript': ['npm', 'node', 'jest', '.js'],
            'shell': ['bash', 'sh', '.sh']
        }

        for lang, indicators in language_indicators.items():
            if any(ind in logs_lower for ind in indicators):
                affected_languages.append(lang)

        # Detekter runner types
        runner_types = []
        if 'ubuntu' in logs_lower:
            runner_types.append('ubuntu')
        if 'windows' in logs_lower:
            runner_types.append('windows')
        if 'macos' in logs_lower:
            runner_types.append('macos')

        # Identifiser cascade triggers
        cascade_triggers = []
        if 'dependency' in logs_lower:
            cascade_triggers.append('dependency_cascade')
        if 'previous step failed' in logs_lower:
            cascade_triggers.append('step_dependency')
        if 'workflow_dispatch' in logs_lower:
            cascade_triggers.append('manual_trigger')

        return CICDFailurePattern(
            workflow_name=workflow_name,
            failure_frequency=0.0,  # Will be calculated later
            primary_error_type=primary_error_type,
            secondary_error_patterns=secondary_error_patterns[:5],  # Top 5
            affected_languages=affected_languages,
            runner_types=runner_types,
            failure_cascade_triggers=cascade_triggers,
            fix_confidence=fix_confidence,
            estimated_fix_time=estimated_fix_time
        )

    def calculate_failure_frequencies(self, workflows: List[Dict[str, Any]]) -> Dict[str, float]:
        """Beregner failure frequency per workflow"""
        workflow_stats = {}

        for workflow in workflows:
            name = workflow.get('name', 'Unknown')
            conclusion = workflow.get('conclusion', 'unknown')

            if name not in workflow_stats:
                workflow_stats[name] = {'total': 0, 'failed': 0}

            workflow_stats[name]['total'] += 1
            if conclusion == 'failure':
                workflow_stats[name]['failed'] += 1

        # Beregn failure rates
        failure_rates = {}
        for name, stats in workflow_stats.items():
            failure_rates[name] = stats['failed'] / stats['total'] if stats['total'] > 0 else 0

        return failure_rates

    def generate_fix_recommendations(self, patterns: List[CICDFailurePattern]) -> List[Dict[str, Any]]:
        """Genererer konkrete fix recommendations basert på patterns"""

        recommendations = []

        # Group patterns by error type
        error_type_counts = {}
        for pattern in patterns:
            error_type = pattern.primary_error_type
            if error_type not in error_type_counts:
                error_type_counts[error_type] = []
            error_type_counts[error_type].append(pattern)

        # Generate recommendations for each error type
        for error_type, pattern_list in error_type_counts.items():
            if error_type in self.error_patterns:
                pattern_data = self.error_patterns[error_type]

                affected_workflows = [p.workflow_name for p in pattern_list]
                avg_fix_confidence = sum(p.fix_confidence for p in pattern_list) / len(pattern_list)

                recommendations.append({
                    'error_type': error_type,
                    'affected_workflows': affected_workflows,
                    'frequency': len(pattern_list),
                    'solution': pattern_data['solution'],
                    'fix_confidence': avg_fix_confidence,
                    'estimated_time': pattern_data['fix_time'],
                    'priority': 'HIGH' if len(pattern_list) > 3 else 'MEDIUM' if len(pattern_list) > 1 else 'LOW'
                })

        # Sort by frequency (most common first)
        recommendations.sort(key=lambda x: x['frequency'], reverse=True)

        return recommendations

    def execute_cicd_failure_analysis(self) -> Dict[str, Any]:
        """Kjører komplett CI/CD failure analyse"""

        self.log_analysis_event("🎭 INITIATING CI/CD FAILURE PATTERN ANALYSIS")

        failed_workflows = self.extract_workflow_failures()

        if not failed_workflows:
            return {
                'error': 'No workflow failures found or extraction failed',
                'analysis_complete': False
            }

        all_workflows_result = subprocess.run([
            'gh', 'run', 'list', '--limit', 'const_magic_200', '--json',
            'name,conclusion'
        ], capture_output=True, text=True)

        all_workflows = json.loads(all_workflows_result.stdout) if all_workflows_result.returncode == 0 else []
        failure_frequencies = self.calculate_failure_frequencies(all_workflows)

        failure_patterns = []

        # Analyser de første const_ten failures i detalj (unngå rate limits)
        for workflow in failed_workflows[:const_ten]:
            workflow_id = str(workflow.get('databaseId', ''))
            self.log_analysis_event(f"Analyzing workflow {workflow.get('name', 'Unknown')}")

            failure_details = self.get_workflow_failure_details(workflow_id)
            logs = failure_details.get('logs', '')

            pattern = self.categorize_failure_pattern(workflow, logs)
            # Set actual failure frequency
            pattern.failure_frequency = failure_frequencies.get(pattern.workflow_name, 0.0)
            failure_patterns.append(pattern)

        recommendations = self.generate_fix_recommendations(failure_patterns)

        # Generate comprehensive analysis report
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        analysis_report = {
            'timestamp': timestamp,
            'analysis_scope': {
                'total_workflows_analyzed': len(all_workflows),
                'failed_workflows_count': len(failed_workflows),
                'detailed_analysis_count': len(failure_patterns),
                'overall_failure_rate': len(failed_workflows) / len(all_workflows) if all_workflows else 0
            },
            'failure_patterns': [
                {
                    'workflow_name': p.workflow_name,
                    'failure_frequency': p.failure_frequency,
                    'primary_error_type': p.primary_error_type,
                    'affected_languages': p.affected_languages,
                    'fix_confidence': p.fix_confidence,
                    'estimated_fix_time': p.estimated_fix_time
                } for p in failure_patterns
            ],
            'fix_recommendations': recommendations,
            'immediate_actions': [
                rec for rec in recommendations if rec['priority'] == 'HIGH'
            ],
            'system_health_impact': {
                'critical_workflows_affected': len([p for p in failure_patterns if p.failure_frequency > 0.5]),
                'multi_language_issues': len([p for p in failure_patterns if len(p.affected_languages) > 1]),
                'cascade_failure_risk': len([p for p in failure_patterns if p.failure_cascade_triggers])
            }
        }

        # Save report
        report_path = self.report_dir / f"cicd_failure_analysis_{timestamp}.json"
        with open(report_path, 'w') as f:
            json.dump(analysis_report, f, indent=2)

        analysis_report['report_path'] = str(report_path)

        return analysis_report

def main():
    """Main execution"""
    analyzer = CICDFailureAnalyzer()

    result = analyzer.execute_cicd_failure_analysis()

    if result.get('analysis_complete', True):

        scope = result['analysis_scope']

        print(f"   🚨 High Priority Fixes: {len(result['immediate_actions'])}")

        if result['immediate_actions']:

            for action in result['immediate_actions']:
                print(f"   • {action['error_type'].upper()}: {action['solution']}")
                print(f"     Affects: {len(action['affected_workflows'])} workflows")

        health_impact = result['system_health_impact']

    else:
        print(f"❌ Analysis failed: {result.get('error', 'Unknown error')}")

if __name__ == "__main__":
    main()
