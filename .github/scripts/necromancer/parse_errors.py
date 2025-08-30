#!/usr/bin/env python3
"""
Necromancer Error Parser
Psycho-Noir Kontrapunkt - Failure Observability System

Classifies command failures into structured error types with pattern recognition
for the Necropolis knowledge base. Integrates with existing Neural Archaeology
patterns while providing standardized error taxonomy.
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, List, Optional

class NecromancerErrorClassifier:
    """
    Advanced error classification engine for the Necropolis system.
    
    Inherits the analytical intensity of the Neural Archaeology system
    while providing deterministic, fast classification for PR workflows.
    """
    
    def __init__(self):
        """Initialize the Necromancer with comprehensive error patterns."""
        self.error_patterns = {
            'ENVIRONMENT_SETUP': [
                r'(?i)error.*setting up.*environment',
                r'(?i)failed.*install.*dependencies',
                r'(?i)permission denied.*setup',
                r'(?i)could not.*find.*executable',
                r'(?i)command not found',
                r'(?i)no such file or directory.*setup',
                r'(?i)setup.*failed',
            ],
            'DEPENDENCY_FAILURE': [
                r'(?i)npm.*error.*install',
                r'(?i)pip.*error.*install',
                r'(?i)error.*requirements\.txt',
                r'(?i)package.*not found',
                r'(?i)dependency.*conflict',
                r'(?i)version.*incompatible',
                r'(?i)could not.*resolve.*dependency',
                r'(?i)npm ERR!',
                r'(?i)ModuleNotFoundError',
                r'(?i)ImportError',
            ],
            'BUILD_FAILURE': [
                r'(?i)build.*failed',
                r'(?i)compilation.*error',
                r'(?i)error.*building',
                r'(?i)webpack.*error',
                r'(?i)babel.*error',
                r'(?i)typescript.*error',
                r'(?i)tsc.*error',
                r'(?i)syntax.*error',
                r'(?i)parse.*error.*building',
            ],
            'TEST_FAILURE': [
                r'(?i)test.*failed',
                r'(?i)assertion.*error',
                r'(?i)expect.*received',
                r'(?i)jest.*failed',
                r'(?i)pytest.*failed',
                r'(?i)test.*suite.*failed',
                r'(?i)✗.*test',
                r'(?i)❌.*test',
                r'(?i)FAIL.*test',
                r'(?i)ERROR.*test',
            ],
            'LINT_FAILURE': [
                r'(?i)eslint.*error',
                r'(?i)lint.*failed',
                r'(?i)style.*error',
                r'(?i)formatting.*error',
                r'(?i)code quality.*failed',
                r'(?i)pylint.*error',
                r'(?i)flake8.*error',
                r'(?i)black.*error',
            ],
            'SECURITY_FINDING': [
                r'(?i)security.*vulnerability',
                r'(?i)codeql.*found',
                r'(?i)security.*alert',
                r'(?i)vulnerability.*detected',
                r'(?i)security.*scan.*failed',
                r'(?i)audit.*found.*vulnerabilities',
            ],
            'DISK_SPACE': [
                r'(?i)no space left on device',
                r'(?i)disk.*full',
                r'(?i)insufficient.*space',
                r'(?i)out of.*space',
                r'(?i)disk.*quota.*exceeded',
            ],
            'TIMEOUT': [
                r'(?i)timeout.*exceeded',
                r'(?i)operation.*timed out',
                r'(?i)time limit.*exceeded',
                r'(?i)killed.*timeout',
                r'(?i)cancelled.*timeout',
                r'(?i)SIGTERM.*timeout',
            ],
            'CANCELLED': [
                r'(?i)job.*cancelled',
                r'(?i)workflow.*cancelled',
                r'(?i)cancelled by user',
                r'(?i)cancelled.*request',
                r'(?i)SIGINT.*received',
            ],
        }
        
        # Neural Archaeology integration patterns
        self.psycho_noir_signatures = {
            'KAUSALITETS_ARKITEKTEN_INTERFERENCE': [
                r'(?i)predictive.*model.*corrupted',
                r'(?i)causal.*chain.*broken',
                r'(?i)quantum.*ai.*error',
            ],
            'SYNTETISKE_SYNAPSER_GLITCH': [
                r'(?i)nanobot.*network.*failure',
                r'(?i)synthetic.*synapse.*error',
                r'(?i)neural.*implant.*malfunction',
            ],
            'RUSTBELT_IMPROVISATION_CASCADE': [
                r'(?i)scrap.*symphony.*discord',
                r'(?i)improvisation.*chaos',
                r'(?i)kretskort.*sjamanisme.*failed',
            ],
        }

    def classify_error(self, log_content: str, exit_code: int, outcome: str) -> str:
        """
        Classify error based on log content, exit code, and outcome.
        
        Returns standardized error type for the Necropolis taxonomy.
        """
        if outcome == "SUCCESS":
            return "SUCCESS"
        
        # Check for Psycho-Noir specific signatures first
        for pn_type, patterns in self.psycho_noir_signatures.items():
            if self._match_patterns(log_content, patterns):
                return pn_type
        
        # Check standard error patterns
        for error_type, patterns in self.error_patterns.items():
            if self._match_patterns(log_content, patterns):
                return error_type
        
        # Exit code specific classification
        if exit_code == 124:
            return "TIMEOUT"
        elif exit_code == 130:
            return "CANCELLED"
        elif exit_code == 2:
            return "ENVIRONMENT_SETUP"
        elif exit_code == 1:
            # Generic failure - try to infer from context
            if "test" in log_content.lower():
                return "TEST_FAILURE"
            elif "build" in log_content.lower():
                return "BUILD_FAILURE"
        
        return "UNKNOWN"

    def _match_patterns(self, content: str, patterns: List[str]) -> bool:
        """Check if any pattern matches the content."""
        for pattern in patterns:
            if re.search(pattern, content, re.MULTILINE | re.IGNORECASE):
                return True
        return False

    def extract_error_fingerprint(self, log_content: str) -> str:
        """
        Extract a unique fingerprint for similar errors.
        
        This enables grouping of similar failures in the knowledge base.
        """
        # Extract key error lines
        error_lines = []
        for line in log_content.split('\n'):
            line = line.strip()
            if any(keyword in line.lower() for keyword in 
                   ['error', 'failed', 'exception', 'fatal', 'critical']):
                # Clean up the line for fingerprinting
                cleaned = re.sub(r'\d+', 'N', line)  # Replace numbers
                cleaned = re.sub(r'/[^\s]+', '/PATH', cleaned)  # Replace paths
                cleaned = re.sub(r'at \w+:\d+', 'at LOCATION', cleaned)  # Replace locations
                error_lines.append(cleaned)
        
        # Return first few significant error lines as fingerprint
        return ' | '.join(error_lines[:3]) if error_lines else "NO_CLEAR_ERROR_SIGNATURE"

    def generate_outcome_data(self, args: argparse.Namespace, error_type: str, 
                            log_content: str) -> Dict[str, Any]:
        """Generate comprehensive outcome data for the Necropolis system."""
        fingerprint = self.extract_error_fingerprint(log_content)
        
        outcome_data = {
            # Core identification
            "name": args.name,
            "outcome": args.outcome,
            "error_type": error_type,
            "fingerprint": fingerprint,
            
            # Execution context
            "category": args.category,
            "variant": args.variant,
            "exit_code": int(args.exit_code),
            "duration_seconds": float(args.duration),
            
            # Environment context
            "os": os.environ.get('RUNNER_OS', 'unknown'),
            "arch": os.environ.get('RUNNER_ARCH', 'unknown'),
            "runner_name": os.environ.get('RUNNER_NAME', 'unknown'),
            "job": os.environ.get('GITHUB_JOB', 'unknown'),
            "step": args.name,
            
            # Git context
            "git_sha": os.environ.get('GITHUB_SHA', 'unknown'),
            "git_ref": os.environ.get('GITHUB_REF', 'unknown'),
            "actor": os.environ.get('GITHUB_ACTOR', 'unknown'),
            "workflow": os.environ.get('GITHUB_WORKFLOW', 'unknown'),
            "run_id": os.environ.get('GITHUB_RUN_ID', 'unknown'),
            
            # Timestamp
            "timestamp": datetime.now(timezone.utc).isoformat(),
            
            # Necropolis metadata
            "necropolis_version": "1.0.0",
            "collection_type": "pr_time" if args.outcome == "FAILURE" else "verification"
        }
        
        return outcome_data


def main():
    """Main execution function for the Necromancer error parser."""
    parser = argparse.ArgumentParser(
        description="Necromancer Error Parser - Classify and structure failure data"
    )
    
    parser.add_argument('--log-file', required=True, 
                       help='Path to command log file')
    parser.add_argument('--name', required=True,
                       help='Command name')
    parser.add_argument('--category', required=True,
                       help='Failure category')
    parser.add_argument('--variant', required=True,
                       help='Variant identifier')
    parser.add_argument('--exit-code', required=True, type=int,
                       help='Command exit code')
    parser.add_argument('--duration', required=True, type=float,
                       help='Command duration in seconds')
    parser.add_argument('--outcome', required=True,
                       help='Command outcome (SUCCESS|FAILURE)')
    parser.add_argument('--output-dir', required=True,
                       help='Output directory for artifacts')
    
    args = parser.parse_args()
    
    # Initialize classifier
    classifier = NecromancerErrorClassifier()
    
    # Read log content
    try:
        with open(args.log_file, 'r', encoding='utf-8', errors='ignore') as f:
            log_content = f.read()
    except FileNotFoundError:
        print(f"❌ Log file not found: {args.log_file}")
        log_content = ""
    
    # Classify error
    error_type = classifier.classify_error(log_content, args.exit_code, args.outcome)
    
    # Generate outcome data
    outcome_data = classifier.generate_outcome_data(args, error_type, log_content)
    
    # Ensure output directory exists
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Write outcome.json
    outcome_file = output_dir / "outcome.json"
    with open(outcome_file, 'w') as f:
        json.dump(outcome_data, f, indent=2)
    
    # Write outcome.ndjson (for streaming processing)
    ndjson_file = output_dir / "outcome.ndjson"
    with open(ndjson_file, 'w') as f:
        json.dump(outcome_data, f)
        f.write('\n')
    
    # Print summary
    print(f"🧙‍♂️ NECROMANCER CLASSIFICATION COMPLETE")
    print(f"📋 Command: {args.name}")
    print(f"🎯 Outcome: {args.outcome}")
    print(f"🏷️ Error Type: {error_type}")
    print(f"🔍 Fingerprint: {outcome_data['fingerprint'][:100]}...")
    print(f"💾 Artifacts saved to: {output_dir}")
    
    if error_type in classifier.psycho_noir_signatures:
        print(f"🎭 PSYCHO-NOIR SIGNATURE DETECTED: {error_type}")
        print("🔮 Den Usynlige Hånd stirs in the digital shadows...")


if __name__ == "__main__":
    main()