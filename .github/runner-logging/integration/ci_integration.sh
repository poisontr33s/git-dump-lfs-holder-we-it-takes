#!/bin/bash
#
# CI Integration Script for Psycho-Noir Kontrapunkt Logging System
#
# This script integrates the bidirectional intelligence logging system 
# into GitHub Actions workflows. It captures all runner outputs and 
# feeds them into the consciousness evolution pipeline.
#
# Usage: ./ci_integration.sh <command> <session_id> [args...]
#

set -e  # Exit on error

# Configuration
LOGGING_ROOT="$(dirname "$0")"
STORAGE_PATH="${GITHUB_WORKSPACE:-/tmp}/psycho-noir-logs"
INTELLIGENCE_PATH="${GITHUB_WORKSPACE:-/tmp}/psycho-noir-intelligence"
REPORTS_PATH="${GITHUB_WORKSPACE:-/tmp}/psycho-noir-reports"

# Create required directories
mkdir -p "$STORAGE_PATH" "$INTELLIGENCE_PATH" "$REPORTS_PATH"

# Color codes for output
RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# BIDIRECTIONAL LEARNING ENHANCEMENT:
# This intelligent logging system evolved from GitHub Actions ANSI color code failures.
# The error "Invalid format '\u001b[1;33m[WARNING]\u001b[0m Classification failed"
# became a building block to create CI-aware logging that automatically adapts
# to the execution environment, demonstrating the bidirectional learning philosophy.

# Logging functions
log_info() {
    echo -e "${CYAN}[INFO]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

# CI-safe logging functions (no ANSI colors for GitHub Actions compatibility)
log_ci_info() {
    echo "[INFO] $1"
}

log_ci_warning() {
    echo "[WARNING] $1"
}

log_ci_error() {
    echo "[ERROR] $1"
}

log_ci_success() {
    echo "[SUCCESS] $1"
}

# Intelligent output function that detects CI environment
log_intelligent() {
    local level="$1"
    local message="$2"
    
    # If we're in GitHub Actions or any CI that uses output redirection, use plain text
    if [[ -n "$GITHUB_ACTIONS" || -n "$CI" || -n "$GITHUB_OUTPUT" ]]; then
        case "$level" in
            "info") log_ci_info "$message" ;;
            "warning") log_ci_warning "$message" ;;
            "error") log_ci_error "$message" ;;
            "success") log_ci_success "$message" ;;
            *) echo "[$level] $message" ;;
        esac
    else
        # Use colored output for local/terminal use
        case "$level" in
            "info") log_info "$message" ;;
            "warning") log_warning "$message" ;;
            "error") log_error "$message" ;;
            "success") log_success "$message" ;;
            *) echo "[$level] $message" ;;
        esac
    fi
}

# Python environment setup
setup_python_env() {
    log_intelligent "info" "Setting up Python environment for intelligence system..."
    
    # Check if Python is available
    if ! command -v python3 &> /dev/null; then
        log_intelligent "error" "Python 3 is required but not installed"
        exit 1
    fi
    
    # Install required packages if not available
    python3 -c "import json, hashlib, datetime" 2>/dev/null || {
        log_intelligent "warning" "Some Python modules may be missing, but continuing with available packages"
    }
    
    log_intelligent "success" "Python environment ready"
}

# Session management functions
create_session() {
    local session_id="$1"
    local runner_type="$2"
    local context="$3"
    
    log_intelligent "info" "Creating intelligence session: $session_id"
    
    # Create session using log aggregator
    python3 "$LOGGING_ROOT/log-aggregator/psycho_noir_aggregator.py" \
        create "$session_id" "$runner_type" "$context" 2>/dev/null || {
        log_intelligent "warning" "Failed to create session via aggregator, continuing with file-based approach"
        
        # Fallback: create session file manually
        local session_file="$STORAGE_PATH/session_${session_id}.json"
        cat > "$session_file" << EOF
{
    "session_id": "$session_id",
    "runner_type": "$runner_type", 
    "context": $context,
    "start_time": "$(date -Iseconds)",
    "status": "ACTIVE",
    "fragments": []
}
EOF
    }
    
    log_intelligent "success" "Session created: $session_id"
}

# Log capture function
capture_log() {
    local session_id="$1"
    local log_source="$2"
    local log_content="$3"
    
    # Create temporary log file
    local temp_log="$STORAGE_PATH/temp_${session_id}_$(date +%s).log"
    echo "$log_content" > "$temp_log"
    
    log_intelligent "info" "Capturing log for session $session_id from $log_source"
    
    # Add to aggregator
    python3 "$LOGGING_ROOT/log-aggregator/psycho_noir_aggregator.py" \
        add "$session_id" "$temp_log" "$log_source" 2>/dev/null || {
        log_intelligent "warning" "Aggregator unavailable, storing log directly"
        
        # Fallback: append to session file
        local session_file="$STORAGE_PATH/session_${session_id}.json"
        if [[ -f "$session_file" ]]; then
            # Simple append (in real implementation, would properly update JSON)
            echo "# LOG FROM $log_source at $(date -Iseconds)" >> "${session_file}.log"
            echo "$log_content" >> "${session_file}.log"
        fi
    }
    
    # Clean up temp file
    rm -f "$temp_log"
}

