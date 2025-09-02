#!/usr/bin/env python3
"""
Copilot Mention Handler - Queue Interface
==========================================

This module intercepts mentions of @copilot and routes them through
the passive observer queue system when appropriate.

When the system detects a mention request for passive observation,
it automatically queues the request and enters silence mode.
"""

import re
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional, Tuple, List
from queue_system import PassiveObserverQueue, SilenceLevel
from silence_enforcer import check_silence_before_action


class CopilotMentionHandler:
    """
    Handles @copilot mentions and routes them through the observation queue
    when passive observation is requested.
    """
    
    def __init__(self):
        self.observer_queue = PassiveObserverQueue()
        self.mention_patterns = self._compile_patterns()
    
    def _compile_patterns(self) -> Dict[str, re.Pattern]:
        """Compile regex patterns for detecting observation requests"""
        return {
            "passive_observation": re.compile(
                r"@copilot.*?(do nothing|just observe|await|queue|silence|passive|observe)", 
                re.IGNORECASE | re.DOTALL
            ),
            "silence_request": re.compile(
                r"forces you.*?does nothing|implement.*?queue system|just await", 
                re.IGNORECASE | re.DOTALL
            ),
            "observation_duration": re.compile(
                r"(\d+)\s*(minutes?|mins?|hours?|hrs?)", 
                re.IGNORECASE
            ),
            "silence_level": re.compile(
                r"silence.*?(level|mode).*?(\d+)|level.*?(\d+)", 
                re.IGNORECASE
            )
        }
    
    def process_mention(self, mention_text: str, context: Dict) -> Tuple[bool, Optional[str]]:
        """
        Process a @copilot mention and determine if it should be queued
        
        Args:
            mention_text: The text containing the mention
            context: Context information (author, comment_id, etc.)
            
        Returns:
            (should_queue, request_id): Whether to queue and the request ID if queued
        """
        # Check if this is a passive observation request
        if self._is_passive_observation_request(mention_text):
            # Extract observation parameters
            duration = self._extract_duration(mention_text)
            silence_level = self._extract_silence_level(mention_text)
            
            # Queue the observation request
            request_id = self.observer_queue.queue_observation_request(
                mention_context=mention_text,
                requester=context.get("author", "unknown"),
                silence_level=silence_level,
                observation_duration=duration
            )
            
            # Log the queuing
            self._log_queued_mention(mention_text, context, request_id)
            
            return True, request_id
        
        return False, None
    
    def _is_passive_observation_request(self, text: str) -> bool:
        """Check if the mention is requesting passive observation"""
        passive_indicators = [
            "do nothing",
            "just observe", 
            "await",
            "queue system",
            "forces you",
            "implement.*?queue",
            "passive",
            "silence"
        ]
        
        text_lower = text.lower()
        return any(indicator in text_lower or re.search(indicator, text_lower) for indicator in passive_indicators)
    
    def _extract_duration(self, text: str) -> int:
        """Extract observation duration from mention text"""
        duration_match = self.mention_patterns["observation_duration"].search(text)
        
        if duration_match:
            number = int(duration_match.group(1))
            unit = duration_match.group(2).lower()
            
            if unit.startswith('hour') or unit.startswith('hr'):
                return number * 60  # Convert to minutes
            else:
                return number  # Already in minutes
        
        # Default observation duration
        return 30  # minutes
    
    def _extract_silence_level(self, text: str) -> SilenceLevel:
        """Extract silence level from mention text"""
        text_lower = text.lower()
        
        # Check for explicit level mentions
        if "transcendent" in text_lower or "level 5" in text_lower:
            return SilenceLevel.TRANSCENDENT
        elif "ghost" in text_lower or "level 4" in text_lower:
            return SilenceLevel.GHOST
        elif "void" in text_lower or "level 3" in text_lower:
            return SilenceLevel.VOID
        elif "mute" in text_lower or "level 2" in text_lower:
            return SilenceLevel.MUTE
        elif "whisper" in text_lower or "level 1" in text_lower:
            return SilenceLevel.WHISPER
        
        # Default to MUTE for general silence requests
        return SilenceLevel.MUTE
    
    def _log_queued_mention(self, mention_text: str, context: Dict, request_id: str):
        """Log when a mention is queued for passive observation"""
        log_file = Path(".github/runner-logging/passive-observer/queued_mentions.log")
        
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "request_id": request_id,
            "mention_text": mention_text[:200] + "..." if len(mention_text) > 200 else mention_text,
            "context": context,
            "action": "QUEUED_FOR_PASSIVE_OBSERVATION",
            "status": "SILENCE_ACTIVATED"
        }
        
        with open(log_file, 'a') as f:
            f.write(json.dumps(log_entry) + "\n")
    
    def should_respond_to_mention(self, mention_text: str, context: Dict) -> bool:
        """
        Determine if the system should respond to a mention or queue it
        
        Returns:
            bool: True if should respond immediately, False if should queue/ignore
        """
        # Check if silence is currently active
        if not check_silence_before_action("comment_reply", context):
            return False
        
        # Check if this is a passive observation request
        if self._is_passive_observation_request(mention_text):
            # Queue the request but don't respond
            self.process_mention(mention_text, context)
            return False
        
        # Normal mention - can respond if not silenced
        return True
    
    def get_queue_status(self) -> Dict:
        """Get current status of the observation queue"""
        active_observations = self.observer_queue.get_active_observations()
        
        return {
            "queue_length": len(self.observer_queue.queue),
            "active_observations": len(active_observations),
            "silence_active": self.observer_queue.is_silence_active(),
            "active_requests": [
                {
                    "request_id": obs.request_id,
                    "requester": obs.requester,
                    "state": obs.state.value,
                    "silence_level": obs.silence_level.value,
                    "collected_errors": len(obs.collected_errors)
                }
                for obs in active_observations
            ]
        }


