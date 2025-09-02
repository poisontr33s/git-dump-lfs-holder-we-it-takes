#!/usr/bin/env python3
"""
🎭 PSYCHO-NOIR KONTRAPUNKT: HYPER-ANALYTICAL GITHUB INTEGRATION SYSTEM
====================================================================

Et panoptisk system for å strukturere kaos fra GitHub notifications, 
PRs, Issues, sub-Issues og andre "GitHub-flavored fabrications" til 
intelligente, handlingsrettede innsikter.

Kode-agnostisk: Håndterer Python, Ruby, Shell, HTML, pnpm og alle andre rariteter.
"""

import json
import subprocess
import time
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from collections import defaultdict
import re

@dataclass
class GitHubFailureContext:
    """Strukturert representasjon av en GitHub-basert feil"""
    source_type: str  # PR, Issue, Workflow, Notification
    source_id: str
    title: str
    language_stack: List[str]  # Python, Ruby, Shell, HTML, etc.
    failure_category: str  # Build, Test, Deployment, Integration
    notification_flood_level: int  # 0-10 scale
    structural_debt_indicators: List[str]
    actionability_score: float  # 0-10, hvor handlingsbar er dette?
    kaos_entropy_level: float  # 0-10, hvor mye kaos skaper dette?
    
@dataclass 
class RepositoryHealthMetrics:
    """Overordnet helse-status for repository"""
    total_notifications: int
    unresolved_pr_count: int
    sub_pr_count: int  # PRs som spawner andre PRs
    issue_cascade_depth: int  # Hvor dypt går issue-chains?
    runner_failure_rate: float  # Failure rate for 70+ runners
    structural_debt_score: float  # 0-100 total structural debt
    code_language_chaos_index: float  # Hvor fragmentert er codebase?

class HyperAnalyticalGitHubIntegrator:
    """Master integrator for strukturering av GitHub kaos"""
    
    def __init__(self):
        self.report_dir = Path("data/rapporter/github_integration")
        self.report_dir.mkdir(parents=True, exist_ok=True)
        
        # Kode-agnostiske språk-detektorer
        self.language_patterns = {
            'python': ['.py', 'requirements.txt', 'pyproject.toml', 'setup.py'],
            'ruby': ['.rb', 'Gemfile', '.gemspec', 'Rakefile'],
            'shell': ['.sh', '.bash', '.zsh', 'Dockerfile'],
            'html': ['.html', '.htm', '.css', '.js'],
            'javascript': ['.js', '.ts', '.json', 'package.json', 'pnpm-lock.yaml'],
            'config': ['.yml', '.yaml', '.toml', '.ini', '.cfg']
        }
    
    def log_panoptic_event(self, event: str, details: Any = None):
        """Panoptisk logging med timestamp"""
        timestamp = time.strftime("%H:%M:%S")
        print(f"🎭 {timestamp} - PANOPTICON: {event}")
        if details:
            print(f"    📊 {details}")
    
    def extract_notification_flood_data(self) -> Dict[str, Any]:
        """Trekker ut GitHub notifications og måler flood-nivå"""
        self.log_panoptic_event("EXTRACTING NOTIFICATION FLOOD DATA...")
        
        try:
            # Hent alle PRs
            pr_result = subprocess.run([
                'gh', 'pr', 'list', '--state', 'all', '--json', 
                'number,title,state,createdAt,updatedAt,mergeable,url'
            ], capture_output=True, text=True)
            
            # Hent alle Issues  
            issue_result = subprocess.run([
                'gh', 'issue', 'list', '--state', 'all', '--json',
                'number,title,state,createdAt,updatedAt,url'
            ], capture_output=True, text=True)
            
            # Hent workflow runs (siste 100)
            workflow_result = subprocess.run([
                'gh', 'run', 'list', '--limit', '100', '--json',
                'databaseId,name,status,conclusion,createdAt,url'
            ], capture_output=True, text=True)
            
            prs = json.loads(pr_result.stdout) if pr_result.returncode == 0 else []
            issues = json.loads(issue_result.stdout) if issue_result.returncode == 0 else []
            workflows = json.loads(workflow_result.stdout) if workflow_result.returncode == 0 else []
            
            return {
                'prs': prs,
                'issues': issues, 
                'workflows': workflows,
                'extraction_time': time.time()
            }
            
        except Exception as e:
            self.log_panoptic_event("EXTRACTION FAILED", str(e))
            return {'prs': [], 'issues': [], 'workflows': [], 'error': str(e)}
    
    def analyze_language_stack_chaos(self) -> Dict[str, Any]:
        """Analyserer språk-diversitet og fragmentering i codebase"""
        self.log_panoptic_event("ANALYZING LANGUAGE STACK CHAOS...")
        
        language_distribution = defaultdict(int)
        total_files = 0
        
        # Gå gjennom alle filer og kategoriser språk
        for root_path in ['.', 'backend', 'frontend', 'arkiv_gamle_ruby_prosjekter']:
            path = Path(root_path)
            if not path.exists():
                continue
                
            for file_path in path.rglob('*'):
                if file_path.is_file():
                    total_files += 1
                    
                    # Identifiser språk basert på filendelse
                    for language, patterns in self.language_patterns.items():
                        if any(str(file_path).endswith(pattern) or 
                              file_path.name == pattern for pattern in patterns):
                            language_distribution[language] += 1
                            break
                    else:
                        language_distribution['unknown'] += 1
        
        # Beregn kaos-indeks basert på språk-spredning
        if total_files > 0:
            language_entropy = len(language_distribution) / 10.0  # Normalisert
            dominant_language_ratio = max(language_distribution.values()) / total_files
            chaos_index = language_entropy * (1 - dominant_language_ratio) * 10
        else:
            chaos_index = 0
            
        return {
            'language_distribution': dict(language_distribution),
            'total_files': total_files,
            'language_diversity': len(language_distribution),
            'chaos_index': min(10.0, chaos_index),
            'dominant_language': max(language_distribution, key=language_distribution.get) if language_distribution else 'none'
        }
    
    def categorize_failure_context(self, item: Dict[str, Any], item_type: str) -> GitHubFailureContext:
        """Kategoriserer et GitHub-element til strukturert feil-kontekst"""
        
        title = item.get('title', item.get('name', 'Unknown'))
        
        # Detekter failure category basert på tittel og metadata
        failure_category = 'Unknown'
        if any(word in title.lower() for word in ['build', 'compile', 'dependency']):
            failure_category = 'Build'
        elif any(word in title.lower() for word in ['test', 'spec', 'assert']):
            failure_category = 'Test'  
        elif any(word in title.lower() for word in ['deploy', 'release', 'production']):
            failure_category = 'Deployment'
        elif any(word in title.lower() for word in ['integration', 'api', 'service']):
            failure_category = 'Integration'
        elif any(word in title.lower() for word in ['security', 'vulnerability', 'cve']):
            failure_category = 'Security'
        elif any(word in title.lower() for word in ['revert', 'rollback', 'fix']):
            failure_category = 'Hotfix'
        
        # Estimate actionability score
        actionability_indicators = [
            'fix' in title.lower(),
            'implement' in title.lower(),
            'add' in title.lower(),
            'update' in title.lower(),
            item.get('state') == 'open',
            item_type in ['pr', 'issue']
        ]
        actionability_score = sum(actionability_indicators) * 2.0  # 0-10 scale
        
        # Estimate kaos entropy level
        kaos_indicators = [
            'revert' in title.lower(),
            'emergency' in title.lower(), 
            'critical' in title.lower(),
            'urgent' in title.lower(),
            len(title) > 100,  # Overly long titles indicate confusion
        ]
        kaos_entropy = sum(kaos_indicators) * 2.0  # 0-10 scale
        
        return GitHubFailureContext(
            source_type=item_type,
            source_id=str(item.get('number', item.get('databaseId', 'unknown'))),
            title=title,
            language_stack=[],  # Will be populated by language analysis
            failure_category=failure_category,
            notification_flood_level=5,  # Default, can be refined
            structural_debt_indicators=[],  # Will be populated by debt analysis
            actionability_score=actionability_score,
            kaos_entropy_level=kaos_entropy
        )
    
    def calculate_repository_health_metrics(self, github_data: Dict[str, Any], 
                                          language_data: Dict[str, Any]) -> RepositoryHealthMetrics:
        """Beregner overordnede helse-metrikker for repository"""
        
        prs = github_data.get('prs', [])
        issues = github_data.get('issues', [])
        workflows = github_data.get('workflows', [])
        
        # Count unresolved items
        unresolved_prs = len([pr for pr in prs if pr.get('state') == 'open'])
        unresolved_issues = len([issue for issue in issues if issue.get('state') == 'open'])
        
        # Count sub-PRs (PRs that reference other PRs)
        sub_pr_count = len([pr for pr in prs if 
                           any(word in pr.get('title', '').lower() 
                               for word in ['sub', 'follow-up', 'part', 'fix for'])])
        
        # Calculate workflow failure rate
        failed_workflows = len([w for w in workflows if w.get('conclusion') == 'failure'])
        total_workflows = len(workflows)
        failure_rate = failed_workflows / total_workflows if total_workflows > 0 else 0
        
        # Estimate structural debt based on various indicators
        debt_indicators = [
            unresolved_prs > 5,  # Too many open PRs
            sub_pr_count > 2,    # Cascading PR dependencies  
            failure_rate > 0.3,  # High failure rate
            language_data.get('chaos_index', 0) > 5,  # Language fragmentation
            len([pr for pr in prs if 'revert' in pr.get('title', '').lower()]) > 1  # Multiple reverts
        ]
        structural_debt_score = sum(debt_indicators) * 20  # 0-100 scale
        
        return RepositoryHealthMetrics(
            total_notifications=len(prs) + len(issues) + failed_workflows,
            unresolved_pr_count=unresolved_prs,
            sub_pr_count=sub_pr_count,
            issue_cascade_depth=max(3, unresolved_issues // 2),  # Estimate based on volume
            runner_failure_rate=failure_rate,
            structural_debt_score=structural_debt_score,
            code_language_chaos_index=language_data.get('chaos_index', 0)
        )
    
    def generate_actionable_intelligence_report(self, failure_contexts: List[GitHubFailureContext],
                                              health_metrics: RepositoryHealthMetrics) -> Dict[str, Any]:
        """Genererer handlingsrettet intelligence-rapport"""
        
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        
        # Prioriter failure contexts etter actionability
        high_priority = [fc for fc in failure_contexts if fc.actionability_score >= 6]
        medium_priority = [fc for fc in failure_contexts if 3 <= fc.actionability_score < 6]
        low_priority = [fc for fc in failure_contexts if fc.actionability_score < 3]
        
        # Identifiser systematiske problemer
        systematic_issues = defaultdict(int)
        for fc in failure_contexts:
            systematic_issues[fc.failure_category] += 1
        
        # Generer konkrete anbefalinger
        immediate_actions = []
        
        if health_metrics.runner_failure_rate > 0.5:
            immediate_actions.append({
                'action': 'STABILIZE CI/CD PIPELINE',
                'reason': f'Runner failure rate: {health_metrics.runner_failure_rate:.1%}',
                'impact': 'CRITICAL - Blocks all development'
            })
            
        if health_metrics.unresolved_pr_count > 10:
            immediate_actions.append({
                'action': 'PR TRIAGE AND MERGE STRATEGY',
                'reason': f'{health_metrics.unresolved_pr_count} unresolved PRs creating bottlenecks',
                'impact': 'HIGH - Slows feature delivery'
            })
        
        if health_metrics.code_language_chaos_index > 7:
            immediate_actions.append({
                'action': 'CONSOLIDATE LANGUAGE STACK',
                'reason': f'Chaos index: {health_metrics.code_language_chaos_index:.1f}/10',
                'impact': 'MEDIUM - Increases maintenance burden'
            })
        
        report = {
            'timestamp': timestamp,
            'repository_health': asdict(health_metrics),
            'failure_analysis': {
                'total_failures_analyzed': len(failure_contexts),
                'high_priority_items': len(high_priority),
                'medium_priority_items': len(medium_priority), 
                'low_priority_items': len(low_priority),
                'systematic_patterns': dict(systematic_issues)
            },
            'immediate_actions': immediate_actions,
            'strategic_recommendations': [
                'Implement automated triage system for GitHub notifications',
                'Establish PR dependency tracking to prevent cascade failures',
                'Deploy predictive CI/CD failure detection using Neural Archaeology',
                'Create language consolidation roadmap to reduce chaos index'
            ],
            'next_analysis_triggers': [
                'When runner failure rate > 60%',
                'When unresolved PR count > 15', 
                'When new systematic failure pattern emerges',
                'Weekly scheduled health check'
            ]
        }
        
        # Lagre rapport
        report_path = self.report_dir / f"github_integration_report_{timestamp}.json"
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
            
        return report
    
    def execute_hyper_analytical_integration(self) -> Dict[str, Any]:
        """Kjører full hyper-analytisk GitHub integrasjon"""
        
        self.log_panoptic_event("🎭 INITIATING HYPER-ANALYTICAL GITHUB INTEGRATION")
        
        print("\n🌊 PHASE 1: NOTIFICATION FLOOD EXTRACTION")
        print("=" * 60)
        github_data = self.extract_notification_flood_data()
        
        print("\n🔍 PHASE 2: LANGUAGE STACK CHAOS ANALYSIS") 
        print("=" * 60)
        language_data = self.analyze_language_stack_chaos()
        
        print("\n🧠 PHASE 3: FAILURE CONTEXT CATEGORIZATION")
        print("=" * 60)
        failure_contexts = []
        
        # Kategoriser PRs
        for pr in github_data.get('prs', []):
            context = self.categorize_failure_context(pr, 'pr')
            failure_contexts.append(context)
            
        # Kategoriser Issues
        for issue in github_data.get('issues', []):
            context = self.categorize_failure_context(issue, 'issue')
            failure_contexts.append(context)
            
        # Kategoriser Workflow failures
        failed_workflows = [w for w in github_data.get('workflows', []) 
                           if w.get('conclusion') == 'failure']
        for workflow in failed_workflows:
            context = self.categorize_failure_context(workflow, 'workflow')
            failure_contexts.append(context)
        
        print("\n📊 PHASE 4: REPOSITORY HEALTH METRICS")
        print("=" * 60)
        health_metrics = self.calculate_repository_health_metrics(github_data, language_data)
        
        print("\n🎯 PHASE 5: ACTIONABLE INTELLIGENCE GENERATION")
        print("=" * 60)
        intelligence_report = self.generate_actionable_intelligence_report(
            failure_contexts, health_metrics)
        
        print("\n🎭 HYPER-ANALYTICAL INTEGRATION COMPLETE")
        print("=" * 60)
        
        # Presenter resultater
        self.log_panoptic_event("REPOSITORY HEALTH STATUS", 
            f"Structural Debt: {health_metrics.structural_debt_score}/100")
        self.log_panoptic_event("FAILURE ANALYSIS COMPLETE",
            f"{len(failure_contexts)} contexts analyzed")
        self.log_panoptic_event("LANGUAGE CHAOS INDEX",
            f"{language_data.get('chaos_index', 0):.1f}/10")
        self.log_panoptic_event("IMMEDIATE ACTIONS IDENTIFIED", 
            f"{len(intelligence_report['immediate_actions'])} critical actions")
        
        return intelligence_report

def main():
    """Main execution point"""
    integrator = HyperAnalyticalGitHubIntegrator()
    
    print("🎭 PSYCHO-NOIR KONTRAPUNKT: HYPER-ANALYTICAL GITHUB INTEGRATION")
    print("================================================================")
    print("🎯 OBJECTIVE: Transform GitHub chaos into structured intelligence")
    print("🔧 APPROACH: Kode-agnostisk, panoptisk analyse")
    print("")
    
    result = integrator.execute_hyper_analytical_integration()
    
    print(f"\n🏆 INTEGRATION RESULTS:")
    print(f"   📊 Repository Health: {result['repository_health']['structural_debt_score']}/100 structural debt")
    print(f"   🎯 High Priority Items: {result['failure_analysis']['high_priority_items']}")
    print(f"   🚨 Immediate Actions: {len(result['immediate_actions'])}")
    
    if result['immediate_actions']:
        print(f"\n🔥 CRITICAL ACTIONS REQUIRED:")
        for action in result['immediate_actions']:
            print(f"   • {action['action']}")
            print(f"     Reason: {action['reason']}")
            print(f"     Impact: {action['impact']}")
    
    print(f"\n🎭 DEN USYNLIGE HÅND: GitHub chaos structured into actionable intelligence")

if __name__ == "__main__":
    main()