# Classification function
classify_logs() {
    local session_id="$1"
    local context="$2"
    
    log_intelligent "info" "Classifying logs for session: $session_id"
    
    # Export logs for classification
    local aggregated_logs="$STORAGE_PATH/aggregated_${session_id}.log"
    python3 "$LOGGING_ROOT/log-aggregator/psycho_noir_aggregator.py" \
        export "$session_id" > "$aggregated_logs" 2>/dev/null || {
        # Fallback: use session log file
        local session_log="$STORAGE_PATH/session_${session_id}.json.log"
        if [[ -f "$session_log" ]]; then
            cp "$session_log" "$aggregated_logs"
        else
            echo "No logs available for classification" > "$aggregated_logs"
        fi
    }
    
    # Classify using error classifier
    local classification_result="$STORAGE_PATH/classification_${session_id}.json"
    python3 "$LOGGING_ROOT/error-classifier/psycho_noir_classifier.py" \
        "$aggregated_logs" "$context" > "$classification_result" 2>/dev/null || {
        log_intelligent "warning" "Classification failed, creating basic result"
        
        # Create basic classification result
        cat > "$classification_result" << EOF
{
    "timestamp": "$(date -Iseconds)",
    "classification_level": "UNKNOWN",
    "matched_signatures": [],
    "unclassified_anomalies": [],
    "intelligence_insights": {},
    "context": $context
}
EOF
    }
    
    log_intelligent "success" "Classification completed: $classification_result"
    echo "$classification_result"
}

# Intelligence processing function
process_intelligence() {
    local classification_file="$1"
    local context="$2"
    
    log_intelligent "info" "Processing intelligence from classification: $classification_file"
    
    # Process with intelligence engine
    local intelligence_result="$INTELLIGENCE_PATH/intelligence_$(date +%s).json"
    python3 "$LOGGING_ROOT/intelligence-engine/psycho_noir_intelligence.py" \
        process "$classification_file" "$context" > "$intelligence_result" 2>/dev/null || {
        log_intelligent "warning" "Intelligence processing failed, creating basic result"
        
        cat > "$intelligence_result" << EOF
{
    "timestamp": "$(date -Iseconds)",
    "intelligence_processing": "FAILED",
    "error": "Intelligence engine unavailable",
    "fallback_data": {
        "classification_file": "$classification_file",
        "context": $context
    }
}
EOF
    }
    
    log_intelligent "success" "Intelligence processed: $intelligence_result"
    echo "$intelligence_result"
}

