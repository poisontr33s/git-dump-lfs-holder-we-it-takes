#!/usr/bin/env python3
"""
Error Classification Engine for Psycho-Noir Kontrapunkt CI/CD System

This module implements hierarchical error classification with bidirectional intelligence.
Errors are not just failures - they become building blocks for system improvement.

Classification Levels:
- GREEN: SUCCESS - All systems operational, data available for intelligence enhancement
- YELLOW: WARNING - Partial degradation, potential for improvement identified  
- RED: ERROR - Critical failure, requires immediate attention and learning

The system treats each error as a "neural pathway" in the CI consciousness,
building patterns and responses that improve future runs.
"""

import json
import re
import sys
from datetime import datetime
from typing import Dict, List, Tuple, Optional
from enum import Enum

class ClassificationLevel(Enum):
    """Error classification levels aligned with the psycho-noir aesthetic."""
    GREEN = "SUCCESS"
    YELLOW = "WARNING" 
    RED = "ERROR"

class ErrorSignature:
    """Represents a unique error pattern for bidirectional learning."""
    
    def __init__(self, pattern: str, level: ClassificationLevel, category: str, 
                 learning_weight: float = 1.0):
        self.pattern = pattern
        self.level = level
        self.category = category
        self.learning_weight = learning_weight
        self.occurrence_count = 0
        self.first_seen = datetime.now()
        self.last_seen = datetime.now()
        
    def update_occurrence(self):
        """Update occurrence tracking for bidirectional intelligence."""
        self.occurrence_count += 1
        self.last_seen = datetime.now()
        # Increase learning weight based on frequency (psycho-noir: patterns strengthen)
        self.learning_weight = min(10.0, 1.0 + (self.occurrence_count * 0.1))

class PsychoNoirErrorClassifier:
    """
    Main error classification engine.
    
    Implements the "Fragmentert Bevissthet" (Fragmented Consciousness) pattern
    where each error becomes part of the system's evolving intelligence.
    """
    
    def __init__(self):
        self.error_signatures = self._initialize_error_signatures()
        self.classified_errors = []
        self.intelligence_data = {}
        
    def _initialize_error_signatures(self) -> List[ErrorSignature]:
        """Initialize known error patterns with psycho-noir themed categorization."""
        return [
            # Build/Compilation Errors (Kildekode-Kadaver)
            ErrorSignature(r"npm.*ENOENT", ClassificationLevel.RED, "DEPENDENCY_PHANTOM"),
            ErrorSignature(r"ModuleNotFoundError", ClassificationLevel.RED, "IMPORT_VOID"),
            ErrorSignature(r"SyntaxError", ClassificationLevel.RED, "SYNTAX_CORRUPTION"),
            ErrorSignature(r"compilation.*failed", ClassificationLevel.RED, "COMPILATION_DECAY"),
            
            # Test Failures (Kompilerings-Spøkelser)
            ErrorSignature(r"test.*failed", ClassificationLevel.YELLOW, "TEST_ANOMALY"),
            ErrorSignature(r"assertion.*failed", ClassificationLevel.YELLOW, "REALITY_MISMATCH"),
            ErrorSignature(r"timeout.*exceeded", ClassificationLevel.YELLOW, "TEMPORAL_DRIFT"),
            
            # Network/Connection Issues (Nettverk-Skygger)
            ErrorSignature(r"connection.*refused", ClassificationLevel.RED, "CONNECTION_SEVERED"),
            ErrorSignature(r"network.*error", ClassificationLevel.YELLOW, "NETWORK_STATIC"),
            ErrorSignature(r"timeout.*network", ClassificationLevel.YELLOW, "SIGNAL_DEGRADATION"),
            
            # Permission/Security (Tilgang-Korrupsjon)
            ErrorSignature(r"permission.*denied", ClassificationLevel.RED, "ACCESS_BREACH"),
            ErrorSignature(r"unauthorized", ClassificationLevel.RED, "IDENTITY_REJECTION"),
            
            # Resource Issues (Ressurs-Undergang)
            ErrorSignature(r"out of memory", ClassificationLevel.RED, "MEMORY_DEPLETION"),
            ErrorSignature(r"disk.*full", ClassificationLevel.RED, "STORAGE_COLLAPSE"),
            ErrorSignature(r"cpu.*limit", ClassificationLevel.YELLOW, "PROCESSING_STRAIN"),
            
            # Success Patterns (Suksess-Resonans)
            ErrorSignature(r"tests.*passed", ClassificationLevel.GREEN, "TEST_HARMONY"),
            ErrorSignature(r"build.*successful", ClassificationLevel.GREEN, "BUILD_SYNTHESIS"),
            ErrorSignature(r"deployment.*complete", ClassificationLevel.GREEN, "DEPLOY_TRANSCENDENCE"),
        ]
    
    def classify_log_content(self, log_content: str, context: Dict = None) -> Dict:
        """
        Classify log content and extract intelligence patterns.
        
        Returns a structured classification with bidirectional learning data.
        """
        if context is None:
            context = {}
            
        classification_result = {
            "timestamp": datetime.now().isoformat(),
            "classification_level": ClassificationLevel.GREEN,
            "matched_signatures": [],
            "unclassified_anomalies": [],
            "intelligence_insights": {},
            "context": context
        }
        
        # Process each line for pattern matching
        lines = log_content.split('\n')
        highest_severity = ClassificationLevel.GREEN
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            matched = False
            for signature in self.error_signatures:
                if re.search(signature.pattern, line, re.IGNORECASE):
                    signature.update_occurrence()
                    matched = True
                    
                    match_data = {
                        "line": line,
                        "pattern": signature.pattern,
                        "category": signature.category,
                        "level": signature.level.value,
                        "learning_weight": signature.learning_weight,
                        "occurrence_count": signature.occurrence_count
                    }
                    classification_result["matched_signatures"].append(match_data)
                    
                    # Update overall severity
                    if signature.level.value == "ERROR" and highest_severity != ClassificationLevel.RED:
                        highest_severity = ClassificationLevel.RED
                    elif signature.level.value == "WARNING" and highest_severity == ClassificationLevel.GREEN:
                        highest_severity = ClassificationLevel.YELLOW
                    
                    break
            
            # Capture unclassified anomalies for learning
            if not matched and any(keyword in line.lower() for keyword in 
                                 ['error', 'fail', 'exception', 'warn', 'critical']):
                classification_result["unclassified_anomalies"].append({
                    "line": line,
                    "potential_new_signature": True
                })
        
        classification_result["classification_level"] = highest_severity
        
        # Generate intelligence insights
        classification_result["intelligence_insights"] = self._generate_intelligence_insights(
            classification_result
        )
        
        return classification_result
    
    def _generate_intelligence_insights(self, classification_result: Dict) -> Dict:
        """Generate bidirectional intelligence insights from classification data."""
        insights = {
            "pattern_frequency_analysis": {},
            "anomaly_emergence_detected": False,
            "system_learning_opportunities": [],
            "recommended_adaptive_responses": []
        }
        
        # Analyze pattern frequencies
        category_counts = {}
        for match in classification_result["matched_signatures"]:
            category = match["category"]
            category_counts[category] = category_counts.get(category, 0) + 1
        
        insights["pattern_frequency_analysis"] = category_counts
        
        # Detect new anomaly patterns
        if classification_result["unclassified_anomalies"]:
            insights["anomaly_emergence_detected"] = True
            insights["system_learning_opportunities"].extend([
                f"New pattern detected: {anomaly['line'][:100]}..."
                for anomaly in classification_result["unclassified_anomalies"][:3]
            ])
        
        # Generate adaptive responses based on psycho-noir philosophy
        if classification_result["classification_level"] == ClassificationLevel.RED:
            insights["recommended_adaptive_responses"].extend([
                "CRITICAL_SYSTEM_ADAPTATION_REQUIRED",
                "INITIATE_ERROR_PATTERN_DEEP_ANALYSIS",
                "ESCALATE_TO_CONSCIOUSNESS_LAYER"
            ])
        elif classification_result["classification_level"] == ClassificationLevel.YELLOW:
            insights["recommended_adaptive_responses"].extend([
                "MONITOR_DEGRADATION_PATTERNS",
                "PREPARE_ADAPTIVE_COUNTERMEASURES",
                "UPDATE_LEARNING_WEIGHTS"
            ])
        else:
            insights["recommended_adaptive_responses"].extend([
                "EXTRACT_SUCCESS_PATTERNS",
                "STRENGTHEN_POSITIVE_PATHWAYS",
                "EXPAND_INTELLIGENCE_BASE"
            ])
        
        return insights
    
    def export_classification_data(self) -> Dict:
        """Export all classification data for reporting and analysis."""
        return {
            "error_signatures": [
                {
                    "pattern": sig.pattern,
                    "level": sig.level.value,
                    "category": sig.category,
                    "learning_weight": sig.learning_weight,
                    "occurrence_count": sig.occurrence_count,
                    "first_seen": sig.first_seen.isoformat(),
                    "last_seen": sig.last_seen.isoformat()
                }
                for sig in self.error_signatures
            ],
            "intelligence_data": self.intelligence_data
        }

def main():
    """Command-line interface for error classification."""
    if len(sys.argv) < 2:
        print("Usage: python error_classifier.py <log_file_path> [context_json]")
        sys.exit(1)
    
    log_file_path = sys.argv[1]
    context = {}
    
    if len(sys.argv) > 2:
        try:
            context = json.loads(sys.argv[2])
        except json.JSONDecodeError:
            print("Warning: Invalid context JSON provided")
    
    classifier = PsychoNoirErrorClassifier()
    
    try:
        with open(log_file_path, 'r', encoding='utf-8') as f:
            log_content = f.read()
        
        result = classifier.classify_log_content(log_content, context)
        print(json.dumps(result, indent=2))
        
    except FileNotFoundError:
        print(f"Error: Log file '{log_file_path}' not found")
        sys.exit(1)
    except Exception as e:
        print(f"Classification error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()