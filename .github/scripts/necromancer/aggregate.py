#!/usr/bin/env python3
"""
Necromancer Aggregator
Psycho-Noir Kontrapunkt - Failure Observability System

Aggregates failure data from multiple necromancer artifacts into comprehensive
reports and pushes to the necropolis branch for persistent knowledge storage.
"""

import argparse
import json
import os
import shutil
import zipfile
from collections import defaultdict, Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, List, Optional

class NecropolisAggregator:
    """
    Advanced aggregation engine for the Necropolis knowledge base.
    
    Merges distributed failure artifacts into structured taxonomy reports
    and maintains the perpetual errors-to-solutions loop.
    """
    
    def __init__(self, artifacts_dir: str, output_dir: str):
        """Initialize aggregator with input and output directories."""
        self.artifacts_dir = Path(artifacts_dir)
        self.output_dir = Path(output_dir)
        self.timestamp = datetime.now(timezone.utc)
        self.run_id = os.environ.get('GITHUB_RUN_ID', 'unknown')
        
        # Create output structure
        self.knowledge_base_dir = self.output_dir / "necropolis" / "knowledge-base"
        self.runs_dir = self.output_dir / "necropolis" / "runs" / self.timestamp.strftime("%Y-%m-%d") / self.timestamp.strftime("%H%M")
        
        self.knowledge_base_dir.mkdir(parents=True, exist_ok=True)
        self.runs_dir.mkdir(parents=True, exist_ok=True)

    def discover_necromancer_artifacts(self) -> List[Path]:
        """Discover all necromancer artifacts in the artifacts directory."""
        artifacts = []
        
        # Look for both direct artifacts and zip files
        for item in self.artifacts_dir.rglob("*"):
            if item.is_file():
                if item.name.startswith("necromancer-") and item.suffix == ".zip":
                    artifacts.append(item)
                elif item.name in ["outcome.json", "outcome.ndjson"]:
                    artifacts.append(item)
        
        print(f"🔍 Discovered {len(artifacts)} necromancer artifacts")
        return artifacts

    def extract_artifact_data(self, artifact_path: Path) -> List[Dict[str, Any]]:
        """Extract outcome data from artifact."""
        outcomes = []
        
        if artifact_path.suffix == ".zip":
            # Extract zip and look for outcome files
            with zipfile.ZipFile(artifact_path, 'r') as zf:
                extract_dir = self.artifacts_dir / f"extracted_{artifact_path.stem}"
                extract_dir.mkdir(exist_ok=True)
                zf.extractall(extract_dir)
                
                # Find outcome files in extracted content
                for outcome_file in extract_dir.rglob("outcome.json"):
                    try:
                        with open(outcome_file, 'r') as f:
                            outcomes.append(json.load(f))
                    except (json.JSONDecodeError, FileNotFoundError) as e:
                        print(f"⚠️ Failed to read {outcome_file}: {e}")
                
                # Clean up extracted files
                shutil.rmtree(extract_dir, ignore_errors=True)
        
        elif artifact_path.name == "outcome.json":
            try:
                with open(artifact_path, 'r') as f:
                    outcomes.append(json.load(f))
            except (json.JSONDecodeError, FileNotFoundError) as e:
                print(f"⚠️ Failed to read {artifact_path}: {e}")
        
        return outcomes

    def aggregate_outcomes(self, all_outcomes: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Aggregate all outcomes into comprehensive taxonomy report."""
        
        # Basic statistics
        total_outcomes = len(all_outcomes)
        failures = [o for o in all_outcomes if o.get('outcome') == 'FAILURE']
        successes = [o for o in all_outcomes if o.get('outcome') == 'SUCCESS']
        
        # Error type classification
        error_types = Counter(o.get('error_type', 'UNKNOWN') for o in failures)
        
        # Category breakdown
        category_stats = defaultdict(lambda: {'total': 0, 'failures': 0, 'success_rate': 0})
        for outcome in all_outcomes:
            category = outcome.get('category', 'unknown')
            category_stats[category]['total'] += 1
            if outcome.get('outcome') == 'FAILURE':
                category_stats[category]['failures'] += 1
        
        # Calculate success rates
        for category, stats in category_stats.items():
            if stats['total'] > 0:
                stats['success_rate'] = round((stats['total'] - stats['failures']) / stats['total'] * 100, 2)
        
        # Fingerprint analysis for similar failures
        fingerprint_groups = defaultdict(list)
        for outcome in failures:
            fingerprint = outcome.get('fingerprint', 'NO_FINGERPRINT')
            fingerprint_groups[fingerprint].append(outcome)
        
        # Sort by frequency
        top_fingerprints = sorted(
            fingerprint_groups.items(),
            key=lambda x: len(x[1]),
            reverse=True
        )[:10]
        
        # Variant analysis
        variant_stats = defaultdict(lambda: {'total': 0, 'failures': 0})
        for outcome in all_outcomes:
            variant = outcome.get('variant', 'unknown')
            variant_stats[variant]['total'] += 1
            if outcome.get('outcome') == 'FAILURE':
                variant_stats[variant]['failures'] += 1
        
        # Psycho-Noir specific analysis
        psycho_noir_patterns = {}
        pn_keywords = ['KAUSALITETS_ARKITEKTEN', 'SYNTETISKE_SYNAPSER', 'RUSTBELT_IMPROVISATION']
        for keyword in pn_keywords:
            matching_failures = [o for o in failures if keyword in o.get('error_type', '')]
            if matching_failures:
                psycho_noir_patterns[keyword] = {
                    'count': len(matching_failures),
                    'examples': [o['fingerprint'] for o in matching_failures[:3]]
                }
        
        # Build comprehensive report
        report = {
            'metadata': {
                'generated_at': self.timestamp.isoformat(),
                'run_id': self.run_id,
                'git_sha': os.environ.get('GITHUB_SHA', 'unknown'),
                'workflow': os.environ.get('GITHUB_WORKFLOW', 'unknown'),
                'necropolis_version': '1.0.0'
            },
            'summary': {
                'total_outcomes': total_outcomes,
                'total_failures': len(failures),
                'total_successes': len(successes),
                'overall_success_rate': round(len(successes) / total_outcomes * 100, 2) if total_outcomes > 0 else 0,
                'unique_error_types': len(error_types),
                'unique_fingerprints': len(fingerprint_groups)
            },
            'error_taxonomy': {
                'error_types': dict(error_types),
                'top_fingerprints': [
                    {
                        'fingerprint': fp[:200] + '...' if len(fp) > 200 else fp,
                        'count': len(outcomes),
                        'examples': [o['name'] for o in outcomes[:3]]
                    }
                    for fp, outcomes in top_fingerprints
                ],
                'psycho_noir_signatures': psycho_noir_patterns
            },
            'category_analysis': dict(category_stats),
            'variant_analysis': dict(variant_stats),
            'recommendations': self._generate_recommendations(failures, error_types, category_stats)
        }
        
        return report

    def _generate_recommendations(self, failures: List[Dict], error_types: Counter, 
                                category_stats: Dict) -> List[str]:
        """Generate actionable recommendations based on failure patterns."""
        recommendations = []
        
        # Error type recommendations
        if error_types.get('DEPENDENCY_FAILURE', 0) > 2:
            recommendations.append("🔧 Consider implementing dependency caching and lock file validation")
        
        if error_types.get('TIMEOUT', 0) > 1:
            recommendations.append("⏰ Review timeout configurations and optimize long-running processes")
        
        if error_types.get('TEST_FAILURE', 0) > 3:
            recommendations.append("🧪 Implement test result caching and parallel test execution")
        
        # Category-specific recommendations
        for category, stats in category_stats.items():
            if stats['success_rate'] < 70 and stats['total'] > 2:
                recommendations.append(f"📊 Category '{category}' has low success rate ({stats['success_rate']}%) - needs attention")
        
        # Psycho-Noir specific recommendations
        psycho_noir_failures = [f for f in failures if any(kw in f.get('error_type', '') for kw in ['KAUSALITETS', 'SYNTETISKE', 'RUSTBELT'])]
        if psycho_noir_failures:
            recommendations.append("🎭 Psycho-Noir digital manifestations detected - Den Usynlige Hånd influence growing")
            recommendations.append("🔮 Consider implementing chaos engineering practices to strengthen system resilience")
        
        if not recommendations:
            recommendations.append("✅ System appears stable - continue monitoring for emerging patterns")
        
        return recommendations

    def save_individual_outcomes(self, all_outcomes: List[Dict[str, Any]]):
        """Save individual outcome files to knowledge base."""
        for i, outcome in enumerate(all_outcomes):
            filename = f"{outcome.get('name', 'unknown').replace(' ', '_').replace('/', '_')}_{i}.json"
            filepath = self.runs_dir / filename
            
            with open(filepath, 'w') as f:
                json.dump(outcome, f, indent=2)

    def save_taxonomy_report(self, report: Dict[str, Any]):
        """Save the comprehensive taxonomy report."""
        # Save to current run
        report_file = self.runs_dir / "taxonomy_report.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        # Save to knowledge base root
        kb_report_file = self.knowledge_base_dir / f"latest_taxonomy_report.json"
        with open(kb_report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        # Create markdown summary
        markdown_file = self.runs_dir / "README.md"
        self._create_markdown_summary(report, markdown_file)

    def _create_markdown_summary(self, report: Dict[str, Any], output_file: Path):
        """Create a human-readable markdown summary."""
        with open(output_file, 'w') as f:
            f.write(f"# Necropolis Report - {report['metadata']['generated_at'][:19]}\n\n")
            
            f.write("## 📊 Summary\n")
            summary = report['summary']
            f.write(f"- **Total Outcomes**: {summary['total_outcomes']}\n")
            f.write(f"- **Success Rate**: {summary['overall_success_rate']}%\n")
            f.write(f"- **Failures**: {summary['total_failures']}\n")
            f.write(f"- **Unique Error Types**: {summary['unique_error_types']}\n\n")
            
            f.write("## 🏷️ Error Types\n")
            for error_type, count in report['error_taxonomy']['error_types'].items():
                f.write(f"- **{error_type}**: {count} occurrences\n")
            f.write("\n")
            
            f.write("## 🔍 Top Failure Patterns\n")
            for i, fp_info in enumerate(report['error_taxonomy']['top_fingerprints'][:5], 1):
                f.write(f"{i}. **Count**: {fp_info['count']} - {fp_info['fingerprint'][:100]}...\n")
            f.write("\n")
            
            if report['error_taxonomy']['psycho_noir_signatures']:
                f.write("## 🎭 Psycho-Noir Manifestations\n")
                for pattern, info in report['error_taxonomy']['psycho_noir_signatures'].items():
                    f.write(f"- **{pattern}**: {info['count']} manifestations\n")
                f.write("\n")
            
            f.write("## 💡 Recommendations\n")
            for rec in report['recommendations']:
                f.write(f"- {rec}\n")
            f.write("\n")
            
            f.write(f"---\n*Generated by Necropolis Aggregator - Run {report['metadata']['run_id']}*\n")


def main():
    """Main execution function for the aggregator."""
    parser = argparse.ArgumentParser(
        description="Necromancer Aggregator - Merge failure artifacts into knowledge base"
    )
    
    parser.add_argument('--artifacts-dir', required=True,
                       help='Directory containing necromancer artifacts')
    parser.add_argument('--output-dir', required=True,
                       help='Output directory for aggregated reports')
    
    args = parser.parse_args()
    
    # Initialize aggregator
    aggregator = NecropolisAggregator(args.artifacts_dir, args.output_dir)
    
    print("🧙‍♂️ NECROPOLIS AGGREGATOR STARTING")
    print(f"📂 Artifacts dir: {args.artifacts_dir}")
    print(f"📁 Output dir: {args.output_dir}")
    
    # Discover artifacts
    artifacts = aggregator.discover_necromancer_artifacts()
    
    if not artifacts:
        print("⚠️ No necromancer artifacts found")
        # Create empty report
        empty_report = {
            'metadata': {
                'generated_at': aggregator.timestamp.isoformat(),
                'run_id': aggregator.run_id,
                'necropolis_version': '1.0.0'
            },
            'summary': {
                'total_outcomes': 0,
                'total_failures': 0,
                'total_successes': 0,
                'overall_success_rate': 100,
                'unique_error_types': 0,
                'unique_fingerprints': 0
            },
            'error_taxonomy': {'error_types': {}, 'top_fingerprints': [], 'psycho_noir_signatures': {}},
            'category_analysis': {},
            'variant_analysis': {},
            'recommendations': ["✅ No failures detected - system operating smoothly"]
        }
        aggregator.save_taxonomy_report(empty_report)
        return
    
    # Extract all outcome data
    all_outcomes = []
    for artifact in artifacts:
        outcomes = aggregator.extract_artifact_data(artifact)
        all_outcomes.extend(outcomes)
        print(f"📦 Extracted {len(outcomes)} outcomes from {artifact.name}")
    
    print(f"📊 Total outcomes collected: {len(all_outcomes)}")
    
    # Aggregate outcomes
    report = aggregator.aggregate_outcomes(all_outcomes)
    
    # Save results
    aggregator.save_individual_outcomes(all_outcomes)
    aggregator.save_taxonomy_report(report)
    
    print("✅ NECROPOLIS AGGREGATION COMPLETE")
    print(f"📋 Report saved to: {aggregator.runs_dir}")
    print(f"🏛️ Knowledge base updated: {aggregator.knowledge_base_dir}")
    
    # Print summary
    print(f"\n📊 SUMMARY:")
    print(f"   Outcomes processed: {report['summary']['total_outcomes']}")
    print(f"   Success rate: {report['summary']['overall_success_rate']}%")
    print(f"   Unique error types: {report['summary']['unique_error_types']}")
    
    if report['error_taxonomy']['psycho_noir_signatures']:
        print(f"\n🎭 PSYCHO-NOIR ACTIVITY DETECTED:")
        for pattern, info in report['error_taxonomy']['psycho_noir_signatures'].items():
            print(f"   {pattern}: {info['count']} manifestations")


if __name__ == "__main__":
    main()