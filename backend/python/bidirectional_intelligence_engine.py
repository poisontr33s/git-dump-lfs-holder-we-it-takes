#!/usr/bin/env python3
"""
PSYCHO-NOIR KONTRAPUNKT: BIDIRECTIONAL LEARNING ENGINE
======================================================

Advanced system for converting failure patterns into predictive intelligence
and automated fix recommendation system. The neural archaeology of failed runs
transformed into proactive system resilience.

DEN USYNLIGE HÅND: From chaos to order, from failure to wisdom.
"""

import json
import sqlite3
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
import datetime
import re
import hashlib
from collections import defaultdict, Counter

from failure_archaeology_system import (
    FailureArchaeologyDB, FailureArtifact, FailureDomain, 
    FailureSeverity, PredictiveFailureEngine
)

@dataclass
class FixPattern:
    """Represents a successful fix pattern extracted from resolved failures"""
    pattern_id: str
    error_signature_pattern: str
    domain: FailureDomain
    fix_strategy: str
    success_rate: float
    context_requirements: Dict[str, Any]
    implementation_steps: List[str]
    prevention_measures: List[str]
    related_patterns: List[str]

@dataclass
class PredictiveAlert:
    """Alert generated when system predicts potential failure"""
    alert_id: str
    timestamp: str
    predicted_failure_type: str
    confidence_level: float
    risk_factors: List[str]
    recommended_preemptive_actions: List[str]
    similar_historical_cases: List[str]

class AdvancedPatternExtractor:
    """Extract sophisticated patterns from failure data"""
    
    def __init__(self, archaeology_db: FailureArchaeologyDB):
        self.db = archaeology_db
        
    def extract_fix_patterns(self) -> List[FixPattern]:
        """Extract successful fix patterns from resolved failures"""
        print("🔍 EXTRACTING FIX PATTERNS FROM RESOLVED FAILURES...")
        
        # Get all resolved failures
        with sqlite3.connect(self.db.db_path) as conn:
            resolved_failures = conn.execute("""
                SELECT * FROM failure_artifacts 
                WHERE resolution_status IN ('patched', 'systematic_fix')
            """).fetchall()
        
        patterns = []
        pattern_groups = defaultdict(list)
        
        # Group similar failures by error signature patterns
        for row in resolved_failures:
            artifact = self.db._row_to_artifact(row)
            
            # Extract base pattern from error signature
            base_pattern = self._extract_base_pattern(artifact.error_signature)
            pattern_groups[base_pattern].append(artifact)
        
        # Generate fix patterns for each group
        for base_pattern, artifacts in pattern_groups.items():
            if len(artifacts) >= 2:  # Need multiple instances to establish pattern
                pattern = self._create_fix_pattern(base_pattern, artifacts)
                if pattern:
                    patterns.append(pattern)
        
        print(f"✅ EXTRACTED {len(patterns)} FIX PATTERNS")
        return patterns
    
    def _extract_base_pattern(self, error_signature: str) -> str:
        """Extract base pattern from specific error signature"""
        # Remove specific details, keep core pattern
        pattern = re.sub(r'\d+', 'N', error_signature)  # Replace numbers
        pattern = re.sub(r'[A-F0-9]{8,}', 'HEXADDR', pattern)  # Replace hex addresses
        pattern = re.sub(r'[a-f0-9]{12,}', 'HASH', pattern)  # Replace hashes
        return pattern
    
    def _create_fix_pattern(self, base_pattern: str, artifacts: List[FailureArtifact]) -> Optional[FixPattern]:
        """Create a fix pattern from similar failures"""
        if not artifacts:
            return None
        
        # Analyze successful fixes
        successful_fixes = []
        for artifact in artifacts:
            for fix_attempt in artifact.attempted_fixes:
                if fix_attempt.get("outcome") == "success":
                    successful_fixes.append(fix_attempt)
        
        if not successful_fixes:
            return None
        
        # Calculate success rate and extract common strategies
        success_rate = len(successful_fixes) / len(artifacts)
        
        # Extract most common fix strategy
        fix_descriptions = [fix.get("description", "") for fix in successful_fixes]
        strategy_counter = Counter(fix_descriptions)
        most_common_strategy = strategy_counter.most_common(1)[0][0] if strategy_counter else "Unknown"
        
        # Extract implementation steps from learning extractions
        implementation_steps = []
        prevention_measures = []
        
        for artifact in artifacts:
            if artifact.learning_extraction:
                # Simple heuristic to extract actionable steps
                if "implement" in artifact.learning_extraction.lower():
                    implementation_steps.append(artifact.learning_extraction)
                if artifact.prevention_strategy:
                    prevention_measures.append(artifact.prevention_strategy)
        
        pattern_id = hashlib.md5(base_pattern.encode()).hexdigest()[:12]
        
        return FixPattern(
            pattern_id=pattern_id,
            error_signature_pattern=base_pattern,
            domain=artifacts[0].domain,
            fix_strategy=most_common_strategy,
            success_rate=success_rate,
            context_requirements=self._extract_context_requirements(artifacts),
            implementation_steps=list(set(implementation_steps)),
            prevention_measures=list(set(prevention_measures)),
            related_patterns=[]
        )
    
    def _extract_context_requirements(self, artifacts: List[FailureArtifact]) -> Dict[str, Any]:
        """Extract common context requirements from artifacts"""
        contexts = [artifact.context_snapshot for artifact in artifacts]
        
        # Find common keys and typical values
        common_context = {}
        all_keys = set()
        for context in contexts:
            all_keys.update(context.keys())
        
        for key in all_keys:
            values = [ctx.get(key) for ctx in contexts if key in ctx]
            if values:
                common_context[key] = Counter(values).most_common(1)[0][0]
        
        return common_context

