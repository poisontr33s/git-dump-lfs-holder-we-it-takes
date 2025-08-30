#!/bin/bash

# 🎭 PSYCHO-NOIR KONTRAPUNKT DEPLOYMENT ORCHESTRATOR 🎭
# =====================================================
#
# Advanced deployment script med environment-specific logic,
# health checks, rollback capabilities, og comprehensive logging.
#
# DEPLOYMENT_SIGNATURE: 0xORCHESTRATED_DEPLOYMENT_OPERATIONAL
# AUTOMATION_LEVEL: ENTERPRISE_GRADE_ORCHESTRATION

set -euo pipefail

# 🎭 Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd)"
PROJECT_ROOT="$(dirname "$(dirname "$SCRIPT_DIR")")"
DEPLOYMENT_CONFIG="$SCRIPT_DIR/deployment-config.yml"
DOCKER_COMPOSE="$SCRIPT_DIR/docker-compose.yml"
LOG_FILE="/tmp/psychonoir-deployment-$(date +%Y%m%d_%H%M%S).log"

# 🎨 Colors for neural-noir aesthetics
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m'

# 🎭 Logging Functions
log() {
    local level="$1"
    shift
    local message="$*"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    echo -e "${timestamp} [${level}] ${message}" | tee -a "$LOG_FILE"
}

info() {
    log "${CYAN}INFO${NC}" "$*"
}

warn() {
    log "${YELLOW}WARN${NC}" "$*"
}

error() {
    log "${RED}ERROR${NC}" "$*"
}

success() {
    log "${GREEN}SUCCESS${NC}" "$*"
}

neural_header() {
    echo -e "${MAGENTA}"
    cat << 'EOF'
🎭 ================================================ 🎭
    PSYCHO-NOIR KONTRAPUNKT DEPLOYMENT ENGINE
    
    Neural Orchestration Protocol: ACTIVE
    Deployment Signature: 0xDEPLOYMENT_ORCHESTRATED
🎭 ================================================ 🎭
EOF
    echo -e "${NC}"
}

# 🔍 Functions
show_usage() {
    cat << EOF
🎭 Psycho-Noir Kontrapunkt Deployment Script

Usage: $0 [OPTIONS] <environment>

Environments:
  production  - Full production deployment
  staging     - Staging environment 
  testing     - Testing environment
  development - Development environment

Options:
  -h, --help              Show this help message
  -v, --verbose           Enable verbose logging
  -d, --dry-run           Simulate deployment without executing
  -f, --force             Force deployment without confirmation
  -r, --rollback          Rollback to previous version
  -b, --backup            Create backup before deployment
  -m, --monitor           Enable post-deployment monitoring
  --image-tag TAG         Use specific image tag
  --health-timeout SECS   Health check timeout (default: 300)

Examples:
  $0 staging
  $0 production --backup --monitor
  $0 testing --dry-run --verbose
  $0 production --rollback
EOF
}

# 🏥 Health Check Function
health_check() {
    local environment="$1"
    local timeout="${2:-300}"
    local url="http://localhost"
    
    case "$environment" in
        production) url="http://localhost:80" ;;
        staging) url="http://localhost:8080" ;;
        testing) url="http://localhost:8888" ;;
        development) url="http://localhost:5000" ;;
    esac
    
    info "🏥 Performing health check for $environment environment..."
    info "🔍 Health check URL: $url/health"
    
    local start_time=$(date +%s)
    local end_time=$((start_time + timeout))
    
    while [ $(date +%s) -lt $end_time ]; do
        if curl -s -f "$url/health" > /dev/null 2>&1; then
            success "✅ Health check PASSED for $environment"
            return 0
        fi
        
        info "⏳ Waiting for service to be ready... ($(( end_time - $(date +%s) ))s remaining)"
        sleep 5
    done
    
    error "❌ Health check FAILED for $environment after ${timeout}s"
    return 1
}

