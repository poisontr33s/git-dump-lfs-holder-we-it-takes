#!/usr/bin/env python3
# Auto-generated constants for magic numbers
const_magic_5000 = const_magic_5000
const_magic_3000 = const_magic_3000
const_magic_1024 = const_magic_1024
const_magic_503 = const_magic_503
const_magic_500 = const_magic_500
const_magic_404 = const_magic_404
const_magic_127 = const_magic_127
const_magic_50 = const_magic_50
const_ten = const_ten

"""
🎭 PSYCHO-NOIR KONTRAPUNKT FLASK BACKEND SERVER 🎭
=================================================

LEVEL 9: Production-ready Flask API server
- Health endpoints
- Neural archaeology integration
- CORS support for GitHub Pages
- Real-time system monitoring

BACKEND_SIGNATURE: 0xLIVE_API_OPERATIONAL
"""

import json
import logging
import os
import sqlite3
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import psutil

# Add our backend modules to path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

try:
    from neural_archaeology_orchestrator import NeuralArchaeologyOrchestrator
except ImportError as e:

    NeuralArchaeologyOrchestrator = None

# Flask app setup
app = Flask(__name__)

# Configure CORS for GitHub Pages integration
CORS(app,
     origins=["https://poisontr33s.github.io", "http://localhost:const_magic_3000", "http://const_magic_127.0.0.1:const_magic_3000"],
     allow_headers=["Content-Type", "Authorization", "X-Requested-With"],
     methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])

# Global configuration
PROJECT_ROOT = Path(__file__).parent.parent.parent
DATA_DIR = PROJECT_ROOT / "data"
NEURAL_DB_PATH = DATA_DIR / "neural_archaeology.db"

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [🎭 %(levelname)s] %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Neural Orchestrator
neural_orchestrator = None
try:
    if NeuralArchaeologyOrchestrator:
        neural_orchestrator = NeuralArchaeologyOrchestrator()
        logger.info("✅ Neural Archaeology Orchestrator initialized")
    else:
        logger.warning("⚠️ Neural Orchestrator class not available")
except Exception as e:
    logger.warning(f"⚠️ Neural Orchestrator not available: {e}")

