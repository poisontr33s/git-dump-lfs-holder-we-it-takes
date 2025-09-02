#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Auto-generated constants for magic numbers
const_magic_50 = const_magic_50

"""
FAILED RUNS HARVESTER
Psycho-Noir Kontrapunkt - Høster og prosesserer failed runs fra GitHub Actions og Copilot

Dette scriptet:
1. Samler inn alle failed runs fra GitHub Actions/Copilot runners
2. Parser error logs og ekstraherer nøkkelinformasjon
3. Feeder dataene til Failure Archaeology systemet
4. Genererer learning reports og prevention strategies
"""

import json
import subprocess
import re
import datetime
from pathlib import Path
from typing import Dict, List, Optional
from failure_archaeology import FailureArchaeologist

class FailedRunsHarvester:
    """
    HARVESTER - Samler inn og prosesserer failed runs systematisk

    Implementerer Den Usynlige Hånds pattern recognition på tvers av:
    - GitHub Actions failures
    - Copilot runner crashes
    - Bot failures
    - Code quality issues
    - Deployment failures
    """

    def __init__(self, repo_path: str = "."):
        self.repo_path = Path(repo_path)
        self.archaeologist = FailureArchaeologist()

    def harvest_github_actions_failures(self) -> List[Dict]:
        """Høster failed GitHub Actions runs"""

        try:
            # Get list of workflow runs (failed ones)
            result = subprocess.run([
                'gh', 'run', 'list',
                '--status', 'failure',
                '--limit', 'const_magic_50',
                '--json', 'databaseId,status,conclusion,workflowName,displayTitle,createdAt,url'
            ], capture_output=True, text=True, cwd=self.repo_path)

            if result.returncode != 0:

                return []

            failed_runs = json.loads(result.stdout)

            processed_failures = []
            for run in failed_runs:
                failure_details = self._process_github_action_failure(run)
                if failure_details:
                    processed_failures.append(failure_details)

            print(f"✅ Processed {len(processed_failures)} GitHub Actions failures")
            return processed_failures

        except Exception as e:

            return []

    def _process_github_action_failure(self, run: Dict) -> Optional[Dict]:
        """Prosesserer en enkelt GitHub Action failure"""
        try:
            # Get detailed logs for this run
            result = subprocess.run([
                'gh', 'run', 'view', str(run['databaseId']),
                '--log-failed'
            ], capture_output=True, text=True, cwd=self.repo_path)

            if result.returncode != 0:
                error_trace = f"Failed to fetch logs: {result.stderr}"
            else:
                error_trace = result.stdout

            # Extract key information
            failure_details = {
                'source': 'github_actions',
                'run_id': run['databaseId'],
                'workflow_name': run['workflowName'],
                'title': run['displayTitle'],
                'created_at': run['createdAt'],
                'url': run['url'],
                'error_trace': error_trace,
                'context': {
                    'workflow': run['workflowName'],
                    'status': run['status'],
                    'conclusion': run['conclusion'],
                    'platform': 'github_actions'
                }
            }

            return failure_details

        except Exception as e:
            print(f"❌ Error processing run {run.get('databaseId', 'unknown')}: {e}")
            return None

    def generate_comprehensive_report(self) -> Dict:
        """Genererer en komprehensiv rapport over alle failures og læring"""

        # For now, focus on GitHub Actions since that's most reliable
        github_failures = self.harvest_github_actions_failures()

        all_failures = {
            'github_actions': github_failures,
            'copilot_runners': [],  # Will be populated when we have better log access
            'bot_failures': [],
            'code_quality': []
        }

        # Process through archaeology
        archaeology_results = self.process_failures_with_archaeology(all_failures)

        # Generate final report
        report = {
            'timestamp': datetime.datetime.now().isoformat(),
            'summary': {
                'total_failures_found': sum(len(failures) for failures in all_failures.values()),
                'failure_breakdown': {k: len(v) for k, v in all_failures.items()},
                'processed_through_archaeology': archaeology_results['processed_count']
            },
            'raw_failures': all_failures,
            'archaeology_analysis': archaeology_results['learning_library'],
            'preemptive_logging_strategy': archaeology_results['preemptive_config'],
            'bidirectional_learning_recommendations': archaeology_results['recommendations']
        }

        # Save comprehensive report
        report_file = Path("data/failure_archaeology/comprehensive_failure_report.json")
        report_file.parent.mkdir(parents=True, exist_ok=True)

        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)

        return report

    def process_failures_with_archaeology(self, all_failures: Dict[str, List[Dict]]) -> Dict:
        """Prosesserer alle failures gjennom Failure Archaeology systemet"""

        processed_count = 0

        for failure_type, failures in all_failures.items():
            for failure in failures:
                try:
                    # Map failure data to archaeology format
                    failure_id = self.archaeologist.catalog_failure(
                        failure_type=failure.get('source', failure_type),
                        error_trace=failure.get('error_trace', 'No trace available'),
                        context=failure.get('context', {}),
                        root_cause_hypothesis=self._generate_hypothesis(failure),
                        severity=self._assess_severity(failure)
                    )

                    processed_count += 1

                except Exception as e:

        # Generate comprehensive report
        learning_library = self.archaeologist.export_learning_library()
        preemptive_config = self.archaeologist.generate_preemptive_logging_config()
        recommendations = self.archaeologist.get_bidirectional_learning_recommendations()

        return {
            'learning_library': learning_library,
            'preemptive_config': preemptive_config,
            'recommendations': recommendations,
            'processed_count': processed_count
        }

    def _generate_hypothesis(self, failure: Dict) -> str:
        """Genererer initial hypothesis om root cause"""
        error_trace = failure.get('error_trace', '').lower()

        if 'timeout' in error_trace:
            return "Network/resource timeout issue"
        elif 'memory' in error_trace:
            return "Memory allocation or leak issue"
        elif 'permission' in error_trace or 'access' in error_trace:
            return "Permission or access rights issue"
        elif 'connection' in error_trace:
            return "Network connectivity issue"
        elif 'syntax' in error_trace or 'parse' in error_trace:
            return "Code syntax or parsing issue"
        else:
            return "Unknown - requires further investigation"

    def _assess_severity(self, failure: Dict) -> int:
        """Vurderer severity av en failure (1-5)"""
        error_trace = failure.get('error_trace', '').lower()
        source = failure.get('source', '').lower()

        # High severity indicators
        if any(word in error_trace for word in ['panic', 'fatal', 'crash', 'segfault']):
            return 5

        # GitHub Actions failures are often blocking
        if source == 'github_actions':
            return 4

        # Bot failures can be disruptive
        if source == 'bot_failure':
            return 3

        # Code quality issues are usually low severity
        if source == 'code_quality':
            return 2

        # Default medium severity
        return 3

def main():
    """Main execution function"""

    harvester = FailedRunsHarvester()
    report = harvester.generate_comprehensive_report()

    for failure_type, count in report['summary']['failure_breakdown'].items():

    recommendations = report['bidirectional_learning_recommendations']

    if recommendations.get('immediate_actions'):

        for action in recommendations['immediate_actions'][:3]:
            print(f"    - {action.get('action', 'No action specified')}")

    if recommendations.get('systematic_improvements'):

        for improvement in recommendations['systematic_improvements'][:3]:
            print(f"    - {improvement.get('improvement', 'No improvement specified')}")

if __name__ == "__main__":
    main()
