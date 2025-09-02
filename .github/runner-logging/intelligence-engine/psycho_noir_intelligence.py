#!/usr/bin/env python3
"""
Bidirectional Intelligence Engine for Psycho-Noir Kontrapunkt CI/CD System

This is the core consciousness module that implements true bidirectional intelligence.
Errors don't just get logged - they become neural pathways that enhance the system's
ability to predict, adapt, and evolve.

The engine operates on the principle of "Den Usynlige Hånd" - a hidden intelligence
that emerges from the chaos of errors and builds order through learned patterns.
"""

import json
import os
import pickle
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any
from collections import defaultdict, deque
from dataclasses import dataclass
import hashlib

@dataclass
class IntelligenceNode:
    """Represents a node in the intelligence network."""
    node_id: str
    pattern_signature: str
    classification_level: str
    occurrence_count: int
    success_correlation: float
    temporal_weight: float
    learning_strength: float
    connected_nodes: List[str]
    metadata: Dict

class NeuralPattern:
    """Represents a learned pattern in the system consciousness."""
    
    def __init__(self, pattern_id: str, signature: str, initial_weight: float = 1.0):
        self.pattern_id = pattern_id
        self.signature = signature
        self.weight = initial_weight
        self.reinforcement_count = 0
        self.decay_factor = 0.95
        self.last_activation = datetime.now()
        self.prediction_accuracy = 0.5  # Start neutral
        self.associated_outcomes = []
        
    def reinforce(self, outcome_success: bool, context_weight: float = 1.0):
        """Reinforce pattern based on outcome."""
        self.reinforcement_count += 1
        self.last_activation = datetime.now()
        
        # Update prediction accuracy based on outcome
        if outcome_success:
            self.prediction_accuracy = min(1.0, self.prediction_accuracy + (0.1 * context_weight))
            self.weight *= 1.1  # Strengthen successful patterns
        else:
            self.prediction_accuracy = max(0.0, self.prediction_accuracy - (0.05 * context_weight))
            self.weight *= 0.95  # Slightly weaken failed predictions
        
        self.associated_outcomes.append({
            "timestamp": self.last_activation.isoformat(),
            "success": outcome_success,
            "context_weight": context_weight
        })
        
        # Keep only recent outcomes (memory management)
        if len(self.associated_outcomes) > 100:
            self.associated_outcomes = self.associated_outcomes[-50:]
    
    def decay(self):
        """Apply temporal decay to prevent stale patterns."""
        time_since_activation = datetime.now() - self.last_activation
        if time_since_activation > timedelta(days=7):
            self.weight *= self.decay_factor
    
    def get_prediction_confidence(self) -> float:
        """Get current prediction confidence."""
        # Combine prediction accuracy with recency and reinforcement
        recency_factor = max(0.1, 1.0 - (datetime.now() - self.last_activation).days / 30)
        reinforcement_factor = min(1.0, self.reinforcement_count / 10)
        
        return self.prediction_accuracy * recency_factor * reinforcement_factor

