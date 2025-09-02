#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FAILURE ARCHAEOLOGY SYSTEM
Psycho-Noir Kontrapunkt - Systematisk katalogisering og læring fra failed runs

Dette systemet transformerer feilerfaringer til proaktiv intelligens ved å:
1. Katalogisere alle failed runs systematisk
2. Identifisere mønstre og root causes  
3. Generere pre-emptive logging strategier
4. Skape bidirectional learning loops
"""

import json
import datetime
import re
import hashlib
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from pathlib import Path
import logging

@dataclass
class FailureArcheologyEntry:
    """En katalogisert feilerfaring - grunnsteinen i vårt læringssystem"""
    failure_id: str
    timestamp: str
    failure_type: str  # 'copilot_runner', 'bot_failure', 'code_quality', 'deployment', etc.
    error_signature: str  # Unique identifier for this type of error
    context: Dict  # Environment, settings, attempted operation
    error_trace: str  # Full error output
    root_cause_hypothesis: str
    severity: int  # 1-5 scale
    recovery_actions_attempted: List[str]
    recovery_success: bool
    learning_extraction: Dict  # What we learned from this failure
    prevention_strategy: Optional[str] = None
    related_failures: List[str] = None  # IDs of similar failures
    
class FailureArchaeologist:
    """
    FAILURE ARCHAEOLOGIST - Graver fram læring fra ruinene av failed runs
    
    Implementerer systematic failure mining med Psycho-Noir tematikk:
    - Skyskraperens presisjon i katalogisering
    - Rustbeltets improvisasjon i recovery
    - Den Usynlige Hånds pattern recognition på tvers av domener
    """
    
    def __init__(self, archive_path: str = "data/failure_archaeology"):
        self.archive_path = Path(archive_path)
        self.archive_path.mkdir(parents=True, exist_ok=True)
        
        # Initialize logging
        logging.basicConfig(
            filename=self.archive_path / "archaeology_log.txt",
            level=logging.INFO,
            format='%(asctime)s - FAILURE_ARCHAEOLOGIST - %(levelname)s - %(message)s'
        )
        
        self.failure_database = self._load_failure_database()
        self.pattern_library = self._load_pattern_library()
    
    def _generate_failure_id(self, error_trace: str, context: Dict) -> str:
        """Genererer unik ID for hver feilerfaring"""
        identifier_string = f"{error_trace[:200]}{str(context)}"
        return f"FAIL_{hashlib.md5(identifier_string.encode()).hexdigest()[:12]}"
    
    def _extract_error_signature(self, error_trace: str) -> str:
        """Ekstraherer karakteristisk signatur fra error trace"""
        # Fjern timestamps, paths, og andre variable elementer
        signature = re.sub(r'\d{4}-\d{2}-\d{2}[\s\d\:\.]+', '[TIMESTAMP]', error_trace)
        signature = re.sub(r'/[^\s]+/', '[PATH]/', signature)
        signature = re.sub(r'line \d+', 'line [NUM]', signature)
        signature = re.sub(r'process \d+', 'process [PID]', signature)
        
        # Behold kun første 500 chars av den normaliserte signaturen
        return signature[:500]
    
    def catalog_failure(
        self, 
        failure_type: str,
        error_trace: str,
        context: Dict,
        root_cause_hypothesis: str = "",
        severity: int = 3,
        recovery_actions: List[str] = None
    ) -> str:
        """
        HOVEDFUNKSJON: Katalogiserer en ny feilerfaring i biblioteket
        """
        failure_id = self._generate_failure_id(error_trace, context)
        error_signature = self._extract_error_signature(error_trace)
        
        # Sjekk om vi har sett denne type feil før
        related_failures = self._find_related_failures(error_signature)
        
        entry = FailureArcheologyEntry(
            failure_id=failure_id,
            timestamp=datetime.datetime.now().isoformat(),
            failure_type=failure_type,
            error_signature=error_signature,
            context=context,
            error_trace=error_trace,
            root_cause_hypothesis=root_cause_hypothesis,
            severity=severity,
            recovery_actions_attempted=recovery_actions or [],
            recovery_success=False,  # Settes til True når løsning finnes
            learning_extraction={},
            related_failures=related_failures
        )
        
        self.failure_database[failure_id] = entry
        self._save_failure_database()
        
        logging.info(f"CATALOGED_FAILURE: {failure_id} - {failure_type}")
        
        # Trigger pattern analysis hvis vi har flere relaterte feil
        if len(related_failures) >= 2:
            self._analyze_failure_pattern(error_signature)
        
        return failure_id
    
    def _find_related_failures(self, error_signature: str) -> List[str]:
        """Finner relaterte feilerfaringer basert på error signature likhet"""
        related = []
        
        for fid, entry in self.failure_database.items():
            # Simple similarity check - kan forbedres med fuzzy matching
            similarity = self._calculate_signature_similarity(error_signature, entry.error_signature)
            if similarity > 0.7:  # 70% likhet threshold
                related.append(fid)
        
        return related
    
    def _calculate_signature_similarity(self, sig1: str, sig2: str) -> float:
        """Beregner likhet mellom to error signatures"""
        # Simple word-based similarity - kan forbedres
        words1 = set(sig1.lower().split())
        words2 = set(sig2.lower().split())
        
        if not words1 or not words2:
            return 0.0
        
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        return len(intersection) / len(union)
    
    def _analyze_failure_pattern(self, error_signature: str):
        """Analyserer mønstre i relaterte feilerfaringer"""
        related_entries = [
            entry for entry in self.failure_database.values() 
            if entry.error_signature == error_signature
        ]
        
        if len(related_entries) < 2:
            return
        
        # Pattern analyse logikk
        pattern = {
            'signature': error_signature,
            'frequency': len(related_entries),
            'severity_trend': [e.severity for e in related_entries],
            'common_context_elements': self._extract_common_context(related_entries),
            'successful_recovery_actions': self._extract_successful_recoveries(related_entries),
            'prevention_strategy': self._generate_prevention_strategy(related_entries)
        }
        
        self.pattern_library[error_signature] = pattern
        self._save_pattern_library()
        
        logging.info(f"PATTERN_IDENTIFIED: {error_signature[:50]}... (frequency: {len(related_entries)})")
    
    def _extract_common_context(self, entries: List[FailureArcheologyEntry]) -> Dict:
        """Ekstraherer felles kontekstelementer fra relaterte feilerfaringer"""
        common_elements = {}
        
        # Finn felles nøkler på tvers av entries
        all_keys = set()
        for entry in entries:
            all_keys.update(entry.context.keys())
        
        for key in all_keys:
            values = [entry.context.get(key) for entry in entries if key in entry.context]
            if len(set(values)) == 1:  # Samme verdi i alle entries
                common_elements[key] = values[0]
        
        return common_elements
    
    def _extract_successful_recoveries(self, entries: List[FailureArcheologyEntry]) -> List[str]:
        """Finner recovery actions som har ført til suksess"""
        successful_actions = []
        
        for entry in entries:
            if entry.recovery_success:
                successful_actions.extend(entry.recovery_actions_attempted)
        
        # Return unique actions
        return list(set(successful_actions))
    
    def _generate_prevention_strategy(self, entries: List[FailureArcheologyEntry]) -> str:
        """Genererer prevention strategy basert på pattern analyse"""
        common_context = self._extract_common_context(entries)
        successful_recoveries = self._extract_successful_recoveries(entries)
        
        strategy_parts = []
        
        if common_context:
            strategy_parts.append(f"Pre-check conditions: {common_context}")
        
        if successful_recoveries:
            strategy_parts.append(f"Apply proven recovery: {successful_recoveries}")
        
        return " | ".join(strategy_parts) if strategy_parts else "No prevention strategy identified yet"
    
    def generate_preemptive_logging_config(self) -> Dict:
        """
        HOVEDFUNKSJON: Genererer pre-emptive logging config basert på failure patterns
        """
        logging_config = {
            'high_risk_operations': [],
            'monitoring_points': [],
            'alert_conditions': [],
            'recovery_procedures': {}
        }
        
        for signature, pattern in self.pattern_library.items():
            if pattern['frequency'] >= 3:  # Høy-frekvente feilerfaringer
                logging_config['high_risk_operations'].append({
                    'signature': signature[:100],
                    'frequency': pattern['frequency'],
                    'monitoring_strategy': f"Enhanced logging for: {signature[:50]}..."
                })
                
                if 'common_context_elements' in pattern:
                    for key, value in pattern['common_context_elements'].items():
                        logging_config['monitoring_points'].append({
                            'context_key': key,
                            'trigger_value': value,
                            'action': f"Increase log verbosity when {key}={value}"
                        })
        
        return logging_config
    
    def get_bidirectional_learning_recommendations(self) -> Dict:
        """
        Genererer bidirectional learning anbefalinger - failed runs → prevention → success
        """
        recommendations = {
            'immediate_actions': [],
            'systematic_improvements': [],
            'prevention_implementations': []
        }
        
        # Analyser høy-frekvente feilerfaringer
        frequent_patterns = [
            (sig, pattern) for sig, pattern in self.pattern_library.items() 
            if pattern['frequency'] >= 2
        ]
        
        for signature, pattern in frequent_patterns:
            recommendations['immediate_actions'].append({
                'pattern': signature[:100],
                'frequency': pattern['frequency'],
                'action': f"Implement prevention: {pattern.get('prevention_strategy', 'TBD')}"
            })
        
        # Systematiske forbedringer
        failure_types = {}
        for entry in self.failure_database.values():
            failure_types[entry.failure_type] = failure_types.get(entry.failure_type, 0) + 1
        
        for ftype, count in sorted(failure_types.items(), key=lambda x: x[1], reverse=True):
            recommendations['systematic_improvements'].append({
                'failure_type': ftype,
                'count': count,
                'improvement': f"Strengthen {ftype} error handling and validation"
            })
        
        return recommendations
    
    def export_learning_library(self) -> Dict:
        """Eksporterer hele learning library for external use"""
        return {
            'failure_database': {fid: asdict(entry) for fid, entry in self.failure_database.items()},
            'pattern_library': self.pattern_library,
            'statistics': self._generate_statistics(),
            'recommendations': self.get_bidirectional_learning_recommendations()
        }
    
    def _generate_statistics(self) -> Dict:
        """Genererer statistikk over failure archaeology biblioteket"""
        if not self.failure_database:
            return {'total_failures': 0}
        
        total_failures = len(self.failure_database)
        failure_types = {}
        severity_distribution = {}
        
        for entry in self.failure_database.values():
            failure_types[entry.failure_type] = failure_types.get(entry.failure_type, 0) + 1
            severity_distribution[entry.severity] = severity_distribution.get(entry.severity, 0) + 1
        
        return {
            'total_failures': total_failures,
            'unique_patterns': len(self.pattern_library),
            'failure_types': failure_types,
            'severity_distribution': severity_distribution,
            'recovery_success_rate': sum(1 for e in self.failure_database.values() if e.recovery_success) / total_failures
        }
    
    def _load_failure_database(self) -> Dict[str, FailureArcheologyEntry]:
        """Laster failure database fra disk"""
        db_file = self.archive_path / "failure_database.json"
        
        if not db_file.exists():
            return {}
        
        try:
            with open(db_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Convert dict back to FailureArcheologyEntry objects
            database = {}
            for fid, entry_dict in data.items():
                database[fid] = FailureArcheologyEntry(**entry_dict)
            
            return database
        except Exception as e:
            logging.error(f"Failed to load failure database: {e}")
            return {}
    
    def _save_failure_database(self):
        """Lagrer failure database til disk"""
        db_file = self.archive_path / "failure_database.json"
        
        try:
            # Convert FailureArcheologyEntry objects to dict for JSON serialization
            data = {fid: asdict(entry) for fid, entry in self.failure_database.items()}
            
            with open(db_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logging.error(f"Failed to save failure database: {e}")
    
    def _load_pattern_library(self) -> Dict:
        """Laster pattern library fra disk"""
        pattern_file = self.archive_path / "pattern_library.json"
        
        if not pattern_file.exists():
            return {}
        
        try:
            with open(pattern_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logging.error(f"Failed to load pattern library: {e}")
            return {}
    
    def _save_pattern_library(self):
        """Lagrer pattern library til disk"""
        pattern_file = self.archive_path / "pattern_library.json"
        
        try:
            with open(pattern_file, 'w', encoding='utf-8') as f:
                json.dump(self.pattern_library, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logging.error(f"Failed to save pattern library: {e}")

# TESTING & DEMONSTRATION FUNCTIONS

def demonstrate_failure_archaeology():
    """Demonstrerer failure archaeology systemet med eksempel-data"""
    archaeologist = FailureArchaeologist()
    
    # Simuler noen typiske feilerfaringer
    test_failures = [
        {
            'failure_type': 'copilot_runner',
            'error_trace': 'ERROR: GitHub Copilot runner failed - Connection timeout after 30s at line 45',
            'context': {'environment': 'vscode', 'os': 'linux', 'copilot_version': '1.234'},
            'root_cause_hypothesis': 'Network connectivity issues during peak hours'
        },
        {
            'failure_type': 'bot_failure', 
            'error_trace': 'BOT_PANIC: Memory allocation failed at 0xDEADBEEF - SOUL_NOT_FOUND exception',
            'context': {'bot_type': 'neural_archaeology', 'memory_usage': '95%', 'uptime': '72h'},
            'root_cause_hypothesis': 'Memory leak in long-running bot process'
        },
        {
            'failure_type': 'code_quality',
            'error_trace': 'QUALITY_CHECK_FAILED: Pylint score 3.2/10 - 47 violations detected',
            'context': {'file': 'dialogue_analyzer.py', 'violations': ['unused-variable', 'line-too-long']},
            'root_cause_hypothesis': 'Rapid development without code review'
        }
    ]
    
    # Katalogiser feilerfaringene
    for failure in test_failures:
        failure_id = archaeologist.catalog_failure(**failure)
        print(f"CATALOGED: {failure_id} - {failure['failure_type']}")
    
    # Generer preemptive logging config
    logging_config = archaeologist.generate_preemptive_logging_config()
    print(f"\nPREEMPTIVE LOGGING CONFIG: {json.dumps(logging_config, indent=2)}")
    
    # Få bidirectional learning recommendations
    recommendations = archaeologist.get_bidirectional_learning_recommendations()
    print(f"\nLEARNING RECOMMENDATIONS: {json.dumps(recommendations, indent=2)}")
    
    # Eksporter complete learning library
    learning_library = archaeologist.export_learning_library()
    
    # Save til fil for later use
    export_file = Path("data/failure_archaeology/complete_learning_export.json")
    export_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(export_file, 'w', encoding='utf-8') as f:
        json.dump(learning_library, f, indent=2, ensure_ascii=False)
    
    print(f"\nLEARNING LIBRARY EXPORTED TO: {export_file}")
    
    return archaeologist

if __name__ == "__main__":
    print("🔍 FAILURE ARCHAEOLOGY SYSTEM - Starting demonstration...")
    archaeologist = demonstrate_failure_archaeology()
    print("✅ Demonstration complete!")
