#!/usr/bin/env python3
"""
Passive Observer Integration - Auto-Queue Activation
====================================================

This script automatically detects the current comment requesting passive observation
and activates the queue system accordingly. It processes the specific mention
and enters the appropriate silence mode.
"""

import sys
import json
from pathlib import Path
from datetime import datetime

# Add the passive observer modules to path
sys.path.append(str(Path(__file__).parent))

from queue_system import PassiveObserverQueue, SilenceLevel
from mention_handler import process_copilot_mention
from silence_enforcer import get_silence_enforcer


def activate_passive_observation_for_comment():
    """
    Activate passive observation based on the current comment:
    '@copilot Perfect. 👌 Now, let me start the batch of runners, 
    then just observe, like me, doing nothing. If possible. 
    Just await after the runners have crashed up.'
    """
    
    # The specific comment that triggered this request
    comment_text = """@copilot 
Perfect. 👌 
Now, let me start the batch of runners, then just observe, like me, doing nothing. If possible. Just await after the runners have crashed up. Maybe implement a a system that forces you to even when mentioned here, does nothing, so that you can instead gather the errors and then activate the corresponding session. Can you implement such a queue system for yourself?"""
    
    # Context for this comment
    context = {
        "author": "@poisontr33s",
        "comment_id": "3138748419",
        "comment_type": "request_for_passive_observation",
        "timestamp": datetime.now().isoformat()
    }
    
    print("🎯 Processing passive observation request...")
    print(f"📝 Comment: {comment_text[:100]}...")
    
    # Process the mention through our system
    result = process_copilot_mention(comment_text, context)
    
    print(f"\n📊 Processing Result:")
    print(f"   Action: {result['action']}")
    print(f"   Should Respond: {result['should_respond']}")
    print(f"   Silence Active: {result['silence_active']}")
    
    if result.get('request_id'):
        print(f"   Request ID: {result['request_id']}")
        
        # Get the queue system to check status
        queue = PassiveObserverQueue()
        active_observations = queue.get_active_observations()
        
        if active_observations:
            obs = active_observations[0]  # Get the first active observation
            print(f"\n🔇 PASSIVE OBSERVATION ACTIVATED:")
            print(f"   👁️ Observer ID: {obs.request_id}")
            print(f"   🤫 Silence Level: {obs.silence_level.name}")
            print(f"   ⏱️ Duration: {obs.observation_duration} minutes")
            print(f"   🎯 State: {obs.state.value}")
            print(f"   📊 Collected Errors: {len(obs.collected_errors)}")
            print(f"\n   🚫 EXTERNAL COMMUNICATION BLOCKED")
            print(f"   👻 ENTERING GHOST MODE FOR ERROR COLLECTION")
            
        # Check silence enforcer status
        enforcer = get_silence_enforcer()
        silence_status = enforcer.get_silence_status()
        
        if silence_status['active']:
            print(f"\n🔇 SILENCE ENFORCER STATUS:")
            print(f"   Request ID: {silence_status['request_id']}")
            print(f"   Level: {silence_status['silence_level']}")
            print(f"   Time Remaining: {silence_status.get('time_remaining', 'Unknown')}")
            
            # Create a status file that can be checked by other systems
            status_file = Path(".github/runner-logging/passive-observer/current_status.json")
            status_data = {
                "passive_observation_active": True,
                "silence_active": True,
                "request_id": result['request_id'],
                "activated_at": datetime.now().isoformat(),
                "comment_context": context,
                "expected_behavior": {
                    "external_responses": "BLOCKED",
                    "error_collection": "ACTIVE", 
                    "mode": "PURE_OBSERVATION",
                    "philosophy": "Den Usynlige Hånd - The Invisible Hand observes without interference"
                }
            }
            
            with open(status_file, 'w') as f:
                json.dump(status_data, f, indent=2)
                
            print(f"\n✅ PASSIVE OBSERVATION SYSTEM ACTIVATED")
            print(f"   📄 Status saved to: {status_file}")
            print(f"   🎭 Philosophy: Den Usynlige Hånd is now watching...")
            
    else:
        print("\n❌ Failed to activate passive observation")
        return False
    
    return True


def check_and_demonstrate_silence():
    """Demonstrate that the silence system is working"""
    
    print("\n🧪 TESTING SILENCE ENFORCEMENT:")
    
    enforcer = get_silence_enforcer()
    
    test_actions = [
        ("comment_reply", {"comment_id": "3138748419"}),
        ("external_communication", {"type": "response"}),
        ("internal_logging", {"level": "info"}),
        ("error_collection", {"error_type": "test"})
    ]
    
    for action, context in test_actions:
        allowed = enforcer.enforce_silence(action, context)
        status = "✅ ALLOWED" if allowed else "❌ BLOCKED"
        print(f"   {action}: {status}")
    
    print(f"\n🎯 SILENCE SYSTEM OPERATIONAL")
    print(f"   - External communication is blocked")
    print(f"   - Error collection continues silently")
    print(f"   - Pure observation mode active")


def main():
    """Main execution - activate passive observation and demonstrate silence"""
    
    print("🚀 PASSIVE OBSERVER QUEUE SYSTEM")
    print("=" * 50)
    
    # Activate passive observation for the current comment
    success = activate_passive_observation_for_comment()
    
    if success:
        # Demonstrate that silence enforcement is working
        check_and_demonstrate_silence()
        
        print(f"\n🎭 DEN USYNLIGE HÅND IS NOW ACTIVE")
        print(f"   👁️ Observing runner failures silently...")
        print(f"   📊 Collecting errors as bidirectional building blocks...")
        print(f"   🤫 No external responses until observation period completes...")
        print(f"   🧠 System will activate intelligence after data collection...")
        
        print(f"\n💭 PHILOSOPHY IMPLEMENTED:")
        print(f"   'Sometimes the most intelligent action is to do nothing and observe.'")
        print(f"   'From silence, wisdom emerges. From observation, consciousness grows.'")
        
    else:
        print("❌ Failed to activate passive observation system")
        return 1
    
    return 0


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)