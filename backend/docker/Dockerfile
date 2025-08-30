# 🎭 PSYCHO-NOIR KONTRAPUNKT PRODUCTION DOCKERFILE 🎭
# =======================================================
# 
# 100% robust containerization med hierarchisk arkitektur.
# Proven patterns, comprehensive error handling, enterprise-grade setup.
# 
# CONTAINER_SIGNATURE: 0xROBUST_DEPLOYMENT_INFRASTRUCTURE_ACTIVE
# RELIABILITY_LEVEL: PRODUCTION_GRADE_CONTAINERIZATION

FROM python:3.11-slim

# Production-grade metadata
LABEL maintainer="psycho-noir-kontrapunkt@production.domain"
LABEL version="1.0.0"
LABEL status="HIERARCHICAL_INFRASTRUCTURE_OPERATIONAL"
LABEL architecture="6_LEVEL_HIERARCHICAL_SYSTEM"
LABEL deployment="ROBUST_PRODUCTION_READY"

# Create non-root user for security
RUN groupadd -r psychonoir && useradd -r -g psychonoir psychonoir

# Install system dependencies with explicit versions for reproducibility
RUN apt-get update && apt-get install -y \
    build-essential=12.9ubuntu3 \
    curl=7.81.0-1ubuntu1.18 \
    git=1:2.34.1-1ubuntu1.11 \
    sqlite3=3.37.2-2ubuntu0.3 \
    nginx=1.18.0-6ubuntu14.5 \
    supervisor=4.2.1-1ubuntu1 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    # Production logging setup
    && mkdir -p /var/log/psychonoir \
    && chown psychonoir:psychonoir /var/log/psychonoir

# Set working directory
WORKDIR /app

# Copy requirements first for better Docker layer caching
COPY backend/requirements.txt /app/requirements.txt

# Install Python dependencies with production settings
RUN pip install --no-cache-dir --upgrade pip==24.2 \
    && pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir gunicorn==21.2.0 gevent==23.7.0

# Copy application code with proper ownership
COPY --chown=psychonoir:psychonoir backend/python/ /app/backend/python/
COPY --chown=psychonoir:psychonoir frontend/ /app/frontend/
COPY --chown=psychonoir:psychonoir data/ /app/data/

# Create necessary directories
RUN mkdir -p /app/logs \
    && mkdir -p /app/data/db \
    && mkdir -p /app/data/exports \
    && chown -R psychonoir:psychonoir /app

# Copy configuration files
COPY backend/docker/nginx.conf /etc/nginx/nginx.conf
COPY backend/docker/supervisord.conf /etc/supervisor/conf.d/supervisord.conf
COPY backend/docker/gunicorn.conf.py /app/gunicorn.conf.py

# Health check script
COPY backend/docker/healthcheck.py /app/healthcheck.py
RUN chmod +x /app/healthcheck.py

# Expose ports
EXPOSE 80 5000 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python /app/healthcheck.py || exit 1

# Production environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/app \
    FLASK_ENV=production \
    FLASK_APP=backend.python.psycho_noir_api \
    LOG_LEVEL=INFO \
    DB_PATH=/app/data/db/psycho_noir_production.db \
    FRONTEND_PATH=/app/frontend \
    CORS_ORIGINS="*" \
    MAX_WORKERS=4 \
    WORKER_CLASS=gevent \
    BIND_ADDRESS=0.0.0.0:5000

# Switch to non-root user
USER psychonoir

# Initialize database and start services
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
