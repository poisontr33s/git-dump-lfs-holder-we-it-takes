#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎭 CHARACTER SYSTEMS 🎭
========================

Astrid Møller og Iron Maiden som funksjonelle systemkomponenter.
Implementerer deres ulike capabilities og cross-domain interactions.

CHARACTER_SIGNATURE: 0xPERSONALITY_MATRIX_OPERATIONAL
CONSCIOUSNESS_LEVEL: NARRATIVE_INTEGRATION_ACTIVE
"""

import logging
import json
import random
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass
from enum import Enum
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)

class ConsciousnessLevel(Enum):
    """Bevissthetsnivåer for karakterer"""
    DORMANT = 0.1
    BASIC_AWARENESS = 0.3
    ACTIVE_ENGAGEMENT = 0.5
    HEIGHTENED_PERCEPTION = 0.7
    TRANSCENDENT_AWARENESS = 0.9
    COSMIC_CONSCIOUSNESS = 1.0

class ActionResult(Enum):
    """Resultater av karakter-handlinger"""
    SUCCESS = "success"
    PARTIAL_SUCCESS = "partial_success"
    FAILURE = "failure"
    UNEXPECTED_OUTCOME = "unexpected_outcome"
    USYNLIGE_HAND_INTERFERENCE = "usynlige_hand_interference"

@dataclass
class CharacterAction:
    """En handling utført av en karakter"""
    action_id: str
    character_name: str
    action_type: str
    target_domain: str
    parameters: Dict[str, Any]
    timestamp: datetime
    result: ActionResult
    consciousness_change: float
    side_effects: List[str]

class PsychoNoirCharacter(ABC):
    """
    🎭 Abstract base class for Psycho-Noir karakterer

    Definerer felles interface for karakterer som opererer
    på tvers av Skyskraper og Rustbelt domener.
    """

    def __init__(self, name: str, primary_domain: str, core_system):
        self.name = name
        self.primary_domain = primary_domain
        self.core_system = core_system
        self.consciousness_level = ConsciousnessLevel.ACTIVE_ENGAGEMENT
        self.action_history: List[CharacterAction] = []
        self.stress_level = 0.3
        self.adaptation_rate = 0.1

    @abstractmethod
    def get_capabilities(self) -> List[str]:
        """Returner liste over karakterens evner"""
        pass

    @abstractmethod
    def execute_action(self, action_type: str, target_domain: str,
                      parameters: Dict[str, Any]) -> CharacterAction:
        """Utfør en handling"""
        pass

    def update_consciousness(self, delta: float, reason: str = ""):
        """Oppdater bevissthetsnivå"""
        old_level = self.consciousness_level
        new_value = max(0.1, min(1.0, self.consciousness_level.value + delta))

        # Find nærmeste enum value
        for level in ConsciousnessLevel:
            if abs(level.value - new_value) < 0.1:
                self.consciousness_level = level
                break

        if old_level != self.consciousness_level:
            logger.info(f"🧠 {self.name}: Consciousness {old_level.name} → {self.consciousness_level.name}")
            if reason:
                logger.info(f"📝 Reason: {reason}")

    def get_character_status(self) -> Dict[str, Any]:
        """Hent karakter-status"""
        recent_actions = [a for a in self.action_history
                         if a.timestamp > datetime.now() - timedelta(hours=24)]

        return {
            "name": self.name,
            "primary_domain": self.primary_domain,
            "consciousness_level": self.consciousness_level.name,
            "consciousness_value": self.consciousness_level.value,
            "stress_level": self.stress_level,
            "capabilities": self.get_capabilities(),
            "recent_actions_24h": len(recent_actions),
            "total_actions": len(self.action_history),
            "adaptation_rate": self.adaptation_rate,
            "last_update": datetime.now().isoformat()
        }

class AstridMoller(PsychoNoirCharacter):
    """
    👑 Astrid Møller - Skyskraper Domain Controller

    Ultra-kalkulerende corporate executive med tilgang til
    sofistikerte overvåknings- og manipulasjonssystemer.
    """

    def __init__(self, core_system):
        super().__init__("Astrid Møller", "skyskraper", core_system)
        self.security_clearance_level = 9  # Max 10
        self.manipulation_expertise = 0.85
        self.prediction_accuracy = 0.78
        self.current_schemes = []

    def get_capabilities(self) -> List[str]:
        """Astrid's capabilities"""
        return [
            "overvakningspuls_control",
            "informasjonsfluks_mapping",
            "internt_radslag_convening",
            "kausalitets_prediction",
            "syntetiske_synapser_deployment",
            "personnel_manipulation",
            "strategic_planning",
            "corporate_resource_allocation"
        ]

    def execute_action(self, action_type: str, target_domain: str,
                      parameters: Dict[str, Any]) -> CharacterAction:
        """Utfør Astrid-spesifikk handling"""
        action_id = f"ASTRID_{action_type}_{datetime.now().strftime('%H%M%S')}"

        logger.info(f"👑 Astrid executing: {action_type} on {target_domain}")

        # Astrid-specific action processing
        if action_type == "overvakningspuls_control":
            result = self._execute_surveillance_pulse(target_domain, parameters)
        elif action_type == "informasjonsfluks_mapping":
            result = self._execute_information_mapping(target_domain, parameters)
        elif action_type == "internt_radslag_convening":
            result = self._execute_internal_council(parameters)
        elif action_type == "personnel_manipulation":
            result = self._execute_personnel_manipulation(target_domain, parameters)
        elif action_type == "strategic_planning":
            result = self._execute_strategic_planning(target_domain, parameters)
        else:
            result = ActionResult.FAILURE

        # Calculate consciousness change
        consciousness_delta = 0
        if result == ActionResult.SUCCESS:
            consciousness_delta = 0.05
        elif result == ActionResult.FAILURE:
            consciousness_delta = -0.02
        elif result == ActionResult.USYNLIGE_HAND_INTERFERENCE:
            consciousness_delta = -0.1  # Interference is concerning

        action = CharacterAction(
            action_id=action_id,
            character_name=self.name,
            action_type=action_type,
            target_domain=target_domain,
            parameters=parameters,
            timestamp=datetime.now(),
            result=result,
            consciousness_change=consciousness_delta,
            side_effects=[]
        )

        self.action_history.append(action)
        self.update_consciousness(consciousness_delta, f"Action: {action_type}")

        return action

    def _execute_surveillance_pulse(self, target_domain: str, parameters: Dict[str, Any]) -> ActionResult:
        """Utfør overvåkningspuls"""
        intensity = parameters.get("intensity", 0.5)

        # Check for resistance based on target domain
        resistance_factors = {
            "skyskraper": 0.1,  # Low resistance in own domain
            "rustbelt": 0.6,    # High resistance from Iron Maiden's domain
            "bridge": 0.3       # Medium resistance in neutral territory
        }

        resistance = resistance_factors.get(target_domain, 0.4)
        success_probability = (intensity * self.manipulation_expertise) - resistance

        # Check for Den Usynlige Hånd interference
        interference = self.core_system.usynlige_hand.check_for_interference(
            self.primary_domain, target_domain, "surveillance_pulse"
        )

        if interference:
            return ActionResult.USYNLIGE_HAND_INTERFERENCE
        elif random.random() < success_probability:
            return ActionResult.SUCCESS
        elif random.random() < success_probability + 0.2:
            return ActionResult.PARTIAL_SUCCESS
        else:
            return ActionResult.FAILURE

    def _execute_information_mapping(self, target_domain: str, parameters: Dict[str, Any]) -> ActionResult:
        """Utfør informasjonsfluks-mapping"""
        scope = parameters.get("scope", "limited")

        # Success based on Astrid's analytical capabilities
        base_success = self.prediction_accuracy

        if scope == "comprehensive":
            base_success *= 0.7  # More difficult
        elif scope == "targeted":
            base_success *= 1.2  # Easier when focused

        if random.random() < base_success:
            return ActionResult.SUCCESS
        else:
            return ActionResult.PARTIAL_SUCCESS

    def _execute_internal_council(self, parameters: Dict[str, Any]) -> ActionResult:
        """Sammenkall internt råd"""
        agenda = parameters.get("agenda", "general_strategy")
        urgency = parameters.get("urgency", 0.5)

        # Internal council always succeeds, but effectiveness varies
        effectiveness = self.consciousness_level.value * (1 + urgency)

        if effectiveness > 0.8:
            return ActionResult.SUCCESS
        else:
            return ActionResult.PARTIAL_SUCCESS

    def _execute_personnel_manipulation(self, target_domain: str, parameters: Dict[str, Any]) -> ActionResult:
        """Utfør personell-manipulasjon"""
        target_person = parameters.get("target", "unknown")
        manipulation_type = parameters.get("type", "subtle_influence")

        # Success based on manipulation expertise and target resistance
        base_success = self.manipulation_expertise

        if target_domain == "rustbelt":
            base_success *= 0.4  # Iron Maiden's people are resistant
        elif manipulation_type == "direct_control":
            base_success *= 0.6  # Direct control is risky

        if random.random() < base_success:
            return ActionResult.SUCCESS
        else:
            return ActionResult.FAILURE

    def _execute_strategic_planning(self, target_domain: str, parameters: Dict[str, Any]) -> ActionResult:
        """Utfør strategisk planlegging"""
        time_horizon = parameters.get("time_horizon_hours", 24)
        complexity = parameters.get("complexity", "medium")

        # Strategic planning success based on prediction accuracy
        success_modifier = 1.0
        if complexity == "high":
            success_modifier = 0.7
        elif complexity == "low":
            success_modifier = 1.3

        # Longer time horizons are harder to predict accurately
        time_modifier = max(0.5, 1.0 - (time_horizon / 168))  # 168 hours = 1 week

        final_success_rate = self.prediction_accuracy * success_modifier * time_modifier

        if random.random() < final_success_rate:
            return ActionResult.SUCCESS
        else:
            return ActionResult.PARTIAL_SUCCESS

