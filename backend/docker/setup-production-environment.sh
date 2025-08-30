#!/bin/bash

# 🎭 PSYCHO-NOIR KONTRAPUNKT PRODUCTION ENVIRONMENT SETUP 🎭
# ===========================================================
#
# Complete production environment initialization script
# Med security hardening, SSL setup, og system optimization
#
# PRODUCTION_SETUP_SIGNATURE: 0xPRODUCTION_ENVIRONMENT_INITIALIZED
# SECURITY_LEVEL: ENTERPRISE_HARDENED

set -euo pipefail

# 🎭 Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd)"
PROJECT_ROOT="$(dirname "$(dirname "$SCRIPT_DIR")")"
PRODUCTION_BASE_DIR="/var/psychonoir/production"
SSL_BASE_DIR="/etc/ssl/psychonoir"
LOG_FILE="/var/log/psychonoir-production-setup-$(date +%Y%m%d_%H%M%S).log"

# 🎨 Colors
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
    echo -e "${timestamp} [${level}] ${message}" | tee -a "$LOG_FILE" 2>/dev/null || echo -e "${timestamp} [${level}] ${message}"
}

info() { log "${CYAN}INFO${NC}" "$*"; }
warn() { log "${YELLOW}WARN${NC}" "$*"; }
error() { log "${RED}ERROR${NC}" "$*"; }
success() { log "${GREEN}SUCCESS${NC}" "$*"; }

neural_header() {
    echo -e "${MAGENTA}"
    cat << 'EOF'
🎭 ============================================================ 🎭
    PSYCHO-NOIR KONTRAPUNKT PRODUCTION ENVIRONMENT SETUP
    
    Neural Production Protocol: INITIALIZING
    Security Level: ENTERPRISE_HARDENED
    Environment Signature: 0xPRODUCTION_ENVIRONMENT_SETUP
🎭 ============================================================ 🎭
EOF
    echo -e "${NC}"
}

# 🛡️ Security Validation
check_root_privileges() {
    if [[ $EUID -ne 0 ]]; then
        error "❌ This script must be run as root for production setup"
        exit 1
    fi
    success "✅ Root privileges confirmed"
}

# 📂 Directory Structure Setup
setup_directory_structure() {
    info "📂 Setting up production directory structure..."
    
    local directories=(
        "$PRODUCTION_BASE_DIR"
        "$PRODUCTION_BASE_DIR/data"
        "$PRODUCTION_BASE_DIR/data/db"
        "$PRODUCTION_BASE_DIR/postgres"
        "$PRODUCTION_BASE_DIR/postgres-backups"
        "$PRODUCTION_BASE_DIR/redis"
        "$PRODUCTION_BASE_DIR/prometheus"
        "$PRODUCTION_BASE_DIR/grafana"
        "$PRODUCTION_BASE_DIR/alertmanager"
        "$PRODUCTION_BASE_DIR/backups"
        "$PRODUCTION_BASE_DIR/config"
        "/var/log/psychonoir/production"
        "/var/log/nginx/psychonoir"
        "$SSL_BASE_DIR"
        "/etc/psychonoir/backup"
    )
    
    for dir in "${directories[@]}"; do
        if [[ ! -d "$dir" ]]; then
            mkdir -p "$dir"
            info "📁 Created directory: $dir"
        else
            info "📁 Directory exists: $dir"
        fi
    done
    
    # Set proper permissions
    chown -R 1000:1000 "$PRODUCTION_BASE_DIR"
    chmod -R 755 "$PRODUCTION_BASE_DIR"
    chmod -R 750 "$SSL_BASE_DIR"
    
    success "✅ Directory structure setup completed"
}

