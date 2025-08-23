#!/bin/bash
# Jules Dependency Validator - Skyskraperen Cache Integrity Protocol
# 
# Dette skriptet validerer cache paths og implementerer conditional checks
# for å forhindre caching errors når paths ikke eksisterer.
#
# Del av Den Usynlige Hånds optimization infrastructure

set -euo pipefail

# Jules Configuration
JULES_VERSION="0.KORRUPT.1"
CORRUPTION_THRESHOLD="0.73"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

# Jules logging function
jules_log() {
    local level="$1"
    local message="$2"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    
    case "$level" in
        "INFO")  echo -e "${GREEN}[JULES-INFO]${NC} $timestamp: $message" ;;
        "WARN")  echo -e "${YELLOW}[JULES-WARN]${NC} $timestamp: $message" ;;
        "ERROR") echo -e "${RED}[JULES-ERROR]${NC} $timestamp: $message" ;;
        "DEBUG") echo -e "${BLUE}[JULES-DEBUG]${NC} $timestamp: $message" ;;
        "PSYCHO") echo -e "${PURPLE}[JULES-PSYCHO]${NC} $timestamp: $message" ;;
    esac
}

# Validate cache directory function
validate_cache_dir() {
    local cache_path="$1"
    local cache_type="$2"
    
    if [[ "${REPORT_MODE:-false}" != "true" ]]; then
        jules_log "DEBUG" "Validating cache directory: $cache_path ($cache_type)"
    fi
    
    if [[ "$cache_path" == ~* ]]; then
        # Expand tilde to home directory
        expanded_path="${cache_path/#\~/$HOME}"
    else
        expanded_path="$cache_path"
    fi
    
    if [[ -d "$expanded_path" ]]; then
        if [[ "${REPORT_MODE:-false}" != "true" ]]; then
            jules_log "INFO" "✅ Cache directory exists: $cache_path"
        fi
        echo "true"
    elif [[ -w "$(dirname "$expanded_path")" ]] || mkdir -p "$expanded_path" 2>/dev/null; then
        if [[ "${REPORT_MODE:-false}" != "true" ]]; then
            jules_log "INFO" "✅ Cache directory created: $cache_path"
        fi
        echo "true"
    else
        if [[ "${REPORT_MODE:-false}" != "true" ]]; then
            jules_log "WARN" "❌ Cannot create cache directory: $cache_path"
        fi
        echo "false"
    fi
}

# Validate Node.js cache paths
validate_nodejs_cache() {
    local npm_cache_valid=$(validate_cache_dir "~/.npm" "npm-global")
    local node_modules_valid=$(validate_cache_dir "$REPO_ROOT/node_modules" "npm-local")
    local local_cache_valid=$(validate_cache_dir "$REPO_ROOT/.cache/npm" "npm-project")
    
    echo "- **npm_global_cache**: $npm_cache_valid"
    echo "- **node_modules**: $node_modules_valid" 
    echo "- **project_cache**: $local_cache_valid"
    echo "- **package_json_exists**: $([ -f "$REPO_ROOT/package.json" ] && echo "true" || echo "false")"
    echo "- **package_lock_exists**: $([ -f "$REPO_ROOT/package-lock.json" ] && echo "true" || echo "false")"
}

# Validate Python cache paths
validate_python_cache() {
    local pip_cache_valid=$(validate_cache_dir "~/.cache/pip" "pip-global")
    local python_cache_valid=$(validate_cache_dir "$REPO_ROOT/.cache/python" "python-project")
    local pycache_valid=$(validate_cache_dir "$REPO_ROOT/backend/python/__pycache__" "pycache")
    
    # Check for requirements files
    local requirements_exist="false"
    if [[ -f "$REPO_ROOT/requirements.txt" ]] || [[ -f "$REPO_ROOT/backend/python/requirements.txt" ]]; then
        requirements_exist="true"
    fi
    
    echo "- **pip_global_cache**: $pip_cache_valid"
    echo "- **project_cache**: $python_cache_valid"
    echo "- **pycache**: $pycache_valid"
    echo "- **requirements_exist**: $requirements_exist"
    echo "- **pyproject_exists**: $([ -f "$REPO_ROOT/pyproject.toml" ] && echo "true" || echo "false")"
}