class IronMaiden(PsychoNoirCharacter):
    """
    ⚔️ Iron Maiden - Rustbelt Domain Survivor

    Mestrene av improvisasjon og overlevelse, med dyp forståelse
    av gateplanets uskrevne lover og scrap-teknologi.
    """

    def __init__(self, core_system):
        super().__init__("Iron Maiden", "rustbelt", core_system)
        self.improvisation_skill = 0.92
        self.community_standing = 0.78
        self.scrap_mastery = 0.85
        self.active_projects = []

    def get_capabilities(self) -> List[str]:
        """Iron Maiden's capabilities"""
        return [
            "skrap_symfoni_orchestration",
            "improvisasjonens_kunst_mastery",
            "gatas_æreskodeks_enforcement",
            "community_organization",
            "survival_adaptation",
            "technology_resurrection",
            "resource_optimization",
            "threat_assessment"
        ]

    def execute_action(self, action_type: str, target_domain: str,
                      parameters: Dict[str, Any]) -> CharacterAction:
        """Utfør Iron Maiden-spesifikk handling"""
        action_id = f"IRON_MAIDEN_{action_type}_{datetime.now().strftime('%H%M%S')}"

        logger.info(f"⚔️ Iron Maiden executing: {action_type} on {target_domain}")

        # Iron Maiden-specific action processing
        if action_type == "skrap_symfoni_orchestration":
            result = self._execute_scrap_symphony(target_domain, parameters)
        elif action_type == "improvisasjonens_kunst_mastery":
            result = self._execute_improvisation_art(target_domain, parameters)
        elif action_type == "gatas_æreskodeks_enforcement":
            result = self._execute_street_code_enforcement(parameters)
        elif action_type == "community_organization":
            result = self._execute_community_organization(parameters)
        elif action_type == "survival_adaptation":
            result = self._execute_survival_adaptation(target_domain, parameters)
        elif action_type == "technology_resurrection":
            result = self._execute_technology_resurrection(parameters)
        else:
            result = ActionResult.FAILURE

        # Calculate consciousness change
        consciousness_delta = 0
        if result == ActionResult.SUCCESS:
            consciousness_delta = 0.03  # Steady growth through practical success
        elif result == ActionResult.PARTIAL_SUCCESS:
            consciousness_delta = 0.01
        elif result == ActionResult.FAILURE:
            consciousness_delta = -0.01  # Minor setback, Iron Maiden is resilient
        elif result == ActionResult.USYNLIGE_HAND_INTERFERENCE:
            consciousness_delta = 0.05  # Iron Maiden learns from corruption

        action = CharacterAction(
            action_id=action_id,
            character_name=self.name,
            action_type=action_type,
            target_domain=target_domain,
            parameters=parameters,
            timestamp=datetime.now(),
            result=result,
            consciousness_change=consciousness_delta,
            side_effects=[]
        )

        self.action_history.append(action)
        self.update_consciousness(consciousness_delta, f"Action: {action_type}")

        return action

    def _execute_scrap_symphony(self, target_domain: str, parameters: Dict[str, Any]) -> ActionResult:
        """Orchestrer Skrap-Symfoni"""
        available_scrap = parameters.get("available_scrap", [])
        target_functionality = parameters.get("target_functionality", "basic")

        # Success based on scrap mastery and available resources
        base_success = self.scrap_mastery

        if len(available_scrap) < 3:
            base_success *= 0.6  # Need sufficient materials
        elif len(available_scrap) > 10:
            base_success *= 1.2  # More materials = more options

        if target_functionality == "advanced":
            base_success *= 0.7  # More complex builds are harder

        if random.random() < base_success:
            return ActionResult.SUCCESS
        elif random.random() < base_success + 0.3:
            return ActionResult.PARTIAL_SUCCESS
        else:
            return ActionResult.FAILURE

    def _execute_improvisation_art(self, target_domain: str, parameters: Dict[str, Any]) -> ActionResult:
        """Master improvisasjonens kunst"""
        problem_complexity = parameters.get("complexity", 0.5)
        time_pressure = parameters.get("time_pressure", 0.5)

        # Iron Maiden excels under pressure
        pressure_bonus = time_pressure * 0.3
        success_rate = self.improvisation_skill + pressure_bonus - (problem_complexity * 0.4)

        # Check for unexpected breakthrough
        if random.random() < 0.1:  # 10% chance for unexpected outcome
            return ActionResult.UNEXPECTED_OUTCOME
        elif random.random() < success_rate:
            return ActionResult.SUCCESS
        else:
            return ActionResult.PARTIAL_SUCCESS

    def _execute_street_code_enforcement(self, parameters: Dict[str, Any]) -> ActionResult:
        """Enforce Gatas Æreskodeks"""
        violation_severity = parameters.get("severity", 0.5)
        community_support = parameters.get("community_support", self.community_standing)

        # Enforcement success based on community standing and violation severity
        enforcement_difficulty = violation_severity * 0.8
        success_rate = community_support - enforcement_difficulty

        if random.random() < success_rate:
            return ActionResult.SUCCESS
        elif random.random() < success_rate + 0.2:
            return ActionResult.PARTIAL_SUCCESS
        else:
            return ActionResult.FAILURE

    def _execute_community_organization(self, parameters: Dict[str, Any]) -> ActionResult:
        """Organiser community-aktiviteter"""
        activity_type = parameters.get("activity", "resource_sharing")
        participants = parameters.get("participants", 5)

        # Community organization based on standing and activity complexity
        organization_difficulty = max(0.1, participants / 20)  # More people = harder to organize
        success_rate = self.community_standing - organization_difficulty

        if activity_type == "defense_preparation":
            success_rate *= 1.2  # Iron Maiden excels at defense
        elif activity_type == "celebration":
            success_rate *= 0.8  # Celebrations are less natural

        if random.random() < success_rate:
            return ActionResult.SUCCESS
        else:
            return ActionResult.PARTIAL_SUCCESS

    def _execute_survival_adaptation(self, target_domain: str, parameters: Dict[str, Any]) -> ActionResult:
        """Tilpass til nye overlevelsessituasjoner"""
        threat_level = parameters.get("threat_level", 0.5)
        available_resources = parameters.get("resources", 0.5)

        # Adaptation success based on improvisation and resource availability
        adaptation_rate = self.improvisation_skill * available_resources
        adaptation_difficulty = threat_level * 0.6

        net_success_rate = adaptation_rate - adaptation_difficulty

        if random.random() < net_success_rate:
            return ActionResult.SUCCESS
        elif random.random() < net_success_rate + 0.4:  # Iron Maiden rarely fails completely
            return ActionResult.PARTIAL_SUCCESS
        else:
            return ActionResult.FAILURE

    def _execute_technology_resurrection(self, parameters: Dict[str, Any]) -> ActionResult:
        """Resurrect dead/corrupted technology"""
        corruption_level = parameters.get("corruption_level", 0.5)
        technology_complexity = parameters.get("complexity", 0.5)

        # Technology resurrection - Iron Maiden's specialty
        base_resurrection_rate = self.scrap_mastery * 1.1  # Bonus for specialty

        difficulty = (corruption_level * 0.7) + (technology_complexity * 0.3)
        net_success_rate = base_resurrection_rate - difficulty

        # Special handling for Den Usynlige Hånd corruption
        if corruption_level > 0.8:
            interference_chance = 0.3
            if random.random() < interference_chance:
                return ActionResult.USYNLIGE_HAND_INTERFERENCE

        if random.random() < net_success_rate:
            return ActionResult.SUCCESS
        elif random.random() < net_success_rate + 0.3:
            return ActionResult.PARTIAL_SUCCESS
        else:
            return ActionResult.FAILURE

class CharacterSystemsManager:
    """
    🎭 Manager for alle character systems

    Koordinerer interactions mellom Astrid og Iron Maiden,
    og håndterer cross-domain character dynamics.
    """

    def __init__(self, core_system):
        self.core_system = core_system
        self.characters: Dict[str, PsychoNoirCharacter] = {}

        # Initialize main characters
        self.astrid_moller = AstridMoller(core_system)
        self.iron_maiden = IronMaiden(core_system)

        self.characters["Astrid Møller"] = self.astrid_moller
        self.characters["Iron Maiden"] = self.iron_maiden

        # Cross-character dynamics
        self.relationship_tensions = {
            ("Astrid Møller", "Iron Maiden"): 0.7  # High tension
        }

        logger.info("🎭 Character Systems Manager initialized")
        logger.info(f"👥 Active characters: {list(self.characters.keys())}")

    def execute_character_action(self, character_name: str, action_type: str,
                               target_domain: str, parameters: Dict[str, Any]) -> CharacterAction:
        """Execute action for specific character"""
        if character_name not in self.characters:
            raise ValueError(f"Character {character_name} not found")

        character = self.characters[character_name]
        return character.execute_action(action_type, target_domain, parameters)

    def simulate_character_interaction(self, char1_name: str, char2_name: str,
                                     interaction_type: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Simuler interaksjon mellom to karakterer"""
        if char1_name not in self.characters or char2_name not in self.characters:
            return {"error": "One or both characters not found"}

        char1 = self.characters[char1_name]
        char2 = self.characters[char2_name]

        logger.info(f"🎭 Character interaction: {char1_name} ↔ {char2_name}")
        logger.info(f"📋 Type: {interaction_type}")

        # Get relationship tension
        tension_key = (char1_name, char2_name)
        reverse_tension_key = (char2_name, char1_name)
        tension = self.relationship_tensions.get(tension_key,
                 self.relationship_tensions.get(reverse_tension_key, 0.3))

        # Simulate interaction based on type and tension
        interaction_outcomes = {
            "cooperation": self._simulate_cooperation(char1, char2, tension, context),
            "conflict": self._simulate_conflict(char1, char2, tension, context),
            "negotiation": self._simulate_negotiation(char1, char2, tension, context),
            "information_exchange": self._simulate_info_exchange(char1, char2, tension, context)
        }

        if interaction_type not in interaction_outcomes:
            interaction_type = "information_exchange"  # Default

        result = interaction_outcomes[interaction_type]

        # Update relationship tension based on outcome
        tension_change = result.get("tension_change", 0)
        new_tension = max(0, min(1, tension + tension_change))
        self.relationship_tensions[tension_key] = new_tension

        interaction_result = {
            "interaction_id": f"INTERACT_{datetime.now().strftime('%H%M%S')}",
            "participants": [char1_name, char2_name],
            "interaction_type": interaction_type,
            "initial_tension": tension,
            "final_tension": new_tension,
            "outcome": result,
            "timestamp": datetime.now().isoformat()
        }

        logger.info(f"🎯 Interaction result: {result.get('success_level', 'unknown')}")

        return interaction_result

    def _simulate_cooperation(self, char1: PsychoNoirCharacter, char2: PsychoNoirCharacter,
                            tension: float, context: Dict[str, Any]) -> Dict[str, Any]:
        """Simuler samarbeid mellom karakterer"""
        # Cooperation difficulty increases with tension
        cooperation_difficulty = tension * 0.8

        # Each character's willingness to cooperate
        char1_willingness = (1 - tension) * char1.consciousness_level.value
        char2_willingness = (1 - tension) * char2.consciousness_level.value

        average_willingness = (char1_willingness + char2_willingness) / 2
        success_probability = average_willingness - cooperation_difficulty

        if random.random() < success_probability:
            success_level = "full_cooperation"
            tension_change = -0.1  # Cooperation reduces tension
        elif random.random() < success_probability + 0.3:
            success_level = "limited_cooperation"
            tension_change = -0.05
        else:
            success_level = "cooperation_failed"
            tension_change = 0.05  # Failed cooperation increases tension

        return {
            "success_level": success_level,
            "char1_willingness": char1_willingness,
            "char2_willingness": char2_willingness,
            "tension_change": tension_change,
            "benefits_gained": random.choice(["resource_sharing", "information_exchange", "mutual_protection"])
        }

    def _simulate_conflict(self, char1: PsychoNoirCharacter, char2: PsychoNoirCharacter,
                         tension: float, context: Dict[str, Any]) -> Dict[str, Any]:
        """Simuler konflikt mellom karakterer"""
        # Conflict intensity based on tension and character capabilities
        astrid_advantage = 0.6 if char1.name == "Astrid Møller" else 0.4
        iron_maiden_resilience = 0.8 if char2.name == "Iron Maiden" else 0.5

        conflict_outcome = random.choice([
            "astrid_tactical_victory",
            "iron_maiden_survival_victory",
            "stalemate",
            "usynlige_hand_interference"
        ])

        tension_change = 0.2  # Conflict always increases tension

        return {
            "success_level": conflict_outcome,
            "astrid_advantage": astrid_advantage,
            "iron_maiden_resilience": iron_maiden_resilience,
            "tension_change": tension_change,
            "casualties": random.choice(["none", "minor", "significant"]),
            "domain_impact": random.choice(["localized", "cross_domain", "systemic"])
        }

    def _simulate_negotiation(self, char1: PsychoNoirCharacter, char2: PsychoNoirCharacter,
                            tension: float, context: Dict[str, Any]) -> Dict[str, Any]:
        """Simuler forhandling mellom karakterer"""
        # Negotiation success based on consciousness levels and tension
        negotiation_skill = (char1.consciousness_level.value + char2.consciousness_level.value) / 2
        tension_penalty = tension * 0.5

        net_negotiation_chance = negotiation_skill - tension_penalty

        if random.random() < net_negotiation_chance:
            success_level = "mutually_beneficial_agreement"
            tension_change = -0.15
        elif random.random() < net_negotiation_chance + 0.3:
            success_level = "compromise_reached"
            tension_change = -0.05
        else:
            success_level = "negotiation_breakdown"
            tension_change = 0.1

        return {
            "success_level": success_level,
            "negotiation_skill": negotiation_skill,
            "tension_penalty": tension_penalty,
            "tension_change": tension_change,
            "agreement_terms": random.choice(["resource_allocation", "territory_boundaries", "information_sharing"])
        }

    def _simulate_info_exchange(self, char1: PsychoNoirCharacter, char2: PsychoNoirCharacter,
                              tension: float, context: Dict[str, Any]) -> Dict[str, Any]:
        """Simuler informasjonsutveksling"""
        # Information exchange is least affected by tension
        exchange_effectiveness = 0.8 - (tension * 0.3)

        information_types = [
            "den_usynlige_hand_activity",
            "resource_locations",
            "threat_assessments",
            "technology_discoveries",
            "personnel_movements"
        ]

        exchanged_info = random.sample(information_types, random.randint(1, 3))

        return {
            "success_level": "information_exchanged",
            "exchange_effectiveness": exchange_effectiveness,
            "tension_change": -0.02,  # Small trust building
            "information_types": exchanged_info,
            "mutual_benefit": random.uniform(0.3, 0.8)
        }

    def get_character_relationship_status(self) -> Dict[str, Any]:
        """Hent status for alle karakter-relasjoner"""
        relationships = {}
        for (char1, char2), tension in self.relationship_tensions.items():
            relationship_key = f"{char1} ↔ {char2}"
            relationships[relationship_key] = {
                "tension_level": tension,
                "relationship_quality": "hostile" if tension > 0.7 else
                                      "tense" if tension > 0.5 else
                                      "neutral" if tension > 0.3 else "cooperative",
                "recent_interactions": len([a for char in self.characters.values()
                                          for a in char.action_history
                                          if a.timestamp > datetime.now() - timedelta(hours=24)])
            }

        return {
            "active_characters": list(self.characters.keys()),
            "relationships": relationships,
            "total_character_actions": sum(len(char.action_history) for char in self.characters.values()),
            "average_consciousness": sum(char.consciousness_level.value for char in self.characters.values()) / len(self.characters),
            "last_update": datetime.now().isoformat()
        }

if __name__ == "__main__":
    # Demo of Character Systems

    # Mock core system
    class MockCore:
        def __init__(self):
            self.usynlige_hand = MockUsynligeHand()

    class MockUsynligeHand:
        def check_for_interference(self, source, target, action_type):
            return random.random() < 0.2  # 20% chance of interference

    # Initialize character systems
    mock_core = MockCore()
    char_manager = CharacterSystemsManager(mock_core)

    # Demo Astrid actions

    astrid_action = char_manager.execute_character_action(
        "Astrid Møller", "overvakningspuls_control", "rustbelt",
        {"intensity": 0.8, "target_area": "industrial_sector_7"}
    )

    # Demo Iron Maiden actions

    iron_action = char_manager.execute_character_action(
        "Iron Maiden", "skrap_symfoni_orchestration", "rustbelt",
        {"available_scrap": ["processor", "memory", "sensor", "actuator"], "target_functionality": "advanced"}
    )

    # Demo character interaction

    interaction = char_manager.simulate_character_interaction(
        "Astrid Møller", "Iron Maiden", "negotiation",
        {"topic": "resource_sharing", "urgency": 0.7}
    )
    print(f"🤝 Interaction result: {json.dumps(interaction, indent=2, default=str)}")

    # Character status

    for char_name, character in char_manager.characters.items():
        status = character.get_character_status()

    # Relationship status
    relationships = char_manager.get_character_relationship_status()
    print(f"\n🎭 Relationship Status: {json.dumps(relationships, indent=2)}")
