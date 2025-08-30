#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎭 PSYCHO-NOIR KONTRAPUNKT - CORE ORCHESTRATOR 🎭
================================================

Hovedorchestrator for det dualitiske systemet mellom Skyskraper og Rustbelt.
Håndterer cross-domain interactions og Den Usynlige Hånds manifestasjoner.

CORRUPTION_SIGNATURE: 0xDEADBEEF_CORE_ORCHESTRATION_ACTIVE
SYSTEM_STATUS: DUAL_DOMAIN_INITIALIZATION_PENDING
"""

import logging
import sqlite3
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
from enum import Enum

# Konfigurer logging med Psycho-Noir estetikk
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] 🎭 %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

class DomainType(Enum):
    """Domene-typer i Psycho-Noir Kontrapunkt universet"""
    SKYSKRAPER = "skyskraper"
    RUSTBELT = "rustbelt" 
    BRIDGE = "bridge"
    CORRUPTED = "corrupted"  # Den Usynlige Hånds påvirkning

class CorruptionLevel(Enum):
    """Korrupsjonsnivåer for Den Usynlige Hånds påvirkning"""
    CLEAN = 0.0
    MINOR_GLITCH = 0.25
    MODERATE_CORRUPTION = 0.5
    SEVERE_DISTORTION = 0.75
    TOTAL_SUBVERSION = 1.0

class PsychoNoirKontrapunkt:
    """
    🎭 Hovedorchestrator for Psycho-Noir Kontrapunkt systemet
    
    Koordinerer interaksjoner mellom:
    - Skyskraperen (høyteknologisk maktdomene)
    - Rustbeltet (industrielt overlevelsesdomene)
    - Den Usynlige Hånd (skjult manipulasjonslayet)
    """
    
    def __init__(self, data_path: str = "data/psycho_noir.db"):
        """
        Initialiserer core system med database connection
        
        Args:
            data_path: Sti til SQLite database for persistent storage
        """
        self.data_path = Path(data_path)
        self.data_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize database connection
        self.db_connection = sqlite3.connect(str(self.data_path))
        self._setup_database()
        
        # Core domain instances (lazy loading)
        self._skyskraper = None
        self._rustbelt = None
        self._usynlige_hand = None
        
        # System state tracking
        self.system_state = {
            "initialization_time": datetime.now(),
            "active_domains": [],
            "corruption_events": [],
            "cross_domain_interactions": 0
        }
        
        logger.info("🎭 PSYCHO-NOIR KONTRAPUNKT CORE INITIALIZED")
        logger.info(f"📊 Database: {self.data_path}")
        
    def _setup_database(self):
        """Setup database schema for Psycho-Noir Kontrapunkt"""
        cursor = self.db_connection.cursor()
        
        # Domains table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS domains (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(50) NOT NULL,
                type VARCHAR(20) NOT NULL,
                corruption_level REAL DEFAULT 0.0,
                last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                metadata TEXT  -- JSON for domain-specific data
            )
        """)
        
        # Characters table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS characters (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(100) NOT NULL,
                domain_id INTEGER,
                consciousness_level REAL DEFAULT 0.5,
                status VARCHAR(50) DEFAULT 'active',
                capabilities TEXT,  -- JSON array of capabilities
                FOREIGN KEY (domain_id) REFERENCES domains(id)
            )
        """)
        
        # Den Usynlige Hånd events table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usynlige_hand_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                domain_affected VARCHAR(50),
                manifestation_type VARCHAR(100),
                corruption_signature VARCHAR(255),
                severity_level REAL,
                metadata TEXT  -- JSON for event-specific data
            )
        """)
        
        # Cross-domain interactions table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS cross_domain_interactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                source_domain VARCHAR(50),
                target_domain VARCHAR(50),
                interaction_type VARCHAR(100),
                success BOOLEAN,
                interference_detected BOOLEAN DEFAULT FALSE,
                metadata TEXT
            )
        """)
        
        self.db_connection.commit()
        logger.info("📊 Database schema initialized")
        
    @property
    def skyskraper(self):
        """Lazy loading av Skyskraper domain"""
        if self._skyskraper is None:
            try:
                from skyskraper_systems import SkyscraperDomain
                self._skyskraper = SkyscraperDomain(self)
                self._register_domain("Skyskraperen", DomainType.SKYSKRAPER)
            except ImportError:
                logger.warning("Skyskraper systems not available")
                return None
        return self._skyskraper
        
    @property 
    def rustbelt(self):
        """Lazy loading av Rustbelt domain"""
        if self._rustbelt is None:
            try:
                from rustbelt_systems import RustbeltDomain
                self._rustbelt = RustbeltDomain(self)
                self._register_domain("Rustbeltet", DomainType.RUSTBELT)
            except ImportError:
                logger.warning("Rustbelt systems not available")
                return None
        return self._rustbelt
        
    @property
    def usynlige_hand(self):
        """Lazy loading av Den Usynlige Hånd"""
        if self._usynlige_hand is None:
            try:
                from usynlige_hand_detector import UsynligeHand
                self._usynlige_hand = UsynligeHand(self)
            except ImportError:
                logger.warning("Usynlige Hand detector not available")
                return None
        return self._usynlige_hand
        
    def _register_domain(self, name: str, domain_type: DomainType, 
                        corruption_level: float = 0.0):
        """Registrer et domene i database"""
        cursor = self.db_connection.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO domains (name, type, corruption_level, metadata)
            VALUES (?, ?, ?, ?)
        """, (name, domain_type.value, corruption_level, json.dumps({})))
        self.db_connection.commit()
        
        self.system_state["active_domains"].append(name)
        logger.info(f"🏗️ Domain registered: {name} ({domain_type.value})")
        
    def cross_domain_interaction(self, source_domain: str, target_domain: str, 
                                interaction_type: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Håndter interaksjon mellom domener med potensial for Den Usynlige Hånds innblanding
        
        Args:
            source_domain: Kilde-domene (skyskraper/rustbelt)
            target_domain: Mål-domene
            interaction_type: Type interaksjon (data_exchange, resource_request, etc.)
            data: Interaksjonsdata
            
        Returns:
            Dict med resultatet av interaksjonen
        """
        interaction_id = self.system_state["cross_domain_interactions"] + 1
        self.system_state["cross_domain_interactions"] = interaction_id
        
        logger.info(f"🌐 Cross-domain interaction #{interaction_id}: {source_domain} → {target_domain}")
        logger.info(f"📋 Type: {interaction_type}")
        
        # Check for Den Usynlige Hånd interference
        interference_detected = self.usynlige_hand.check_for_interference(
            source_domain, target_domain, interaction_type
        )
        
        success = True
        result_data = data.copy()
        
        if interference_detected:
            logger.warning(f"🕵️ Den Usynlige Hånd interference detected in interaction #{interaction_id}")
            # Apply corruption/manipulation to the interaction
            result_data = self.usynlige_hand.apply_interference(result_data)
            success = False
            
        # Log interaction to database
        cursor = self.db_connection.cursor()
        cursor.execute("""
            INSERT INTO cross_domain_interactions 
            (source_domain, target_domain, interaction_type, success, interference_detected, metadata)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (source_domain, target_domain, interaction_type, success, 
              interference_detected, json.dumps(result_data)))
        self.db_connection.commit()
        
        return {
            "interaction_id": interaction_id,
            "success": success,
            "interference_detected": interference_detected,
            "data": result_data,
            "timestamp": datetime.now().isoformat()
        }
        
    def get_system_status(self) -> Dict[str, Any]:
        """Hent komplett system-status"""
        cursor = self.db_connection.cursor()
        
        # Count domains
        cursor.execute("SELECT type, COUNT(*) FROM domains GROUP BY type")
        domain_counts = dict(cursor.fetchall())
        
        # Recent corruption events
        cursor.execute("""
            SELECT COUNT(*) FROM usynlige_hand_events 
            WHERE timestamp > datetime('now', '-1 hour')
        """)
        recent_corruption_events = cursor.fetchone()[0]
        
        # Cross-domain interaction stats
        cursor.execute("""
            SELECT 
                COUNT(*) as total,
                SUM(CASE WHEN success = 1 THEN 1 ELSE 0 END) as successful,
                SUM(CASE WHEN interference_detected = 1 THEN 1 ELSE 0 END) as interfered
            FROM cross_domain_interactions
            WHERE timestamp > datetime('now', '-24 hours')
        """)
        interaction_stats = cursor.fetchone()
        
        return {
            "system_uptime": str(datetime.now() - self.system_state["initialization_time"]),
            "active_domains": self.system_state["active_domains"],
            "domain_counts": domain_counts,
            "recent_corruption_events": recent_corruption_events,
            "daily_interactions": {
                "total": interaction_stats[0] or 0,
                "successful": interaction_stats[1] or 0,
                "interfered": interaction_stats[2] or 0
            },
            "corruption_signature": "0xDEADBEEF_SYSTEM_OPERATIONAL"
        }
        
    def emergency_shutdown(self, reason: str = "Manual shutdown"):
        """Emergency shutdown med logging"""
        logger.warning(f"🚨 EMERGENCY SHUTDOWN INITIATED: {reason}")
        
        # Log shutdown event
        cursor = self.db_connection.cursor()
        cursor.execute("""
            INSERT INTO usynlige_hand_events 
            (domain_affected, manifestation_type, corruption_signature, severity_level, metadata)
            VALUES (?, ?, ?, ?, ?)
        """, ("SYSTEM", "EMERGENCY_SHUTDOWN", "0xSHUTDOWN", 1.0, 
              json.dumps({"reason": reason, "timestamp": datetime.now().isoformat()})))
        
        self.db_connection.commit()
        self.db_connection.close()
        
        logger.info("🎭 PSYCHO-NOIR KONTRAPUNKT CORE SHUTDOWN COMPLETE")
        
    def __del__(self):
        """Cleanup ved garbage collection"""
        if hasattr(self, 'db_connection'):
            self.db_connection.close()

# Factory function for easy instantiation
def create_psycho_noir_system(data_path: str = "data/psycho_noir.db") -> PsychoNoirKontrapunkt:
    """
    Factory function for creating PsychoNoirKontrapunkt instance
    
    Args:
        data_path: Path to SQLite database
        
    Returns:
        Configured PsychoNoirKontrapunkt instance
    """
    return PsychoNoirKontrapunkt(data_path)

if __name__ == "__main__":
    # Demo/test execution
    print("🎭✨ PSYCHO-NOIR KONTRAPUNKT CORE DEMO ✨🎭")
    print("=" * 50)
    
    # Create system instance
    system = create_psycho_noir_system()
    
    # Display initial status
    status = system.get_system_status()
    print(f"🌌 System Status: {json.dumps(status, indent=2)}")
    
    # Test cross-domain interaction
    result = system.cross_domain_interaction(
        "skyskraper", "rustbelt", "data_probe",
        {"target": "industrial_sensors", "access_level": "surveillance"}
    )
    print(f"🌐 Cross-domain test: {json.dumps(result, indent=2)}")
    
    # Cleanup
    system.emergency_shutdown("Demo complete")
    print("\n✨ Demo execution complete ✨")