# 🔐 SSL Certificate Setup
setup_ssl_certificates() {
    info "🔐 Setting up SSL certificates..."
    
    local ssl_config="$SSL_BASE_DIR/openssl.conf"
    
    # Create SSL configuration
    cat > "$ssl_config" << EOF
[req]
distinguished_name = req_distinguished_name
req_extensions = v3_req
prompt = no

[req_distinguished_name]
C = NO
ST = Oslo
L = Oslo  
O = Psycho-Noir Kontrapunkt
OU = Neural Archaeology Division
CN = psychonoir.local

[v3_req]
keyUsage = nonRepudiation, digitalSignature, keyEncipherment
subjectAltName = @alt_names

[alt_names]
DNS.1 = psychonoir.local
DNS.2 = *.psychonoir.local
DNS.3 = grafana.psychonoir.local
DNS.4 = prometheus.psychonoir.local
DNS.5 = alerts.psychonoir.local
IP.1 = 127.0.0.1
IP.2 = ::1
EOF

    # Generate SSL certificates if they don't exist
    if [[ ! -f "$SSL_BASE_DIR/psychonoir.crt" ]]; then
        info "🔑 Generating SSL certificates..."
        
        # Generate private key
        openssl genrsa -out "$SSL_BASE_DIR/psychonoir.key" 4096
        
        # Generate certificate signing request
        openssl req -new -key "$SSL_BASE_DIR/psychonoir.key" \
            -out "$SSL_BASE_DIR/psychonoir.csr" \
            -config "$ssl_config"
        
        # Generate self-signed certificate
        openssl x509 -req -days 365 \
            -in "$SSL_BASE_DIR/psychonoir.csr" \
            -signkey "$SSL_BASE_DIR/psychonoir.key" \
            -out "$SSL_BASE_DIR/psychonoir.crt" \
            -extensions v3_req \
            -extfile "$ssl_config"
        
        # Create service-specific certificates
        cp "$SSL_BASE_DIR/psychonoir.crt" "$SSL_BASE_DIR/grafana.crt"
        cp "$SSL_BASE_DIR/psychonoir.key" "$SSL_BASE_DIR/grafana.key"
        
        # Set proper permissions
        chmod 600 "$SSL_BASE_DIR"/*.key
        chmod 644 "$SSL_BASE_DIR"/*.crt
        
        success "✅ SSL certificates generated"
    else
        success "✅ SSL certificates already exist"
    fi
}

# 🔧 System Optimization
optimize_system() {
    info "🔧 Optimizing system for production workload..."
    
    # Kernel parameters for high-performance applications
    cat > /etc/sysctl.d/99-psychonoir-production.conf << EOF
# 🎭 Psycho-Noir Kontrapunkt Production Optimizations

# Network optimizations
net.core.somaxconn = 1024
net.core.netdev_max_backlog = 5000
net.ipv4.tcp_max_syn_backlog = 1024
net.ipv4.tcp_congestion_control = bbr
net.ipv4.tcp_slow_start_after_idle = 0

# Memory management
vm.swappiness = 10
vm.dirty_ratio = 15
vm.dirty_background_ratio = 5
vm.max_map_count = 262144

# File system optimizations
fs.file-max = 65536
fs.inotify.max_user_watches = 524288

# Security enhancements
kernel.dmesg_restrict = 1
kernel.kptr_restrict = 2
kernel.yama.ptrace_scope = 1
net.ipv4.conf.all.send_redirects = 0
net.ipv4.conf.default.send_redirects = 0
net.ipv4.conf.all.accept_redirects = 0
net.ipv4.conf.default.accept_redirects = 0
EOF

    # Apply kernel parameters
    sysctl -p /etc/sysctl.d/99-psychonoir-production.conf
    
    # Optimize Docker daemon
    mkdir -p /etc/docker
    cat > /etc/docker/daemon.json << EOF
{
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "50m",
    "max-file": "3"
  },
  "storage-driver": "overlay2",
  "live-restore": true,
  "userland-proxy": false,
  "experimental": false,
  "metrics-addr": "127.0.0.1:9323",
  "default-ulimits": {
    "nofile": {
      "Name": "nofile",
      "Hard": 64000,
      "Soft": 64000
    }
  }
}
EOF

    # Restart Docker to apply changes
    systemctl restart docker
    
    success "✅ System optimization completed"
}

# 🔐 Security Hardening
setup_security_hardening() {
    info "🔐 Implementing security hardening measures..."
    
    # Firewall rules
    if command -v ufw &> /dev/null; then
        ufw --force reset
        ufw default deny incoming
        ufw default allow outgoing
        
        # Allow essential services
        ufw allow 22/tcp   # SSH
        ufw allow 80/tcp   # HTTP
        ufw allow 443/tcp  # HTTPS
        ufw allow 3000/tcp # Grafana
        ufw allow 9090/tcp # Prometheus
        ufw allow 9093/tcp # AlertManager
        
        ufw --force enable
        success "✅ Firewall configured"
    fi
    
    # Fail2ban configuration for additional protection
    if command -v fail2ban-server &> /dev/null; then
        cat > /etc/fail2ban/jail.d/psychonoir-production.conf << EOF
[DEFAULT]
bantime = 3600
findtime = 600
maxretry = 3

[sshd]
enabled = true
port = ssh
filter = sshd
logpath = /var/log/auth.log
maxretry = 3

[nginx-http-auth]
enabled = true
port = http,https
filter = nginx-http-auth
logpath = /var/log/nginx/psychonoir/error.log
maxretry = 5

[docker-auth]
enabled = true
port = 2376
filter = docker-auth
logpath = /var/log/docker.log
maxretry = 3
EOF

        systemctl restart fail2ban
        success "✅ Fail2ban configured"
    fi
    
    # AppArmor profiles (if available)
    if command -v aa-status &> /dev/null; then
        info "🛡️ AppArmor security profiles available"
    fi
    
    success "✅ Security hardening completed"
}

# 📊 Environment Configuration
setup_environment_files() {
    info "📊 Setting up environment configuration..."
    
    local env_file="$PRODUCTION_BASE_DIR/config/.env.production"
    
    cat > "$env_file" << EOF
# 🎭 PSYCHO-NOIR KONTRAPUNKT PRODUCTION ENVIRONMENT
# =================================================

# Application Configuration
FLASK_ENV=production
LOG_LEVEL=INFO
FRONTEND_PATH=/app/frontend

# Database Configuration
POSTGRES_DB=psychonoir_production
POSTGRES_USER=psychonoir_user
POSTGRES_PASSWORD=CHANGE_THIS_PASSWORD_IN_PRODUCTION
DB_PATH=/app/data/db/psycho_noir_production.db

# Security Configuration
CORS_ORIGINS=https://psychonoir.yourdomain.com
SSL_ENABLED=true
RATE_LIMIT_ENABLED=true
RATE_LIMIT_REQUESTS=1000
RATE_LIMIT_WINDOW=3600
CSRF_PROTECTION_ENABLED=true
SESSION_COOKIE_SECURE=true
SESSION_COOKIE_HTTPONLY=true

# Performance Configuration
PRODUCTION_MAX_WORKERS=8
PRODUCTION_WORKER_CONNECTIONS=1000

# Monitoring Configuration  
GRAFANA_ADMIN_PASSWORD=CHANGE_THIS_PASSWORD_IN_PRODUCTION
GRAFANA_DOMAIN=grafana.psychonoir.local

# Backup Configuration
BACKUP_S3_ENABLED=false
BACKUP_S3_BUCKET=
BACKUP_S3_REGION=
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
BACKUP_WEBHOOK_URL=

# Email Configuration
SMTP_ENABLED=false
SMTP_HOST=
SMTP_USER=
SMTP_PASSWORD=
SMTP_FROM_ADDRESS=noreply@psychonoir.local
EOF

    chmod 600 "$env_file"
    chown 1000:1000 "$env_file"
    
    warn "⚠️  IMPORTANT: Update passwords and sensitive configuration in $env_file"
    success "✅ Environment configuration created"
}

# 🚀 Service Validation
validate_production_setup() {
    info "🚀 Validating production setup..."
    
    # Check Docker availability
    if ! docker --version &> /dev/null; then
        error "❌ Docker is not installed or not accessible"
        return 1
    fi
    
    # Check Docker Compose
    if ! docker compose version &> /dev/null; then
        error "❌ Docker Compose is not installed or not accessible"
        return 1
    fi
    
    # Validate SSL certificates
    if [[ -f "$SSL_BASE_DIR/psychonoir.crt" ]] && [[ -f "$SSL_BASE_DIR/psychonoir.key" ]]; then
        if openssl x509 -in "$SSL_BASE_DIR/psychonoir.crt" -text -noout &> /dev/null; then
            success "✅ SSL certificates are valid"
        else
            error "❌ SSL certificates are invalid"
            return 1
        fi
    else
        error "❌ SSL certificates are missing"
        return 1
    fi
    
    # Check directory permissions
    if [[ -d "$PRODUCTION_BASE_DIR" ]] && [[ -r "$PRODUCTION_BASE_DIR" ]] && [[ -w "$PRODUCTION_BASE_DIR" ]]; then
        success "✅ Production directories are accessible"
    else
        error "❌ Production directories have permission issues"
        return 1
    fi
    
    success "✅ Production setup validation completed"
}

# 📋 Usage Instructions
show_post_setup_instructions() {
    info "📋 Production Environment Setup Complete!"
    
    cat << EOF

🎭 PSYCHO-NOIR KONTRAPUNKT PRODUCTION ENVIRONMENT READY 🎭
============================================================

Next Steps:
1. 🔐 Update passwords in: $PRODUCTION_BASE_DIR/config/.env.production
2. 🌐 Configure your domain DNS to point to this server
3. 🚀 Deploy the application:
   cd $PROJECT_ROOT
   docker compose -f backend/docker/docker-compose.production.yml --env-file $PRODUCTION_BASE_DIR/config/.env.production up -d

4. 📊 Access services:
   - Application: https://your-domain.com
   - Grafana: https://grafana.your-domain.com:3000
   - Prometheus: https://prometheus.your-domain.com:9090

5. 🔍 Monitor logs:
   - Application: /var/log/psychonoir/production/
   - Nginx: /var/log/nginx/psychonoir/
   - System: $LOG_FILE

6. 🔄 Setup automated backups by enabling the backup profile:
   docker compose -f backend/docker/docker-compose.production.yml --profile backup up -d

Security Notes:
- 🛡️ Firewall is configured and active
- 🔐 SSL certificates are self-signed (replace with CA-signed for production)
- 🚨 Fail2ban is configured for intrusion prevention
- 📊 All services run with security hardening enabled

Environment Signature: 0xPRODUCTION_ENVIRONMENT_OPERATIONAL
============================================================

EOF
}

# 🎭 Main Setup Function
main() {
    neural_header
    
    info "🎭 Starting production environment setup..."
    
    # Validate prerequisites
    check_root_privileges
    
    # Core setup functions
    setup_directory_structure
    setup_ssl_certificates
    optimize_system
    setup_security_hardening
    setup_environment_files
    validate_production_setup
    
    # Complete setup
    show_post_setup_instructions
    
    success "🎭 Production environment setup completed successfully!"
    success "📋 Setup log available at: $LOG_FILE"
}

# 🚀 Execute Main Function
main "$@"
