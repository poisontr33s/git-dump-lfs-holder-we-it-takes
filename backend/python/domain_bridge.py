#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🌐 DOMAIN BRIDGE SYSTEMS 🌐
============================

Cross-domain communication og interaction management mellom
Skyskraper og Rustbelt, med detection av Den Usynlige Hånds interferens.

BRIDGE_SIGNATURE: 0xCROSS_DOMAIN_PROTOCOLS_ACTIVE
COMMUNICATION_STATUS: INTER_DOMAIN_CHANNEL_OPERATIONAL
"""

import logging
import json
import random
import hashlib
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Union, Tuple
from dataclasses import dataclass
from enum import Enum
from collections import defaultdict

logger = logging.getLogger(__name__)

class BridgeProtocol(Enum):
    """Kommunikasjonsprotokoller mellom domener"""
    DIRECT_LINK = "direct_link"
    ENCRYPTED_CHANNEL = "encrypted_channel"
    DEAD_DROP = "dead_drop"
    PROXY_RELAY = "proxy_relay"
    EMERGENCY_BROADCAST = "emergency_broadcast"

class MessagePriority(Enum):
    """Prioritetsnivåer for meldinger"""
    LOW = 1
    NORMAL = 2
    HIGH = 3
    URGENT = 4
    EMERGENCY = 5

class CommunicationStatus(Enum):
    """Status for kommunikasjonsforsøk"""
    SUCCESS = "success"
    PARTIAL_DELIVERY = "partial_delivery"
    DELIVERY_FAILED = "delivery_failed"
    INTERCEPTED = "intercepted"
    CORRUPTED = "corrupted"
    INTERFERENCE_DETECTED = "interference_detected"

@dataclass
class BridgeMessage:
    """En melding sendt mellom domener"""
    message_id: str
    source_domain: str
    target_domain: str
    sender: str
    recipient: str
    content: Dict[str, Any]
    priority: MessagePriority
    protocol: BridgeProtocol
    timestamp: datetime
    delivery_status: CommunicationStatus
    encryption_level: float
    interference_detected: bool

@dataclass
class DomainGateway:
    """Gateway mellom to domener"""
    gateway_id: str
    domain_a: str
    domain_b: str
    security_level: float
    bandwidth_capacity: int
    current_load: int
    status: str
    last_maintenance: datetime

class DomainBridge:
    """
    🌐 Hovedklasse for cross-domain communication
    
    Håndterer sikker kommunikasjon mellom Skyskraper og Rustbelt,
    med automatisk detection og mitigation av Den Usynlige Hånds interferens.
    """
    
    def __init__(self, core_system):
        self.core_system = core_system
        self.bridge_name = "Cross-Domain Communication Bridge"
        
        # Communication infrastructure
        self.active_gateways: Dict[str, DomainGateway] = {}
        self.message_queue: List[BridgeMessage] = []
        self.message_history: List[BridgeMessage] = []
        self.routing_table = {}
        
        # Security and monitoring
        self.encryption_keys = {}
        self.communication_logs = []
        self.interference_patterns = defaultdict(list)
        
        # Initialize default gateways
        self._initialize_default_gateways()
        
        logger.info("🌐 Domain Bridge initialized")
        logger.info(f"🚪 Active gateways: {len(self.active_gateways)}")
        
    def _initialize_default_gateways(self):
        """Initialize standard gateways mellom domener"""
        # Primary Skyskraper-Rustbelt gateway
        primary_gateway = DomainGateway(
            gateway_id="SKY_RUST_PRIMARY",
            domain_a="skyskraper",
            domain_b="rustbelt",
            security_level=0.7,
            bandwidth_capacity=1000,
            current_load=0,
            status="operational",
            last_maintenance=datetime.now() - timedelta(days=2)
        )
        self.active_gateways[primary_gateway.gateway_id] = primary_gateway
        
        # Emergency backup gateway
        backup_gateway = DomainGateway(
            gateway_id="SKY_RUST_BACKUP",
            domain_a="skyskraper", 
            domain_b="rustbelt",
            security_level=0.5,
            bandwidth_capacity=500,
            current_load=0,
            status="standby",
            last_maintenance=datetime.now() - timedelta(days=7)
        )
        self.active_gateways[backup_gateway.gateway_id] = backup_gateway
        
        # Bridge monitoring gateway
        monitor_gateway = DomainGateway(
            gateway_id="BRIDGE_MONITOR",
            domain_a="bridge",
            domain_b="bridge",
            security_level=0.9,
            bandwidth_capacity=2000,
            current_load=0,
            status="operational",
            last_maintenance=datetime.now()
        )
        self.active_gateways[monitor_gateway.gateway_id] = monitor_gateway
        
    def send_message(self, source_domain: str, target_domain: str, sender: str, 
                    recipient: str, content: Dict[str, Any], 
                    priority: MessagePriority = MessagePriority.NORMAL,
                    protocol: BridgeProtocol = BridgeProtocol.DIRECT_LINK) -> BridgeMessage:
        """
        Send melding mellom domener
        
        Args:
            source_domain: Avsender-domene
            target_domain: Mottaker-domene  
            sender: Avsender ID
            recipient: Mottaker ID
            content: Meldingsinnhold
            priority: Prioritetsnivå
            protocol: Kommunikasjonsprotokoll
            
        Returns:
            BridgeMessage objekt med delivery status
        """
        message_id = f"MSG_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{random.randint(1000, 9999)}"
        
        logger.info(f"📨 Sending message: {sender}@{source_domain} → {recipient}@{target_domain}")
        logger.info(f"📋 Protocol: {protocol.value}, Priority: {priority.name}")
        
        # Create message object
        message = BridgeMessage(
            message_id=message_id,
            source_domain=source_domain,
            target_domain=target_domain,
            sender=sender,
            recipient=recipient,
            content=content,
            priority=priority,
            protocol=protocol,
            timestamp=datetime.now(),
            delivery_status=CommunicationStatus.SUCCESS,  # Default, will be updated
            encryption_level=0.0,
            interference_detected=False
        )
        
        # Process message through communication pipeline
        message = self._route_message(message)
        message = self._apply_security_protocol(message)
        message = self._check_for_interference(message)
        message = self._attempt_delivery(message)
        
        # Store message
        self.message_history.append(message)
        if message.delivery_status != CommunicationStatus.SUCCESS:
            self.message_queue.append(message)  # Queue for retry
            
        # Log communication
        self._log_communication(message)
        
        return message
        
    def _route_message(self, message: BridgeMessage) -> BridgeMessage:
        """Rute melding gjennom riktig gateway"""
        # Find best gateway for routing
        available_gateways = [gw for gw in self.active_gateways.values()
                            if (gw.domain_a == message.source_domain and gw.domain_b == message.target_domain) or
                               (gw.domain_b == message.source_domain and gw.domain_a == message.target_domain)]
        
        if not available_gateways:
            logger.warning(f"❌ No gateway found for {message.source_domain} → {message.target_domain}")
            message.delivery_status = CommunicationStatus.DELIVERY_FAILED
            return message
            
        # Select best gateway based on load and security
        best_gateway = min(available_gateways, 
                          key=lambda gw: gw.current_load / gw.bandwidth_capacity)
        
        # Update gateway load
        message_size = len(json.dumps(message.content, default=str))
        best_gateway.current_load += message_size
        
        logger.info(f"🚪 Routing via gateway: {best_gateway.gateway_id}")
        
        # Store routing info in message
        if not hasattr(message, 'routing_info'):
            message.routing_info = {}
        message.routing_info['gateway_used'] = best_gateway.gateway_id
        message.routing_info['message_size'] = message_size
        
        return message
        
    def _apply_security_protocol(self, message: BridgeMessage) -> BridgeMessage:
        """Apply sikkerhetsprotokoller til melding"""
        # Determine encryption level based on protocol and content sensitivity
        base_encryption = {
            BridgeProtocol.DIRECT_LINK: 0.3,
            BridgeProtocol.ENCRYPTED_CHANNEL: 0.8,
            BridgeProtocol.DEAD_DROP: 0.6,
            BridgeProtocol.PROXY_RELAY: 0.7,
            BridgeProtocol.EMERGENCY_BROADCAST: 0.2  # Speed over security
        }
        
        encryption_level = base_encryption[message.protocol]
        
        # Increase encryption for sensitive content
        sensitive_keywords = ["classified", "secret", "surveillance", "manipulation", "usynlige_hand"]
        content_str = json.dumps(message.content, default=str).lower()
        
        for keyword in sensitive_keywords:
            if keyword in content_str:
                encryption_level = min(1.0, encryption_level + 0.2)
                break
                
        # Apply priority-based encryption adjustment
        if message.priority.value >= MessagePriority.URGENT.value:
            encryption_level = min(1.0, encryption_level + 0.1)
            
        message.encryption_level = encryption_level
        
        # Simulate encryption process
        if encryption_level > 0.5:
            # Strong encryption - modify content representation
            encrypted_content = message.content.copy()
            encrypted_content['_encryption_signature'] = f"0x{random.randint(0x10000, 0xFFFFF):X}"
            encrypted_content['_encryption_level'] = encryption_level
            message.content = encrypted_content
            
        logger.info(f"🔐 Security applied: {encryption_level:.2%} encryption")
        
        return message
        
    def _check_for_interference(self, message: BridgeMessage) -> BridgeMessage:
        """Check for Den Usynlige Hånd interference"""
        # Check with main detection system
        interference_detected = self.core_system.usynlige_hand.check_for_interference(
            message.source_domain, message.target_domain, "message_transmission"
        )
        
        if interference_detected:
            logger.warning(f"🕵️ Interference detected in message transmission: {message.message_id}")
            message.interference_detected = True
            
            # Apply interference effects
            interference_effects = [
                "message_delay",
                "content_corruption", 
                "routing_misdirection",
                "encryption_weakness",
                "delivery_failure"
            ]
            
            chosen_effect = random.choice(interference_effects)
            
            if chosen_effect == "message_delay":
                # Simulate delay (logged for tracking)
                message.routing_info = getattr(message, 'routing_info', {})
                message.routing_info['interference_delay'] = random.randint(5, 30)
                
            elif chosen_effect == "content_corruption":
                # Corrupt message content
                message.content = self.core_system.usynlige_hand.apply_interference(message.content)
                message.delivery_status = CommunicationStatus.CORRUPTED
                
            elif chosen_effect == "routing_misdirection":
                # Message gets misrouted
                message.delivery_status = CommunicationStatus.DELIVERY_FAILED
                
            elif chosen_effect == "encryption_weakness":
                # Reduce encryption effectiveness
                message.encryption_level *= 0.5
                
            elif chosen_effect == "delivery_failure":
                # Complete delivery failure
                message.delivery_status = CommunicationStatus.DELIVERY_FAILED
                
            # Log interference pattern
            self.interference_patterns[message.source_domain + "->" + message.target_domain].append({
                "timestamp": datetime.now(),
                "effect": chosen_effect,
                "message_id": message.message_id
            })
            
        return message
        
    def _attempt_delivery(self, message: BridgeMessage) -> BridgeMessage:
        """Attempt å levere melding til mottaker"""
        if message.delivery_status == CommunicationStatus.DELIVERY_FAILED:
            return message  # Already failed, don't attempt delivery
            
        # Calculate delivery probability based on various factors
        base_delivery_rate = 0.85
        
        # Protocol-specific success rates
        protocol_rates = {
            BridgeProtocol.DIRECT_LINK: 0.9,
            BridgeProtocol.ENCRYPTED_CHANNEL: 0.8,
            BridgeProtocol.DEAD_DROP: 0.7,
            BridgeProtocol.PROXY_RELAY: 0.75,
            BridgeProtocol.EMERGENCY_BROADCAST: 0.95
        }
        
        delivery_rate = protocol_rates[message.protocol]
        
        # Priority affects delivery success
        if message.priority.value >= MessagePriority.URGENT.value:
            delivery_rate += 0.1
            
        # Interference reduces delivery rate
        if message.interference_detected:
            delivery_rate *= 0.6
            
        # Gateway load affects delivery
        if hasattr(message, 'routing_info') and 'gateway_used' in message.routing_info:
            gateway_id = message.routing_info['gateway_used']
            if gateway_id in self.active_gateways:
                gateway = self.active_gateways[gateway_id]
                load_factor = gateway.current_load / gateway.bandwidth_capacity
                delivery_rate *= max(0.3, 1.0 - load_factor)
                
        # Attempt delivery
        delivery_success = random.random() < delivery_rate
        
        if delivery_success:
            if message.interference_detected:
                message.delivery_status = CommunicationStatus.PARTIAL_DELIVERY
            else:
                message.delivery_status = CommunicationStatus.SUCCESS
        else:
            message.delivery_status = CommunicationStatus.DELIVERY_FAILED
            
        logger.info(f"📬 Delivery attempt: {message.delivery_status.value}")
        
        return message
        
    def _log_communication(self, message: BridgeMessage):
        """Log communication for analysis og debugging"""
        log_entry = {
            "timestamp": message.timestamp.isoformat(),
            "message_id": message.message_id,
            "route": f"{message.source_domain} → {message.target_domain}",
            "sender": message.sender,
            "recipient": message.recipient,
            "protocol": message.protocol.value,
            "priority": message.priority.name,
            "delivery_status": message.delivery_status.value,
            "encryption_level": message.encryption_level,
            "interference_detected": message.interference_detected,
            "content_size": len(json.dumps(message.content, default=str))
        }
        
        self.communication_logs.append(log_entry)
        
        # Keep logs limited to recent entries
        if len(self.communication_logs) > 1000:
            self.communication_logs = self.communication_logs[-500:]  # Keep last 500
            
    def retry_failed_messages(self, max_retries: int = 3) -> Dict[str, int]:
        """Retry failed messages in queue"""
        retry_stats = {"attempted": 0, "successful": 0, "still_failed": 0}
        
        messages_to_retry = [msg for msg in self.message_queue 
                           if msg.delivery_status in [CommunicationStatus.DELIVERY_FAILED, 
                                                     CommunicationStatus.CORRUPTED]]
        
        for message in messages_to_retry:
            retry_stats["attempted"] += 1
            
            # Apply retry logic - reduce interference probability
            original_content = message.content
            message.interference_detected = False
            message.delivery_status = CommunicationStatus.SUCCESS
            
            # Retry delivery process
            message = self._check_for_interference(message)
            message = self._attempt_delivery(message)
            
            if message.delivery_status == CommunicationStatus.SUCCESS:
                retry_stats["successful"] += 1
                self.message_queue.remove(message)
            else:
                retry_stats["still_failed"] += 1
                
        logger.info(f"🔄 Message retry completed: {retry_stats}")
        return retry_stats
        
    def establish_secure_channel(self, domain_a: str, domain_b: str, 
                               security_level: float = 0.8) -> str:
        """Etabler sikker kommunikasjonskanal mellom domener"""
        channel_id = f"SECURE_{domain_a}_{domain_b}_{datetime.now().strftime('%H%M%S')}"
        
        # Create dedicated secure gateway
        secure_gateway = DomainGateway(
            gateway_id=channel_id,
            domain_a=domain_a,
            domain_b=domain_b,
            security_level=security_level,
            bandwidth_capacity=500,  # Smaller capacity for security
            current_load=0,
            status="operational",
            last_maintenance=datetime.now()
        )
        
        self.active_gateways[channel_id] = secure_gateway
        
        # Generate encryption keys for channel
        key_pair = f"0x{random.randint(0x100000, 0xFFFFFF):X}_{random.randint(0x100000, 0xFFFFFF):X}"
        self.encryption_keys[channel_id] = {
            "key_pair": key_pair,
            "creation_time": datetime.now(),
            "security_level": security_level
        }
        
        logger.info(f"🔐 Secure channel established: {channel_id}")
        logger.info(f"🔒 Security level: {security_level:.2%}")
        
        return channel_id
        
    def broadcast_emergency_message(self, source_domain: str, sender: str, 
                                  content: Dict[str, Any]) -> List[BridgeMessage]:
        """Broadcast emergency melding til alle domener"""
        logger.warning(f"🚨 EMERGENCY BROADCAST from {sender}@{source_domain}")
        
        target_domains = ["skyskraper", "rustbelt", "bridge"]
        emergency_messages = []
        
        for target_domain in target_domains:
            if target_domain != source_domain:
                message = self.send_message(
                    source_domain=source_domain,
                    target_domain=target_domain,
                    sender=sender,
                    recipient="ALL",
                    content=content,
                    priority=MessagePriority.EMERGENCY,
                    protocol=BridgeProtocol.EMERGENCY_BROADCAST
                )
                emergency_messages.append(message)
                
        logger.warning(f"📢 Emergency broadcast sent to {len(emergency_messages)} domains")
        return emergency_messages
        
    def analyze_communication_patterns(self, hours_back: int = 24) -> Dict[str, Any]:
        """Analyser kommunikasjonsmønstre for anomalier"""
        cutoff_time = datetime.now() - timedelta(hours=hours_back)
        recent_messages = [msg for msg in self.message_history 
                          if msg.timestamp > cutoff_time]
        
        if not recent_messages:
            return {"error": "No recent messages to analyze"}
            
        # Basic statistics
        total_messages = len(recent_messages)
        successful_deliveries = len([m for m in recent_messages 
                                   if m.delivery_status == CommunicationStatus.SUCCESS])
        
        # Domain activity
        domain_activity = defaultdict(int)
        for message in recent_messages:
            domain_activity[message.source_domain] += 1
            domain_activity[message.target_domain] += 1
            
        # Interference analysis
        interference_count = len([m for m in recent_messages if m.interference_detected])
        
        # Protocol usage
        protocol_usage = defaultdict(int)
        for message in recent_messages:
            protocol_usage[message.protocol.value] += 1
            
        # Gateway load analysis
        gateway_loads = {gw_id: gw.current_load for gw_id, gw in self.active_gateways.items()}
        
        analysis = {
            "analysis_period_hours": hours_back,
            "total_messages": total_messages,
            "successful_deliveries": successful_deliveries,
            "delivery_success_rate": successful_deliveries / total_messages if total_messages > 0 else 0,
            "interference_incidents": interference_count,
            "interference_rate": interference_count / total_messages if total_messages > 0 else 0,
            "domain_activity": dict(domain_activity),
            "protocol_usage": dict(protocol_usage),
            "gateway_loads": gateway_loads,
            "active_gateways": len(self.active_gateways),
            "queued_messages": len(self.message_queue),
            "analysis_timestamp": datetime.now().isoformat()
        }
        
        return analysis
        
    def get_bridge_status(self) -> Dict[str, Any]:
        """Hent komplett bridge status"""
        recent_interference = []
        for domain_pair, patterns in self.interference_patterns.items():
            recent_patterns = [p for p in patterns 
                             if p["timestamp"] > datetime.now() - timedelta(hours=1)]
            if recent_patterns:
                recent_interference.append({
                    "domain_pair": domain_pair,
                    "incident_count": len(recent_patterns),
                    "latest_effect": recent_patterns[-1]["effect"]
                })
                
        return {
            "bridge_name": self.bridge_name,
            "active_gateways": len(self.active_gateways),
            "message_queue_size": len(self.message_queue),
            "total_messages_processed": len(self.message_history),
            "recent_interference_incidents": len(recent_interference),
            "interference_patterns": recent_interference,
            "secure_channels_active": len(self.encryption_keys),
            "communication_logs": len(self.communication_logs),
            "last_update": datetime.now().isoformat(),
            "bridge_signature": "0xCROSS_DOMAIN_BRIDGE_OPERATIONAL"
        }

if __name__ == "__main__":
    # Demo of Domain Bridge Systems
    print("🌐✨ DOMAIN BRIDGE SYSTEMS DEMO ✨🌐")
    print("=" * 50)
    
    # Mock core system
    class MockCore:
        def __init__(self):
            self.usynlige_hand = MockUsynligeHand()
            
    class MockUsynligeHand:
        def check_for_interference(self, source, target, action_type):
            return random.random() < 0.3  # 30% chance of interference
            
        def apply_interference(self, data):
            corrupted = data.copy()
            corrupted["_corruption_signature"] = "0xDEADBEEF_INTERFERENCE"
            return corrupted
    
    # Initialize bridge system
    mock_core = MockCore()
    bridge = DomainBridge(mock_core)
    
    # Test message sending
    print("\n📨 Testing message transmission...")
    message1 = bridge.send_message(
        source_domain="skyskraper",
        target_domain="rustbelt", 
        sender="Astrid_Moller",
        recipient="Iron_Maiden",
        content={"subject": "Resource allocation proposal", "data": {"resources": ["water", "power"], "allocation": [0.6, 0.4]}},
        priority=MessagePriority.HIGH,
        protocol=BridgeProtocol.ENCRYPTED_CHANNEL
    )
    print(f"📬 Message 1: {message1.delivery_status.value} (Interference: {message1.interference_detected})")
    
    # Test emergency broadcast
    print("\n🚨 Testing emergency broadcast...")
    emergency_messages = bridge.broadcast_emergency_message(
        source_domain="rustbelt",
        sender="Iron_Maiden",
        content={"alert": "Massive corruption detected in sector 7", "threat_level": "CRITICAL", "immediate_action_required": True}
    )
    print(f"📢 Emergency broadcast sent: {len(emergency_messages)} messages")
    
    # Test secure channel
    print("\n🔐 Testing secure channel establishment...")
    secure_channel = bridge.establish_secure_channel("skyskraper", "rustbelt", 0.9)
    print(f"🔒 Secure channel established: {secure_channel}")
    
    # Test message retry
    print("\n🔄 Testing message retry system...")
    retry_stats = bridge.retry_failed_messages()
    print(f"♻️ Retry results: {retry_stats}")
    
    # Communication analysis
    print("\n📊 Testing communication analysis...")
    analysis = bridge.analyze_communication_patterns(1)  # Last 1 hour
    print(f"📈 Analysis: {json.dumps(analysis, indent=2, default=str)}")
    
    # Bridge status
    status = bridge.get_bridge_status()
    print(f"\n🌐 Bridge Status: {json.dumps(status, indent=2)}")
    
    print("\n✨ Domain Bridge Demo complete ✨")