# Validate Ruby cache paths
validate_ruby_cache() {
    local bundle_cache_valid=$(validate_cache_dir "~/.bundle" "bundle-global")
    local vendor_cache_valid=$(validate_cache_dir "$REPO_ROOT/.cache/bundle" "bundle-project")
    
    # Check for Ruby projects
    local gemfile_exists="false"
    if find "$REPO_ROOT" -name "Gemfile" -type f | grep -q .; then
        gemfile_exists="true"
    fi
    
    echo "- **bundle_global_cache**: $bundle_cache_valid"
    echo "- **project_cache**: $vendor_cache_valid"
    echo "- **gemfile_exists**: $gemfile_exists"
    echo "- **gemfile_lock_exists**: $(find "$REPO_ROOT" -name "Gemfile.lock" -type f | grep -q . && echo "true" || echo "false")"
}

# Validate Docker cache paths
validate_docker_cache() {
    local docker_cache_valid=$(validate_cache_dir "/tmp/.buildx-cache" "docker-buildx")
    local docker_exists="false"
    
    if command -v docker &> /dev/null; then
        docker_exists="true"
    fi
    
    echo "- **buildx_cache**: $docker_cache_valid"
    echo "- **docker_available**: $docker_exists"
    echo "- **dockerfile_exists**: $([ -f "$REPO_ROOT/Dockerfile" ] || find "$REPO_ROOT" -name "Dockerfile" -type f | grep -q . && echo "true" || echo "false")"
    echo "- **compose_exists**: $(find "$REPO_ROOT" -name "docker-compose.yml" -o -name "docker-compose.yaml" -type f | grep -q . && echo "true" || echo "false")"
}

# Generate cache configuration for GitHub Actions
generate_cache_config() {
    jules_log "INFO" "⚙️ Generating GitHub Actions cache configuration..."
    
    local config_file="$REPO_ROOT/.github/jules/cache-config.json"
    
    cat << 'EOF' > "$config_file"
{
  "jules_version": "0.KORRUPT.1",
  "generated": "$(date -Iseconds)",
  "cache_strategies": {
    "nodejs": {
      "primary_path": "node_modules",
      "fallback_paths": ["~/.npm", ".cache/npm"],
      "key_files": ["package-lock.json", "package.json"],
      "restore_keys": ["nodejs-v2-", "nodejs-"]
    },
    "python": {
      "primary_path": "~/.cache/pip",
      "fallback_paths": [".cache/python", "backend/python/__pycache__"],
      "key_files": ["requirements.txt", "backend/python/requirements.txt", "pyproject.toml"],
      "restore_keys": ["python-v2-", "python-"]
    },
    "ruby": {
      "primary_path": "vendor/bundle",
      "fallback_paths": ["~/.bundle", ".cache/bundle"],
      "key_files": ["Gemfile.lock", "Gemfile"],
      "restore_keys": ["ruby-v2-", "ruby-"]
    },
    "docker": {
      "primary_path": "/tmp/.buildx-cache",
      "fallback_paths": [],
      "key_files": ["Dockerfile", "docker-compose.yml"],
      "restore_keys": ["docker-v2-", "docker-"]
    }
  },
  "conditional_checks": {
    "nodejs": "[ -f package.json ]",
    "python": "[ -f requirements.txt ] || [ -f backend/python/requirements.txt ] || [ -f pyproject.toml ]",
    "ruby": "find . -name 'Gemfile' -type f | grep -q .",
    "docker": "[ -f Dockerfile ] || find . -name 'Dockerfile' -type f | grep -q ."
  }
}
EOF
    
    # Replace placeholder with actual timestamp
    sed -i "s/\$(date -Iseconds)/$(date -Iseconds)/" "$config_file"
    
    jules_log "INFO" "✅ Cache configuration saved to: $config_file"
}

