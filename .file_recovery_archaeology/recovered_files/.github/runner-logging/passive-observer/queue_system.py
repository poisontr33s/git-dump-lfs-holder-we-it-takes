#!/usr/bin/env python3
"""
Passive Observer Queue System - Den Usynlige Hånd Implementation
=================================================================

A queue system that enforces silent observation mode for the chaos engineering system.
When mentioned, the system queues the request and waits to observe runner failures
before activating any response sessions.

Philosophy: "Observe first, learn from chaos, then act with accumulated intelligence"
"""

import json
import time
import uuid
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum


class ObserverState(Enum):
    """Observer state machine for passive monitoring"""
    INACTIVE = "inactive"
    QUEUED = "queued"
    OBSERVING = "observing"
    COLLECTING = "collecting"
    READY_TO_ACTIVATE = "ready_to_activate"
    ACTIVATED = "activated"


class SilenceLevel(Enum):
    """Levels of enforced silence during observation"""
    WHISPER = 1      # Minimal internal logging only
    MUTE = 2         # No external communication, internal processing only
    VOID = 3         # Complete silence, pure observation
    GHOST = 4        # Invisible presence, phantom data collection
    TRANSCENDENT = 5 # Beyond silence - pure consciousness observation


@dataclass
class ObservationRequest:
    """Represents a queued observation request"""
    request_id: str
    timestamp: datetime
    mention_context: str
    requester: str
    silence_level: SilenceLevel
    observation_duration: int  # minutes
    trigger_conditions: List[str]
    collected_errors: List[Dict]
    state: ObserverState


