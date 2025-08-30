# 🐍 PSYCHO-NOIR KONTRAPUNKT GUNICORN CONFIGURATION 🐍
# ======================================================
# 
# 100% robust WSGI server configuration med production settings.
# Proven patterns, optimal performance, comprehensive error handling.
# 
# GUNICORN_SIGNATURE: 0xROBUST_WSGI_SERVER_OPERATIONAL
# PERFORMANCE_LEVEL: ENTERPRISE_GRADE_OPTIMIZATION

import multiprocessing
import os

# Server socket
bind = os.environ.get('BIND_ADDRESS', '0.0.0.0:5000')
backlog = 2048

# Worker processes
workers = int(os.environ.get('MAX_WORKERS', multiprocessing.cpu_count() * 2 + 1))
worker_class = os.environ.get('WORKER_CLASS', 'gevent')
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 50
preload_app = True
timeout = 30
keepalive = 2

# Restart workers
max_requests = 1000
max_requests_jitter = 100
worker_tmp_dir = '/dev/shm'

# Logging
accesslog = '/var/log/psychonoir/gunicorn_access.log'
errorlog = '/var/log/psychonoir/gunicorn_error.log'
loglevel = os.environ.get('LOG_LEVEL', 'info').lower()
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

# Process naming
proc_name = 'psychonoir_gunicorn'

# Security
limit_request_line = 4094
limit_request_fields = 100
limit_request_field_size = 8190

# SSL configuration (if certificates are available)
keyfile = os.environ.get('SSL_KEYFILE')
certfile = os.environ.get('SSL_CERTFILE')
ca_certs = os.environ.get('SSL_CA_CERTS')
ssl_version = 2  # TLS

# Performance tuning
sendfile = True

# Development vs Production settings
if os.environ.get('FLASK_ENV') == 'development':
    reload = True
    workers = 1
    loglevel = 'debug'
else:
    # Production optimizations
    preload_app = True
    worker_tmp_dir = '/dev/shm'
    
# Error handling
def when_ready(server):
    """Called just after the server is started."""
    server.log.info("🎭 Psycho-Noir Kontrapunkt API server ready")
    server.log.info(f"🌐 Listening on: {bind}")
    server.log.info(f"👥 Workers: {workers}")
    server.log.info(f"⚙️ Worker class: {worker_class}")

def worker_int(worker):
    """Called just after a worker exited on SIGINT or SIGQUIT."""
    worker.log.info("🔄 Worker received INT or QUIT signal")

def pre_fork(server, worker):
    """Called just before a worker is forked."""
    server.log.info(f"🚀 Worker {worker.pid} forked")

def post_fork(server, worker):
    """Called just after a worker has been forked."""
    server.log.info(f"✅ Worker {worker.pid} initialized")

def worker_abort(worker):
    """Called when a worker received the SIGABRT signal."""
    worker.log.error(f"❌ Worker {worker.pid} aborted")

def pre_exec(server):
    """Called just before a new master process is forked."""
    server.log.info("🔄 Pre-exec: Forking new master process")

def pre_request(worker, req):
    """Called just before a worker processes the request."""
    worker.log.debug(f"📨 Processing request: {req.uri}")

def post_request(worker, req, environ, resp):
    """Called after a worker processes the request."""
    worker.log.debug(f"✅ Request completed: {req.uri} - {resp.status}")

# Custom error handlers
def on_exit(server):
    """Called just before exiting."""
    server.log.info("🛑 Psycho-Noir Kontrapunkt API server shutting down")

def on_reload(server):
    """Called to recycle workers during a reload via SIGHUP."""
    server.log.info("🔄 Reloading Psycho-Noir Kontrapunkt API server")

# Environment-specific configurations
pythonpath = '/app'
chdir = '/app'

# User and group (security)
user = 'psychonoir'
group = 'psychonoir'

# File permissions
umask = 0o027

# Graceful shutdown
graceful_timeout = 120

# Thread settings (if using threaded workers)
threads = 2
thread_class = 'gevent'

# Memory optimization
worker_tmp_dir = '/dev/shm'

# Custom application factory
def application(environ, start_response):
    """Custom WSGI application factory with error handling."""
    try:
        from backend.python.psycho_noir_api import app
        return app(environ, start_response)
    except Exception as e:
        import traceback
        error_msg = f"❌ Application factory error: {e}\n{traceback.format_exc()}"
        print(error_msg)
        start_response('500 Internal Server Error', [('Content-Type', 'text/plain')])
        return [error_msg.encode('utf-8')]
