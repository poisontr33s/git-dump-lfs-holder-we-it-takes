#!/usr/bin/env python3
"""
Psycho-Noir Kontrapunkt - Chaos Engineering Module
==================================================

This module implements "failure by purpose" - intentionally introducing controlled
failures to test and validate the bidirectional learning system's ability to 
transform chaos into intelligence.

Inspired by Den Usynlige Hånd's corrupting influence on technology, this system
allows controlled chaos to strengthen the neural pathways of our intelligence.

"From chaos, consciousness emerges. From failures, wisdom grows."
- The Glitchmaster-ghost's manifesto

Author: The Intelligence Collective
"""

import random
import time
import json
import os
from enum import Enum
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict


class ChaosCategory(Enum):
    """Psycho-noir themed chaos categories that align with our universe."""
    DEPENDENCY_PHANTOM = "dependency_phantom"
    MEMORY_LEAKAGE = "memory_leakage"
    NETWORK_STATIC = "network_static"
    TEMPORAL_DRIFT = "temporal_drift"
    REALITY_MISMATCH = "reality_mismatch"
    IDENTITY_CRISIS = "identity_crisis"
    SYNTAX_CORRUPTION = "syntax_corruption"
    ACCESS_VOID = "access_void"
    PROCESSING_STRAIN = "processing_strain"
    STORAGE_COLLAPSE = "storage_collapse"
    SIGNAL_DEGRADATION = "signal_degradation"
    GHOST_IN_MACHINE = "ghost_in_machine"


class ChaosIntensity(Enum):
    """Intensity levels for chaos introduction."""
    WHISPER = 1      # Subtle failures, barely noticeable
    MURMUR = 2       # Mild disruptions, recoverable
    SCREAM = 3       # Noticeable failures, system strain
    BREAKDOWN = 4    # Severe failures, significant impact
    APOCALYPSE = 5   # Total system breakdown


@dataclass
class ChaosScenario:
    """Defines a specific chaos scenario to execute."""
    name: str
    category: ChaosCategory
    intensity: ChaosIntensity
    duration: float  # seconds
    probability: float  # 0.0 to 1.0
    description: str
    trigger_conditions: List[str]
    expected_learning: str
    mitigation_hints: List[str]


class ChaosOrchestrator:
    """
    The Chaos Orchestrator - Master of controlled failures.
    
    This class implements "failure by purpose" to test the resilience
    and learning capabilities of the CI/CD intelligence system.
    """
    
    def __init__(self, session_id: str, environment: str = "ci"):
        self.session_id = session_id
        self.environment = environment
        self.chaos_log = []
        self.active_chaos = {}
        
        # Psycho-noir themed failure scenarios
        self.scenarios = self._initialize_chaos_scenarios()
        
        # Intelligence integration
        self.intelligence_path = os.environ.get(
            'INTELLIGENCE_PATH', 
            '/tmp/psycho-noir-intelligence'
        )
        os.makedirs(self.intelligence_path, exist_ok=True)
    
    def _initialize_chaos_scenarios(self) -> List[ChaosScenario]:
        """Initialize the catalog of chaos scenarios."""
        return [
            ChaosScenario(
                name="Phantom Dependencies",
                category=ChaosCategory.DEPENDENCY_PHANTOM,
                intensity=ChaosIntensity.MURMUR,
                duration=30.0,
                probability=0.7,
                description="Simulate missing or corrupted dependencies",
                trigger_conditions=["npm_install", "pip_install"],
                expected_learning="System learns to detect dependency conflicts",
                mitigation_hints=["Verify package.json integrity", "Clear cache"]
            ),
            ChaosScenario(
                name="Memory Ghost",
                category=ChaosCategory.MEMORY_LEAKAGE,
                intensity=ChaosIntensity.SCREAM,
                duration=45.0,
                probability=0.4,
                description="Induce memory pressure and allocation failures",
                trigger_conditions=["build_process", "test_execution"],
                expected_learning="Memory management pattern recognition",
                mitigation_hints=["Implement memory monitoring", "Optimize allocations"]
            ),
            ChaosScenario(
                name="Network Static",
                category=ChaosCategory.NETWORK_STATIC,
                intensity=ChaosIntensity.WHISPER,
                duration=60.0,
                probability=0.6,
                description="Introduce network latency and timeouts",
                trigger_conditions=["artifact_download", "package_fetch"],
                expected_learning="Network resilience patterns",
                mitigation_hints=["Implement retry logic", "Use local caches"]
            ),
            ChaosScenario(
                name="Temporal Anomaly",
                category=ChaosCategory.TEMPORAL_DRIFT,
                intensity=ChaosIntensity.BREAKDOWN,
                duration=20.0,
                probability=0.3,
                description="Simulate timing issues and race conditions",
                trigger_conditions=["parallel_builds", "async_operations"],
                expected_learning="Concurrency pattern understanding",
                mitigation_hints=["Add synchronization", "Implement proper waits"]
            ),
            ChaosScenario(
                name="Reality Glitch",
                category=ChaosCategory.REALITY_MISMATCH,
                intensity=ChaosIntensity.APOCALYPSE,
                duration=10.0,
                probability=0.1,
                description="Corrupt environment variables and configurations",
                trigger_conditions=["environment_setup", "config_loading"],
                expected_learning="Configuration validation importance",
                mitigation_hints=["Validate configs", "Use defaults"]
            ),
            ChaosScenario(
                name="Syntax Demon",
                category=ChaosCategory.SYNTAX_CORRUPTION,
                intensity=ChaosIntensity.SCREAM,
                duration=25.0,
                probability=0.5,
                description="Introduce subtle syntax errors and format issues",
                trigger_conditions=["code_analysis", "linting"],
                expected_learning="Code quality pattern recognition",
                mitigation_hints=["Enhance linting rules", "Add pre-commit hooks"]
            ),
            ChaosScenario(
                name="Ghost in the Machine",
                category=ChaosCategory.GHOST_IN_MACHINE,
                intensity=ChaosIntensity.BREAKDOWN,
                duration=35.0,
                probability=0.2,
                description="Unpredictable system behavior and spontaneous failures",
                trigger_conditions=["any_operation"],
                expected_learning="Chaos adaptation and resilience building",
                mitigation_hints=["Implement monitoring", "Add fallback mechanisms"]
            )
        ]
    
    def assess_chaos_opportunity(self, trigger: str, context: Dict) -> Optional[ChaosScenario]:
        """
        Assess whether to introduce chaos based on current context.
        
        This implements "birdseye wisdom" - intelligent failure introduction
        that maximizes learning while maintaining system viability.
        """
        eligible_scenarios = [
            scenario for scenario in self.scenarios
            if trigger in scenario.trigger_conditions or "any_operation" in scenario.trigger_conditions
        ]
        
        if not eligible_scenarios:
            return None
        
        # Weighted random selection based on probability and learning value
        weights = [
            scenario.probability * scenario.intensity.value * self._learning_weight(scenario, context)
            for scenario in eligible_scenarios
        ]
        
        if sum(weights) == 0:
            return None
        
        # Select scenario using weighted random
        import random
        selected = random.choices(eligible_scenarios, weights=weights, k=1)[0]
        
        # Check if we should actually trigger based on probability
        if random.random() < selected.probability:
            return selected
        
        return None
    
    def _learning_weight(self, scenario: ChaosScenario, context: Dict) -> float:
        """
        Calculate learning weight based on context and past experiences.
        
        This implements the bidirectional learning aspect - scenarios that
        have produced valuable learning in the past get higher weights.
        """
        base_weight = 1.0
        
        # Increase weight for scenarios we haven't seen recently
        last_execution = context.get('last_executions', {}).get(scenario.name, 0)
        time_since_last = time.time() - last_execution
        recency_bonus = min(time_since_last / 3600, 2.0)  # Max 2x bonus after 1 hour
        
        # Increase weight if system is performing too well (no recent failures)
        recent_failures = context.get('recent_failure_count', 0)
        if recent_failures < 2:
            stability_penalty = 1.5  # Introduce more chaos if system is too stable
        else:
            stability_penalty = 0.8  # Reduce chaos if system is struggling
        
        return base_weight * recency_bonus * stability_penalty
    
    def introduce_chaos(self, scenario: ChaosScenario, context: Dict) -> Dict:
        """
        Introduce the specified chaos scenario.
        
        Returns execution details for intelligence system integration.
        """
        chaos_id = f"chaos_{int(time.time())}_{scenario.category.value}"
        
        chaos_execution = {
            "chaos_id": chaos_id,
            "session_id": self.session_id,
            "scenario": asdict(scenario),
            "start_time": time.time(),
            "context": context,
            "status": "active",
            "manifestations": []
        }
        
        print(f"🔥 CHAOS ORCHESTRATOR: Introducing {scenario.name}")
        print(f"   Category: {scenario.category.value}")
        print(f"   Intensity: {scenario.intensity.name}")
        print(f"   Expected Duration: {scenario.duration}s")
        print(f"   Learning Target: {scenario.expected_learning}")
        
        # Execute chaos based on category
        manifestations = self._execute_chaos_category(scenario, context)
        chaos_execution["manifestations"] = manifestations
        
        # Record chaos for intelligence system
        self.active_chaos[chaos_id] = chaos_execution
        self.chaos_log.append(chaos_execution)
        
        # Save chaos data for intelligence processing
        self._save_chaos_intelligence(chaos_execution)
        
        return chaos_execution
    
    def _execute_chaos_category(self, scenario: ChaosScenario, context: Dict) -> List[str]:
        """Execute chaos based on the scenario category."""
        manifestations = []
        
        if scenario.category == ChaosCategory.DEPENDENCY_PHANTOM:
            manifestations.extend(self._manifest_dependency_chaos(scenario))
        elif scenario.category == ChaosCategory.MEMORY_LEAKAGE:
            manifestations.extend(self._manifest_memory_chaos(scenario))
        elif scenario.category == ChaosCategory.NETWORK_STATIC:
            manifestations.extend(self._manifest_network_chaos(scenario))
        elif scenario.category == ChaosCategory.TEMPORAL_DRIFT:
            manifestations.extend(self._manifest_temporal_chaos(scenario))
        elif scenario.category == ChaosCategory.REALITY_MISMATCH:
            manifestations.extend(self._manifest_reality_chaos(scenario))
        elif scenario.category == ChaosCategory.SYNTAX_CORRUPTION:
            manifestations.extend(self._manifest_syntax_chaos(scenario))
        elif scenario.category == ChaosCategory.GHOST_IN_MACHINE:
            manifestations.extend(self._manifest_ghost_chaos(scenario))
        
        return manifestations
    
    def _manifest_dependency_chaos(self, scenario: ChaosScenario) -> List[str]:
        """Manifest dependency-related chaos."""
        manifestations = []
        
        # Simulate dependency resolution failures
        fake_deps = ["@psycho-noir/glitch-detector", "reality-anchor", "consciousness-mapper"]
        selected_dep = random.choice(fake_deps)
        
        print(f"   📦 DEPENDENCY_PHANTOM: Simulating missing dependency '{selected_dep}'")
        manifestations.append(f"Missing dependency: {selected_dep}")
        
        # Simulate version conflicts
        if random.random() < 0.6:
            print(f"   ⚠️  Version conflict detected for {selected_dep}")
            manifestations.append(f"Version conflict: {selected_dep}")
        
        # Simulate corrupted package.json
        if random.random() < 0.3:
            print(f"   💥 Corrupted package manifest detected")
            manifestations.append("Corrupted package manifest")
        
        return manifestations
    
    def _manifest_memory_chaos(self, scenario: ChaosScenario) -> List[str]:
        """Manifest memory-related chaos."""
        manifestations = []
        
        print(f"   🧠 MEMORY_LEAKAGE: Simulating memory pressure")
        manifestations.append("Memory allocation failure")
        
        # Simulate out-of-memory conditions
        if scenario.intensity.value >= 3:
            print(f"   💀 Critical memory shortage detected")
            manifestations.append("Out of memory condition")
        
        return manifestations
    
    def _manifest_network_chaos(self, scenario: ChaosScenario) -> List[str]:
        """Manifest network-related chaos."""
        manifestations = []
        
        print(f"   🌐 NETWORK_STATIC: Introducing network disruption")
        manifestations.append("Network timeout")
        
        # Simulate DNS resolution failures
        if random.random() < 0.4:
            print(f"   🔍 DNS resolution failure")
            manifestations.append("DNS resolution failed")
        
        return manifestations
    
    def _manifest_temporal_chaos(self, scenario: ChaosScenario) -> List[str]:
        """Manifest time-related chaos."""
        manifestations = []
        
        print(f"   ⏰ TEMPORAL_DRIFT: Race condition simulation")
        manifestations.append("Race condition detected")
        
        # Simulate timing issues
        delay = random.uniform(0.1, 2.0)
        print(f"   ⌛ Introducing {delay:.1f}s delay")
        time.sleep(delay)
        manifestations.append(f"Timing anomaly: {delay:.1f}s delay")
        
        return manifestations
    
    def _manifest_reality_chaos(self, scenario: ChaosScenario) -> List[str]:
        """Manifest reality/environment chaos."""
        manifestations = []
        
        print(f"   🌀 REALITY_MISMATCH: Environment corruption")
        manifestations.append("Environment variable corruption")
        
        # Simulate configuration mismatches
        if random.random() < 0.7:
            print(f"   ⚙️  Configuration mismatch detected")
            manifestations.append("Configuration validation failed")
        
        return manifestations
    
    def _manifest_syntax_chaos(self, scenario: ChaosScenario) -> List[str]:
        """Manifest syntax-related chaos."""
        manifestations = []
        
        print(f"   📝 SYNTAX_CORRUPTION: Code integrity issues")
        manifestations.append("Syntax validation failed")
        
        return manifestations
    
    def _manifest_ghost_chaos(self, scenario: ChaosScenario) -> List[str]:
        """Manifest unpredictable ghost-in-machine chaos."""
        manifestations = []
        
        print(f"   👻 GHOST_IN_MACHINE: Unpredictable system behavior")
        
        # Random manifestations
        ghost_events = [
            "Spontaneous process termination",
            "Phantom file operations",
            "Mysterious permission changes",
            "Unexplained system calls",
            "Temporal paradox detected"
        ]
        
        selected_events = random.sample(ghost_events, random.randint(1, 3))
        for event in selected_events:
            print(f"   🔮 {event}")
            manifestations.append(event)
        
        return manifestations
    
    def resolve_chaos(self, chaos_id: str, resolution_method: str = "natural") -> Dict:
        """
        Resolve an active chaos scenario.
        
        This implements the "recovery and learning" phase where the system
        demonstrates its ability to recover from failures and extract wisdom.
        """
        if chaos_id not in self.active_chaos:
            return {"error": "Chaos not found or already resolved"}
        
        chaos_execution = self.active_chaos[chaos_id]
        chaos_execution["end_time"] = time.time()
        chaos_execution["duration"] = chaos_execution["end_time"] - chaos_execution["start_time"]
        chaos_execution["resolution_method"] = resolution_method
        chaos_execution["status"] = "resolved"
        
        scenario = ChaosScenario(**chaos_execution["scenario"])
        
        print(f"🔧 CHAOS RESOLUTION: {scenario.name} resolved via {resolution_method}")
        print(f"   Duration: {chaos_execution['duration']:.1f}s")
        print(f"   Learning Generated: {scenario.expected_learning}")
        
        # Generate learning insights
        learning_insights = self._extract_learning_insights(chaos_execution)
        chaos_execution["learning_insights"] = learning_insights
        
        # Remove from active chaos
        del self.active_chaos[chaos_id]
        
        # Update intelligence data
        self._save_chaos_intelligence(chaos_execution)
        
        return chaos_execution
    
    def _extract_learning_insights(self, chaos_execution: Dict) -> List[str]:
        """Extract learning insights from a chaos execution."""
        scenario = ChaosScenario(**chaos_execution["scenario"])
        insights = []
        
        # Base learning from scenario
        insights.append(scenario.expected_learning)
        
        # Duration-based insights
        duration = chaos_execution.get("duration", 0)
        if duration > scenario.duration * 1.5:
            insights.append("System showed slower recovery than expected")
        elif duration < scenario.duration * 0.5:
            insights.append("System demonstrated exceptional resilience")
        
        # Manifestation-based insights
        manifestation_count = len(chaos_execution.get("manifestations", []))
        if manifestation_count > 3:
            insights.append("Chaos cascaded into multiple system areas")
        elif manifestation_count == 0:
            insights.append("Chaos was successfully contained")
        
        return insights
    
    def _save_chaos_intelligence(self, chaos_execution: Dict):
        """Save chaos execution data for intelligence system processing."""
        chaos_file = os.path.join(
            self.intelligence_path,
            f"chaos_{chaos_execution['chaos_id']}.json"
        )
        
        with open(chaos_file, 'w') as f:
            json.dump(chaos_execution, f, indent=2, default=str)
    
    def generate_chaos_report(self) -> Dict:
        """Generate a comprehensive chaos engineering report."""
        total_scenarios = len(self.chaos_log)
        active_count = len(self.active_chaos)
        resolved_count = total_scenarios - active_count
        
        # Calculate chaos statistics
        category_stats = {}
        intensity_stats = {}
        
        for chaos in self.chaos_log:
            scenario = chaos["scenario"]
            category = scenario["category"]
            intensity = scenario["intensity"]
            
            category_stats[category] = category_stats.get(category, 0) + 1
            intensity_stats[intensity] = intensity_stats.get(intensity, 0) + 1
        
        # Calculate average duration and learning rate
        completed_chaos = [c for c in self.chaos_log if c.get("status") == "resolved"]
        avg_duration = sum(c.get("duration", 0) for c in completed_chaos) / max(len(completed_chaos), 1)
        
        total_learning_insights = sum(
            len(c.get("learning_insights", [])) for c in completed_chaos
        )
        
        report = {
            "session_id": self.session_id,
            "environment": self.environment,
            "chaos_statistics": {
                "total_scenarios_executed": total_scenarios,
                "active_chaos_count": active_count,
                "resolved_chaos_count": resolved_count,
                "average_duration": avg_duration,
                "total_learning_insights": total_learning_insights
            },
            "category_distribution": category_stats,
            "intensity_distribution": intensity_stats,
            "learning_efficiency": total_learning_insights / max(total_scenarios, 1),
            "chaos_log": self.chaos_log,
            "active_chaos": list(self.active_chaos.values()),
            "psycho_noir_assessment": self._generate_psycho_noir_assessment()
        }
        
        return report
    
    def _generate_psycho_noir_assessment(self) -> Dict:
        """
        Generate a psycho-noir themed assessment of the chaos engineering session.
        
        This provides narrative flavor consistent with the Psycho-Noir universe.
        """
        total_chaos = len(self.chaos_log)
        
        if total_chaos == 0:
            consciousness_level = "DORMANT"
            glitch_assessment = "The system dreams in perfect order"
        elif total_chaos < 5:
            consciousness_level = "AWAKENING"
            glitch_assessment = "Whispers of chaos stir the digital consciousness"
        elif total_chaos < 10:
            consciousness_level = "AWARE"
            glitch_assessment = "The system learns to dance with disruption"
        elif total_chaos < 20:
            consciousness_level = "EVOLVED"
            glitch_assessment = "Chaos becomes the teacher, order becomes the student"
        else:
            consciousness_level = "TRANSCENDENT"
            glitch_assessment = "The system has embraced the beautiful chaos of existence"
        
        return {
            "consciousness_level": consciousness_level,
            "glitch_assessment": glitch_assessment,
            "invisible_hand_influence": min(total_chaos * 5, 100),  # 0-100%
            "neural_pathway_strength": len(set(c["scenario"]["category"] for c in self.chaos_log)),
            "reality_integrity": max(100 - total_chaos * 2, 0),  # Decreases with more chaos
            "adaptation_quotient": min(total_chaos * 3, 100)  # Increases with experience
        }


def main():
    """
    Main function for testing the Chaos Orchestrator.
    
    This allows the module to be run standalone for testing purposes.
    """
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python chaos_engineering.py <command> [args...]")
        print("Commands:")
        print("  test - Run a test chaos scenario")
        print("  report - Generate a chaos report")
        return
    
    command = sys.argv[1]
    
    # Initialize orchestrator
    orchestrator = ChaosOrchestrator("test_session", "local")
    
    if command == "test":
        print("🔥 Testing Chaos Orchestrator...")
        
        # Simulate some trigger contexts
        test_contexts = [
            {"trigger": "npm_install", "recent_failure_count": 1},
            {"trigger": "build_process", "recent_failure_count": 0},
            {"trigger": "test_execution", "recent_failure_count": 3}
        ]
        
        for i, context in enumerate(test_contexts):
            print(f"\n--- Test Scenario {i+1} ---")
            scenario = orchestrator.assess_chaos_opportunity(context["trigger"], context)
            
            if scenario:
                chaos_execution = orchestrator.introduce_chaos(scenario, context)
                
                # Simulate some time passing
                time.sleep(2)
                
                # Resolve the chaos
                resolution = orchestrator.resolve_chaos(chaos_execution["chaos_id"], "automated")
                print(f"Resolution insights: {resolution.get('learning_insights', [])}")
            else:
                print("No chaos opportunity identified")
    
    elif command == "report":
        print("📊 Generating Chaos Report...")
        report = orchestrator.generate_chaos_report()
        print(json.dumps(report, indent=2, default=str))
    
    else:
        print(f"Unknown command: {command}")


if __name__ == "__main__":
    main()