# 📦 Backup Function
create_backup() {
    local environment="$1"
    
    info "📦 Creating backup for $environment environment..."
    
    local backup_dir="/tmp/psychonoir-backup-$(date +%Y%m%d_%H%M%S)"
    mkdir -p "$backup_dir"
    
    # Backup database
    if [ -f "data/psycho_noir_${environment}.db" ]; then
        cp "data/psycho_noir_${environment}.db" "$backup_dir/"
        success "✅ Database backup created"
    fi
    
    # Backup configuration
    if [ -f "$DEPLOYMENT_CONFIG" ]; then
        cp "$DEPLOYMENT_CONFIG" "$backup_dir/"
        success "✅ Configuration backup created"
    fi
    
    # Backup logs
    if [ -d "logs" ]; then
        cp -r logs "$backup_dir/"
        success "✅ Logs backup created"
    fi
    
    echo "$backup_dir" > "/tmp/psychonoir-last-backup-$environment"
    success "📦 Backup completed: $backup_dir"
}

# 🔄 Rollback Function
rollback_deployment() {
    local environment="$1"
    
    warn "🔄 Initiating rollback for $environment environment..."
    
    local backup_file="/tmp/psychonoir-last-backup-$environment"
    if [ ! -f "$backup_file" ]; then
        error "❌ No backup found for rollback"
        return 1
    fi
    
    local backup_dir=$(cat "$backup_file")
    if [ ! -d "$backup_dir" ]; then
        error "❌ Backup directory not found: $backup_dir"
        return 1
    fi
    
    # Stop current services
    info "🛑 Stopping current services..."
    docker-compose -f "$DOCKER_COMPOSE" down || true
    
    # Restore from backup
    info "📦 Restoring from backup: $backup_dir"
    
    if [ -f "$backup_dir/psycho_noir_${environment}.db" ]; then
        cp "$backup_dir/psycho_noir_${environment}.db" "data/"
        success "✅ Database restored"
    fi
    
    if [ -f "$backup_dir/deployment-config.yml" ]; then
        cp "$backup_dir/deployment-config.yml" "$SCRIPT_DIR/"
        success "✅ Configuration restored"
    fi
    
    # Restart services
    info "🚀 Restarting services after rollback..."
    docker-compose -f "$DOCKER_COMPOSE" up -d
    
    success "🔄 Rollback completed for $environment"
}

# 🚀 Main Deployment Function
deploy_environment() {
    local environment="$1"
    local image_tag="${2:-latest}"
    local dry_run="$3"
    local force="$4"
    local create_backup_flag="$5"
    
    info "🚀 Starting deployment for environment: $environment"
    info "🏷️ Image tag: $image_tag"
    
    # Validate environment
    if ! yq eval ".${environment}" "$DEPLOYMENT_CONFIG" > /dev/null 2>&1; then
        error "❌ Invalid environment: $environment"
        return 1
    fi
    
    # Create backup if requested
    if [ "$create_backup_flag" = "true" ]; then
        create_backup "$environment"
    fi
    
    # Confirmation prompt
    if [ "$force" != "true" ] && [ "$dry_run" != "true" ]; then
        echo -e "${YELLOW}⚠️  About to deploy to $environment environment${NC}"
        read -p "Continue? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            info "🚫 Deployment cancelled by user"
            return 1
        fi
    fi
    
    if [ "$dry_run" = "true" ]; then
        info "🎭 DRY RUN MODE - Simulating deployment..."
        info "Would deploy $image_tag to $environment"
        info "Configuration: $(yq eval ".${environment}" "$DEPLOYMENT_CONFIG")"
        return 0
    fi
    
    # Pull latest image
    info "📥 Pulling container image: $image_tag"
    docker pull "ghcr.io/poisontr33s/psychonoir-kontrapunkt:$image_tag" || {
        warn "⚠️  Failed to pull image, using local version"
    }
    
    # Set environment variables
    export ENVIRONMENT="$environment"
    export IMAGE_TAG="$image_tag"
    
    # Deploy with docker-compose
    info "🐳 Deploying containers..."
    docker-compose -f "$DOCKER_COMPOSE" down || true
    docker-compose -f "$DOCKER_COMPOSE" up -d
    
    # Wait for services to start
    info "⏳ Waiting for services to initialize..."
    sleep 10
    
    # Health check
    if ! health_check "$environment"; then
        error "❌ Deployment failed health check"
        warn "🔄 Consider running rollback: $0 $environment --rollback"
        return 1
    fi
    
    success "🎭 Deployment SUCCESSFUL for $environment"
    success "🏷️ Image: $image_tag"
    success "📊 Services: $(docker-compose -f "$DOCKER_COMPOSE" ps --services | wc -l)"
    success "🔗 Endpoint: $(yq eval ".${environment}.ports[0]" "$DEPLOYMENT_CONFIG")"
}