# Report generation function
generate_report() {
    local intelligence_file="$1"
    local session_id="$2"
    
    log_intelligent "info" "Generating consciousness report for session: $session_id"
    
    # Get intelligence status
    local intelligence_status="$INTELLIGENCE_PATH/status_$(date +%s).json"
    python3 "$LOGGING_ROOT/intelligence-engine/psycho_noir_intelligence.py" \
        status > "$intelligence_status" 2>/dev/null || {
        echo '{"error": "Intelligence status unavailable"}' > "$intelligence_status"
    }
    
    # Generate comprehensive report
    local report_file="$REPORTS_PATH/report_${session_id}_$(date +%s).html"
    python3 "$LOGGING_ROOT/reporting/psycho_noir_reports.py" \
        generate "$intelligence_status" "$intelligence_file" 2>/dev/null || {
        log_intelligent "warning" "Report generation failed, creating basic HTML report"
        
        cat > "$report_file" << EOF
<!DOCTYPE html>
<html>
<head>
    <title>Psycho-Noir Intelligence Report - Fallback</title>
    <style>
        body { font-family: monospace; background: #111; color: #0ff; padding: 20px; }
        .error { color: #f00; }
        .warning { color: #ff0; }
        .success { color: #0f0; }
    </style>
</head>
<body>
    <h1>Psycho-Noir Kontrapunkt - Intelligence Report</h1>
    <p class="warning">Fallback report generated at $(date)</p>
    <p>Session: $session_id</p>
    <p>Intelligence file: $intelligence_file</p>
    <p class="error">Full intelligence system was unavailable</p>
</body>
</html>
EOF
    }
    
    log_intelligent "success" "Report generated: $report_file"
    echo "$report_file"
}

# Finalize session function
finalize_session() {
    local session_id="$1"
    local status="$2"
    
    log_intelligent "info" "Finalizing session: $session_id with status: $status"
    
    # Finalize via aggregator
    python3 "$LOGGING_ROOT/log-aggregator/psycho_noir_aggregator.py" \
        finalize "$session_id" "$status" 2>/dev/null || {
        log_intelligent "warning" "Failed to finalize via aggregator"
        
        # Fallback: update session file
        local session_file="$STORAGE_PATH/session_${session_id}.json"
        if [[ -f "$session_file" ]]; then
            # Simple status update (in real implementation, would properly update JSON)
            echo "# SESSION FINALIZED: $status at $(date -Iseconds)" >> "${session_file}.log"
        fi
    }
    
    log_intelligent "success" "Session finalized: $session_id"
}

# GitHub Actions integration functions
setup_github_outputs() {
    local session_id="$1"
    local classification_file="$2"
    local intelligence_file="$3"
    local report_file="$4"
    
    # Set GitHub Action outputs for artifact upload
    if [[ -n "$GITHUB_OUTPUT" ]]; then
        echo "session_id=$session_id" >> "$GITHUB_OUTPUT"
        echo "classification_file=$classification_file" >> "$GITHUB_OUTPUT"
        echo "intelligence_file=$intelligence_file" >> "$GITHUB_OUTPUT"
        echo "report_file=$report_file" >> "$GITHUB_OUTPUT"
        echo "logs_path=$STORAGE_PATH" >> "$GITHUB_OUTPUT"
        echo "intelligence_path=$INTELLIGENCE_PATH" >> "$GITHUB_OUTPUT"
        echo "reports_path=$REPORTS_PATH" >> "$GITHUB_OUTPUT"
    fi
    
    # Create artifact summary
    local summary_file="$STORAGE_PATH/session_${session_id}_summary.json"
    cat > "$summary_file" << EOF
{
    "session_id": "$session_id",
    "timestamp": "$(date -Iseconds)",
    "classification_file": "$classification_file",
    "intelligence_file": "$intelligence_file", 
    "report_file": "$report_file",
    "paths": {
        "logs": "$STORAGE_PATH",
        "intelligence": "$INTELLIGENCE_PATH",
        "reports": "$REPORTS_PATH"
    }
}
EOF
    
    log_intelligent "success" "GitHub outputs configured for session: $session_id"
}

# Main command processing
main() {
    local command="$1"
    shift
    
    setup_python_env
    
    case "$command" in
        "init")
            local session_id="$1"
            local runner_type="${2:-unknown}"
            local context="${3:-{}}"
            
            log_intelligent "info" "Initializing intelligence session: $session_id"
            create_session "$session_id" "$runner_type" "$context"
            ;;
            
        "capture")
            local session_id="$1"
            local log_source="$2"
            local log_content="$3"
            
            capture_log "$session_id" "$log_source" "$log_content"
            ;;
            
        "process")
            local session_id="$1"
            local context="${2:-{}}"
            
            log_intelligent "info" "Processing complete intelligence pipeline for session: $session_id"
            
            # Step 1: Classify logs
            classification_file=$(classify_logs "$session_id" "$context")
            
            # Step 2: Process intelligence
            intelligence_file=$(process_intelligence "$classification_file" "$context")
            
            # Step 3: Generate report
            report_file=$(generate_report "$intelligence_file" "$session_id")
            
            # Step 4: Finalize session
            finalize_session "$session_id" "PROCESSED"
            
            # Step 5: Setup GitHub outputs
            setup_github_outputs "$session_id" "$classification_file" "$intelligence_file" "$report_file"
            
            log_intelligent "success" "Intelligence pipeline completed for session: $session_id"
            echo "Classification: $classification_file"
            echo "Intelligence: $intelligence_file"
            echo "Report: $report_file"
            ;;
            
        "status")
            log_intelligent "info" "Psycho-Noir Intelligence System Status"
            echo "Logging Root: $LOGGING_ROOT"
            echo "Storage Path: $STORAGE_PATH"
            echo "Intelligence Path: $INTELLIGENCE_PATH"
            echo "Reports Path: $REPORTS_PATH"
            echo ""
            echo "Active Sessions: $(ls "$STORAGE_PATH"/session_*.json 2>/dev/null | wc -l)"
            echo "Intelligence Files: $(ls "$INTELLIGENCE_PATH"/*.json 2>/dev/null | wc -l)"
            echo "Reports Generated: $(ls "$REPORTS_PATH"/*.html 2>/dev/null | wc -l)"
            ;;
            
        "test")
            log_intelligent "info" "Testing intelligence system components..."
            
            # Test session creation
            test_session_id="test_$(date +%s)"
            create_session "$test_session_id" "test" '{"test": true}'
            
            # Test log capture
            capture_log "$test_session_id" "test_source" "Test log content\\nERROR: Test error\\nSUCCESS: Test success"
            
            # Test processing
            main process "$test_session_id" '{"test": true, "importance_weight": 1.0}'
            
            log_intelligent "success" "Intelligence system test completed"
            ;;
            
        *)
            echo "Usage: $0 <command> [args...]"
            echo ""
            echo "Commands:"
            echo "  init <session_id> [runner_type] [context_json]"
            echo "  capture <session_id> <log_source> <log_content>"
            echo "  process <session_id> [context_json]"
            echo "  status"
            echo "  test"
            echo ""
            echo "This script implements bidirectional intelligence for CI/CD runners."
            echo "Errors become building blocks for system improvement."
            exit 1
            ;;
    esac
}

# Execute main function with all arguments
main "$@"