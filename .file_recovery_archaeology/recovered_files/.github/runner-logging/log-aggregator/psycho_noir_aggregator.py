#!/usr/bin/env python3
"""
Log Aggregator for Psycho-Noir Kontrapunkt CI/CD System

This module collects, processes, and structures all runner outputs into
a unified intelligence stream. Each log becomes part of the system's
evolving consciousness, contributing to the bidirectional learning process.

The aggregator operates on the "Syntetiske Synapser" principle - collecting
disparate data fragments and weaving them into coherent intelligence patterns.
"""

import json
import os
import re
import sys
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
import gzip
import base64

class LogFragment:
    """Represents a single log fragment in the consciousness stream."""
    
    def __init__(self, content: str, source: str, timestamp: str = None, 
                 metadata: Dict = None):
        self.content = content
        self.source = source
        self.timestamp = timestamp or datetime.now().isoformat()
        self.metadata = metadata or {}
        self.fragment_id = self._generate_fragment_id()
        self.processed = False
        
    def _generate_fragment_id(self) -> str:
        """Generate unique fragment identifier for tracking."""
        content_hash = hashlib.sha256(
            f"{self.content}{self.source}{self.timestamp}".encode()
        ).hexdigest()[:16]
        return f"fragment_{content_hash}"
    
    def to_dict(self) -> Dict:
        """Convert fragment to dictionary for serialization."""
        return {
            "fragment_id": self.fragment_id,
            "content": self.content,
            "source": self.source,
            "timestamp": self.timestamp,
            "metadata": self.metadata,
            "processed": self.processed
        }

class RunnerSession:
    """Represents a complete CI/CD runner session with all associated logs."""
    
    def __init__(self, session_id: str, runner_type: str, context: Dict = None):
        self.session_id = session_id
        self.runner_type = runner_type
        self.context = context or {}
        self.fragments = []
        self.start_time = datetime.now()
        self.end_time = None
        self.status = "RUNNING"
        self.intelligence_summary = {}
        
    def add_fragment(self, fragment: LogFragment):
        """Add a log fragment to this session."""
        self.fragments.append(fragment)
        
    def finalize_session(self, status: str = "COMPLETED"):
        """Mark session as complete and generate intelligence summary."""
        self.end_time = datetime.now()
        self.status = status
        self._generate_intelligence_summary()
        
    def _generate_intelligence_summary(self):
        """Generate intelligence summary for bidirectional learning."""
        self.intelligence_summary = {
            "session_duration": (self.end_time - self.start_time).total_seconds(),
            "fragment_count": len(self.fragments),
            "error_density": self._calculate_error_density(),
            "pattern_signatures": self._extract_pattern_signatures(),
            "learning_value": self._assess_learning_value()
        }
    
    def _calculate_error_density(self) -> float:
        """Calculate error density for the session."""
        if not self.fragments:
            return 0.0
        
        error_indicators = ['error', 'fail', 'exception', 'critical', 'fatal']
        error_lines = 0
        total_lines = 0
        
        for fragment in self.fragments:
            lines = fragment.content.split('\n')
            total_lines += len(lines)
            for line in lines:
                if any(indicator in line.lower() for indicator in error_indicators):
                    error_lines += 1
        
        return error_lines / max(total_lines, 1)
    
    def _extract_pattern_signatures(self) -> List[str]:
        """Extract unique pattern signatures for intelligence building."""
        signatures = set()
        
        for fragment in self.fragments:
            # Extract error patterns, build patterns, timing patterns
            patterns = re.findall(r'(ERROR:|WARN:|INFO:|Build|Test|Deploy)[^\\n]*', 
                                fragment.content, re.IGNORECASE)
            for pattern in patterns[:10]:  # Limit to prevent explosion
                signatures.add(pattern[:100])  # Truncate long patterns
        
        return list(signatures)
    
    def _assess_learning_value(self) -> float:
        """Assess the learning value of this session for bidirectional intelligence."""
        value = 0.0
        
        # High error density = high learning value (failures teach us)
        value += self.intelligence_summary["error_density"] * 3.0
        
        # Unique patterns = learning value
        value += len(self.intelligence_summary["pattern_signatures"]) * 0.1
        
        # Session duration impact (very short or very long sessions are interesting)
        duration = self.intelligence_summary["session_duration"]
        if duration < 30 or duration > 600:  # Less than 30s or more than 10min
            value += 1.0
        
        return min(value, 10.0)  # Cap at 10.0
    
    def to_dict(self) -> Dict:
        """Convert session to dictionary for serialization."""
        return {
            "session_id": self.session_id,
            "runner_type": self.runner_type,
            "context": self.context,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "status": self.status,
            "fragment_count": len(self.fragments),
            "intelligence_summary": self.intelligence_summary,
            "fragments": [fragment.to_dict() for fragment in self.fragments]
        }

class PsychoNoirLogAggregator:
    """
    Main log aggregation engine implementing the "Kausalitets-Arkitekt" pattern.
    
    Collects all runner outputs and weaves them into a unified intelligence
    fabric for bidirectional learning and system improvement.
    """
    
    def __init__(self, storage_path: str = None):
        self.storage_path = Path(storage_path or "/tmp/psycho-noir-logs")
        self.storage_path.mkdir(parents=True, exist_ok=True)
        
        self.active_sessions = {}
        self.completed_sessions = []
        self.intelligence_patterns = {}
        
        # Initialize intelligence tracking
        self.global_patterns = {
            "error_evolution": [],
            "success_pathways": [],
            "anomaly_clusters": [],
            "temporal_patterns": {}
        }
    
    def create_session(self, session_id: str, runner_type: str, 
                      context: Dict = None) -> RunnerSession:
        """Create a new runner session for log aggregation."""
        session = RunnerSession(session_id, runner_type, context)
        self.active_sessions[session_id] = session
        return session
    
    def add_log_content(self, session_id: str, content: str, source: str, 
                       metadata: Dict = None) -> bool:
        """Add log content to an active session."""
        if session_id not in self.active_sessions:
            # Auto-create session if it doesn't exist
            self.create_session(session_id, "auto-detected", {"auto_created": True})
        
        session = self.active_sessions[session_id]
        fragment = LogFragment(content, source, metadata=metadata)
        session.add_fragment(fragment)
        
        # Process fragment immediately for real-time intelligence
        self._process_fragment_intelligence(fragment, session)
        
        return True
    
    def finalize_session(self, session_id: str, status: str = "COMPLETED") -> Optional[RunnerSession]:
        """Finalize a session and move it to completed sessions."""
        if session_id not in self.active_sessions:
            return None
        
        session = self.active_sessions.pop(session_id)
        session.finalize_session(status)
        self.completed_sessions.append(session)
        
        # Update global intelligence patterns
        self._update_global_patterns(session)
        
        # Persist session data
        self._persist_session(session)
        
        return session
    
    def _process_fragment_intelligence(self, fragment: LogFragment, session: RunnerSession):
        """Process individual fragment for immediate intelligence extraction."""
        # Extract immediate patterns
        error_patterns = re.findall(r'(ERROR|FAIL|EXCEPTION)[^\\n]*', 
                                  fragment.content, re.IGNORECASE)
        success_patterns = re.findall(r'(SUCCESS|PASS|COMPLETE)[^\\n]*', 
                                    fragment.content, re.IGNORECASE)
        
        # Update session metadata with immediate findings
        if error_patterns:
            fragment.metadata['immediate_errors'] = error_patterns[:5]
        if success_patterns:
            fragment.metadata['immediate_successes'] = success_patterns[:5]
        
        fragment.processed = True
    
    def _update_global_patterns(self, session: RunnerSession):
        """Update global intelligence patterns with session data."""
        # Track error evolution over time
        if session.intelligence_summary["error_density"] > 0.1:
            self.global_patterns["error_evolution"].append({
                "timestamp": session.end_time.isoformat(),
                "session_id": session.session_id,
                "error_density": session.intelligence_summary["error_density"],
                "runner_type": session.runner_type
            })
        
        # Track success pathways
        if session.status == "COMPLETED" and session.intelligence_summary["error_density"] < 0.05:
            self.global_patterns["success_pathways"].append({
                "timestamp": session.end_time.isoformat(),
                "session_id": session.session_id,
                "runner_type": session.runner_type,
                "duration": session.intelligence_summary["session_duration"],
                "pattern_signatures": session.intelligence_summary["pattern_signatures"]
            })
        
        # Detect anomaly clusters
        learning_value = session.intelligence_summary["learning_value"]
        if learning_value > 5.0:
            self.global_patterns["anomaly_clusters"].append({
                "timestamp": session.end_time.isoformat(),
                "session_id": session.session_id,
                "learning_value": learning_value,
                "anomaly_type": "HIGH_LEARNING_VALUE"
            })
    
    def _persist_session(self, session: RunnerSession):
        """Persist session data to storage."""
        session_file = self.storage_path / f"session_{session.session_id}.json"
        
        try:
            with open(session_file, 'w', encoding='utf-8') as f:
                json.dump(session.to_dict(), f, indent=2)
        except Exception as e:
            print(f"Warning: Failed to persist session {session.session_id}: {e}")
    
    def get_intelligence_report(self) -> Dict:
        """Generate comprehensive intelligence report for bidirectional analysis."""
        return {
            "timestamp": datetime.now().isoformat(),
            "active_sessions": len(self.active_sessions),
            "completed_sessions": len(self.completed_sessions),
            "global_patterns": self.global_patterns,
            "session_summaries": [
                {
                    "session_id": session.session_id,
                    "runner_type": session.runner_type,
                    "status": session.status,
                    "intelligence_summary": session.intelligence_summary
                }
                for session in self.completed_sessions[-10:]  # Last 10 sessions
            ],
            "bidirectional_insights": self._generate_bidirectional_insights()
        }
    
    def _generate_bidirectional_insights(self) -> Dict:
        """Generate insights that can improve future runs."""
        insights = {
            "error_trend_analysis": {},
            "success_pattern_identification": {},
            "optimization_recommendations": [],
            "anomaly_predictions": []
        }
        
        # Analyze error trends
        recent_errors = self.global_patterns["error_evolution"][-20:]
        if recent_errors:
            error_density_trend = [e["error_density"] for e in recent_errors]
            avg_error_density = sum(error_density_trend) / len(error_density_trend)
            insights["error_trend_analysis"] = {
                "average_error_density": avg_error_density,
                "trend": "IMPROVING" if len(error_density_trend) > 1 and 
                        error_density_trend[-1] < error_density_trend[0] else "STABLE"
            }
        
        # Identify success patterns
        success_paths = self.global_patterns["success_pathways"][-10:]
        if success_paths:
            successful_runner_types = {}
            for path in success_paths:
                runner_type = path["runner_type"]
                successful_runner_types[runner_type] = successful_runner_types.get(runner_type, 0) + 1
            
            insights["success_pattern_identification"] = {
                "most_reliable_runner_types": successful_runner_types,
                "average_success_duration": sum(p["duration"] for p in success_paths) / len(success_paths)
            }
        
        # Generate optimization recommendations
        if insights["error_trend_analysis"].get("average_error_density", 0) > 0.2:
            insights["optimization_recommendations"].append(
                "HIGH_ERROR_DENSITY_DETECTED: Consider improving error handling in runners"
            )
        
        if len(self.global_patterns["anomaly_clusters"]) > 5:
            insights["optimization_recommendations"].append(
                "ANOMALY_CLUSTER_DETECTED: Investigate recurring high-learning-value sessions"
            )
        
        return insights
    
    def export_for_classification(self, session_id: str = None) -> str:
        """Export log data in format suitable for error classification."""
        if session_id:
            if session_id in self.active_sessions:
                session = self.active_sessions[session_id]
            else:
                session = next((s for s in self.completed_sessions 
                              if s.session_id == session_id), None)
            if not session:
                return ""
            
            return "\n".join(fragment.content for fragment in session.fragments)
        else:
            # Export all recent session data
            all_content = []
            for session in self.completed_sessions[-5:]:  # Last 5 sessions
                all_content.append(f"=== SESSION {session.session_id} ===")
                for fragment in session.fragments:
                    all_content.append(fragment.content)
                all_content.append("=== END SESSION ===")
            
            return "\n".join(all_content)

def main():
    """Command-line interface for log aggregation."""
    if len(sys.argv) < 3:
        print("Usage: python log_aggregator.py <command> <session_id> [args...]")
        print("Commands:")
        print("  create <session_id> <runner_type> [context_json]")
        print("  add <session_id> <log_file> <source>")
        print("  finalize <session_id> [status]")
        print("  report")
        sys.exit(1)
    
    command = sys.argv[1]
    aggregator = PsychoNoirLogAggregator()
    
    if command == "create":
        session_id = sys.argv[2]
        runner_type = sys.argv[3] if len(sys.argv) > 3 else "unknown"
        context = {}
        if len(sys.argv) > 4:
            try:
                context = json.loads(sys.argv[4])
            except json.JSONDecodeError:
                print("Warning: Invalid context JSON")
        
        session = aggregator.create_session(session_id, runner_type, context)
        print(f"Created session: {session.session_id}")
        
    elif command == "add":
        session_id = sys.argv[2]
        log_file = sys.argv[3]
        source = sys.argv[4] if len(sys.argv) > 4 else "unknown"
        
        try:
            with open(log_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            aggregator.add_log_content(session_id, content, source)
            print(f"Added log content to session: {session_id}")
            
        except FileNotFoundError:
            print(f"Error: Log file '{log_file}' not found")
            sys.exit(1)
            
    elif command == "finalize":
        session_id = sys.argv[2]
        status = sys.argv[3] if len(sys.argv) > 3 else "COMPLETED"
        
        session = aggregator.finalize_session(session_id, status)
        if session:
            print(f"Finalized session: {session.session_id}")
            print(f"Intelligence summary: {session.intelligence_summary}")
        else:
            print(f"Session not found: {session_id}")
            
    elif command == "report":
        report = aggregator.get_intelligence_report()
        print(json.dumps(report, indent=2))
        
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)

if __name__ == "__main__":
    main()