# 📊 Monitoring Function
post_deployment_monitoring() {
    local environment="$1"
    
    info "📊 Starting post-deployment monitoring for $environment..."
    
    # Monitor for 5 minutes
    local end_time=$(($(date +%s) + 300))
    
    while [ $(date +%s) -lt $end_time ]; do
        local remaining=$((end_time - $(date +%s)))
        
        # Check container status
        local running_containers=$(docker-compose -f "$DOCKER_COMPOSE" ps -q | wc -l)
        
        # Check health endpoint
        local health_status="UNKNOWN"
        if curl -s -f "http://localhost/health" > /dev/null 2>&1; then
            health_status="HEALTHY"
        else
            health_status="UNHEALTHY"
        fi
        
        info "📊 Monitoring ($remaining s remaining): Containers: $running_containers, Health: $health_status"
        
        sleep 30
    done
    
    success "📊 Monitoring completed for $environment"
}

# 🎭 Main Script Logic
main() {
    local environment=""
    local dry_run="false"
    local verbose="false"
    local force="false"
    local rollback="false"
    local backup="false"
    local monitor="false"
    local image_tag="latest"
    local health_timeout="300"
    
    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            -h|--help)
                show_usage
                exit 0
                ;;
            -v|--verbose)
                verbose="true"
                set -x
                shift
                ;;
            -d|--dry-run)
                dry_run="true"
                shift
                ;;
            -f|--force)
                force="true"
                shift
                ;;
            -r|--rollback)
                rollback="true"
                shift
                ;;
            -b|--backup)
                backup="true"
                shift
                ;;
            -m|--monitor)
                monitor="true"
                shift
                ;;
            --image-tag)
                image_tag="$2"
                shift 2
                ;;
            --health-timeout)
                health_timeout="$2"
                shift 2
                ;;
            production|staging|testing|development)
                environment="$1"
                shift
                ;;
            *)
                error "Unknown option: $1"
                show_usage
                exit 1
                ;;
        esac
    done
    
    # Validate required arguments
    if [ -z "$environment" ]; then
        error "❌ Environment is required"
        show_usage
        exit 1
    fi
    
    # Initialize
    neural_header
    info "🎭 Initializing Neural Deployment Protocol..."
    info "📂 Project root: $PROJECT_ROOT"
    info "📋 Log file: $LOG_FILE"
    
    # Change to project directory
    cd "$PROJECT_ROOT"
    
    # Execute deployment
    if [ "$rollback" = "true" ]; then
        rollback_deployment "$environment"
    else
        deploy_environment "$environment" "$image_tag" "$dry_run" "$force" "$backup"
        
        if [ "$monitor" = "true" ] && [ "$dry_run" != "true" ]; then
            post_deployment_monitoring "$environment"
        fi
    fi
    
    success "🎭 Deployment orchestration completed"
    success "📋 Full log available at: $LOG_FILE"
}

# 🚀 Execute Main Function
main "$@"
