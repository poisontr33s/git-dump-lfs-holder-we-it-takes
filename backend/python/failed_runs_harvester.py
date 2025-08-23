#!/usr/bin/env python3
"""
PSYCHO-NOIR KONTRAPUNKT: FAILED RUNS HARVESTER
==============================================

Automatisk innsamling og katalogisering av 40+ failed runs fra GitHub Actions,
Copilot runners, og andre automatiserte systemer for bidireksjonell læring.

DEN USYNLIGE HÅND: Chaos harvested for wisdom.
"""

import json
import subprocess
import datetime
import re
from pathlib import Path
from typing import Dict, List, Any, Optional
import hashlib
import yaml

from failure_archaeology_system import (
    FailureArchaeologyDB, FailureArtifact, FailureDomain, 
    FailureSeverity, PredictiveFailureEngine, BidirectionalLearningLoop
)

class FailedRunsHarvester:
    """Innhenting og katalogisering av failed runs fra forskjellige kilder"""
    
    def __init__(self):
        self.archaeology_db = FailureArchaeologyDB()
        self.harvest_log = []
        
    def harvest_github_actions_failures(self, repo: str = "poisontr33s/PsychoNoir-Kontrapunkt") -> List[Dict[str, Any]]:
        """Innhent failed runs fra GitHub Actions"""
        print(f"🔍 HARVESTING GitHub Actions failures for {repo}...")
        
        try:
            # Get workflow runs (last 100)
            result = subprocess.run([
                "gh", "run", "list", 
                "--repo", repo,
                "--status", "failure",
                "--limit", "50",
                "--json", "databaseId,displayTitle,event,status,conclusion,createdAt,updatedAt,workflowName,headBranch"
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                failed_runs = json.loads(result.stdout)
                print(f"📊 Found {len(failed_runs)} failed workflow runs")
                
                detailed_failures = []
                for run in failed_runs[:10]:  # Process first 10 for detailed analysis
                    details = self._get_failure_details(repo, run["databaseId"])
                    if details:
                        detailed_failures.append({
                            "run_info": run,
                            "failure_details": details
                        })
                
                return detailed_failures
            else:
                print(f"❌ Failed to fetch GitHub Actions data: {result.stderr}")
                return []
                
        except Exception as e:
            print(f"❌ Error harvesting GitHub Actions failures: {e}")
            return []
    
    def _get_failure_details(self, repo: str, run_id: int) -> Optional[Dict[str, Any]]:
        """Hent detaljerte feilmeldinger for en spesifikk run"""
        try:
            # Get jobs for this run
            result = subprocess.run([
                "gh", "run", "view", str(run_id),
                "--repo", repo,
                "--json", "jobs"
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                run_data = json.loads(result.stdout)
                
                failure_details = {
                    "failed_jobs": [],
                    "error_patterns": [],
                    "logs_summary": ""
                }
                
                for job in run_data.get("jobs", []):
                    if job.get("conclusion") == "failure":
                        failure_details["failed_jobs"].append({
                            "name": job.get("name"),
                            "steps": [step for step in job.get("steps", []) if step.get("conclusion") == "failure"]
                        })
                
                return failure_details
            
        except Exception as e:
            print(f"⚠️ Could not get details for run {run_id}: {e}")
            
        return None
    
    def catalog_failures_from_harvest(self, harvested_data: List[Dict[str, Any]]) -> List[str]:
        """Katalogiser innhøstede feil i archaeology database"""
        cataloged_ids = []
        
        for failure_data in harvested_data:
            run_info = failure_data["run_info"]
            failure_details = failure_data["failure_details"]
            
            # Generate failure artifact
            failure_id = hashlib.md5(
                f"{run_info['databaseId']}_{run_info['workflowName']}".encode()
            ).hexdigest()[:12]
            
            # Determine domain based on workflow name and content
            domain = self._determine_failure_domain(run_info, failure_details)
            severity = self._assess_failure_severity(failure_details)
            
            # Extract error signature
            error_signature = self._extract_error_signature(failure_details)
            
            artifact = FailureArtifact(
                failure_id=failure_id,
                timestamp=run_info["createdAt"],
                domain=domain,
                severity=severity,
                error_signature=error_signature,
                raw_error_data=json.dumps(failure_details, indent=2),
                context_snapshot={
                    "workflow": run_info["workflowName"],
                    "branch": run_info["headBranch"],
                    "event": run_info["event"],
                    "run_id": run_info["databaseId"]
                },
                attempted_fixes=[],  # Will be populated as we learn
                resolution_status="unresolved",
                learning_extraction="Newly cataloged from GitHub Actions harvest"
            )
            
            cataloged_id = self.archaeology_db.catalog_failure(artifact)
            cataloged_ids.append(cataloged_id)
            
        return cataloged_ids
    
    def _determine_failure_domain(self, run_info: Dict[str, Any], failure_details: Dict[str, Any]) -> FailureDomain:
        """Bestem hvilket domene feilen tilhører"""
        workflow_name = run_info.get("workflowName", "").lower()
        
        if "copilot" in workflow_name or "ci" in workflow_name or "deploy" in workflow_name:
            return FailureDomain.SKYSKRAPER_SYSTEMS
        elif "test" in workflow_name or "build" in workflow_name:
            return FailureDomain.RUSTBELT_IMPROVISATION
        else:
            return FailureDomain.INVISIBLE_HAND_CHAOS
    
    def _assess_failure_severity(self, failure_details: Dict[str, Any]) -> FailureSeverity:
        """Vurder alvorlighetsgraden til feilen"""
        failed_jobs_count = len(failure_details.get("failed_jobs", []))
        
        if failed_jobs_count == 1:
            return FailureSeverity.GLITCH
        elif failed_jobs_count <= 3:
            return FailureSeverity.CORRUPTION
        elif failed_jobs_count <= 5:
            return FailureSeverity.SYSTEM_BREACH
        else:
            return FailureSeverity.CAUSAL_COLLAPSE
    
    def _extract_error_signature(self, failure_details: Dict[str, Any]) -> str:
        """Ekstrahér en unik signatur for denne typen feil"""
        signatures = []
        
        for job in failure_details.get("failed_jobs", []):
            job_name = job.get("name", "unknown")
            signatures.append(f"JOB_FAILURE_{job_name.upper().replace(' ', '_')}")
        
        if not signatures:
            return "UNKNOWN_FAILURE_PATTERN"
        
        return "_".join(signatures)
    
    def generate_harvest_report(self, cataloged_ids: List[str]) -> Dict[str, Any]:
        """Generer en rapport fra innhøstingen"""
        patterns = self.archaeology_db.get_failure_patterns()
        
        report = {
            "harvest_timestamp": datetime.datetime.now().isoformat(),
            "total_failures_cataloged": len(cataloged_ids),
            "cataloged_failure_ids": cataloged_ids,
            "failure_patterns": patterns,
            "recommendations": self._generate_harvest_recommendations(patterns)
        }
        
        return report
    
    def _generate_harvest_recommendations(self, patterns: Dict[str, Any]) -> List[str]:
        """Generer anbefalinger basert på failure patterns"""
        recommendations = []
        
        domain_dist = patterns.get("domain_distribution", {})
        severity_trends = patterns.get("severity_trends", {})
        
        # Skyskraper systems issues
        if domain_dist.get("skyskraper_systems", 0) > 5:
            recommendations.append("SKYSKRAPER ALERT: High automation failure rate detected. Consider implementing more robust error handling in CI/CD pipelines.")
        
        # Rustbelt improvisation issues
        if domain_dist.get("rustbelt_improvisation", 0) > 3:
            recommendations.append("RUSTBELT RESILIENCE: Manual intervention patterns detected. Document successful workarounds for systematic improvements.")
        
        # Severity distribution analysis
        if severity_trends.get("causal_collapse", 0) > 0:
            recommendations.append("⚠️ CRITICAL: Causal collapse events detected. Implement checkpoint/rollback mechanisms immediately.")
        
        if not recommendations:
            recommendations.append("System appears stable. Continue monitoring for emerging patterns.")
        
        return recommendations

def main():
    """Main execution flow"""
    print("🔍 PSYCHO-NOIR KONTRAPUNKT: FAILED RUNS HARVESTER ACTIVATED")
    print("=" * 60)
    
    harvester = FailedRunsHarvester()
    
    # Harvest GitHub Actions failures
    failed_runs = harvester.harvest_github_actions_failures()
    
    if failed_runs:
        print(f"📊 Processing {len(failed_runs)} failed runs...")
        
        # Catalog the failures
        cataloged_ids = harvester.catalog_failures_from_harvest(failed_runs)
        
        # Generate and save report
        report = harvester.generate_harvest_report(cataloged_ids)
        
        # Save report to file
        report_path = Path("data/generert/failure_harvest_report.json")
        report_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(report_path, "w") as f:
            json.dump(report, f, indent=2)
        
        print(f"📋 HARVEST COMPLETE!")
        print(f"   - Cataloged: {len(cataloged_ids)} failures")
        print(f"   - Report saved: {report_path}")
        print(f"   - Database: data/generert/failure_archaeology.db")
        
        # Print recommendations
        print("\n🎯 RECOMMENDATIONS:")
        for rec in report["recommendations"]:
            print(f"   • {rec}")
        
    else:
        print("❌ No failed runs harvested. Check GitHub authentication and repository access.")

if __name__ == "__main__":
    main()
