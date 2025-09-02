#!/usr/bin/env python3
"""
Enhanced Failed Runs Harvester with Aggressive Multi-Source Data Collection
Designed to repurpose ALL failure data as building blocks for intelligence
"""

import argparse
import asyncio
import json
import logging
import sqlite3
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional
import hashlib
import re

class AggressiveFailureHarvester:
    """
    Supercharged failure harvester that treats every error as valuable data
    """
    
    def __init__(self, db_path: str = "data/generert/failure_archaeology.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.logger = self._setup_logging()
        self.harvested_failures = []
        self.repurposable_patterns = {}
        
    def _setup_logging(self) -> logging.Logger:
        """Setup aggressive logging for all harvest operations"""
        logger = logging.getLogger("AggressiveFailureHarvester")
        logger.setLevel(logging.DEBUG)
        
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
        return logger
    
    def initialize_expanded_database(self):
        """Initialize database with expanded schema for maximum data capture"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Enhanced failures table with repurposing metadata
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS failures (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                failure_id TEXT UNIQUE,
                category TEXT,
                severity TEXT,
                error_message TEXT,
                context TEXT,
                timestamp TEXT,
                source_type TEXT,
                runner_info TEXT,
                repurpose_potential INTEGER DEFAULT 1,
                building_block_value TEXT,
                correlation_signature TEXT,
                extraction_metadata TEXT
            )
        ''')
        
        # Repurposable patterns table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS repurposable_patterns (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pattern_signature TEXT UNIQUE,
                pattern_type TEXT,
                reuse_frequency INTEGER DEFAULT 0,
                building_block_applications TEXT,
                transformation_potential TEXT,
                last_repurposed TEXT
            )
        ''')
        
        # Cross-correlation table for pattern relationships
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS pattern_correlations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pattern_a TEXT,
                pattern_b TEXT,
                correlation_strength REAL,
                combined_potential TEXT,
                synthesis_opportunities TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
        self.logger.info("🗃️ Expanded database schema initialized for aggressive harvesting")
    
    async def harvest_from_multiple_sources(self, aggressive_mode: bool = False):
        """
        Aggressively harvest failure data from all possible sources
        """
        self.logger.info("🔥 INITIATING AGGRESSIVE MULTI-SOURCE FAILURE HARVEST")
        
        sources = [
            "github_actions",
            "workflow_logs", 
            "container_failures",
            "service_integration_failures",
            "polyglot_failures",
            "resource_exhaustion_events",
            "permission_violations",
            "network_chaos_events",
            "compiler_errors",
            "dependency_conflicts"
        ]
        
        if aggressive_mode:
            sources.extend([
                "intentional_memory_corruption",
                "timeout_stress_scenarios", 
                "filesystem_corruption_sims",
                "cascading_failure_chains",
                "cross_platform_inconsistencies"
            ])
        
        harvested_count = 0
        
        for source in sources:
            try:
                failures = await self._harvest_from_source(source)
                for failure in failures:
                    if self._store_failure_with_repurpose_metadata(failure):
                        harvested_count += 1
                        
                self.logger.info(f"📡 Harvested {len(failures)} failures from {source}")
                
            except Exception as e:
                self.logger.error(f"❌ Error harvesting from {source}: {e}")
        
        self.logger.info(f"✅ AGGRESSIVE HARVEST COMPLETE: {harvested_count} failures ready for repurposing")
        return harvested_count
    
    async def _harvest_from_source(self, source: str) -> List[Dict[str, Any]]:
        """
        Harvest failures from specific source with repurposing focus
        """
        failures = []
        
        if source == "github_actions":
            # Enhanced GitHub Actions harvesting
            failures.extend(await self._harvest_github_actions_comprehensive())
            
        elif source == "intentional_memory_corruption":
            # Simulate memory corruption failures for pattern learning
            failures.extend(self._generate_memory_corruption_patterns())
            
        elif source == "cascading_failure_chains":
            # Generate cascading failure scenarios
            failures.extend(self._generate_cascading_patterns())
            
        elif source == "polyglot_failures":
            # Multi-language failure patterns
            failures.extend(self._generate_polyglot_patterns())
            
        elif source == "resource_exhaustion_events":
            # Resource exhaustion patterns
            failures.extend(self._generate_resource_exhaustion_patterns())
            
        # Add more source handlers as needed...
        
        return failures
    
    async def _harvest_github_actions_comprehensive(self) -> List[Dict[str, Any]]:
        """
        Comprehensive GitHub Actions failure harvesting
        """
        # Simulate extensive GitHub Actions failure patterns
        patterns = [
            {
                "failure_id": f"gh_actions_{int(time.time())}_{i}",
                "category": "AGGRESSIVE_MULTI_RUNNER_FAILURE",
                "severity": "HIGH_LEARNING_VALUE", 
                "error_message": f"Matrix job failure on runner {runner} with scenario {scenario}",
                "context": f"Workflow: Aggressive Failure Harvesting | Runner: {runner} | Scenario: {scenario}",
                "source_type": "github_actions_matrix",
                "runner_info": runner,
                "building_block_value": "cross_platform_inconsistency_detection",
                "repurpose_potential": 5
            }
            for i, (runner, scenario) in enumerate([
                ("ubuntu-20.04", "memory_corruption"),
                ("ubuntu-22.04", "dependency_conflict"), 
                ("windows-2019", "permission_violation"),
                ("windows-2022", "timeout_stress"),
                ("macos-11", "filesystem_chaos"),
                ("macos-12", "network_isolation"),
                ("macos-13", "compiler_version_mismatch"),
                ("ubuntu-latest", "container_chaos"),
                ("windows-latest", "service_integration_failure"),
                ("macos-latest", "resource_exhaustion")
            ])
        ]
        
        return patterns
    
    def _generate_memory_corruption_patterns(self) -> List[Dict[str, Any]]:
        """Generate memory corruption failure patterns for learning"""
        return [
            {
                "failure_id": f"mem_corrupt_{int(time.time())}_001",
                "category": "MEMORY_CORRUPTION_SIMULATION",
                "severity": "CRITICAL_LEARNING",
                "error_message": "RecursionError: maximum recursion depth exceeded while calling Python object",
                "context": "Intentional memory corruption simulation for neural archaeology training",
                "source_type": "controlled_failure_simulation",
                "building_block_value": "recursion_limit_boundary_detection",
                "repurpose_potential": 4
            },
            {
                "failure_id": f"mem_corrupt_{int(time.time())}_002", 
                "category": "MEMORY_EXHAUSTION_PATTERN",
                "severity": "CRITICAL_LEARNING",
                "error_message": "MemoryError: Unable to allocate array with shape and data type",
                "context": "Memory exhaustion attack simulation",
                "source_type": "controlled_failure_simulation",
                "building_block_value": "memory_boundary_stress_testing",
                "repurpose_potential": 5
            }
        ]
    
    def _generate_cascading_patterns(self) -> List[Dict[str, Any]]:
        """Generate cascading failure patterns"""
        return [
            {
                "failure_id": f"cascade_{int(time.time())}_001",
                "category": "CASCADING_DEPENDENCY_FAILURE",
                "severity": "HIGH_LEARNING_VALUE",
                "error_message": "ImportError: cannot import name 'HTTPSConnectionPool' from 'urllib3.poolmanager'",
                "context": "Intentional dependency version conflict cascade",
                "source_type": "controlled_cascade_simulation",
                "building_block_value": "dependency_conflict_chain_analysis",
                "repurpose_potential": 4
            }
        ]
    
    def _generate_polyglot_patterns(self) -> List[Dict[str, Any]]:
        """Generate multi-language failure patterns"""
        return [
            {
                "failure_id": f"polyglot_{int(time.time())}_py",
                "category": "POLYGLOT_VERSION_CONFLICT",
                "severity": "CROSS_LANGUAGE_LEARNING",
                "error_message": "python: command not found (expected python2.7)",
                "context": "Ancient Python version requirement failure",
                "source_type": "polyglot_version_chaos",
                "building_block_value": "cross_language_compatibility_mapping",
                "repurpose_potential": 3
            },
            {
                "failure_id": f"polyglot_{int(time.time())}_node",
                "category": "POLYGLOT_RUNTIME_FAILURE",
                "severity": "CROSS_LANGUAGE_LEARNING", 
                "error_message": "node: --version flag requires Node.js v20+ but found v16",
                "context": "Node.js version compatibility chaos",
                "source_type": "polyglot_version_chaos",
                "building_block_value": "runtime_version_boundary_detection",
                "repurpose_potential": 3
            }
        ]
    
    def _generate_resource_exhaustion_patterns(self) -> List[Dict[str, Any]]:
        """Generate resource exhaustion patterns"""
        return [
            {
                "failure_id": f"resource_{int(time.time())}_disk", 
                "category": "RESOURCE_EXHAUSTION_ATTACK",
                "severity": "RESOURCE_BOUNDARY_LEARNING",
                "error_message": "OSError: [Errno 28] No space left on device",
                "context": "Intentional disk space exhaustion simulation",
                "source_type": "resource_stress_simulation",
                "building_block_value": "resource_limit_boundary_mapping",
                "repurpose_potential": 4
            }
        ]
    
    def _store_failure_with_repurpose_metadata(self, failure: Dict[str, Any]) -> bool:
        """
        Store failure with enhanced repurposing metadata
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Generate correlation signature for pattern matching
            correlation_sig = self._generate_correlation_signature(failure)
            
            # Enhanced metadata for repurposing
            extraction_metadata = json.dumps({
                "extraction_timestamp": datetime.now().isoformat(),
                "repurpose_applications": self._identify_repurpose_applications(failure),
                "transformation_possibilities": self._identify_transformations(failure),
                "cross_correlation_potential": self._assess_correlation_potential(failure)
            })
            
            cursor.execute('''
                INSERT OR REPLACE INTO failures (
                    failure_id, category, severity, error_message, context,
                    timestamp, source_type, runner_info, repurpose_potential,
                    building_block_value, correlation_signature, extraction_metadata
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                failure["failure_id"],
                failure["category"], 
                failure["severity"],
                failure["error_message"],
                failure["context"],
                failure.get("timestamp", datetime.now().isoformat()),
                failure["source_type"],
                failure.get("runner_info", "unknown"),
                failure.get("repurpose_potential", 1),
                failure.get("building_block_value", "general_failure_pattern"),
                correlation_sig,
                extraction_metadata
            ))
            
            conn.commit()
            conn.close()
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Error storing failure {failure.get('failure_id', 'unknown')}: {e}")
            return False
    
    def _generate_correlation_signature(self, failure: Dict[str, Any]) -> str:
        """Generate signature for cross-correlation analysis"""
        # Create signature from key failure characteristics
        sig_components = [
            failure.get("category", ""),
            failure.get("severity", ""),
            failure.get("source_type", ""),
            failure.get("building_block_value", "")
        ]
        
        signature_string = "|".join(sig_components)
        return hashlib.md5(signature_string.encode()).hexdigest()[:16]
    
    def _identify_repurpose_applications(self, failure: Dict[str, Any]) -> List[str]:
        """Identify potential applications for repurposing this failure data"""
        applications = []
        
        category = failure.get("category", "").lower()
        error_msg = failure.get("error_message", "").lower()
        
        if "memory" in category or "memory" in error_msg:
            applications.extend([
                "stress_testing_baseline",
                "memory_limit_calibration", 
                "resource_monitoring_thresholds"
            ])
        
        if "timeout" in category or "timeout" in error_msg:
            applications.extend([
                "performance_benchmarking",
                "timeout_optimization",
                "latency_boundary_detection"
            ])
        
        if "dependency" in category or "import" in error_msg:
            applications.extend([
                "dependency_compatibility_matrix",
                "version_conflict_prediction",
                "package_ecosystem_mapping"
            ])
        
        return applications
    
    def _identify_transformations(self, failure: Dict[str, Any]) -> List[str]:
        """Identify ways this failure data can be transformed"""
        transformations = [
            "negative_test_case_generation",
            "boundary_condition_mapping",
            "failure_pattern_templates"
        ]
        
        # Add specific transformations based on failure type
        if failure.get("repurpose_potential", 1) > 3:
            transformations.extend([
                "predictive_model_training_data",
                "automated_fix_strategy_seed",
                "chaos_engineering_scenario_template"
            ])
        
        return transformations
    
    def _assess_correlation_potential(self, failure: Dict[str, Any]) -> str:
        """Assess potential for cross-correlation with other failures"""
        potential_levels = ["low", "medium", "high", "critical"]
        
        # Assess based on failure characteristics
        repurpose_score = failure.get("repurpose_potential", 1)
        
        if repurpose_score >= 4:
            return "critical"
        elif repurpose_score >= 3:
            return "high"
        elif repurpose_score >= 2:
            return "medium"
        else:
            return "low"
    
    async def generate_repurposing_report(self) -> Dict[str, Any]:
        """Generate comprehensive report on repurposable failure data"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get comprehensive statistics
        cursor.execute("SELECT COUNT(*) FROM failures")
        total_failures = cursor.fetchone()[0]
        
        cursor.execute("""
            SELECT source_type, COUNT(*) as count, AVG(repurpose_potential) as avg_potential
            FROM failures 
            GROUP BY source_type 
            ORDER BY avg_potential DESC
        """)
        source_breakdown = cursor.fetchall()
        
        cursor.execute("""
            SELECT building_block_value, COUNT(*) as frequency
            FROM failures
            GROUP BY building_block_value
            ORDER BY frequency DESC
            LIMIT 10
        """)
        top_building_blocks = cursor.fetchall()
        
        conn.close()
        
        report = {
            "report_timestamp": datetime.now().isoformat(),
            "total_harvestable_failures": total_failures,
            "source_breakdown": [
                {
                    "source": source,
                    "failure_count": count,
                    "average_repurpose_potential": round(avg_potential, 2)
                }
                for source, count, avg_potential in source_breakdown
            ],
            "top_building_blocks": [
                {
                    "building_block_type": block_type,
                    "frequency": frequency
                }
                for block_type, frequency in top_building_blocks
            ],
            "repurposing_opportunities": self._calculate_repurposing_opportunities(total_failures)
        }
        
        return report
    
    def _calculate_repurposing_opportunities(self, total_failures: int) -> Dict[str, Any]:
        """Calculate specific repurposing opportunities from failure data"""
        return {
            "stress_test_scenarios": min(total_failures * 0.3, 50),
            "negative_test_cases": min(total_failures * 0.5, 100),
            "chaos_engineering_templates": min(total_failures * 0.2, 30),
            "predictive_model_training_samples": total_failures,
            "boundary_condition_mappings": min(total_failures * 0.4, 75),
            "automated_fix_strategies": min(total_failures * 0.1, 20)
        }

async def main():
    parser = argparse.ArgumentParser(description="Aggressive Failure Harvester for Neural Archaeology")
    parser.add_argument("--aggressive-mode", action="store_true", 
                       help="Enable aggressive harvesting from all sources including simulated failures")
    parser.add_argument("--db-path", default="data/generert/failure_archaeology.db",
                       help="Path to archaeology database")
    
    args = parser.parse_args()
    
    harvester = AggressiveFailureHarvester(args.db_path)
    harvester.initialize_expanded_database()
    
    # Perform aggressive harvesting
    harvested_count = await harvester.harvest_from_multiple_sources(args.aggressive_mode)
    
    # Generate repurposing report
    report = await harvester.generate_repurposing_report()
    
    # Save report
    report_path = Path("data/rapporter") / f"aggressive_harvest_report_{int(time.time())}.json"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(report_path, "w") as f:
        json.dump(report, f, indent=2)
    
    print(f"🔥 AGGRESSIVE HARVEST COMPLETE!")
    print(f"📊 Harvested: {harvested_count} failures")
    print(f"🧠 Total repurposable failures: {report['total_harvestable_failures']}")
    print(f"📄 Report saved: {report_path}")
    
    # Print top repurposing opportunities
    print(f"\n🎯 TOP REPURPOSING OPPORTUNITIES:")
    for opportunity, count in report['repurposing_opportunities'].items():
        print(f"   {opportunity}: {count} potential applications")

if __name__ == "__main__":
    asyncio.run(main())
