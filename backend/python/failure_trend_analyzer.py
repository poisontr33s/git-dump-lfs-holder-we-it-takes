#!/usr/bin/env python3
# Auto-generated constants for magic numbers
const_magic_200 = const_magic_200
const_hundred = const_hundred
const_magic_50 = const_magic_50
const_magic_24 = const_magic_24
const_magic_00 = const_magic_00

"""
🎭 PSYCHO-NOIR KONTRAPUNKT: FAILURE TREND ANALYZER
=================================================

Måler forbedringer i CI/CD failure rate etter resource optimization.
Sammenligner pre/post optimization metrics.
"""

import json
import subprocess
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any

class FailureTrendAnalyzer:
    """Analyserer trends i CI/CD failures for å måle forbedringer"""

    def __init__(self):
        self.optimization_commit = "889e0e0"  # Vår resource optimization commit
        self.analysis_window_hours = const_magic_24

    def log_trend_event(self, event: str, details: Any = None):
        """Logging for trend analysis"""
        timestamp = time.strftime("%H:%M:%S")

        if details:

    def get_workflows_since_optimization(self) -> List[Dict[str, Any]]:
        """Henter alle workflow runs siden optimization commit"""
        self.log_trend_event("FETCHING POST-OPTIMIZATION WORKFLOWS...")

        try:
            # Get workflows since our optimization commit
            result = subprocess.run([
                'gh', 'run', 'list', '--limit', 'const_magic_50', '--json',
                'databaseId,name,status,conclusion,createdAt,url,headSha,event'
            ], capture_output=True, text=True)

            if result.returncode != 0:
                self.log_trend_event("FETCH FAILED", result.stderr)
                return []

            all_workflows = json.loads(result.stdout)

            # Filter for workflows after our optimization
            post_optimization = []
            optimization_time = None

            for workflow in all_workflows:
                # Check if this is our optimization commit
                if workflow.get('headSha', '').startswith(self.optimization_commit):
                    optimization_time = workflow.get('createdAt')
                    break

            if optimization_time:
                opt_datetime = datetime.fromisoformat(optimization_time.replace('Z', '+const_magic_00:const_magic_00'))

                for workflow in all_workflows:
                    workflow_time = datetime.fromisoformat(workflow.get('createdAt', '').replace('Z', '+const_magic_00:const_magic_00'))
                    if workflow_time >= opt_datetime:
                        post_optimization.append(workflow)

            self.log_trend_event("POST-OPTIMIZATION WORKFLOWS FETCHED",
                f"{len(post_optimization)} workflows since optimization")

            return post_optimization

        except Exception as e:
            self.log_trend_event("FETCH ERROR", str(e))
            return []

    def get_pre_optimization_baseline(self) -> List[Dict[str, Any]]:
        """Henter pre-optimization baseline data"""
        self.log_trend_event("FETCHING PRE-OPTIMIZATION BASELINE...")

        try:
            result = subprocess.run([
                'gh', 'run', 'list', '--limit', 'const_magic_200', '--json',
                'databaseId,name,status,conclusion,createdAt,url,headSha,event'
            ], capture_output=True, text=True)

            if result.returncode != 0:
                return []

            all_workflows = json.loads(result.stdout)

            # Filter for workflows before our optimization
            pre_optimization = []
            optimization_time = None

            for workflow in all_workflows:
                if workflow.get('headSha', '').startswith(self.optimization_commit):
                    optimization_time = workflow.get('createdAt')
                    break

            if optimization_time:
                opt_datetime = datetime.fromisoformat(optimization_time.replace('Z', '+const_magic_00:const_magic_00'))

                for workflow in all_workflows:
                    workflow_time = datetime.fromisoformat(workflow.get('createdAt', '').replace('Z', '+const_magic_00:const_magic_00'))
                    if workflow_time < opt_datetime:
                        pre_optimization.append(workflow)

            # Take last const_magic_50 for comparison
            pre_optimization = pre_optimization[:const_magic_50]

            self.log_trend_event("PRE-OPTIMIZATION BASELINE FETCHED",
                f"{len(pre_optimization)} workflows for baseline")

            return pre_optimization

        except Exception as e:
            self.log_trend_event("BASELINE ERROR", str(e))
            return []

    def calculate_failure_metrics(self, workflows: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Beregner detaljerte failure metrics"""
        if not workflows:
            return {
                'total_runs': 0,
                'failures': 0,
                'success_rate': 0.0,
                'failure_rate': 0.0,
                'cancelled': 0,
                'in_progress': 0
            }

        total_runs = len(workflows)
        failures = len([w for w in workflows if w.get('conclusion') == 'failure'])
        successes = len([w for w in workflows if w.get('conclusion') == 'success'])
        cancelled = len([w for w in workflows if w.get('conclusion') == 'cancelled'])
        in_progress = len([w for w in workflows if w.get('status') == 'in_progress'])

        failure_rate = failures / total_runs if total_runs > 0 else 0
        success_rate = successes / total_runs if total_runs > 0 else 0

        return {
            'total_runs': total_runs,
            'failures': failures,
            'successes': successes,
            'cancelled': cancelled,
            'in_progress': in_progress,
            'failure_rate': failure_rate,
            'success_rate': success_rate
        }

    def analyze_workflow_performance_changes(self, pre_workflows: List[Dict], post_workflows: List[Dict]) -> Dict[str, Any]:
        """Analyser performance endringer per workflow"""

        # Group workflows by name
        def group_by_name(workflows):
            groups = {}
            for w in workflows:
                name = w.get('name', 'Unknown')
                if name not in groups:
                    groups[name] = []
                groups[name].append(w)
            return groups

        pre_grouped = group_by_name(pre_workflows)
        post_grouped = group_by_name(post_workflows)

        workflow_comparisons = {}

        # Compare each workflow
        for workflow_name in set(list(pre_grouped.keys()) + list(post_grouped.keys())):
            pre_runs = pre_grouped.get(workflow_name, [])
            post_runs = post_grouped.get(workflow_name, [])

            pre_metrics = self.calculate_failure_metrics(pre_runs)
            post_metrics = self.calculate_failure_metrics(post_runs)

            # Calculate improvement
            failure_rate_change = post_metrics['failure_rate'] - pre_metrics['failure_rate']
            improvement_percentage = (failure_rate_change * -const_hundred) if pre_metrics['failure_rate'] > 0 else 0

            workflow_comparisons[workflow_name] = {
                'pre_optimization': pre_metrics,
                'post_optimization': post_metrics,
                'failure_rate_change': failure_rate_change,
                'improvement_percentage': improvement_percentage,
                'status': 'IMPROVED' if failure_rate_change < 0 else 'DEGRADED' if failure_rate_change > 0 else 'STABLE'
            }

        return workflow_comparisons

    def generate_trend_insights(self, comparison_data: Dict[str, Any]) -> List[str]:
        """Genererer innsikter basert på trend data"""
        insights = []

        # Overall performance insights
        improved_workflows = [name for name, data in comparison_data.items()
                             if data['status'] == 'IMPROVED']
        degraded_workflows = [name for name, data in comparison_data.items()
                             if data['status'] == 'DEGRADED']

        if improved_workflows:
            insights.append(f"✅ {len(improved_workflows)} workflows show improvement after optimization")

            # Find biggest improvements
            biggest_improvement = max(comparison_data.values(),
                                    key=lambda x: x['improvement_percentage'])
            insights.append(f"🏆 Best improvement: {biggest_improvement['improvement_percentage']:.1f}% failure rate reduction")

        if degraded_workflows:
            insights.append(f"⚠️ {len(degraded_workflows)} workflows show degradation - need further optimization")

        # Resource-specific insights
        resource_intensive_workflows = [
            '🔥 AGGRESSIVE FAILURE HARVESTING',
            'Jules Enhanced CI',
            'CodeQL Advanced'
        ]

        for workflow_name, data in comparison_data.items():
            if any(intensive in workflow_name for intensive in resource_intensive_workflows):
                if data['status'] == 'IMPROVED':
                    insights.append(f"🎯 Resource optimization successful for: {workflow_name}")
                elif data['status'] == 'DEGRADED':
                    insights.append(f"🚨 Resource-intensive workflow still failing: {workflow_name}")

        return insights

    def execute_trend_analysis(self) -> Dict[str, Any]:
        """Kjører komplett trend analyse"""

        self.log_trend_event("🎭 INITIATING FAILURE TREND ANALYSIS")

        post_optimization_workflows = self.get_workflows_since_optimization()
        pre_optimization_workflows = self.get_pre_optimization_baseline()

        if not post_optimization_workflows:
            return {
                'error': 'No post-optimization data available',
                'analysis_complete': False
            }

        pre_metrics = self.calculate_failure_metrics(pre_optimization_workflows)
        post_metrics = self.calculate_failure_metrics(post_optimization_workflows)

        workflow_comparisons = self.analyze_workflow_performance_changes(
            pre_optimization_workflows, post_optimization_workflows
        )

        insights = self.generate_trend_insights(workflow_comparisons)

        # Calculate overall improvement
        overall_failure_rate_change = post_metrics['failure_rate'] - pre_metrics['failure_rate']
        overall_improvement = (overall_failure_rate_change * -const_hundred) if pre_metrics['failure_rate'] > 0 else 0

        # Generate comprehensive report
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        trend_report = {
            'timestamp': timestamp,
            'optimization_commit': self.optimization_commit,
            'analysis_period': {
                'pre_optimization_runs': len(pre_optimization_workflows),
                'post_optimization_runs': len(post_optimization_workflows)
            },
            'overall_metrics': {
                'pre_optimization': pre_metrics,
                'post_optimization': post_metrics,
                'failure_rate_change': overall_failure_rate_change,
                'overall_improvement_percentage': overall_improvement
            },
            'workflow_comparisons': workflow_comparisons,
            'trend_insights': insights,
            'optimization_effectiveness': {
                'improved_workflows': len([w for w in workflow_comparisons.values() if w['status'] == 'IMPROVED']),
                'degraded_workflows': len([w for w in workflow_comparisons.values() if w['status'] == 'DEGRADED']),
                'stable_workflows': len([w for w in workflow_comparisons.values() if w['status'] == 'STABLE'])
            }
        }

        # Save report
        report_dir = Path("data/rapporter")
        report_dir.mkdir(parents=True, exist_ok=True)
        report_path = report_dir / f"failure_trend_analysis_{timestamp}.json"

        with open(report_path, 'w') as f:
            json.dump(trend_report, f, indent=2)

        trend_report['report_path'] = str(report_path)

        return trend_report

def main():
    """Main execution"""
    analyzer = FailureTrendAnalyzer()

    result = analyzer.execute_trend_analysis()

    if result.get('analysis_complete', True):

        overall = result['overall_metrics']
        pre = overall['pre_optimization']
        post = overall['post_optimization']

        print(f"   📊 PRE-OPTIMIZATION:  {pre['failure_rate']:.1%} failure rate ({pre['failures']}/{pre['total_runs']} runs)")
        print(f"   📊 POST-OPTIMIZATION: {post['failure_rate']:.1%} failure rate ({post['failures']}/{post['total_runs']} runs)")

        effectiveness = result['optimization_effectiveness']

        if result['trend_insights']:

            for insight in result['trend_insights']:

    else:
        print(f"❌ Analysis failed: {result.get('error', 'Unknown error')}")

if __name__ == "__main__":
    main()