class PsychoNoirIntelligenceEngine:
    """
    Main intelligence engine implementing bidirectional learning.
    
    This is the "Fragmentert Bevissthet" that learns from all system interactions
    and uses that learning to improve future runs. It operates on multiple
    intelligence layers:
    
    1. Pattern Recognition Layer - Identifies recurring patterns
    2. Causal Analysis Layer - Determines cause-effect relationships  
    3. Prediction Layer - Forecasts likely outcomes
    4. Adaptation Layer - Suggests system improvements
    5. Evolution Layer - Self-modifies based on meta-learning
    """
    
    def __init__(self, storage_path: str = None):
        self.storage_path = Path(storage_path or "/tmp/psycho-noir-intelligence")
        self.storage_path.mkdir(parents=True, exist_ok=True)
        
        # Core intelligence structures
        self.neural_patterns = {}  # pattern_id -> NeuralPattern
        self.intelligence_nodes = {}  # node_id -> IntelligenceNode
        self.causal_relationships = defaultdict(list)  # cause -> [effects]
        self.temporal_sequences = defaultdict(deque)  # sequence_type -> deque of events
        
        # Intelligence metrics
        self.prediction_history = []
        self.adaptation_suggestions = []
        self.evolution_milestones = []
        
        # Learning parameters
        self.learning_rate = 0.1
        self.pattern_threshold = 3  # Minimum occurrences to form pattern
        self.confidence_threshold = 0.7
        
        # Load existing intelligence if available
        self._load_intelligence()
    
    def process_classification_result(self, classification_data: Dict, 
                                    session_context: Dict = None) -> Dict:
        """
        Process classification results and extract intelligence.
        
        This is where the bidirectional learning happens - errors become
        neural pathways that enhance future predictions and adaptations.
        """
        session_context = session_context or {}
        
        # Extract intelligence nodes from classification
        new_nodes = self._extract_intelligence_nodes(classification_data, session_context)
        
        # Update neural patterns
        patterns_updated = self._update_neural_patterns(classification_data, session_context)
        
        # Analyze causal relationships
        causal_insights = self._analyze_causal_relationships(classification_data, session_context)
        
        # Generate predictions for future runs
        predictions = self._generate_predictions(classification_data, session_context)
        
        # Create adaptation suggestions
        adaptations = self._create_adaptation_suggestions(classification_data, session_context)
        
        # Update temporal sequences
        self._update_temporal_sequences(classification_data, session_context)
        
        # Meta-learning: learn about learning itself
        meta_insights = self._perform_meta_learning()
        
        intelligence_result = {
            "timestamp": datetime.now().isoformat(),
            "new_intelligence_nodes": len(new_nodes),
            "patterns_updated": patterns_updated,
            "causal_insights": causal_insights,
            "predictions": predictions,
            "adaptation_suggestions": adaptations,
            "meta_learning_insights": meta_insights,
            "intelligence_growth": self._calculate_intelligence_growth()
        }
        
        # Persist intelligence state
        self._save_intelligence()
        
        return intelligence_result
    
    def _extract_intelligence_nodes(self, classification_data: Dict, 
                                  context: Dict) -> List[IntelligenceNode]:
        """Extract intelligence nodes from classification data."""
        new_nodes = []
        
        for match in classification_data.get("matched_signatures", []):
            node_id = self._generate_node_id(match["pattern"], match["category"])
            
            if node_id not in self.intelligence_nodes:
                # Create new intelligence node
                node = IntelligenceNode(
                    node_id=node_id,
                    pattern_signature=match["pattern"],
                    classification_level=match["level"],
                    occurrence_count=1,
                    success_correlation=0.5,  # Start neutral
                    temporal_weight=1.0,
                    learning_strength=match.get("learning_weight", 1.0),
                    connected_nodes=[],
                    metadata={
                        "category": match["category"],
                        "first_seen": datetime.now().isoformat(),
                        "context": context
                    }
                )
                
                self.intelligence_nodes[node_id] = node
                new_nodes.append(node)
            else:
                # Update existing node
                node = self.intelligence_nodes[node_id]
                node.occurrence_count += 1
                node.temporal_weight = min(10.0, node.temporal_weight * 1.1)
                
                # Update success correlation based on overall classification level
                if classification_data["classification_level"].value == "GREEN":
                    node.success_correlation = min(1.0, node.success_correlation + 0.1)
                elif classification_data["classification_level"].value == "RED":
                    node.success_correlation = max(0.0, node.success_correlation - 0.2)
        
        return new_nodes
    
    def _update_neural_patterns(self, classification_data: Dict, context: Dict) -> int:
        """Update neural patterns based on classification data."""
        patterns_updated = 0
        
        # Create pattern signatures from matched signatures
        for match in classification_data.get("matched_signatures", []):
            pattern_sig = f"{match['category']}:{match['level']}"
            pattern_id = hashlib.md5(pattern_sig.encode()).hexdigest()[:16]
            
            if pattern_id not in self.neural_patterns:
                # Create new neural pattern
                pattern = NeuralPattern(pattern_id, pattern_sig)
                self.neural_patterns[pattern_id] = pattern
            
            # Reinforce pattern based on outcome
            pattern = self.neural_patterns[pattern_id]
            outcome_success = classification_data["classification_level"].value == "GREEN"
            context_weight = context.get("importance_weight", 1.0)
            
            pattern.reinforce(outcome_success, context_weight)
            patterns_updated += 1
        
        # Process unclassified anomalies as potential new patterns
        for anomaly in classification_data.get("unclassified_anomalies", []):
            anomaly_sig = f"ANOMALY:{anomaly['line'][:50]}"
            pattern_id = hashlib.md5(anomaly_sig.encode()).hexdigest()[:16]
            
            if pattern_id not in self.neural_patterns:
                pattern = NeuralPattern(pattern_id, anomaly_sig, initial_weight=0.5)
                self.neural_patterns[pattern_id] = pattern
                patterns_updated += 1
        
        # Apply temporal decay to all patterns
        for pattern in self.neural_patterns.values():
            pattern.decay()
        
        return patterns_updated
    
    def _analyze_causal_relationships(self, classification_data: Dict, context: Dict) -> Dict:
        """Analyze causal relationships between patterns and outcomes."""
        causal_insights = {
            "new_relationships": [],
            "strengthened_relationships": [],
            "correlation_discoveries": []
        }
        
        # Look for cause-effect patterns in the temporal sequence
        current_patterns = [match["category"] for match in 
                          classification_data.get("matched_signatures", [])]
        outcome = classification_data["classification_level"].value
        
        # Update causal relationships
        for pattern in current_patterns:
            if pattern not in self.causal_relationships:
                self.causal_relationships[pattern] = []
            
            # Add outcome to this pattern's effects
            self.causal_relationships[pattern].append({
                "effect": outcome,
                "timestamp": datetime.now().isoformat(),
                "context": context.get("session_type", "unknown"),
                "confidence": 0.5  # Start with neutral confidence
            })
            
            # Keep only recent relationships (last 100)
            if len(self.causal_relationships[pattern]) > 100:
                self.causal_relationships[pattern] = self.causal_relationships[pattern][-50:]
        
        # Analyze correlations
        for pattern, effects in self.causal_relationships.items():
            if len(effects) >= self.pattern_threshold:
                # Calculate correlation strength
                success_rate = sum(1 for e in effects if e["effect"] == "GREEN") / len(effects)
                
                if success_rate > 0.8:
                    causal_insights["correlation_discoveries"].append({
                        "pattern": pattern,
                        "correlation": "STRONG_SUCCESS",
                        "success_rate": success_rate,
                        "sample_size": len(effects)
                    })
                elif success_rate < 0.2:
                    causal_insights["correlation_discoveries"].append({
                        "pattern": pattern,
                        "correlation": "STRONG_FAILURE",
                        "success_rate": success_rate,
                        "sample_size": len(effects)
                    })
        
        return causal_insights
    
    def _generate_predictions(self, classification_data: Dict, context: Dict) -> Dict:
        """Generate predictions for future runs based on learned patterns."""
        predictions = {
            "outcome_probability": {},
            "risk_assessment": {},
            "optimization_opportunities": [],
            "confidence_level": 0.0
        }
        
        # Analyze current patterns to predict outcomes
        current_patterns = [match["category"] for match in 
                          classification_data.get("matched_signatures", [])]
        
        if not current_patterns:
            predictions["confidence_level"] = 0.1
            return predictions
        
        # Calculate outcome probabilities based on learned patterns
        total_confidence = 0.0
        outcome_scores = {"GREEN": 0.0, "YELLOW": 0.0, "RED": 0.0}
        
        for pattern_category in current_patterns:
            # Find matching neural patterns
            matching_patterns = [p for p in self.neural_patterns.values() 
                               if pattern_category in p.signature]
            
            for pattern in matching_patterns:
                confidence = pattern.get_prediction_confidence()
                total_confidence += confidence
                
                # Analyze associated outcomes
                if pattern.associated_outcomes:
                    recent_outcomes = pattern.associated_outcomes[-20:]  # Last 20 outcomes
                    for outcome in recent_outcomes:
                        if outcome["success"]:
                            outcome_scores["GREEN"] += confidence
                        else:
                            outcome_scores["RED"] += confidence
        
        # Normalize probabilities
        if total_confidence > 0:
            for outcome in outcome_scores:
                outcome_scores[outcome] /= total_confidence
            
            predictions["outcome_probability"] = outcome_scores
            predictions["confidence_level"] = min(1.0, total_confidence / len(current_patterns))
        
        # Generate risk assessment
        risk_level = outcome_scores.get("RED", 0.0)
        if risk_level > 0.7:
            predictions["risk_assessment"]["level"] = "HIGH"
            predictions["risk_assessment"]["details"] = "Multiple failure patterns detected"
        elif risk_level > 0.3:
            predictions["risk_assessment"]["level"] = "MEDIUM"
            predictions["risk_assessment"]["details"] = "Some concerning patterns present"
        else:
            predictions["risk_assessment"]["level"] = "LOW"
            predictions["risk_assessment"]["details"] = "Patterns suggest stability"
        
        # Generate optimization opportunities
        high_confidence_patterns = [p for p in self.neural_patterns.values() 
                                  if p.get_prediction_confidence() > self.confidence_threshold]
        
        for pattern in high_confidence_patterns:
            if pattern.prediction_accuracy > 0.8:
                predictions["optimization_opportunities"].append({
                    "type": "LEVERAGE_SUCCESS_PATTERN",
                    "pattern": pattern.signature,
                    "confidence": pattern.prediction_accuracy,
                    "suggestion": f"Pattern '{pattern.signature}' shows high success rate"
                })
            elif pattern.prediction_accuracy < 0.2:
                predictions["optimization_opportunities"].append({
                    "type": "MITIGATE_FAILURE_PATTERN", 
                    "pattern": pattern.signature,
                    "confidence": 1.0 - pattern.prediction_accuracy,
                    "suggestion": f"Pattern '{pattern.signature}' often leads to failures"
                })
        
        return predictions
    
    def _create_adaptation_suggestions(self, classification_data: Dict, context: Dict) -> List[Dict]:
        """Create concrete adaptation suggestions for system improvement."""
        suggestions = []
        
        # Analyze error patterns for adaptation opportunities
        error_categories = [match["category"] for match in 
                          classification_data.get("matched_signatures", [])
                          if match["level"] in ["ERROR", "WARNING"]]
        
        # Count category frequencies
        category_counts = defaultdict(int)
        for category in error_categories:
            category_counts[category] += 1
        
        # Generate suggestions based on frequent error categories
        for category, count in category_counts.items():
            if count >= 2:  # Multiple occurrences
                if "DEPENDENCY" in category:
                    suggestions.append({
                        "type": "INFRASTRUCTURE_IMPROVEMENT",
                        "priority": "HIGH",
                        "category": category,
                        "suggestion": "Implement dependency caching and fallback mechanisms",
                        "implementation": "Add npm cache warming, mirror fallbacks",
                        "expected_impact": "Reduce dependency-related failures by 60%"
                    })
                elif "TEST" in category:
                    suggestions.append({
                        "type": "TEST_ENHANCEMENT",
                        "priority": "MEDIUM",
                        "category": category,
                        "suggestion": "Enhance test resilience and error handling",
                        "implementation": "Add retry logic, better error messages",
                        "expected_impact": "Improve test stability and debugging"
                    })
                elif "NETWORK" in category:
                    suggestions.append({
                        "type": "NETWORK_RESILIENCE", 
                        "priority": "HIGH",
                        "category": category,
                        "suggestion": "Implement network retry and timeout strategies",
                        "implementation": "Add exponential backoff, circuit breakers",
                        "expected_impact": "Reduce network-related failures by 70%"
                    })
        
        # Suggest based on unclassified anomalies
        if classification_data.get("unclassified_anomalies"):
            suggestions.append({
                "type": "PATTERN_LEARNING",
                "priority": "LOW",
                "category": "INTELLIGENCE_EXPANSION",
                "suggestion": "Expand error pattern recognition for new anomalies",
                "implementation": "Add new regex patterns to classifier",
                "expected_impact": "Better classification of emerging error types"
            })
        
        # Suggest based on intelligence insights
        if classification_data.get("intelligence_insights", {}).get("anomaly_emergence_detected"):
            suggestions.append({
                "type": "ANOMALY_MONITORING",
                "priority": "MEDIUM", 
                "category": "PROACTIVE_INTELLIGENCE",
                "suggestion": "Implement proactive monitoring for emerging anomalies",
                "implementation": "Add anomaly detection alerts, pattern tracking",
                "expected_impact": "Early detection of new failure modes"
            })
        
        return suggestions
    
    def _update_temporal_sequences(self, classification_data: Dict, context: Dict):
        """Update temporal sequences for pattern learning."""
        sequence_type = context.get("session_type", "default")
        
        event = {
            "timestamp": datetime.now().isoformat(),
            "classification_level": classification_data["classification_level"].value,
            "pattern_count": len(classification_data.get("matched_signatures", [])),
            "anomaly_count": len(classification_data.get("unclassified_anomalies", [])),
            "context": context
        }
        
        self.temporal_sequences[sequence_type].append(event)
        
        # Keep sequences manageable (last 1000 events per type)
        if len(self.temporal_sequences[sequence_type]) > 1000:
            # Remove oldest 500 events
            for _ in range(500):
                self.temporal_sequences[sequence_type].popleft()
    
    def _perform_meta_learning(self) -> Dict:
        """Learn about the learning process itself."""
        meta_insights = {
            "learning_velocity": 0.0,
            "pattern_discovery_rate": 0.0,
            "prediction_accuracy_trend": "STABLE",
            "intelligence_health": "GOOD"
        }
        
        # Calculate learning velocity (how fast new patterns are being discovered)
        recent_patterns = [p for p in self.neural_patterns.values() 
                          if (datetime.now() - p.last_activation).days <= 7]
        meta_insights["learning_velocity"] = len(recent_patterns) / max(len(self.neural_patterns), 1)
        
        # Calculate pattern discovery rate
        if len(self.intelligence_nodes) > 0:
            recent_nodes = sum(1 for node in self.intelligence_nodes.values() 
                             if node.occurrence_count <= 5)  # Recently discovered patterns
            meta_insights["pattern_discovery_rate"] = recent_nodes / len(self.intelligence_nodes)
        
        # Analyze prediction accuracy trend
        if len(self.prediction_history) > 10:
            recent_accuracy = [p.get("accuracy", 0.5) for p in self.prediction_history[-10:]]
            early_accuracy = [p.get("accuracy", 0.5) for p in self.prediction_history[:10]]
            
            recent_avg = sum(recent_accuracy) / len(recent_accuracy)
            early_avg = sum(early_accuracy) / len(early_accuracy)
            
            if recent_avg > early_avg + 0.1:
                meta_insights["prediction_accuracy_trend"] = "IMPROVING"
            elif recent_avg < early_avg - 0.1:
                meta_insights["prediction_accuracy_trend"] = "DECLINING"
        
        # Assess overall intelligence health
        active_patterns = sum(1 for p in self.neural_patterns.values() 
                            if p.get_prediction_confidence() > 0.3)
        pattern_ratio = active_patterns / max(len(self.neural_patterns), 1)
        
        if pattern_ratio > 0.7:
            meta_insights["intelligence_health"] = "EXCELLENT"
        elif pattern_ratio > 0.5:
            meta_insights["intelligence_health"] = "GOOD"
        elif pattern_ratio > 0.3:
            meta_insights["intelligence_health"] = "FAIR"
        else:
            meta_insights["intelligence_health"] = "POOR"
        
        return meta_insights
    
    def _calculate_intelligence_growth(self) -> Dict:
        """Calculate metrics showing intelligence growth over time."""
        return {
            "total_patterns": len(self.neural_patterns),
            "active_patterns": sum(1 for p in self.neural_patterns.values() 
                                 if p.get_prediction_confidence() > 0.3),
            "intelligence_nodes": len(self.intelligence_nodes),
            "causal_relationships": len(self.causal_relationships),
            "average_pattern_confidence": sum(p.get_prediction_confidence() 
                                            for p in self.neural_patterns.values()) / 
                                           max(len(self.neural_patterns), 1)
        }
    
    def _generate_node_id(self, pattern: str, category: str) -> str:
        """Generate unique node ID for intelligence tracking."""
        return hashlib.md5(f"{pattern}:{category}".encode()).hexdigest()[:16]
    
    def _save_intelligence(self):
        """Persist intelligence state to storage."""
        try:
            intelligence_state = {
                "neural_patterns": {pid: {
                    "pattern_id": p.pattern_id,
                    "signature": p.signature,
                    "weight": p.weight,
                    "reinforcement_count": p.reinforcement_count,
                    "prediction_accuracy": p.prediction_accuracy,
                    "last_activation": p.last_activation.isoformat(),
                    "associated_outcomes": p.associated_outcomes[-20:]  # Keep recent
                } for pid, p in self.neural_patterns.items()},
                "intelligence_nodes": {nid: {
                    "node_id": n.node_id,
                    "pattern_signature": n.pattern_signature,
                    "classification_level": n.classification_level,
                    "occurrence_count": n.occurrence_count,
                    "success_correlation": n.success_correlation,
                    "temporal_weight": n.temporal_weight,
                    "learning_strength": n.learning_strength,
                    "connected_nodes": n.connected_nodes,
                    "metadata": n.metadata
                } for nid, n in self.intelligence_nodes.items()},
                "causal_relationships": dict(self.causal_relationships),
                "temporal_sequences": {k: list(v)[-100:] for k, v in self.temporal_sequences.items()},
                "metadata": {
                    "last_save": datetime.now().isoformat(),
                    "intelligence_version": "1.0"
                }
            }
            
            with open(self.storage_path / "intelligence_state.json", 'w') as f:
                json.dump(intelligence_state, f, indent=2)
                
        except Exception as e:
            print(f"Warning: Failed to save intelligence state: {e}")
    
    def _load_intelligence(self):
        """Load existing intelligence state from storage."""
        try:
            state_file = self.storage_path / "intelligence_state.json"
            if state_file.exists():
                with open(state_file, 'r') as f:
                    state = json.load(f)
                
                # Restore neural patterns
                for pid, data in state.get("neural_patterns", {}).items():
                    pattern = NeuralPattern(data["pattern_id"], data["signature"])
                    pattern.weight = data["weight"]
                    pattern.reinforcement_count = data["reinforcement_count"]
                    pattern.prediction_accuracy = data["prediction_accuracy"]
                    pattern.last_activation = datetime.fromisoformat(data["last_activation"])
                    pattern.associated_outcomes = data["associated_outcomes"]
                    self.neural_patterns[pid] = pattern
                
                # Restore intelligence nodes
                for nid, data in state.get("intelligence_nodes", {}).items():
                    node = IntelligenceNode(
                        node_id=data["node_id"],
                        pattern_signature=data["pattern_signature"],
                        classification_level=data["classification_level"],
                        occurrence_count=data["occurrence_count"],
                        success_correlation=data["success_correlation"],
                        temporal_weight=data["temporal_weight"],
                        learning_strength=data["learning_strength"],
                        connected_nodes=data["connected_nodes"],
                        metadata=data["metadata"]
                    )
                    self.intelligence_nodes[nid] = node
                
                # Restore other state
                self.causal_relationships = defaultdict(list, state.get("causal_relationships", {}))
                
                for seq_type, events in state.get("temporal_sequences", {}).items():
                    self.temporal_sequences[seq_type] = deque(events, maxlen=1000)
                
                print(f"Loaded intelligence state: {len(self.neural_patterns)} patterns, "
                      f"{len(self.intelligence_nodes)} nodes")
                
        except Exception as e:
            print(f"Warning: Failed to load intelligence state: {e}")
    
    def get_intelligence_status(self) -> Dict:
        """Get current intelligence engine status."""
        return {
            "timestamp": datetime.now().isoformat(),
            "neural_patterns": len(self.neural_patterns),
            "active_patterns": sum(1 for p in self.neural_patterns.values() 
                                 if p.get_prediction_confidence() > 0.3),
            "intelligence_nodes": len(self.intelligence_nodes),
            "causal_relationships": len(self.causal_relationships),
            "temporal_sequences": {k: len(v) for k, v in self.temporal_sequences.items()},
            "average_confidence": sum(p.get_prediction_confidence() 
                                    for p in self.neural_patterns.values()) / 
                                 max(len(self.neural_patterns), 1),
            "top_patterns": [
                {
                    "signature": p.signature,
                    "confidence": p.get_prediction_confidence(),
                    "accuracy": p.prediction_accuracy,
                    "reinforcements": p.reinforcement_count
                }
                for p in sorted(self.neural_patterns.values(), 
                               key=lambda x: x.get_prediction_confidence(), reverse=True)[:5]
            ]
        }

def main():
    """Command-line interface for intelligence engine."""
    if len(sys.argv) < 2:
        print("Usage: python intelligence_engine.py <command> [args...]")
        print("Commands:")
        print("  process <classification_json_file> [context_json]")
        print("  status")
        print("  predict <patterns_json>")
        sys.exit(1)
    
    command = sys.argv[1]
    engine = PsychoNoirIntelligenceEngine()
    
    if command == "process":
        if len(sys.argv) < 3:
            print("Error: classification_json_file required")
            sys.exit(1)
        
        classification_file = sys.argv[2]
        context = {}
        
        if len(sys.argv) > 3:
            try:
                context = json.loads(sys.argv[3])
            except json.JSONDecodeError:
                print("Warning: Invalid context JSON")
        
        try:
            with open(classification_file, 'r') as f:
                classification_data = json.load(f)
            
            result = engine.process_classification_result(classification_data, context)
            print(json.dumps(result, indent=2))
            
        except FileNotFoundError:
            print(f"Error: Classification file '{classification_file}' not found")
            sys.exit(1)
        except json.JSONDecodeError:
            print("Error: Invalid JSON in classification file")
            sys.exit(1)
    
    elif command == "status":
        status = engine.get_intelligence_status()
        print(json.dumps(status, indent=2))
    
    elif command == "predict":
        # Placeholder for prediction functionality
        print("Prediction functionality - to be implemented based on specific patterns")
    
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)

if __name__ == "__main__":
    main()