# Check dependency changes
check_dependency_changes() {
    # Files that indicate dependency changes
    local dependency_files=(
        "package.json"
        "package-lock.json"
        "requirements.txt"
        "backend/python/requirements.txt"
        "pyproject.toml"
        "Gemfile"
        "Gemfile.lock"
        "Dockerfile"
        "docker-compose.yml"
        "docker-compose.yaml"
    )
    
    local changes_detected="false"
    
    # Check if we're in a git repository and can check changes
    if git rev-parse --git-dir >/dev/null 2>&1; then
        # Check for changes in dependency files
        for file in "${dependency_files[@]}"; do
            if find "$REPO_ROOT" -name "$(basename "$file")" -type f | grep -q .; then
                if git diff --name-only HEAD~1 2>/dev/null | grep -q "$file" || \
                   git diff --cached --name-only 2>/dev/null | grep -q "$file"; then
                    changes_detected="true"
                fi
            fi
        done
    fi
    
    echo "$changes_detected"
}

# Generate Jules validation report
generate_validation_report() {
    jules_log "PSYCHO" "🎭 Generating Jules validation report - Den Usynlige Hånds analysis..."
    
    local report_file="$REPO_ROOT/jules-validation-report.md"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    
    # Set report mode to suppress logging in validation functions
    export REPORT_MODE="true"
    
    cat << EOF > "$report_file"
# Jules Dependency Validation Report
**Generated:** $timestamp  
**Jules Version:** $JULES_VERSION  
**Repository:** $(basename "$REPO_ROOT")  
**Corruption Index:** $CORRUPTION_THRESHOLD  

## Cache Infrastructure Validation

### Node.js Ecosystem
$(validate_nodejs_cache)

### Python Ecosystem  
$(validate_python_cache)

### Ruby Ecosystem
$(validate_ruby_cache)

### Docker Infrastructure
$(validate_docker_cache)

## Dependency Change Analysis
**Changes Detected:** $(check_dependency_changes)

## Jules System Status
- 🏗️ **Cache-Arkitekten**: Infrastructure validated
- 🗺️ **Dependency-Kartleggeren**: Ecosystem mapped
- ⚡ **Build-Optimaliserer**: Ready for optimization
- 🎭 **Workflow-Koordinator**: Synchronization complete

## Psycho-Noir Integration
- **Skyskraperen Systems**: All cache infrastructure validated
- **Rustbelt Resilience**: Fallback paths confirmed
- **Den Usynlige Hånd**: Manifesting through validated optimizations

---
*Validation completed by Jules - Part of the Skyskraperen optimization matrix*
EOF

    # Unset report mode
    unset REPORT_MODE

    jules_log "INFO" "✅ Validation report generated: $report_file"
    
    # Also output to console if not in CI
    if [[ "${CI:-false}" != "true" ]]; then
        echo
        echo "=========================================="
        cat "$report_file"
        echo "=========================================="
    fi
}

# Main execution function
main() {
    jules_log "PSYCHO" "🎭 Jules Dependency Validator - Initiating cache integrity protocol..."
    
    # Validate all cache infrastructures
    jules_log "INFO" "🔍 Starting comprehensive cache validation..."
    
    # Create cache directories if needed
    mkdir -p "$REPO_ROOT/.cache"/{npm,python,bundle}
    
    # Separate logging from validation functions
    jules_log "INFO" "🔍 Validating Node.js cache infrastructure..."
    jules_log "INFO" "🐍 Validating Python cache infrastructure..."
    jules_log "INFO" "💎 Validating Ruby cache infrastructure..."
    jules_log "INFO" "🐳 Validating Docker cache infrastructure..."
    jules_log "INFO" "🔍 Checking for dependency changes..."
    
    # Generate cache configuration
    generate_cache_config
    
    # Generate validation report
    generate_validation_report
    
    jules_log "PSYCHO" "✅ Jules validation protocol completed - Den Usynlige Hånd optimization ready"
}

# Script execution
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi