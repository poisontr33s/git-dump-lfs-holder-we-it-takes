#!/bin/bash
#
# Chaos Integration Script for Psycho-Noir Kontrapunkt Intelligence System
#
# This script integrates the chaos engineering module with the CI/CD intelligence system,
# enabling "failure by purpose" to validate bidirectional learning capabilities.
#
# Usage: ./chaos_integration.sh <command> <session_id> [args...]
#

set -e

# Configuration
SCRIPT_DIR="$(dirname "$0")"
CHAOS_MODULE="$SCRIPT_DIR/../failure-orchestrator/chaos_engineering.py"
INTELLIGENCE_PATH="${GITHUB_WORKSPACE:-/tmp}/psycho-noir-intelligence"
CHAOS_LOG_PATH="${GITHUB_WORKSPACE:-/tmp}/psycho-noir-chaos"

# Create required directories
mkdir -p "$INTELLIGENCE_PATH" "$CHAOS_LOG_PATH"

# Import CI integration utilities
source "$SCRIPT_DIR/ci_integration.sh" 2>/dev/null || {
    echo "Warning: CI integration utilities not available - running in standalone mode"
}

# Chaos-aware logging that adapts to environment
chaos_log() {
    local level="$1"
    local message="$2"
    
    # Use intelligent logging if available, otherwise plain output
    if declare -f log_intelligent >/dev/null 2>&1; then
        log_intelligent "$level" "$message"
    else
        echo "[$level] $message"
    fi
}

# Initialize chaos engineering for a session
chaos_init() {
    local session_id="$1"
    local chaos_intensity="${2:-3}"
    local scenarios_budget="${3:-5}"
    
    chaos_log "info" "Initializing Chaos Engineering for session: $session_id"
    chaos_log "info" "Chaos Intensity: $chaos_intensity/5"
    chaos_log "info" "Scenarios Budget: $scenarios_budget"
    
    # Create chaos session context
    local chaos_context=$(cat << EOF
{
    "session_id": "$session_id",
    "chaos_intensity": $chaos_intensity,
    "scenarios_budget": $scenarios_budget,
    "philosophy": "failure_by_purpose",
    "learning_objective": "bidirectional_intelligence_validation",
    "start_time": "$(date -Iseconds)",
    "environment": "${CI:-local}",
    "psycho_noir_elements": {
        "den_usynlige_hand_enabled": true,
        "glitch_acceptance": true,
        "consciousness_evolution": true
    }
}
EOF
    )
    
    # Save chaos session context
    echo "$chaos_context" > "$CHAOS_LOG_PATH/session_${session_id}.json"
    
    # Initialize chaos orchestrator
    if [[ -f "$CHAOS_MODULE" ]]; then
        python3 "$CHAOS_MODULE" test >/dev/null 2>&1 || {
            chaos_log "warning" "Chaos module test failed - continuing with limited functionality"
        }
        chaos_log "success" "Chaos orchestrator initialized successfully"
    else
        chaos_log "error" "Chaos module not found at $CHAOS_MODULE"
        return 1
    fi
    
    export CHAOS_SESSION_ID="$session_id"
    export CHAOS_INTENSITY="$chaos_intensity"
    export CHAOS_SCENARIOS_BUDGET="$scenarios_budget"
    
    chaos_log "success" "🔥 Chaos Engineering initialized - ready for controlled failures"
}