class BidirectionalIntelligenceEngine:
    """Core engine for bidirectional learning and predictive intelligence"""
    
    def __init__(self, archaeology_db: FailureArchaeologyDB):
        self.db = archaeology_db
        self.pattern_extractor = AdvancedPatternExtractor(archaeology_db)
        self.fix_patterns = []
        self.prediction_cache = {}
        
    def initialize_intelligence(self):
        """Initialize the intelligence engine with existing data"""
        print("🧠 INITIALIZING BIDIRECTIONAL INTELLIGENCE ENGINE...")
        self.fix_patterns = self.pattern_extractor.extract_fix_patterns()
        self._build_pattern_relationships()
        print("✅ INTELLIGENCE ENGINE READY")
    
    def _build_pattern_relationships(self):
        """Build relationships between fix patterns"""
        for i, pattern1 in enumerate(self.fix_patterns):
            for j, pattern2 in enumerate(self.fix_patterns[i+1:], i+1):
                if self._patterns_are_related(pattern1, pattern2):
                    pattern1.related_patterns.append(pattern2.pattern_id)
                    pattern2.related_patterns.append(pattern1.pattern_id)
    
    def _patterns_are_related(self, pattern1: FixPattern, pattern2: FixPattern) -> bool:
        """Determine if two patterns are related"""
        # Simple similarity check
        signature_similarity = self._calculate_signature_similarity(
            pattern1.error_signature_pattern, 
            pattern2.error_signature_pattern
        )
        domain_match = pattern1.domain == pattern2.domain
        
        return signature_similarity > 0.6 or (domain_match and signature_similarity > 0.3)
    
    def _calculate_signature_similarity(self, sig1: str, sig2: str) -> float:
        """Calculate similarity between two error signatures"""
        words1 = set(sig1.split('_'))
        words2 = set(sig2.split('_'))
        
        if not words1 or not words2:
            return 0.0
        
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        return len(intersection) / len(union)
    
    def predict_failure_risk(self, current_context: Dict[str, Any]) -> List[PredictiveAlert]:
        """Predict potential failures based on current context"""
        alerts = []
        
        # Check context against known failure patterns
        for pattern in self.fix_patterns:
            risk_score = self._calculate_risk_score(current_context, pattern)
            
            if risk_score > 0.5:  # Threshold for alert
                alert = PredictiveAlert(
                    alert_id=hashlib.md5(f"{pattern.pattern_id}_{datetime.datetime.now().isoformat()}".encode()).hexdigest()[:12],
                    timestamp=datetime.datetime.now().isoformat(),
                    predicted_failure_type=pattern.error_signature_pattern,
                    confidence_level=risk_score,
                    risk_factors=self._identify_risk_factors(current_context, pattern),
                    recommended_preemptive_actions=pattern.prevention_measures,
                    similar_historical_cases=[pattern.pattern_id]
                )
                alerts.append(alert)
        
        return sorted(alerts, key=lambda x: x.confidence_level, reverse=True)
    
    def _calculate_risk_score(self, context: Dict[str, Any], pattern: FixPattern) -> float:
        """Calculate risk score for a specific pattern given current context"""
        score = 0.0
        total_factors = 0
        
        # Check context requirements match
        for key, expected_value in pattern.context_requirements.items():
            total_factors += 1
            if key in context:
                if context[key] == expected_value:
                    score += 1.0
                elif str(context[key]).lower() in str(expected_value).lower():
                    score += 0.5
        
        # Normalize score
        if total_factors > 0:
            score = score / total_factors
        
        # Apply domain-specific risk modifiers
        if pattern.domain == FailureDomain.SKYSKRAPER_SYSTEMS:
            if "copilot" in str(context).lower() or "automation" in str(context).lower():
                score *= 1.2
        elif pattern.domain == FailureDomain.RUSTBELT_IMPROVISATION:
            if "manual" in str(context).lower() or "patch" in str(context).lower():
                score *= 1.1
        
        return min(score, 1.0)
    
    def _identify_risk_factors(self, context: Dict[str, Any], pattern: FixPattern) -> List[str]:
        """Identify specific risk factors in current context"""
        risk_factors = []
        
        # Check for known problematic conditions
        context_str = str(context).lower()
        
        if "timeout" in context_str:
            risk_factors.append("timeout_conditions_detected")
        if "large" in context_str or "size" in context_str:
            risk_factors.append("scale_related_risk")
        if "network" in context_str or "connection" in context_str:
            risk_factors.append("network_dependency_risk")
        if pattern.domain == FailureDomain.SKYSKRAPER_SYSTEMS and "runner" in context_str:
            risk_factors.append("automation_runner_instability")
        
        return risk_factors
    
    def recommend_fixes(self, error_signature: str, context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Recommend fixes based on similar patterns"""
        recommendations = []
        
        # Find matching patterns
        matching_patterns = []
        base_pattern = self.pattern_extractor._extract_base_pattern(error_signature)
        
        for pattern in self.fix_patterns:
            similarity = self._calculate_signature_similarity(base_pattern, pattern.error_signature_pattern)
            if similarity > 0.4:
                matching_patterns.append((pattern, similarity))
        
        # Sort by similarity and success rate
        matching_patterns.sort(key=lambda x: (x[1], x[0].success_rate), reverse=True)
        
        for pattern, similarity in matching_patterns[:5]:  # Top 5 recommendations
            recommendation = {
                "fix_strategy": pattern.fix_strategy,
                "confidence": similarity * pattern.success_rate,
                "implementation_steps": pattern.implementation_steps,
                "prevention_measures": pattern.prevention_measures,
                "domain": pattern.domain.value,
                "pattern_id": pattern.pattern_id
            }
            recommendations.append(recommendation)
        
        return recommendations
    
    def generate_intelligence_report(self) -> Dict[str, Any]:
        """Generate comprehensive intelligence report"""
        return {
            "report_timestamp": datetime.datetime.now().isoformat(),
            "total_patterns": len(self.fix_patterns),
            "patterns_by_domain": {
                domain.value: len([p for p in self.fix_patterns if p.domain == domain])
                for domain in FailureDomain
            },
            "average_success_rate": sum(p.success_rate for p in self.fix_patterns) / len(self.fix_patterns) if self.fix_patterns else 0,
            "top_fix_strategies": self._get_top_strategies(),
            "system_resilience_score": self._calculate_resilience_score()
        }
    
    def _get_top_strategies(self) -> List[Dict[str, Any]]:
        """Get top performing fix strategies"""
        strategy_performance = defaultdict(list)
        
        for pattern in self.fix_patterns:
            strategy_performance[pattern.fix_strategy].append(pattern.success_rate)
        
        top_strategies = []
        for strategy, rates in strategy_performance.items():
            avg_rate = sum(rates) / len(rates)
            top_strategies.append({
                "strategy": strategy,
                "average_success_rate": avg_rate,
                "usage_count": len(rates)
            })
        
        return sorted(top_strategies, key=lambda x: x["average_success_rate"], reverse=True)[:10]
    
    def _calculate_resilience_score(self) -> float:
        """Calculate overall system resilience score"""
        if not self.fix_patterns:
            return 0.0
        
        # Base score from pattern coverage
        domain_coverage = len(set(p.domain for p in self.fix_patterns)) / len(FailureDomain)
        
        # Average success rate
        avg_success = sum(p.success_rate for p in self.fix_patterns) / len(self.fix_patterns)
        
        # Pattern interconnectedness
        total_relationships = sum(len(p.related_patterns) for p in self.fix_patterns)
        relationship_density = total_relationships / (len(self.fix_patterns) ** 2) if self.fix_patterns else 0
        
        # Combine factors
        resilience_score = (domain_coverage * 0.4 + avg_success * 0.4 + relationship_density * 0.2)
        
        return min(resilience_score, 1.0)

def main():
    """Main execution for testing and demonstration"""
    print("🧠 PSYCHO-NOIR KONTRAPUNKT: BIDIRECTIONAL INTELLIGENCE ENGINE")
    print("=" * 70)
    
    # Initialize systems
    archaeology_db = FailureArchaeologyDB()
    intelligence_engine = BidirectionalIntelligenceEngine(archaeology_db)
    
    # Initialize intelligence
    intelligence_engine.initialize_intelligence()
    
    # Generate intelligence report
    report = intelligence_engine.generate_intelligence_report()
    
    print("\n📊 INTELLIGENCE REPORT:")
    print(json.dumps(report, indent=2))
    
    # Example: Predict risks for current context
    test_context = {
        "operation": "copilot_analysis",
        "file_count": 25,
        "environment": "github_actions",
        "runner_type": "ubuntu-latest"
    }
    
    alerts = intelligence_engine.predict_failure_risk(test_context)
    
    print(f"\n🚨 PREDICTIVE ALERTS ({len(alerts)} detected):")
    for alert in alerts:
        print(f"   • {alert.predicted_failure_type} (Confidence: {alert.confidence_level:.2f})")
        for action in alert.recommended_preemptive_actions:
            print(f"     → {action}")
    
    print("\n✅ BIDIRECTIONAL INTELLIGENCE ENGINE OPERATIONAL")

if __name__ == "__main__":
    main()