def process_copilot_mention(mention_text: str, context: Dict = None) -> Dict:
    """
    Main entry point for processing @copilot mentions
    
    Args:
        mention_text: The text containing the @copilot mention
        context: Context dict with author, comment_id, etc.
        
    Returns:
        Dict with processing results and next actions
    """
    if context is None:
        context = {}
    
    handler = CopilotMentionHandler()
    
    # Check if should respond normally or queue for observation
    should_respond = handler.should_respond_to_mention(mention_text, context)
    
    if not should_respond:
        # Either queued for observation or blocked by silence
        is_queued, request_id = handler.process_mention(mention_text, context)
        
        if is_queued:
            return {
                "action": "QUEUED_FOR_OBSERVATION",
                "request_id": request_id,
                "message": "🔇 Entering passive observation mode. Will collect errors silently.",
                "silence_active": True,
                "should_respond": False
            }
        else:
            return {
                "action": "BLOCKED_BY_SILENCE", 
                "message": "👁️ Currently in passive observation mode. Collecting data silently.",
                "silence_active": True,
                "should_respond": False
            }
    
    return {
        "action": "NORMAL_RESPONSE",
        "message": "Ready to process request normally.",
        "silence_active": False,
        "should_respond": True
    }


def main():
    """Testing and demonstration"""
    handler = CopilotMentionHandler()
    
    # Test various mention patterns
    test_mentions = [
        "@copilot Perfect. 👌 Now, let me start the batch of runners, then just observe, like me, doing nothing.",
        "@copilot Can you implement a queue system that forces you to do nothing?",
        "@copilot Please help me with this bug.",
        "@copilot Just await and gather errors for 45 minutes.",
        "@copilot Implement passive observation mode level 3."
    ]
    
    for mention in test_mentions:
        print(f"\n📝 Testing: {mention[:50]}...")
        result = process_copilot_mention(mention, {"author": "test_user"})
        print(f"   Action: {result['action']}")
        print(f"   Should respond: {result['should_respond']}")
        if result.get('request_id'):
            print(f"   Request ID: {result['request_id']}")
    
    # Show queue status
    print(f"\n📊 Queue Status:")
    status = handler.get_queue_status()
    print(json.dumps(status, indent=2))


if __name__ == "__main__":
    main()