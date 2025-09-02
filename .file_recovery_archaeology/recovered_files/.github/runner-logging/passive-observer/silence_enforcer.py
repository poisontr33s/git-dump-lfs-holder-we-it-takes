#!/usr/bin/env python3
"""
Silence Enforcement Module
==========================

A module that enforces silence during observation periods.
When the passive observer is active, this module prevents any external
communication and ensures pure observation mode.
"""

import json
import os
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any


class SilenceEnforcer:
    """
    Enforces silence during passive observation periods.
    
    This module acts as a gatekeeper that prevents any external communication
    when the observer is in passive mode, ensuring pure data collection.
    """
    
    def __init__(self, observer_dir: str = ".github/runner-logging/passive-observer"):
        self.observer_dir = Path(observer_dir)
        self.observer_dir.mkdir(parents=True, exist_ok=True)
    
    def is_silence_active(self) -> tuple[bool, Optional[Dict]]:
        """
        Check if silence mode is currently active
        
        Returns:
            (is_active, silence_config): Tuple of whether silence is active and config if so
        """
        silence_files = list(self.observer_dir.glob("silence_*.json"))
        
        if not silence_files:
            return False, None
        
        # Check if any silence file is still active
        for silence_file in silence_files:
            try:
                with open(silence_file, 'r') as f:
                    config = json.load(f)
                    
                    if config.get("active", False):
                        end_time = datetime.fromisoformat(config["end_time"])
                        if datetime.now() < end_time:
                            return True, config
                        else:
                            # Expired silence file - clean up
                            silence_file.unlink()
            except Exception:
                # Corrupted silence file - remove it
                silence_file.unlink()
        
        return False, None
    
    def enforce_silence(self, action: str, context: Dict[str, Any] = None) -> bool:
        """
        Enforce silence for a given action
        
        Args:
            action: The action being attempted (e.g., "comment_reply", "external_communication")
            context: Additional context for the action
            
        Returns:
            bool: Whether the action should be allowed (False = blocked by silence)
        """
        is_silent, config = self.is_silence_active()
        
        if not is_silent:
            return True  # No silence - allow action
        
        # Check action against silence configuration
        silence_config = config.get("config", {})
        
        action_rules = {
            "comment_reply": silence_config.get("external_communication", False),
            "external_communication": silence_config.get("external_communication", False), 
            "internal_logging": silence_config.get("internal_logging", True),
            "error_collection": silence_config.get("error_collection", True),
            "ghost_mode": silence_config.get("ghost_mode", False)
        }
        
        allowed = action_rules.get(action, False)
        
        if not allowed:
            self.log_blocked_action(action, context, config)
        
        return allowed
    
    def log_blocked_action(self, action: str, context: Dict, silence_config: Dict):
        """Log when an action is blocked by silence mode"""
        log_file = self.observer_dir / "blocked_actions.log"
        
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "action": action,
            "context": context or {},
            "silence_level": silence_config.get("silence_level", "unknown"),
            "request_id": silence_config.get("request_id", "unknown"),
            "status": "BLOCKED_BY_SILENCE"
        }
        
        with open(log_file, 'a') as f:
            f.write(json.dumps(log_entry) + "\n")
    
    def queue_action_for_later(self, action: str, context: Dict, priority: int = 1):
        """Queue an action to be executed after silence period ends"""
        queue_file = self.observer_dir / "queued_actions.json"
        
        queued_action = {
            "id": f"action_{datetime.now().timestamp()}",
            "action": action,
            "context": context,
            "priority": priority,
            "queued_at": datetime.now().isoformat(),
            "status": "queued"
        }
        
        # Load existing queue
        queued_actions = []
        if queue_file.exists():
            try:
                with open(queue_file, 'r') as f:
                    queued_actions = json.load(f)
            except:
                queued_actions = []
        
        # Add new action
        queued_actions.append(queued_action)
        
        # Save updated queue
        with open(queue_file, 'w') as f:
            json.dump(queued_actions, f, indent=2)
    
    def get_silence_status(self) -> Dict[str, Any]:
        """Get detailed status of current silence mode"""
        is_silent, config = self.is_silence_active()
        
        if not is_silent:
            return {"active": False, "status": "No active silence mode"}
        
        return {
            "active": True,
            "request_id": config.get("request_id", "unknown"),
            "silence_level": config.get("silence_level", "unknown"),
            "start_time": config.get("start_time"),
            "end_time": config.get("end_time"),
            "configuration": config.get("config", {}),
            "time_remaining": self._calculate_time_remaining(config.get("end_time"))
        }
    
    def _calculate_time_remaining(self, end_time_str: str) -> Optional[str]:
        """Calculate time remaining in silence period"""
        try:
            end_time = datetime.fromisoformat(end_time_str)
            remaining = end_time - datetime.now()
            
            if remaining.total_seconds() <= 0:
                return "Expired"
            
            hours, remainder = divmod(remaining.total_seconds(), 3600)
            minutes, seconds = divmod(remainder, 60)
            
            if hours > 0:
                return f"{int(hours)}h {int(minutes)}m"
            else:
                return f"{int(minutes)}m {int(seconds)}s"
        except:
            return None


# Global silence enforcer instance
_silence_enforcer = None


def get_silence_enforcer() -> SilenceEnforcer:
    """Get the global silence enforcer instance"""
    global _silence_enforcer
    if _silence_enforcer is None:
        _silence_enforcer = SilenceEnforcer()
    return _silence_enforcer


def check_silence_before_action(action: str, context: Dict[str, Any] = None) -> bool:
    """
    Decorator function to check silence before performing an action
    
    Usage:
        if not check_silence_before_action("comment_reply", {"comment_id": 123}):
            return  # Action blocked by silence
    """
    return get_silence_enforcer().enforce_silence(action, context)


def silence_status() -> Dict[str, Any]:
    """Get current silence status"""
    return get_silence_enforcer().get_silence_status()


def main():
    """Testing and demonstration"""
    enforcer = SilenceEnforcer()
    
    print("🔇 Silence Enforcer Status:")
    status = enforcer.get_silence_status()
    print(json.dumps(status, indent=2))
    
    # Test enforcement
    actions_to_test = [
        "comment_reply",
        "external_communication", 
        "internal_logging",
        "error_collection"
    ]
    
    for action in actions_to_test:
        allowed = enforcer.enforce_silence(action, {"test": True})
        print(f"Action '{action}': {'✅ ALLOWED' if allowed else '❌ BLOCKED'}")


if __name__ == "__main__":
    main()