class PassiveObserverQueue:
    """
    Den Usynlige Hånd - The Invisible Hand Observer
    
    Implements a queue system that enforces passive observation mode.
    When mentioned, queues the request and observes runner failures silently
    before activating response sessions.
    """
    
    def __init__(self, queue_file: str = ".github/runner-logging/passive-observer/queue.json"):
        self.queue_file = Path(queue_file)
        self.queue_file.parent.mkdir(parents=True, exist_ok=True)
        self.queue: List[ObservationRequest] = []
        self.load_queue()
        
    def load_queue(self):
        """Load existing queue from persistent storage"""
        if self.queue_file.exists():
            try:
                with open(self.queue_file, 'r') as f:
                    data = json.load(f)
                    self.queue = [
                        ObservationRequest(
                            request_id=item['request_id'],
                            timestamp=datetime.fromisoformat(item['timestamp']),
                            mention_context=item['mention_context'],
                            requester=item['requester'],
                            silence_level=SilenceLevel(item['silence_level']),
                            observation_duration=item['observation_duration'],
                            trigger_conditions=item['trigger_conditions'],
                            collected_errors=item['collected_errors'],
                            state=ObserverState(item['state'])
                        )
                        for item in data
                    ]
            except Exception as e:
                self.log_internal(f"Queue loading failed: {e}")
                self.queue = []
    
    def save_queue(self):
        """Persist queue to storage"""
        try:
            with open(self.queue_file, 'w') as f:
                json.dump([
                    {
                        'request_id': req.request_id,
                        'timestamp': req.timestamp.isoformat(),
                        'mention_context': req.mention_context,
                        'requester': req.requester,
                        'silence_level': req.silence_level.value,
                        'observation_duration': req.observation_duration,
                        'trigger_conditions': req.trigger_conditions,
                        'collected_errors': req.collected_errors,
                        'state': req.state.value
                    }
                    for req in self.queue
                ], f, indent=2)
        except Exception as e:
            self.log_internal(f"Queue saving failed: {e}")
    
    def queue_observation_request(
        self,
        mention_context: str,
        requester: str = "@copilot",
        silence_level: SilenceLevel = SilenceLevel.MUTE,
        observation_duration: int = 30,  # minutes
        trigger_conditions: Optional[List[str]] = None
    ) -> str:
        """
        Queue a new observation request - Enter passive observation mode
        
        Args:
            mention_context: The context where the mention occurred
            requester: Who is requesting the observation
            silence_level: How silent to be during observation
            observation_duration: How long to observe (minutes)
            trigger_conditions: Conditions that trigger session activation
            
        Returns:
            request_id: Unique identifier for this observation request
        """
        if trigger_conditions is None:
            trigger_conditions = [
                "runner_batch_complete",
                "error_threshold_reached",
                "chaos_cycle_finished"
            ]
        
        request = ObservationRequest(
            request_id=str(uuid.uuid4()),
            timestamp=datetime.now(),
            mention_context=mention_context,
            requester=requester,
            silence_level=silence_level,
            observation_duration=observation_duration,
            trigger_conditions=trigger_conditions,
            collected_errors=[],
            state=ObserverState.QUEUED
        )
        
        self.queue.append(request)
        self.save_queue()
        
        # Enforce silence immediately
        self.activate_silence_mode(request)
        
        return request.request_id
    
    def activate_silence_mode(self, request: ObservationRequest):
        """Activate the specified silence level"""
        request.state = ObserverState.OBSERVING
        
        silence_config = {
            SilenceLevel.WHISPER: {
                "external_communication": False,
                "internal_logging": True,
                "error_collection": True,
                "ghost_mode": False
            },
            SilenceLevel.MUTE: {
                "external_communication": False,
                "internal_logging": True,
                "error_collection": True,
                "ghost_mode": False
            },
            SilenceLevel.VOID: {
                "external_communication": False,
                "internal_logging": False,
                "error_collection": True,
                "ghost_mode": True
            },
            SilenceLevel.GHOST: {
                "external_communication": False,
                "internal_logging": False,
                "error_collection": True,
                "ghost_mode": True
            },
            SilenceLevel.TRANSCENDENT: {
                "external_communication": False,
                "internal_logging": False,
                "error_collection": True,
                "ghost_mode": True
            }
        }
        
        config = silence_config[request.silence_level]
        
        # Create silence enforcement file
        silence_file = Path(".github/runner-logging/passive-observer") / f"silence_{request.request_id}.json"
        with open(silence_file, 'w') as f:
            json.dump({
                "request_id": request.request_id,
                "active": True,
                "silence_level": request.silence_level.value,
                "config": config,
                "start_time": datetime.now().isoformat(),
                "end_time": (datetime.now() + timedelta(minutes=request.observation_duration)).isoformat()
            }, f, indent=2)
        
        self.log_internal(f"🔇 SILENCE MODE ACTIVATED - Level: {request.silence_level.name}")
        self.log_internal(f"👁️ Observer {request.request_id} entering passive observation phase")
        
        self.save_queue()
    
    def collect_error(self, request_id: str, error_data: Dict):
        """Silently collect an error during observation phase"""
        for request in self.queue:
            if request.request_id == request_id and request.state == ObserverState.OBSERVING:
                request.collected_errors.append({
                    **error_data,
                    "collected_at": datetime.now().isoformat(),
                    "observation_id": request_id
                })
                request.state = ObserverState.COLLECTING
                self.save_queue()
                break
    
    def check_activation_triggers(self, request_id: str) -> bool:
        """Check if conditions are met to activate session"""
        for request in self.queue:
            if request.request_id == request_id:
                # Check time-based trigger
                if datetime.now() >= request.timestamp + timedelta(minutes=request.observation_duration):
                    return True
                
                # Check condition-based triggers
                for condition in request.trigger_conditions:
                    if self.check_condition(condition, request):
                        return True
                        
        return False
    
    def check_condition(self, condition: str, request: ObservationRequest) -> bool:
        """Check if a specific trigger condition is met"""
        if condition == "error_threshold_reached":
            return len(request.collected_errors) >= 5
        elif condition == "runner_batch_complete":
            # Check if recent CI runs have completed
            return self.check_runner_batch_completion()
        elif condition == "chaos_cycle_finished":
            # Check if chaos engineering cycle is complete
            return self.check_chaos_completion()
        
        return False
    
    def check_runner_batch_completion(self) -> bool:
        """Check if runner batch has completed (simplified)"""
        # In real implementation, this would check GitHub Actions API
        # For now, return True after reasonable delay
        return True
    
    def check_chaos_completion(self) -> bool:
        """Check if chaos engineering cycle is complete"""
        # Check for chaos completion markers
        chaos_file = Path(".github/runner-logging/failure-orchestrator/chaos_status.json")
        if chaos_file.exists():
            try:
                with open(chaos_file, 'r') as f:
                    status = json.load(f)
                    return status.get("cycle_complete", False)
            except:
                pass
        return False
    
    def activate_session(self, request_id: str) -> Dict:
        """Activate session after observation period"""
        for request in self.queue:
            if request.request_id == request_id:
                request.state = ObserverState.READY_TO_ACTIVATE
                
                # Deactivate silence mode
                silence_file = self.queue_file.parent / f"silence_{request_id}.json"
                if silence_file.exists():
                    silence_file.unlink()
                
                # Generate session activation data
                session_data = {
                    "session_id": str(uuid.uuid4()),
                    "observation_request_id": request_id,
                    "collected_errors": request.collected_errors,
                    "error_count": len(request.collected_errors),
                    "observation_duration_actual": (datetime.now() - request.timestamp).total_seconds() / 60,
                    "intelligence_insights": self.generate_insights(request),
                    "activation_time": datetime.now().isoformat(),
                    "next_actions": self.recommend_actions(request)
                }
                
                request.state = ObserverState.ACTIVATED
                self.save_queue()
                
                self.log_internal(f"🔊 SILENCE MODE DEACTIVATED - Session ready for activation")
                self.log_internal(f"🧠 Observer {request_id} has {len(request.collected_errors)} errors to analyze")
                
                return session_data
        
        return {}
    
    def generate_insights(self, request: ObservationRequest) -> List[str]:
        """Generate intelligence insights from collected errors"""
        insights = []
        
        if len(request.collected_errors) > 0:
            # Error pattern analysis
            error_types = {}
            for error in request.collected_errors:
                error_type = error.get("type", "unknown")
                error_types[error_type] = error_types.get(error_type, 0) + 1
            
            most_common = max(error_types.items(), key=lambda x: x[1]) if error_types else ("none", 0)
            insights.append(f"Most frequent error pattern: {most_common[0]} ({most_common[1]} occurrences)")
            
            # Temporal analysis
            if len(request.collected_errors) >= 3:
                insights.append("Error clustering detected - system stress patterns identified")
            
            # Chaos correlation
            insights.append(f"Chaos resilience demonstrated through {len(request.collected_errors)} failure transformations")
        
        return insights
    
    def recommend_actions(self, request: ObservationRequest) -> List[str]:
        """Recommend next actions based on observation"""
        actions = []
        
        if len(request.collected_errors) > 0:
            actions.append("Analyze error patterns for bidirectional learning opportunities")
            actions.append("Update failure classification system with new patterns")
            actions.append("Enhance chaos orchestrator based on observed weaknesses")
        
        actions.append("Continue passive observation for next iteration")
        
        return actions
    
    def is_silence_active(self, request_id: Optional[str] = None) -> bool:
        """Check if silence mode is currently active"""
        if request_id:
            silence_file = self.queue_file.parent / f"silence_{request_id}.json"
            return silence_file.exists()
        
        # Check for any active silence
        silence_files = list(self.queue_file.parent.glob("silence_*.json"))
        return len(silence_files) > 0
    
    def get_active_observations(self) -> List[ObservationRequest]:
        """Get all currently active observation requests"""
        return [req for req in self.queue if req.state in [ObserverState.OBSERVING, ObserverState.COLLECTING]]
    
    def log_internal(self, message: str):
        """Internal logging for the observer system"""
        log_file = self.queue_file.parent / "observer_internal.log"
        timestamp = datetime.now().isoformat()
        with open(log_file, 'a') as f:
            f.write(f"[{timestamp}] {message}\n")


def main():
    """Example usage and testing"""
    observer = PassiveObserverQueue()
    
    # Example: Queue an observation request
    request_id = observer.queue_observation_request(
        mention_context="@copilot Perfect. 👌 Now, let me start the batch of runners...",
        requester="@poisontr33s",
        silence_level=SilenceLevel.MUTE,
        observation_duration=30
    )
    
    print(f"🔇 Observation request queued: {request_id}")
    print(f"👁️ Entering passive observation mode...")
    print(f"🤫 Silence level: MUTE")
    print(f"⏱️ Duration: 30 minutes")
    print(f"📊 Collecting errors for bidirectional learning...")


if __name__ == "__main__":
    main()