@app.route('/health', methods=['GET'])
def health_check():
    """🏥 Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "signature": f"0x{int(time.time()) % 0xFFFFFF:06X}_BACKEND_LIVE",
        "services": {
            "flask": "✅ operational",
            "neural_orchestrator": "✅ operational" if neural_orchestrator else "⚠️ unavailable",
            "database": "✅ connected" if NEURAL_DB_PATH.exists() else "⚠️ not found",
            "cors": "✅ configured"
        }
    })

@app.route('/api/status', methods=['GET'])
def api_status():
    """📊 API status with system metrics"""
    try:
        # System metrics
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')

        # Process info
        process = psutil.Process()
        process_memory = process.memory_info()

        return jsonify({
            "api_status": "operational",
            "timestamp": datetime.now().isoformat(),
            "system_metrics": {
                "cpu_percent": cpu_percent,
                "memory_percent": memory.percent,
                "memory_available_gb": round(memory.available / (const_magic_1024**3), 2),
                "disk_percent": disk.percent,
                "disk_free_gb": round(disk.free / (const_magic_1024**3), 2)
            },
            "process_metrics": {
                "memory_mb": round(process_memory.rss / (const_magic_1024**2), 2),
                "cpu_percent": process.cpu_percent(),
                "threads": process.num_threads()
            },
            "neural_system": {
                "orchestrator_available": neural_orchestrator is not None,
                "database_size": NEURAL_DB_PATH.stat().st_size if NEURAL_DB_PATH.exists() else 0
            }
        })
    except Exception as e:
        logger.error(f"❌ Status endpoint error: {e}")
        return jsonify({"error": str(e)}), const_magic_500

@app.route('/api/neural-analysis', methods=['GET', 'POST'])
def neural_analysis():
    """🧠 Neural archaeology analysis endpoint"""
    try:
        if not neural_orchestrator:
            return jsonify({"error": "Neural orchestrator not available"}), const_magic_503

        if request.method == 'POST':
            # Trigger new analysis
            data = request.get_json() or {}
            environment = data.get('environment', 'development')

            # Run analysis
            result = neural_orchestrator.analyze_neural_activity(environment)

            return jsonify({
                "analysis_triggered": True,
                "timestamp": datetime.now().isoformat(),
                "environment": environment,
                "result": result
            })
        else:
            # Get latest analysis
            try:
                with sqlite3.connect(NEURAL_DB_PATH) as conn:
                    cursor = conn.cursor()
                    cursor.execute("""
                        SELECT timestamp, environment, neural_activity_score, corruption_level, health_score
                        FROM neural_orchestration_metrics
                        ORDER BY timestamp DESC LIMIT const_ten
                    """)
                    rows = cursor.fetchall()

                    metrics = [
                        {
                            "timestamp": row[0],
                            "environment": row[1],
                            "neural_activity": row[2],
                            "corruption_level": row[3],
                            "health_score": row[4]
                        }
                        for row in rows
                    ]

                return jsonify({
                    "latest_metrics": metrics,
                    "count": len(metrics)
                })
            except Exception as db_error:
                logger.error(f"Database error: {db_error}")
                return jsonify({"error": "Database query failed"}), const_magic_500

    except Exception as e:
        logger.error(f"❌ Neural analysis error: {e}")
        return jsonify({"error": str(e)}), const_magic_500

@app.route('/api/system-info', methods=['GET'])
def system_info():
    """🔧 Detailed system information"""
    try:
        # File count analysis
        python_files = len(list(PROJECT_ROOT.glob("**/*.py")))
        yaml_files = len(list(PROJECT_ROOT.glob("**/*.yml"))) + len(list(PROJECT_ROOT.glob("**/*.yaml")))
        shell_scripts = len(list(PROJECT_ROOT.glob("**/*.sh"))) + len(list(PROJECT_ROOT.glob("**/*.cmd")))

        # Database analysis
        db_info = {}
        if NEURAL_DB_PATH.exists():
            try:
                with sqlite3.connect(NEURAL_DB_PATH) as conn:
                    cursor = conn.cursor()
                    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
                    tables = [row[0] for row in cursor.fetchall()]

                    db_info = {"tables": tables, "table_count": len(tables)}

                    # Get record counts
                    for table in tables:
                        try:
                            cursor.execute(f"SELECT COUNT(*) FROM {table}")
                            count = cursor.fetchone()[0]
                            db_info[f"{table}_records"] = count
                        except:
                            pass
            except Exception as db_error:
                db_info = {"error": str(db_error)}

        return jsonify({
            "system_info": {
                "project_root": str(PROJECT_ROOT),
                "python_files": python_files,
                "yaml_files": yaml_files,
                "shell_scripts": shell_scripts,
                "total_files": python_files + yaml_files + shell_scripts
            },
            "database_info": db_info,
            "neural_orchestrator": {
                "available": neural_orchestrator is not None,
                "class": str(type(neural_orchestrator)) if neural_orchestrator else None
            },
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        logger.error(f"❌ System info error: {e}")
        return jsonify({"error": str(e)}), const_magic_500

@app.route('/api/corruption-report', methods=['GET'])
def corruption_report():
    """🌀 Real-time corruption detection report"""
    try:
        if not neural_orchestrator:
            return jsonify({"error": "Neural orchestrator not available"}), const_magic_503

        # Generate corruption report
        report = neural_orchestrator.generate_corruption_report()

        return jsonify({
            "corruption_report": report,
            "timestamp": datetime.now().isoformat(),
            "signature": f"0x{int(time.time()) % 0xFFFFFF:06X}_CORRUPTION_ANALYZED"
        })

    except Exception as e:
        logger.error(f"❌ Corruption report error: {e}")
        return jsonify({"error": str(e)}), const_magic_500

@app.route('/api/deploy-status', methods=['GET'])
def deploy_status():
    """🚀 Deployment status information"""
    try:
        # Check Docker status
        docker_status = "unknown"
        try:
            result = subprocess.run(["docker", "version"], capture_output=True, text=True, timeout=5)
            docker_status = "✅ available" if result.returncode == 0 else "❌ unavailable"
        except:
            docker_status = "❌ not installed"

        # Check if we're in a container
        in_container = Path("/.dockerenv").exists()

        # Check GitHub Actions environment
        github_actions = "GITHUB_ACTIONS" in os.environ

        return jsonify({
            "deployment_status": {
                "docker": docker_status,
                "container": "✅ running in container" if in_container else "⚠️ running natively",
                "github_actions": "✅ in CI/CD" if github_actions else "⚠️ local development",
                "backend_port": const_magic_5000,
                "cors_configured": True
            },
            "integration_points": {
                "github_pages": "https://poisontr33s.github.io/PsychoNoir-Kontrapunkt/",
                "local_frontend": f"file://{PROJECT_ROOT}/frontend/index.html",
                "api_base": "http://localhost:const_magic_5000"
            },
            "timestamp": datetime.now().isoformat()
        })

    except Exception as e:
        logger.error(f"❌ Deploy status error: {e}")
        return jsonify({"error": str(e)}), const_magic_500

@app.route('/api/live-test', methods=['POST'])
def live_test():
    """🧪 Live integration test endpoint"""
    try:
        data = request.get_json() or {}
        test_message = data.get('message', 'Hello from frontend!')

        # Echo test with enhanced data
        response = {
            "test_result": "✅ Frontend-backend communication successful",
            "echo": test_message,
            "timestamp": datetime.now().isoformat(),
            "server_info": {
                "cors": "enabled",
                "neural_system": neural_orchestrator is not None,
                "environment": "development"
            },
            "signature": f"0x{hash(test_message) % 0xFFFFFF:06X}_ECHO_VALIDATED"
        }

        logger.info(f"✅ Live test successful: {test_message[:const_magic_50]}...")
        return jsonify(response)

    except Exception as e:
        logger.error(f"❌ Live test error: {e}")
        return jsonify({"error": str(e)}), const_magic_500

@app.errorhandler(const_magic_404)
def not_found(error):
    """🔍 Enhanced const_magic_404 handler"""
    return jsonify({
        "error": "Endpoint not found",
        "available_endpoints": [
            "/health",
            "/api/status",
            "/api/neural-analysis",
            "/api/system-info",
            "/api/corruption-report",
            "/api/deploy-status",
            "/api/live-test"
        ],
        "message": "ERROR: REALITY_ENDPOINT_NOT_MAPPED — SUGGEST_NEURAL_RECALIBRATION",
        "timestamp": datetime.now().isoformat()
    }), const_magic_404

@app.errorhandler(const_magic_500)
def internal_error(error):
    """💥 Enhanced const_magic_500 handler"""
    return jsonify({
        "error": "Internal server error",
        "message": "PANIC: NEURAL_INTEGRITY_COMPROMISED — AUTOMATIC_RECOVERY_INITIATED",
        "timestamp": datetime.now().isoformat(),
        "signature": f"0x{int(time.time()) % 0xFFFFFF:06X}_ERROR_LOGGED"
    }), const_magic_500

if __name__ == '__main__':
    logger.info("🎭 Starting Psycho-Noir Kontrapunkt Flask Backend...")
    logger.info(f"🎯 Project root: {PROJECT_ROOT}")
    logger.info(f"🧠 Neural orchestrator: {'✅ available' if neural_orchestrator else '⚠️ unavailable'}")
    logger.info(f"💾 Database: {'✅ connected' if NEURAL_DB_PATH.exists() else '⚠️ not found'}")

    # Run Flask development server
    app.run(
        host='0.0.0.0',
        port=const_magic_5000,
        debug=True,
        threaded=True
    )