# Assess chaos opportunity for a given trigger
chaos_assess() {
    local session_id="$1"
    local trigger="$2"
    local context_json="${3:-{}}"
    
    chaos_log "info" "Assessing chaos opportunity for trigger: $trigger"
    
    if [[ ! -f "$CHAOS_MODULE" ]]; then
        chaos_log "error" "Chaos module not available"
        return 1
    fi
    
    # Use Python to assess chaos opportunity
    local assessment=$(python3 -c "
import sys
import json
sys.path.append('$(dirname "$CHAOS_MODULE")')
from chaos_engineering import ChaosOrchestrator

orchestrator = ChaosOrchestrator('$session_id', '${CI:-local}')
context = json.loads('$context_json')
scenario = orchestrator.assess_chaos_opportunity('$trigger', context)

if scenario:
    print(f'CHAOS_RECOMMENDED:{scenario.name}:{scenario.category.value}:{scenario.intensity.name}')
else:
    print('NO_CHAOS_RECOMMENDED')
")
    
    echo "$assessment"
    
    if [[ "$assessment" == *"CHAOS_RECOMMENDED"* ]]; then
        chaos_log "warning" "🔥 Chaos opportunity identified: $assessment"
        return 0
    else
        chaos_log "info" "No chaos opportunity identified for current context"
        return 1
    fi
}

# Introduce chaos for a specific scenario
chaos_introduce() {
    local session_id="$1"
    local trigger="$2"
    local context_json="${3:-{}}"
    
    chaos_log "info" "🔥 Introducing chaos for trigger: $trigger"
    
    if [[ ! -f "$CHAOS_MODULE" ]]; then
        chaos_log "error" "Chaos module not available"
        return 1
    fi
    
    # Use Python to introduce chaos
    local chaos_result=$(python3 -c "
import sys
import json
sys.path.append('$(dirname "$CHAOS_MODULE")')
from chaos_engineering import ChaosOrchestrator

orchestrator = ChaosOrchestrator('$session_id', '${CI:-local}')
context = json.loads('$context_json')
scenario = orchestrator.assess_chaos_opportunity('$trigger', context)

if scenario:
    chaos_execution = orchestrator.introduce_chaos(scenario, context)
    print(f'CHAOS_INTRODUCED:{chaos_execution[\"chaos_id\"]}:{scenario.name}')
    
    # Auto-resolve after duration for CI environments
    if '${CI:-}':
        import time
        time.sleep(min(scenario.duration, 10))  # Max 10s in CI
        resolution = orchestrator.resolve_chaos(chaos_execution['chaos_id'], 'automated')
        print(f'CHAOS_RESOLVED:{chaos_execution[\"chaos_id\"]}:{len(resolution.get(\"learning_insights\", []))}')
else:
    print('NO_CHAOS_TO_INTRODUCE')
" 2>&1)
    
    echo "$chaos_result"
    
    # Log chaos results to intelligence system
    if [[ "$chaos_result" == *"CHAOS_INTRODUCED"* ]]; then
        chaos_log "success" "🔥 Chaos introduced successfully"
        
        # Extract chaos results for intelligence integration
        local chaos_summary="Chaos Engineering: $chaos_result"
        
        # Feed to intelligence system if available
        if declare -f ci_integration.sh >/dev/null 2>&1; then
            ci_integration.sh capture "$session_id" "chaos_introduction" "$chaos_summary" || true
        fi
        
        return 0
    else
        chaos_log "info" "No chaos introduced for current context"
        return 1
    fi
}

# Generate chaos report for a session
chaos_report() {
    local session_id="$1"
    
    chaos_log "info" "Generating chaos report for session: $session_id"
    
    if [[ ! -f "$CHAOS_MODULE" ]]; then
        chaos_log "error" "Chaos module not available"
        return 1
    fi
    
    # Generate comprehensive chaos report
    local report_file="$CHAOS_LOG_PATH/chaos_report_${session_id}.json"
    
    python3 -c "
import sys
import json
sys.path.append('$(dirname "$CHAOS_MODULE")')
from chaos_engineering import ChaosOrchestrator

orchestrator = ChaosOrchestrator('$session_id', '${CI:-local}')
report = orchestrator.generate_chaos_report()

with open('$report_file', 'w') as f:
    json.dump(report, f, indent=2, default=str)

# Print summary
print('🧠 CHAOS INTELLIGENCE REPORT SUMMARY:')
print(f'   Total Scenarios: {report[\"chaos_statistics\"][\"total_scenarios_executed\"]}')
print(f'   Learning Insights: {report[\"chaos_statistics\"][\"total_learning_insights\"]}')
print(f'   Consciousness Level: {report[\"psycho_noir_assessment\"][\"consciousness_level\"]}')
print(f'   Den Usynlige Hånd Influence: {report[\"psycho_noir_assessment\"][\"invisible_hand_influence\"]}%')
print(f'   Adaptation Quotient: {report[\"psycho_noir_assessment\"][\"adaptation_quotient\"]}%')
"
    
    chaos_log "success" "Chaos report generated: $report_file"
    
    # Copy to intelligence path for integration
    cp "$report_file" "$INTELLIGENCE_PATH/" 2>/dev/null || true
}

# Validate chaos engineering setup
chaos_validate() {
    chaos_log "info" "Validating chaos engineering setup..."
    
    # Check Python availability
    if ! command -v python3 >/dev/null 2>&1; then
        chaos_log "error" "Python 3 not available - chaos engineering requires Python"
        return 1
    fi
    
    # Check chaos module
    if [[ ! -f "$CHAOS_MODULE" ]]; then
        chaos_log "error" "Chaos module not found at: $CHAOS_MODULE"
        return 1
    fi
    
    # Test chaos module
    if python3 "$CHAOS_MODULE" test >/dev/null 2>&1; then
        chaos_log "success" "Chaos module validation passed"
    else
        chaos_log "warning" "Chaos module test failed - may have limited functionality"
    fi
    
    # Check directories
    if [[ -d "$INTELLIGENCE_PATH" && -d "$CHAOS_LOG_PATH" ]]; then
        chaos_log "success" "Storage paths available"
    else
        chaos_log "warning" "Storage paths may not be accessible"
    fi
    
    chaos_log "success" "✅ Chaos engineering setup validated"
    return 0
}

# Main command dispatcher
main() {
    local command="$1"
    shift
    
    case "$command" in
        "init")
            chaos_init "$@"
            ;;
        "assess")
            chaos_assess "$@"
            ;;
        "introduce")
            chaos_introduce "$@"
            ;;
        "report")
            chaos_report "$@"
            ;;
        "validate")
            chaos_validate "$@"
            ;;
        "status")
            chaos_log "info" "Chaos Engineering Status:"
            chaos_log "info" "  Session ID: ${CHAOS_SESSION_ID:-'Not Set'}"
            chaos_log "info" "  Intensity: ${CHAOS_INTENSITY:-'Not Set'}/5"
            chaos_log "info" "  Scenarios Budget: ${CHAOS_SCENARIOS_BUDGET:-'Not Set'}"
            chaos_log "info" "  Intelligence Path: $INTELLIGENCE_PATH"
            chaos_log "info" "  Chaos Log Path: $CHAOS_LOG_PATH"
            ;;
        *)
            echo "Usage: $0 <command> [args...]"
            echo "Commands:"
            echo "  init <session_id> [intensity] [scenarios_budget] - Initialize chaos engineering"
            echo "  assess <session_id> <trigger> [context_json]     - Assess chaos opportunity"
            echo "  introduce <session_id> <trigger> [context_json]  - Introduce chaos"
            echo "  report <session_id>                              - Generate chaos report"
            echo "  validate                                         - Validate setup"
            echo "  status                                           - Show status"
            return 1
            ;;
    esac
}

# Execute main function if script is run directly
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi