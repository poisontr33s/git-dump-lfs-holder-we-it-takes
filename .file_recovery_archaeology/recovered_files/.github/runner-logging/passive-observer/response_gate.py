#!/usr/bin/env python3
"""
Passive Observer - Response Gate
================================

This script acts as a gate that determines whether the system should respond
to interactions or remain in passive observation mode.

Use this as a check before any external communication to ensure
the "do nothing" mode is respected.
"""

import sys
import json
from pathlib import Path
from datetime import datetime

# Add the passive observer modules to path
sys.path.append(str(Path(__file__).parent))

from silence_enforcer import check_silence_before_action, silence_status


def should_respond_to_comment(comment_id: str = None, action_type: str = "comment_reply") -> dict:
    """
    Check if the system should respond to a comment or remain silent
    
    Args:
        comment_id: The ID of the comment (optional)
        action_type: Type of action ("comment_reply", "external_communication", etc.)
        
    Returns:
        dict: Response decision with reasoning
    """
    
    # Check if silence is active
    status = silence_status()
    
    if not status["active"]:
        return {
            "should_respond": True,
            "reason": "No passive observation active",
            "action": "NORMAL_RESPONSE",
            "silence_active": False
        }
    
    # Check if this specific action is allowed
    context = {"comment_id": comment_id} if comment_id else {}
    allowed = check_silence_before_action(action_type, context)
    
    if not allowed:
        return {
            "should_respond": False,
            "reason": f"Blocked by passive observation - {status['silence_level']} level silence",
            "action": "REMAIN_SILENT",
            "silence_active": True,
            "silence_info": {
                "request_id": status["request_id"],
                "time_remaining": status["time_remaining"],
                "mode": "PURE_OBSERVATION"
            },
            "philosophy": "Den Usynlige Hånd observes without interference"
        }
    
    return {
        "should_respond": True,
        "reason": f"Action '{action_type}' allowed during observation",
        "action": "LIMITED_RESPONSE",
        "silence_active": True
    }


def log_interaction_attempt(comment_id: str, decision: dict):
    """Log when an interaction is attempted during silence"""
    log_file = Path(".github/runner-logging/passive-observer/interaction_log.json")
    
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "comment_id": comment_id,
        "decision": decision,
        "interaction_type": "comment_processing"
    }
    
    # Load existing log
    log_entries = []
    if log_file.exists():
        try:
            with open(log_file, 'r') as f:
                log_entries = json.load(f)
        except:
            log_entries = []
    
    # Add new entry
    log_entries.append(log_entry)
    
    # Keep only last 100 entries
    log_entries = log_entries[-100:]
    
    # Save updated log
    log_file.parent.mkdir(parents=True, exist_ok=True)
    with open(log_file, 'w') as f:
        json.dump(log_entries, f, indent=2)


def main():
    """
    Main function for command-line usage
    
    Usage:
        python response_gate.py [comment_id] [action_type]
    """
    
    # Parse command line arguments
    comment_id = sys.argv[1] if len(sys.argv) > 1 else "3138748419"
    action_type = sys.argv[2] if len(sys.argv) > 2 else "comment_reply"
    
    print("🚪 PASSIVE OBSERVER - RESPONSE GATE")
    print("=" * 40)
    
    # Check if should respond
    decision = should_respond_to_comment(comment_id, action_type)
    
    print(f"📋 Input:")
    print(f"   Comment ID: {comment_id}")
    print(f"   Action Type: {action_type}")
    
    print(f"\n🎯 Decision:")
    print(f"   Should Respond: {decision['should_respond']}")
    print(f"   Reason: {decision['reason']}")
    print(f"   Action: {decision['action']}")
    print(f"   Silence Active: {decision['silence_active']}")
    
    if decision.get('silence_info'):
        print(f"\n🔇 Silence Information:")
        print(f"   Request ID: {decision['silence_info']['request_id']}")
        print(f"   Time Remaining: {decision['silence_info']['time_remaining']}")
        print(f"   Mode: {decision['silence_info']['mode']}")
    
    if decision.get('philosophy'):
        print(f"\n💭 Philosophy:")
        print(f"   {decision['philosophy']}")
    
    # Log the interaction attempt
    log_interaction_attempt(comment_id, decision)
    
    # Return appropriate exit code
    if decision['should_respond']:
        print(f"\n✅ PROCEED WITH RESPONSE")
        return 0
    else:
        print(f"\n🤫 MAINTAIN SILENCE - DO NOT RESPOND")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)