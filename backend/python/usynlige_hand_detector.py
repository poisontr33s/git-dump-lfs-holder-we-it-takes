#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🕵️ DEN USYNLIGE HÅND DETECTOR 🕵️
==================================

Oppdager og analyserer skjulte manipulasjoner på tvers av domener.
System for å identifisere, spore og motarbeide Den Usynlige Hånds innflytelse.

DETECTION_SIGNATURE: 0xHIDDEN_MANIPULATION_SCANNER_ACTIVE
PARANOIA_LEVEL: MAXIMUM_VIGILANCE_PROTOCOLS_ENABLED
"""

import logging
import json
import random
import hashlib
import math
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from enum import Enum
from collections import defaultdict

logger = logging.getLogger(__name__)

class ManipulationType(Enum):
    """Typer manipulasjon fra Den Usynlige Hånd"""
    PROBABILITY_DISTORTION = "probability_distortion"
    CAUSAL_INJECTION = "causal_injection"
    MEMORY_ALTERATION = "memory_alteration"
    DECISION_INFLUENCE = "decision_influence"
    REALITY_GLITCH = "reality_glitch"
    SYSTEM_SUBVERSION = "system_subversion"

class ThreatLevel(Enum):
    """Trusselsnivåer for detekterte anomalier"""
    BENIGN = 0.2
    SUSPICIOUS = 0.4
    CONCERNING = 0.6
    DANGEROUS = 0.8
    CATASTROPHIC = 1.0

@dataclass
class AnomalyPattern:
    """Mønster av anomali/manipulasjon"""
    pattern_id: str
    manipulation_type: ManipulationType
    signature: str
    frequency: float
    domains_affected: List[str]
    first_detected: datetime
    last_detected: datetime
    confidence_level: float

@dataclass
class ManipulationEvent:
    """En enkelt manipulasjonshendelse"""
    event_id: str
    timestamp: datetime
    source_domain: str
    target_domain: str
    manipulation_type: ManipulationType
    threat_level: ThreatLevel
    evidence: Dict[str, Any]
    countermeasures_applied: List[str]

class UsynligeHandDetector:
    """
    🕵️ Hovedklasse for å detektere Den Usynlige Hånds aktivitet
    
    Analyserer tverrgående mønstre, identifiserer anomalier,
    og sporer manipulasjonsnettverk på tvers av domener.
    """
    
    def __init__(self, core_system):
        self.core_system = core_system
        self.detector_name = "Den Usynlige Hånd Detector"
        
        # Detection systems
        self.anomaly_patterns: Dict[str, AnomalyPattern] = {}
        self.manipulation_events: List[ManipulationEvent] = []
        self.baseline_metrics = {}
        self.paranoia_level = 0.7  # Base paranoia/sensitivity
        
        # Tracking systems
        self.causal_chains = defaultdict(list)
        self.probability_deviations = {}
        self.pattern_correlations = {}
        
        logger.info("🕵️ Den Usynlige Hånd Detector initialized")
        logger.info(f"👁️ Paranoia level: {self.paranoia_level:.2%}")
        
    def scan_for_anomalies(self, domain_data: Dict[str, Any], domain_name: str) -> Dict[str, Any]:
        """
        Scan for anomalier i domene-data
        
        Args:
            domain_data: Data fra domenet som skal analyseres
            domain_name: Navn på domenet
            
        Returns:
            Deteksjonsresultat med identifiserte anomalier
        """
        scan_id = f"SCAN_{domain_name}_{datetime.now().strftime('%H%M%S')}"
        logger.info(f"🔍 Scanning {domain_name} for anomalies...")
        
        # Establish baseline if first scan
        if domain_name not in self.baseline_metrics:
            self.baseline_metrics[domain_name] = self._establish_baseline(domain_data)
            logger.info(f"📊 Baseline established for {domain_name}")
            return {
                "scan_id": scan_id,
                "domain": domain_name,
                "baseline_established": True,
                "anomalies_detected": [],
                "threat_level": ThreatLevel.BENIGN.value
            }
            
        # Compare against baseline
        baseline = self.baseline_metrics[domain_name]
        detected_anomalies = []
        
        # Statistical anomaly detection
        for metric, current_value in domain_data.items():
            if metric in baseline and isinstance(current_value, (int, float)):
                baseline_value = baseline[metric]
                deviation = abs(current_value - baseline_value) / (baseline_value + 0.001)  # Avoid division by zero
                
                # Anomaly threshold based on paranoia level
                anomaly_threshold = 0.3 * (1 - self.paranoia_level)  # Higher paranoia = lower threshold
                
                if deviation > anomaly_threshold:
                    anomaly = {
                        "metric": metric,
                        "baseline_value": baseline_value,
                        "current_value": current_value,
                        "deviation": deviation,
                        "severity": min(1.0, deviation / anomaly_threshold)
                    }
                    detected_anomalies.append(anomaly)
                    
        # Pattern-based detection
        pattern_anomalies = self._detect_pattern_anomalies(domain_data, domain_name)
        detected_anomalies.extend(pattern_anomalies)
        
        # Calculate overall threat level
        if not detected_anomalies:
            threat_level = ThreatLevel.BENIGN
        else:
            max_severity = max(a.get("severity", 0) for a in detected_anomalies)
            if max_severity < 0.3:
                threat_level = ThreatLevel.SUSPICIOUS
            elif max_severity < 0.6:
                threat_level = ThreatLevel.CONCERNING
            elif max_severity < 0.9:
                threat_level = ThreatLevel.DANGEROUS
            else:
                threat_level = ThreatLevel.CATASTROPHIC
                
        scan_result = {
            "scan_id": scan_id,
            "domain": domain_name,
            "timestamp": datetime.now().isoformat(),
            "anomalies_detected": detected_anomalies,
            "anomaly_count": len(detected_anomalies),
            "threat_level": threat_level.value,
            "paranoia_level": self.paranoia_level,
            "usynlige_hand_probability": self._calculate_manipulation_probability(detected_anomalies)
        }
        
        # Log significant findings
        if threat_level.value > ThreatLevel.SUSPICIOUS.value:
            logger.warning(f"⚠️ Anomalies detected in {domain_name}: {len(detected_anomalies)} patterns")
            logger.warning(f"🚨 Threat level: {threat_level.name}")
            
        return scan_result
        
    def _establish_baseline(self, domain_data: Dict[str, Any]) -> Dict[str, Any]:
        """Etabler baseline metrics for et domene"""
        baseline = {}
        for key, value in domain_data.items():
            if isinstance(value, (int, float)):
                # Add some randomness to simulate normal variation
                baseline[key] = value + random.uniform(-value*0.1, value*0.1)
            elif isinstance(value, list):
                baseline[key] = len(value)
            elif isinstance(value, dict):
                baseline[key] = len(value)
        return baseline
        
    def _detect_pattern_anomalies(self, domain_data: Dict[str, Any], domain_name: str) -> List[Dict[str, Any]]:
        """Detekter mønstre som indikerer Den Usynlige Hånds aktivitet"""
        pattern_anomalies = []
        
        # Check for known manipulation signatures
        manipulation_signatures = [
            "0xDEADBEEF", "SOUL_NOT_FOUND", "REALITY_MISMATCH", 
            "COMPILER_GHOST", "MEMORY_HEMORRHAGE"
        ]
        
        data_str = json.dumps(domain_data, default=str).upper()
        for signature in manipulation_signatures:
            if signature in data_str:
                pattern_anomalies.append({
                    "type": "manipulation_signature",
                    "signature": signature,
                    "severity": 0.8,
                    "manipulation_type": ManipulationType.SYSTEM_SUBVERSION.value
                })
                
        # Check for probability distortions
        if "probability" in data_str.lower() or "chance" in data_str.lower():
            # Look for unrealistic probability values
            numbers = [float(word) for word in data_str.split() if word.replace('.', '').isdigit()]
            unlikely_probs = [n for n in numbers if 0 <= n <= 1 and (n > 0.95 or n < 0.05)]
            
            if unlikely_probs:
                pattern_anomalies.append({
                    "type": "probability_distortion",
                    "unlikely_probabilities": unlikely_probs,
                    "severity": 0.6,
                    "manipulation_type": ManipulationType.PROBABILITY_DISTORTION.value
                })
                
        return pattern_anomalies
        
    def _calculate_manipulation_probability(self, anomalies: List[Dict[str, Any]]) -> float:
        """Kalkuler sannsynlighet for at anomalier er fra Den Usynlige Hånd"""
        if not anomalies:
            return 0.0
            
        # Base probability on number and severity of anomalies
        total_severity = sum(a.get("severity", 0) for a in anomalies)
        anomaly_count_factor = min(1.0, len(anomalies) / 5)  # Max factor at 5+ anomalies
        
        # Check for manipulation signatures
        signature_bonus = 0.3 if any(a.get("type") == "manipulation_signature" for a in anomalies) else 0
        
        # Paranoia adjustment
        paranoia_modifier = self.paranoia_level * 0.2
        
        probability = min(1.0, (total_severity / len(anomalies)) + anomaly_count_factor + signature_bonus + paranoia_modifier)
        return probability
        
    def check_for_interference(self, source_domain: str, target_domain: str, 
                             interaction_type: str) -> bool:
        """
        Check om Den Usynlige Hånd interfererer med cross-domain interaksjon
        
        Args:
            source_domain: Kilde-domene
            target_domain: Mål-domene
            interaction_type: Type interaksjon
            
        Returns:
            True hvis interferens detekteres
        """
        # Calculate interference probability based on various factors
        base_interference_prob = 0.15  # 15% base chance
        
        # Domain-specific factors
        domain_risk_factors = {
            "skyskraper": 0.1,  # Lower risk due to security
            "rustbelt": 0.2,    # Higher risk due to corruption
            "bridge": 0.3       # Highest risk as neutral ground
        }
        
        source_risk = domain_risk_factors.get(source_domain.lower(), 0.15)
        target_risk = domain_risk_factors.get(target_domain.lower(), 0.15)
        
        # Interaction type risk
        high_risk_interactions = ["data_exchange", "system_access", "resource_transfer"]
        interaction_risk = 0.1 if interaction_type in high_risk_interactions else 0.05
        
        # Recent anomaly activity
        recent_anomalies = [e for e in self.manipulation_events 
                          if e.timestamp > datetime.now() - timedelta(hours=1)]
        anomaly_risk = min(0.3, len(recent_anomalies) * 0.05)
        
        total_interference_prob = (base_interference_prob + source_risk + 
                                 target_risk + interaction_risk + anomaly_risk)
        
        interference_detected = random.random() < total_interference_prob
        
        if interference_detected:
            logger.warning(f"🕵️ Interference detected: {source_domain} → {target_domain}")
            
            # Create manipulation event
            event = ManipulationEvent(
                event_id=f"INTERF_{datetime.now().strftime('%H%M%S')}",
                timestamp=datetime.now(),
                source_domain=source_domain,
                target_domain=target_domain,
                manipulation_type=random.choice(list(ManipulationType)),
                threat_level=ThreatLevel.CONCERNING,
                evidence={
                    "interference_probability": total_interference_prob,
                    "interaction_type": interaction_type,
                    "detection_factors": {
                        "source_risk": source_risk,
                        "target_risk": target_risk,
                        "interaction_risk": interaction_risk,
                        "anomaly_risk": anomaly_risk
                    }
                },
                countermeasures_applied=[]
            )
            
            self.manipulation_events.append(event)
            
        return interference_detected
        
    def apply_interference(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Apply Den Usynlige Hånds interferens til data
        
        Args:
            data: Original data
            
        Returns:
            Manipulert data
        """
        manipulated_data = data.copy()
        
        # Random manipulation types
        manipulation_types = [
            self._apply_probability_distortion,
            self._apply_causal_injection,
            self._apply_memory_alteration,
            self._apply_reality_glitch
        ]
        
        chosen_manipulation = random.choice(manipulation_types)
        manipulated_data = chosen_manipulation(manipulated_data)
        
        # Add corruption signature
        manipulated_data["_usynlige_hand_signature"] = f"0x{random.randint(0x1000, 0xFFFF):X}_MANIPULATED"
        manipulated_data["_manipulation_timestamp"] = datetime.now().isoformat()
        
        logger.warning("🎭 Data manipulation applied by Den Usynlige Hånd")
        
        return manipulated_data
        
    def _apply_probability_distortion(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Distorter sannsynlighetsverdier i data"""
        for key, value in data.items():
            if isinstance(value, float) and 0 <= value <= 1:
                # Subtle distortion
                distortion = random.uniform(-0.1, 0.1)
                data[key] = max(0, min(1, value + distortion))
        return data
        
    def _apply_causal_injection(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Injiser falske årsakssammenhenger"""
        data["_injected_causal_factor"] = random.choice([
            "UNEXPECTED_MARKET_FLUCTUATION",
            "PERSONNEL_BEHAVIOR_ANOMALY", 
            "SYSTEM_RESONANCE_CASCADE",
            "TEMPORAL_CORRELATION_SPIKE"
        ])
        return data
        
    def _apply_memory_alteration(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Endre historiske data subtilt"""
        if "timestamp" in data:
            # Shift timestamp slightly
            if isinstance(data["timestamp"], str):
                try:
                    dt = datetime.fromisoformat(data["timestamp"].replace('Z', '+00:00'))
                    shift = timedelta(minutes=random.randint(-30, 30))
                    data["timestamp"] = (dt + shift).isoformat()
                except:
                    pass
        return data
        
    def _apply_reality_glitch(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Introduser reality glitches"""
        glitch_messages = [
            "ERROR: REALITY_MISMATCH_AT_BYTE_0xDEADBEEF",
            "SOUL_NOT_FOUND",
            "PANIC: TEMPORAL_CONSISTENCY_VIOLATION",
            "COMPILER_GHOST_ACTIVITY_DETECTED"
        ]
        
        data["_reality_glitch"] = random.choice(glitch_messages)
        return data
        
    def trace_causal_chains(self, event_id: str, max_depth: int = 5) -> Dict[str, Any]:
        """
        Trace årsakssammenhenger tilbake til mulige manipulation sources
        
        Args:
            event_id: ID til hendelsen som skal traces
            max_depth: Maksimal dybde for tracing
            
        Returns:
            Causal chain analysis
        """
        logger.info(f"🔍 Tracing causal chains for event: {event_id}")
        
        # Find related events
        related_events = [e for e in self.manipulation_events 
                         if e.event_id == event_id or event_id in str(e.evidence)]
        
        if not related_events:
            return {
                "event_id": event_id,
                "chain_found": False,
                "error": "No related events found"
            }
            
        # Build causal chain
        causal_chain = []
        current_events = related_events
        depth = 0
        
        while current_events and depth < max_depth:
            level_events = []
            for event in current_events:
                level_events.append({
                    "depth": depth,
                    "event_id": event.event_id,
                    "timestamp": event.timestamp.isoformat(),
                    "domains": [event.source_domain, event.target_domain],
                    "manipulation_type": event.manipulation_type.value,
                    "threat_level": event.threat_level.value
                })
                
            causal_chain.append(level_events)
            
            # Find earlier related events (simplified simulation)
            earlier_events = [e for e in self.manipulation_events 
                            if e.timestamp < current_events[0].timestamp - timedelta(minutes=random.randint(1, 60))]
            current_events = random.sample(earlier_events, min(2, len(earlier_events)))
            depth += 1
            
        # Analyze pattern
        manipulation_types = [event["manipulation_type"] for level in causal_chain for event in level]
        pattern_analysis = {
            "chain_length": len(causal_chain),
            "total_events": sum(len(level) for level in causal_chain),
            "manipulation_types": list(set(manipulation_types)),
            "pattern_complexity": len(set(manipulation_types)) / len(manipulation_types) if manipulation_types else 0,
            "usynlige_hand_probability": min(1.0, len(causal_chain) * 0.2 + len(set(manipulation_types)) * 0.1)
        }
        
        result = {
            "event_id": event_id,
            "chain_found": True,
            "causal_chain": causal_chain,
            "pattern_analysis": pattern_analysis,
            "trace_timestamp": datetime.now().isoformat(),
            "investigator_signature": "0xCAUSAL_DETECTIVE_PROTOCOL"
        }
        
        logger.info(f"🔗 Causal chain traced: {pattern_analysis['chain_length']} levels, {pattern_analysis['total_events']} events")
        
        return result
        
    def get_detector_status(self) -> Dict[str, Any]:
        """Hent komplett detector-status"""
        recent_events = [e for e in self.manipulation_events 
                        if e.timestamp > datetime.now() - timedelta(hours=24)]
        
        threat_distribution = defaultdict(int)
        for event in recent_events:
            threat_distribution[event.threat_level.name] += 1
            
        return {
            "detector_name": self.detector_name,
            "paranoia_level": self.paranoia_level,
            "baseline_domains": list(self.baseline_metrics.keys()),
            "anomaly_patterns_tracked": len(self.anomaly_patterns),
            "total_manipulation_events": len(self.manipulation_events),
            "recent_events_24h": len(recent_events),
            "threat_distribution": dict(threat_distribution),
            "last_update": datetime.now().isoformat(),
            "detection_signature": "0xUNSEEN_HAND_VIGILANCE_ACTIVE"
        }

class UsynligeHand:
    """
    🎭 Representasjon av Den Usynlige Hånd som manipulativ kraft
    
    Koordinerer detection og response til skjulte manipulasjoner.
    """
    
    def __init__(self, core_system):
        self.core_system = core_system
        self.detector = UsynligeHandDetector(core_system)
        self.active_manipulations = []
        self.countermeasures = {}
        
    def check_for_interference(self, source_domain: str, target_domain: str, 
                             interaction_type: str) -> bool:
        """Proxy til detector for interference checking"""
        return self.detector.check_for_interference(source_domain, target_domain, interaction_type)
        
    def apply_interference(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Proxy til detector for interference application"""
        return self.detector.apply_interference(data)

if __name__ == "__main__":
    # Demo of Den Usynlige Hånd Detector
    print("🕵️✨ DEN USYNLIGE HÅND DETECTOR DEMO ✨🕵️")
    print("=" * 50)
    
    # Mock core system
    class MockCore:
        def cross_domain_interaction(self, source, target, type_name, data):
            return {"success": True, "data": data}
    
    # Initialize detector
    mock_core = MockCore()
    usynlige_hand = UsynligeHand(mock_core)
    
    # Test anomaly scanning
    print("\n🔍 Testing anomaly scanning...")
    test_data = {
        "system_health": 0.85,
        "error_rate": 0.12,
        "response_time": 1.5,
        "corruption_signatures": ["0xDEADBEEF", "SOUL_NOT_FOUND"],
        "probability_manipulation": 0.97  # Suspiciously high
    }
    
    # First scan (establishes baseline)
    scan1 = usynlige_hand.detector.scan_for_anomalies(test_data, "test_domain")
    print(f"📊 First scan: {json.dumps(scan1, indent=2)}")
    
    # Second scan with anomalies
    anomalous_data = test_data.copy()
    anomalous_data["system_health"] = 0.45  # Significant deviation
    anomalous_data["error_rate"] = 0.67     # High error rate
    
    scan2 = usynlige_hand.detector.scan_for_anomalies(anomalous_data, "test_domain")
    print(f"🚨 Anomaly scan: {json.dumps(scan2, indent=2)}")
    
    # Test interference detection
    print("\n🕵️ Testing interference detection...")
    interference = usynlige_hand.check_for_interference("skyskraper", "rustbelt", "data_exchange")
    print(f"🎭 Interference detected: {interference}")
    
    if interference:
        manipulated = usynlige_hand.apply_interference({"important_data": "original_value"})
        print(f"🎭 Manipulated data: {json.dumps(manipulated, indent=2)}")
    
    # Test causal tracing
    print("\n🔗 Testing causal chain tracing...")
    if usynlige_hand.detector.manipulation_events:
        event_id = usynlige_hand.detector.manipulation_events[0].event_id
        causal_trace = usynlige_hand.detector.trace_causal_chains(event_id)
        print(f"🔍 Causal trace: {json.dumps(causal_trace, indent=2, default=str)}")
    
    # Detector status
    status = usynlige_hand.detector.get_detector_status()
    print(f"\n🕵️ Detector Status: {json.dumps(status, indent=2)}")
    
    print("\n✨ Den Usynlige Hånd Detector Demo complete ✨")
