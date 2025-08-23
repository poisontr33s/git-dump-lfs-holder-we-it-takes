#!/usr/bin/env python3
"""
PSYCHO-NOIR KONTRAPUNKT: NEURAL ARCHAEOLOGY MASTER ORCHESTRATOR
===============================================================

Master system for orchestrating the complete failure-to-wisdom transformation pipeline:
1. Harvest 40+ failed runs from multiple sources
2. Catalog failures in archaeological database
3. Extract bidirectional learning patterns
4. Generate predictive intelligence
5. Provide real-time fix recommendations

This is the apex of turning chaos into order, failure into systematic resilience.

DEN USYNLIGE HÅND: The architect of order from chaos, the neural archaeology of digital evolution.
"""

import asyncio
import json
import sqlite3
import datetime
import argparse
from pathlib import Path
from typing import Dict, List, Any, Optional
import logging
import time

from failure_archaeology_system import (
    FailureArchaeologyDB, FailureArtifact, FailureDomain, 
    FailureSeverity, PredictiveFailureEngine
)
from failed_runs_harvester import FailedRunsHarvester
from bidirectional_intelligence_engine import BidirectionalIntelligenceEngine

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('data/generert/neural_archaeology.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('NeuralArchaeologyOrchestrator')

class NeuralArchaeologyOrchestrator:
    """Master orchestrator for the complete neural archaeology system"""
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or self._default_config()
        self.archaeology_db = FailureArchaeologyDB()
        self.harvester = FailedRunsHarvester()
        self.intelligence_engine = BidirectionalIntelligenceEngine(self.archaeology_db)
        self.execution_log = []
        
        # Ensure output directories exist
        Path("data/generert").mkdir(parents=True, exist_ok=True)
        Path("data/rapporter").mkdir(parents=True, exist_ok=True)
        
    def _default_config(self) -> Dict[str, Any]:
        """Default configuration for the orchestrator"""
        return {
            "harvest_sources": ["github_actions", "manual_logs"],
            "max_failures_to_process": 50,
            "intelligence_threshold": 0.6,
            "report_formats": ["json", "markdown"],
            "auto_fix_recommendations": True,
            "predictive_alerts_enabled": True
        }
    
    async def execute_full_pipeline(self) -> Dict[str, Any]:
        """Execute the complete neural archaeology pipeline"""
        logger.info("🧠 INITIATING NEURAL ARCHAEOLOGY PIPELINE...")
        
        pipeline_start = time.time()
        results = {
            "pipeline_start": datetime.datetime.now().isoformat(),
            "stages": {},
            "errors": [],
            "summary": {}
        }
        
        try:
            # Stage 1: Harvest Failed Runs
            logger.info("📡 STAGE 1: HARVESTING FAILED RUNS...")
            harvest_results = await self._execute_harvest_stage()
            results["stages"]["harvest"] = harvest_results
            
            # Stage 2: Catalog Failures
            logger.info("🗃️ STAGE 2: CATALOGING FAILURES...")
            catalog_results = await self._execute_catalog_stage(harvest_results.get("harvested_data", []))
            results["stages"]["catalog"] = catalog_results
            
            # Stage 3: Initialize Intelligence
            logger.info("🧠 STAGE 3: INITIALIZING INTELLIGENCE ENGINE...")
            intelligence_results = await self._execute_intelligence_stage()
            results["stages"]["intelligence"] = intelligence_results
            
            # Stage 4: Generate Predictions
            logger.info("🔮 STAGE 4: GENERATING PREDICTIVE INTELLIGENCE...")
            prediction_results = await self._execute_prediction_stage()
            results["stages"]["predictions"] = prediction_results
            
            # Stage 5: Generate Reports
            logger.info("📊 STAGE 5: GENERATING COMPREHENSIVE REPORTS...")
            report_results = await self._execute_reporting_stage(results)
            results["stages"]["reporting"] = report_results
            
        except Exception as e:
            logger.error(f"❌ PIPELINE ERROR: {e}")
            results["errors"].append(str(e))
        
        # Calculate pipeline summary
        pipeline_duration = time.time() - pipeline_start
        results["pipeline_duration"] = pipeline_duration
        results["pipeline_end"] = datetime.datetime.now().isoformat()
        results["summary"] = self._generate_pipeline_summary(results)
        
        logger.info("✅ NEURAL ARCHAEOLOGY PIPELINE COMPLETED")
        return results
    
    async def _execute_harvest_stage(self) -> Dict[str, Any]:
        """Execute the failure harvesting stage"""
        harvested_data = []
        errors = []
        
        try:
            # Harvest from GitHub Actions
            if "github_actions" in self.config["harvest_sources"]:
                github_failures = self.harvester.harvest_github_actions_failures()
                harvested_data.extend(github_failures)
                logger.info(f"🔍 Harvested {len(github_failures)} failures from GitHub Actions")
            
            # TODO: Add other harvest sources
            # - Manual log files
            # - VS Code Copilot errors
            # - Terminal command failures
            # - Build system failures
            
        except Exception as e:
            errors.append(f"Harvest error: {e}")
            logger.error(f"Harvest error: {e}")
        
        return {
            "harvested_count": len(harvested_data),
            "harvested_data": harvested_data[:self.config["max_failures_to_process"]],
            "errors": errors,
            "sources_used": self.config["harvest_sources"]
        }
    
    async def _execute_catalog_stage(self, harvested_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Execute the failure cataloging stage"""
        try:
            cataloged_ids = self.harvester.catalog_failures_from_harvest(harvested_data)
            
            return {
                "cataloged_count": len(cataloged_ids),
                "cataloged_ids": cataloged_ids,
                "database_path": str(self.archaeology_db.db_path)
            }
            
        except Exception as e:
            logger.error(f"Catalog error: {e}")
            return {"error": str(e)}
    
    async def _execute_intelligence_stage(self) -> Dict[str, Any]:
        """Execute intelligence engine initialization"""
        try:
            self.intelligence_engine.initialize_intelligence()
            
            intelligence_report = self.intelligence_engine.generate_intelligence_report()
            
            return {
                "patterns_extracted": intelligence_report["total_patterns"],
                "resilience_score": intelligence_report["system_resilience_score"],
                "top_strategies": intelligence_report["top_fix_strategies"][:5],
                "full_report": intelligence_report
            }
            
        except Exception as e:
            logger.error(f"Intelligence error: {e}")
            return {"error": str(e)}
    
    async def _execute_prediction_stage(self) -> Dict[str, Any]:
        """Execute predictive analysis stage"""
        try:
            # Test current context prediction
            current_context = {
                "timestamp": datetime.datetime.now().isoformat(),
                "environment": "production",
                "operation_type": "neural_archaeology_execution",
                "system_load": "normal",
                "recent_changes": True
            }
            
            alerts = self.intelligence_engine.predict_failure_risk(current_context)
            
            return {
                "alerts_generated": len(alerts),
                "high_confidence_alerts": len([a for a in alerts if a.confidence_level > 0.7]),
                "alerts": [
                    {
                        "type": alert.predicted_failure_type,
                        "confidence": alert.confidence_level,
                        "actions": alert.recommended_preemptive_actions
                    }
                    for alert in alerts[:10]  # Top 10 alerts
                ]
            }
            
        except Exception as e:
            logger.error(f"Prediction error: {e}")
            return {"error": str(e)}
    
    async def _execute_reporting_stage(self, pipeline_results: Dict[str, Any]) -> Dict[str, Any]:
        """Execute comprehensive reporting stage"""
        reports_generated = []
        
        try:
            # Generate JSON report
            if "json" in self.config["report_formats"]:
                json_report_path = await self._generate_json_report(pipeline_results)
                reports_generated.append(json_report_path)
            
            # Generate Markdown report
            if "markdown" in self.config["report_formats"]:
                md_report_path = await self._generate_markdown_report(pipeline_results)
                reports_generated.append(md_report_path)
            
            return {
                "reports_generated": reports_generated,
                "total_reports": len(reports_generated)
            }
            
        except Exception as e:
            logger.error(f"Reporting error: {e}")
            return {"error": str(e)}
    
    async def _generate_json_report(self, pipeline_results: Dict[str, Any]) -> str:
        """Generate comprehensive JSON report"""
        report_path = f"data/rapporter/neural_archaeology_report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(report_path, 'w') as f:
            json.dump(pipeline_results, f, indent=2)
        
        logger.info(f"📄 JSON report generated: {report_path}")
        return report_path
    
    async def _generate_markdown_report(self, pipeline_results: Dict[str, Any]) -> str:
        """Generate human-readable Markdown report"""
        report_path = f"data/rapporter/neural_archaeology_report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        
        # Generate Markdown content
        md_content = self._create_markdown_content(pipeline_results)
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(md_content)
        
        logger.info(f"📄 Markdown report generated: {report_path}")
        return report_path
    
    def _create_markdown_content(self, results: Dict[str, Any]) -> str:
        """Create formatted Markdown content for the report"""
        content = f"""# 🧠 PSYCHO-NOIR KONTRAPUNKT: NEURAL ARCHAEOLOGY RAPPORT

**Generert:** {results.get('pipeline_start', 'Unknown')}  
**Varighet:** {results.get('pipeline_duration', 0):.2f} sekunder  
**Status:** {'✅ SUKSESS' if not results.get('errors') else '⚠️ DELVIS SUKSESS'}

---

## 📊 EXECUTIVE SUMMARY

{self._create_executive_summary(results)}

---

## 🔍 PIPELINE STAGES

### 1. 📡 HARVEST STAGE
"""
        
        harvest = results.get("stages", {}).get("harvest", {})
        content += f"""
- **Harvested Failures:** {harvest.get('harvested_count', 0)}
- **Sources:** {', '.join(harvest.get('sources_used', []))}
- **Errors:** {len(harvest.get('errors', []))}
"""
        
        catalog = results.get("stages", {}).get("catalog", {})
        content += f"""
### 2. 🗃️ CATALOG STAGE
- **Cataloged Failures:** {catalog.get('cataloged_count', 0)}
- **Database:** {catalog.get('database_path', 'N/A')}
"""
        
        intelligence = results.get("stages", {}).get("intelligence", {})
        content += f"""
### 3. 🧠 INTELLIGENCE STAGE
- **Patterns Extracted:** {intelligence.get('patterns_extracted', 0)}
- **System Resilience Score:** {intelligence.get('resilience_score', 0.0):.2f}

#### Top Fix Strategies:
"""
        
        for i, strategy in enumerate(intelligence.get('top_strategies', [])[:5], 1):
            content += f"{i}. **{strategy.get('strategy', 'Unknown')}** - Success Rate: {strategy.get('average_success_rate', 0.0):.2f}\n"
        
        predictions = results.get("stages", {}).get("predictions", {})
        content += f"""
### 4. 🔮 PREDICTION STAGE
- **Alerts Generated:** {predictions.get('alerts_generated', 0)}
- **High Confidence Alerts:** {predictions.get('high_confidence_alerts', 0)}

#### Critical Alerts:
"""
        
        for alert in predictions.get('alerts', [])[:5]:
            content += f"- **{alert.get('type', 'Unknown')}** (Confidence: {alert.get('confidence', 0.0):.2f})\n"
            for action in alert.get('actions', []):
                content += f"  - {action}\n"
        
        content += f"""
---

## 🎯 ANBEFALINGER

{self._generate_recommendations(results)}

---

## ⚠️ SYSTEMHELSE

{self._generate_system_health(results)}

---

*Generert av Neural Archaeology Orchestrator - Psycho-Noir Kontrapunkt*
*Den Usynlige Hånd: Kaos transformert til visdom*
"""
        
        return content
    
    def _create_executive_summary(self, results: Dict[str, Any]) -> str:
        """Create executive summary"""
        stages = results.get("stages", {})
        harvest_count = stages.get("harvest", {}).get("harvested_count", 0)
        catalog_count = stages.get("catalog", {}).get("cataloged_count", 0)
        patterns_count = stages.get("intelligence", {}).get("patterns_extracted", 0)
        
        return f"""
Denne rapporten dokumenterer den komplette Neural Archaeology-pipelinen som prosesserte **{harvest_count} failed runs** og transformerte dem til **{patterns_count} læringsmønstre** for prediktiv feilhåndtering.

**Nøkkelresultater:**
- {catalog_count} feil katalogisert i archaeology database
- {patterns_count} fix-mønstre ekstrahert for bidireksjonell læring
- Systemresiliens-score beregnet og prediktive alerter generert
- Automatiserte anbefalinger for proaktiv feilhåndtering tilgjengelig
"""
    
    def _generate_recommendations(self, results: Dict[str, Any]) -> str:
        """Generate actionable recommendations"""
        recommendations = [
            "🔧 **Implementér automatiserte fixes** basert på de mest suksessfulle fix-strategiene",
            "📊 **Overvåk høy-risiko kontekster** identifisert av prediktive modeller",
            "🔄 **Etablér kontinuerlig læring** ved å oppdatere archaeology database regelmessig",
            "⚡ **Prioritér Skyskraper-domenet** hvis høy feilrate detekteres der",
            "🛠️ **Utvid Rustbelt improvisasjons-verktøy** for bedre manuel håndtering"
        ]
        
        return "\n".join(recommendations)
    
    def _generate_system_health(self, results: Dict[str, Any]) -> str:
        """Generate system health assessment"""
        intelligence = results.get("stages", {}).get("intelligence", {})
        resilience_score = intelligence.get('resilience_score', 0.0)
        
        if resilience_score > 0.8:
            health_status = "🟢 **UTMERKET** - Systemet viser høy resiliens"
        elif resilience_score > 0.6:
            health_status = "🟡 **BRA** - Systemet har god resiliens med forbedringspotensial"
        elif resilience_score > 0.4:
            health_status = "🟠 **MODERAT** - Systemet trenger oppmerksomhet"
        else:
            health_status = "🔴 **KRITISK** - Systemet krever umiddelbar handling"
        
        return f"""
**System Resiliens Score:** {resilience_score:.2f}/1.0

**Status:** {health_status}

**Anbefalte Tiltak:** Fortsett å mate systemet med nye failed runs for kontinuerlig forbedring av prediktiv nøyaktighet.
"""
    
    def _generate_pipeline_summary(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate pipeline execution summary"""
        stages = results.get("stages", {})
        
        return {
            "total_failures_processed": stages.get("harvest", {}).get("harvested_count", 0),
            "patterns_learned": stages.get("intelligence", {}).get("patterns_extracted", 0),
            "alerts_generated": stages.get("predictions", {}).get("alerts_generated", 0),
            "pipeline_success": len(results.get("errors", [])) == 0,
            "resilience_improvement": stages.get("intelligence", {}).get("resilience_score", 0.0),
            "execution_timestamp": results.get("pipeline_start")
        }
    
    async def quick_analysis(self, error_signature: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Quick analysis and recommendation for a specific error"""
        if not self.intelligence_engine.fix_patterns:
            self.intelligence_engine.initialize_intelligence()
        
        recommendations = self.intelligence_engine.recommend_fixes(error_signature, context or {})
        
        return {
            "error_signature": error_signature,
            "recommendations": recommendations,
            "analysis_timestamp": datetime.datetime.now().isoformat()
        }

async def main():
    """Main execution function"""
    parser = argparse.ArgumentParser(description="Neural Archaeology Master Orchestrator")
    parser.add_argument("--mode", choices=["full", "harvest", "analyze", "quick"], 
                       default="full", help="Execution mode")
    parser.add_argument("--error", help="Error signature for quick analysis mode")
    parser.add_argument("--config", help="Configuration file path")
    
    args = parser.parse_args()
    
    # Load configuration
    config = None
    if args.config and Path(args.config).exists():
        with open(args.config) as f:
            config = json.load(f)
    
    orchestrator = NeuralArchaeologyOrchestrator(config)
    
    if args.mode == "full":
        print("🧠 EXECUTING FULL NEURAL ARCHAEOLOGY PIPELINE...")
        results = await orchestrator.execute_full_pipeline()
        print(f"\n✅ PIPELINE COMPLETED - Check reports in data/rapporter/")
        
    elif args.mode == "quick" and args.error:
        print(f"🔍 QUICK ANALYSIS FOR ERROR: {args.error}")
        results = await orchestrator.quick_analysis(args.error)
        print(json.dumps(results, indent=2))
        
    else:
        print("❌ Invalid mode or missing parameters")
        return
    
    print("\n🎯 NEURAL ARCHAEOLOGY ORCHESTRATOR COMPLETE")

if __name__ == "__main__":
    asyncio.run(main())
