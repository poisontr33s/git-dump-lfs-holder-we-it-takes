#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FAILURE ARCHAEOLOGY DEMO
Psycho-Noir Kontrapunkt - Demonstrasjon av bidirectional learning system

Demo av hvordan 40+ failed runs transformeres til systematic prevention
"""

import json
import datetime
from pathlib import Path
from failure_archaeology import FailureArchaeologist

def simulate_40_plus_failed_runs():
    """Simulerer 40+ realistic failed runs basert på common patterns"""

    failed_runs = [
        # GitHub Actions failures
        {
            'failure_type': 'github_actions',
            'error_trace': 'ERROR: GitHub Actions timeout after 6h - Process killed due to resource exhaustion',
            'context': {'workflow': 'CI/CD', 'timeout': '6h', 'resource_usage': 'high'},
            'severity': 5
        },
        {
            'failure_type': 'github_actions',
            'error_trace': 'FAILED: Permission denied when accessing secrets - GITHUB_TOKEN invalid',
            'context': {'workflow': 'Deploy', 'step': 'checkout', 'auth': 'failed'},
            'severity': 4
        },
        {
            'failure_type': 'github_actions',
            'error_trace': 'ERROR: Node.js version mismatch - Expected 18.x, found 16.x',
            'context': {'workflow': 'Build', 'node_version': '16.x', 'expected': '18.x'},
            'severity': 3
        },

        # Copilot runner failures
        {
            'failure_type': 'copilot_runner',
            'error_trace': 'COPILOT_PANIC: Connection timeout to OpenAI API - 30s exceeded',
            'context': {'api': 'openai', 'timeout': '30s', 'retry_count': 3},
            'severity': 4
        },
        {
            'failure_type': 'copilot_runner',
            'error_trace': 'ERROR: Copilot extension crashed - Memory allocation failed at 0xDEADBEEF',
            'context': {'extension_version': '1.234', 'memory_usage': '95%', 'uptime': '48h'},
            'severity': 5
        },
        {
            'failure_type': 'copilot_runner',
            'error_trace': 'FAILED: Code completion request failed - Rate limit exceeded',
            'context': {'api_calls': 1000, 'rate_limit': '500/hour', 'user': 'copilot'},
            'severity': 3
        },

        # Bot failures
        {
            'failure_type': 'bot_failure',
            'error_trace': 'BOT_SOUL_NOT_FOUND: Neural archaeology scanner crashed during deep scan',
            'context': {'bot_type': 'neural_archaeology', 'scan_depth': 'deep', 'data_processed': '2GB'},
            'severity': 4
        },
        {
            'failure_type': 'bot_failure',
            'error_trace': 'PANIC: Dialogue enricher bot ran out of memory during processing',
            'context': {'bot_type': 'dialogue_enricher', 'memory_limit': '512MB', 'data_size': '1GB'},
            'severity': 4
        },

        # Code quality failures
        {
            'failure_type': 'code_quality',
            'error_trace': 'PYLINT_FAILED: Score 2.1/10 - 73 violations including critical security issues',
            'context': {'file': 'dialogue_analyzer.py', 'violations': 73, 'security_issues': 5},
            'severity': 4
        },
        {
            'failure_type': 'code_quality',
            'error_trace': 'SYNTAX_ERROR: Unexpected token at line 42 - Missing semicolon in JavaScript',
            'context': {'file': 'script.js', 'line': 42, 'language': 'javascript'},
            'severity': 2
        },

        # Deployment failures
        {
            'failure_type': 'deployment_failure',
            'error_trace': 'DEPLOY_FAILED: Docker build failed - FROM ubuntu:latest could not be resolved',
            'context': {'dockerfile': 'Dockerfile', 'base_image': 'ubuntu:latest', 'registry': 'dockerhub'},
            'severity': 5
        },
        {
            'failure_type': 'deployment_failure',
            'error_trace': 'PORT_CONFLICT: Port 8080 already in use by another process',
            'context': {'port': 8080, 'service': 'web_server', 'conflict': 'existing_process'},
            'severity': 3
        }
    ]

    # Multiply patterns to create 40+ failures with variations
    expanded_failures = []
    for i in range(4):  # Create 4 variations of each pattern
        for base_failure in failed_runs:
            variation = base_failure.copy()
            variation['context'] = base_failure['context'].copy()
            variation['context']['variation_id'] = i + 1
            variation['error_trace'] += f" [Occurrence #{i + 1}]"
            expanded_failures.append(variation)

    return expanded_failures

def demonstrate_bidirectional_learning():
    """Demonstrerer complete bidirectional learning cycle"""

    # Initialize archaeologist
    archaeologist = FailureArchaeologist()

    # Simulate 40+ failed runs

    failed_runs = simulate_40_plus_failed_runs()
    print(f"✅ Generated {len(failed_runs)} failed runs")

    # Catalog all failures

    cataloged_failures = []

    for i, failure in enumerate(failed_runs):
        failure_id = archaeologist.catalog_failure(
            failure_type=failure['failure_type'],
            error_trace=failure['error_trace'],
            context=failure['context'],
            severity=failure['severity']
        )
        cataloged_failures.append(failure_id)

        if (i + 1) % 10 == 0:

    print(f"✅ Successfully cataloged {len(cataloged_failures)} failures")

    # Generate learning insights

    learning_library = archaeologist.export_learning_library()

    print(f"✅ Identified {len(learning_library['pattern_library'])} unique failure patterns")

    # Generate preemptive logging configuration

    preemptive_config = archaeologist.generate_preemptive_logging_config()
    recommendations = archaeologist.get_bidirectional_learning_recommendations()

    print(f"✅ Generated {len(preemptive_config['high_risk_operations'])} high-risk operation monitors")
    print(f"✅ Created {len(recommendations['immediate_actions'])} immediate action items")

    # Save comprehensive results

    comprehensive_results = {
        'demo_timestamp': datetime.datetime.now().isoformat(),
        'input_failures': {
            'total_count': len(failed_runs),
            'failure_types': list(set(f['failure_type'] for f in failed_runs)),
            'severity_distribution': {}
        },
        'learning_library': learning_library,
        'preemptive_prevention': preemptive_config,
        'bidirectional_recommendations': recommendations,
        'transformation_summary': {
            'failures_to_patterns': len(learning_library['pattern_library']),
            'patterns_to_preventions': len(preemptive_config['high_risk_operations']),
            'preventions_to_actions': len(recommendations['immediate_actions'])
        }
    }

    # Calculate severity distribution
    severity_dist = {}
    for failure in failed_runs:
        sev = failure['severity']
        severity_dist[sev] = severity_dist.get(sev, 0) + 1
    comprehensive_results['input_failures']['severity_distribution'] = severity_dist

    # Save to file
    results_file = Path("data/failure_archaeology/bidirectional_learning_demo_results.json")
    results_file.parent.mkdir(parents=True, exist_ok=True)

    with open(results_file, 'w', encoding='utf-8') as f:
        json.dump(comprehensive_results, f, indent=2, ensure_ascii=False)

    # Display summary

    print(f"INPUT: {len(failed_runs)} Failed Runs")
    print("  ├─ GitHub Actions failures: {0}".format(sum(1 for f in failed_runs if f['failure_type'] == 'github_actions')))
    print("  ├─ Copilot runner failures: {0}".format(sum(1 for f in failed_runs if f['failure_type'] == 'copilot_runner')))
    print("  ├─ Bot failures: {0}".format(sum(1 for f in failed_runs if f['failure_type'] == 'bot_failure')))
    print("  └─ Code quality failures: {0}".format(sum(1 for f in failed_runs if f['failure_type'] == 'code_quality')))

    print(f"  ├─ Unique patterns identified: {len(learning_library['pattern_library'])}")
    print(f"  ├─ High-risk operations monitored: {len(preemptive_config['high_risk_operations'])}")
    print(f"  └─ Immediate prevention actions: {len(recommendations['immediate_actions'])}")

    print(f"  ├─ Prevention success rate: {learning_library['statistics'].get('recovery_success_rate', 0):.1%}")
    print(f"  ├─ Learning patterns: {len(learning_library['pattern_library'])} identified")

    return comprehensive_results

if __name__ == "__main__":
    results = demonstrate_bidirectional_learning()
