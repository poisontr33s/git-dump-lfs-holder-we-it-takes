#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Auto-generated constants for magic numbers
const_magic_5000 = 5000
const_magic_500 = 500
const_magic_404 = 404
const_magic_400 = 400
const_hundred = 100

"""
🌐 PSYCHO-NOIR KONTRAPUNKT PORTAL INTEGRATION 🌐
================================================

const_hundred% robust integration mellom backend systems og GitHub Pages portal.
Proven patterns, comprehensive error handling, graceful degradation.

INTEGRATION_SIGNATURE: 0xPORTAL_BACKEND_BRIDGE_ACTIVE
RELIABILITY_LEVEL: ENTERPRISE_GRADE_STABILITY
"""

import logging
import json
import os
from datetime import datetime
from pathlib import Path

try:
    from flask import Flask, jsonify, request, send_from_directory
    from flask_cors import CORS
    FLASK_AVAILABLE = True
except ImportError:

    FLASK_AVAILABLE = False

# Import core systems with fallback
try:
    from psycho_noir_core import create_psycho_noir_system
    CORE_AVAILABLE = True
except ImportError:

    CORE_AVAILABLE = False

class RobustPortalIntegration:
    """Robust portal integration with comprehensive error handling"""

    def __init__(self, frontend_path="../../frontend"):
        self.frontend_path = Path(frontend_path).resolve()
        self.system = None
        self.mock_mode = not CORE_AVAILABLE
        self.app = None

        # Configure logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def initialize_system(self):
        """Initialize backend system with robust error handling"""
        try:
            if CORE_AVAILABLE:
                self.system = create_psycho_noir_system("data/psycho_noir_portal.db")
                self.logger.info("✅ Core system initialized for portal")
            else:
                self.system = MockPortalSystem()
                self.logger.warning("⚠️ Portal running in mock mode")
                self.mock_mode = True
        except Exception as e:
            self.logger.error(f"❌ System initialization failed: {e}")
            self.system = MockPortalSystem()
            self.mock_mode = True

    def create_flask_app(self):
        """Create Flask app with robust configuration"""
        if not FLASK_AVAILABLE:
            raise RuntimeError("Flask not available for portal integration")

        app = Flask(__name__)
        CORS(app)  # Enable CORS for GitHub Pages

        # Production-grade configuration
        app.config.update(
            SECRET_KEY=os.environ.get('SECRET_KEY', 'psycho-noir-kontrapunkt-dev'),
            JSON_SORT_KEYS=False,
            JSONIFY_PRETTYPRINT_REGULAR=True
        )

        self.app = app
        return app

    def get_portal_data(self):
        """Get comprehensive data for portal with fallback"""
        try:
            if self.system:
                status = self.system.get_system_status()

                # Enhance with portal-specific data
                portal_data = {
                    "system_status": status,
                    "portal_meta": {
                        "timestamp": datetime.now().isoformat(),
                        "version": "1.0.0",
                        "mock_mode": self.mock_mode,
                        "integration_status": "active"
                    },
                    "domains": {
                        "skyskraper": self._get_domain_data("skyskraper"),
                        "rustbelt": self._get_domain_data("rustbelt")
                    },
                    "recent_interactions": self._get_recent_interactions(),
                    "anomaly_alerts": self._get_anomaly_alerts()
                }

                return portal_data

            else:
                # Fallback data structure
                return self._get_fallback_data()

        except Exception as e:
            self.logger.error(f"❌ Portal data retrieval failed: {e}")
            return self._get_fallback_data()

    def _get_domain_data(self, domain_name):
        """Get domain-specific data with error handling"""
        try:
            if self.system and hasattr(self.system, domain_name):
                domain = getattr(self.system, domain_name)
                if domain and hasattr(domain, 'get_domain_status'):
                    return domain.get_domain_status()

            # Fallback domain data
            return {
                "domain_name": domain_name,
                "status": "mock" if self.mock_mode else "unavailable",
                "last_update": datetime.now().isoformat()
            }

        except Exception as e:
            self.logger.error(f"❌ Domain {domain_name} data failed: {e}")
            return {"domain_name": domain_name, "status": "error"}

    def _get_recent_interactions(self):
        """Get recent interactions with fallback"""
        try:
            if self.mock_mode:
                return [
                    {
                        "id": "MOCK_001",
                        "source": "skyskraper",
                        "target": "rustbelt",
                        "type": "data_exchange",
                        "timestamp": datetime.now().isoformat(),
                        "status": "mock"
                    }
                ]
            else:
                # Real interaction retrieval would go here
                return []

        except Exception as e:
            self.logger.error(f"❌ Recent interactions failed: {e}")
            return []

    def _get_anomaly_alerts(self):
        """Get anomaly alerts with fallback"""
        try:
            if self.mock_mode:
                return [
                    {
                        "id": "ALERT_001",
                        "type": "interference_pattern",
                        "severity": "medium",
                        "domain": "cross_domain",
                        "timestamp": datetime.now().isoformat(),
                        "message": "Mock anomaly for portal demonstration"
                    }
                ]
            else:
                # Real anomaly detection would go here
                return []

        except Exception as e:
            self.logger.error(f"❌ Anomaly alerts failed: {e}")
            return []

    def _get_fallback_data(self):
        """Fallback data structure for maximum reliability"""
        return {
            "system_status": {
                "status": "fallback_mode",
                "timestamp": datetime.now().isoformat()
            },
            "portal_meta": {
                "timestamp": datetime.now().isoformat(),
                "version": "1.0.0",
                "mock_mode": True,
                "integration_status": "fallback"
            },
            "domains": {
                "skyskraper": {"status": "fallback"},
                "rustbelt": {"status": "fallback"}
            },
            "recent_interactions": [],
            "anomaly_alerts": []
        }

    def create_portal_endpoints(self):
        """Create all portal endpoints with robust error handling"""
        if not self.app:
            raise RuntimeError("Flask app not initialized")

        app = self.app

        @app.route('/api/portal/data')
        def get_portal_data_endpoint():
            """Get comprehensive portal data"""
            try:
                data = self.get_portal_data()
                return jsonify({
                    "success": True,
                    "data": data,
                    "timestamp": datetime.now().isoformat()
                })
            except Exception as e:
                self.logger.error(f"❌ Portal data endpoint failed: {e}")
                return jsonify({
                    "success": False,
                    "error": str(e),
                    "fallback_data": self._get_fallback_data(),
                    "timestamp": datetime.now().isoformat()
                }), const_magic_500

        @app.route('/api/portal/interaction', methods=['POST'])
        def create_interaction_endpoint():
            """Create new interaction via portal"""
            try:
                data = request.get_json()

                if not data:
                    return jsonify({
                        "success": False,
                        "error": "No JSON data provided"
                    }), const_magic_400

                # Validate required fields
                required_fields = ['source', 'target', 'type']
                for field in required_fields:
                    if field not in data:
                        return jsonify({
                            "success": False,
                            "error": f"Missing required field: {field}"
                        }), const_magic_400

                # Execute interaction
                result = self.system.cross_domain_interaction(
                    source_domain=data['source'],
                    target_domain=data['target'],
                    interaction_type=data['type'],
                    data=data.get('interaction_data', {})
                )

                return jsonify({
                    "success": True,
                    "result": result,
                    "timestamp": datetime.now().isoformat()
                })

            except Exception as e:
                self.logger.error(f"❌ Interaction endpoint failed: {e}")
                return jsonify({
                    "success": False,
                    "error": str(e),
                    "timestamp": datetime.now().isoformat()
                }), const_magic_500

        @app.route('/api/portal/status')
        def get_portal_status():
            """Get portal integration status"""
            try:
                return jsonify({
                    "success": True,
                    "portal_status": {
                        "backend_available": CORE_AVAILABLE,
                        "flask_available": FLASK_AVAILABLE,
                        "mock_mode": self.mock_mode,
                        "frontend_path": str(self.frontend_path),
                        "integration_version": "1.0.0"
                    },
                    "timestamp": datetime.now().isoformat()
                })
            except Exception as e:
                return jsonify({
                    "success": False,
                    "error": str(e),
                    "timestamp": datetime.now().isoformat()
                }), const_magic_500

        # Static file serving for development
        @app.route('/')
        def serve_index():
            """Serve portal index page"""
            try:
                if self.frontend_path.exists():
                    return send_from_directory(str(self.frontend_path), 'index.html')
                else:
                    return jsonify({
                        "error": "Frontend not found",
                        "path": str(self.frontend_path),
                        "help": "Portal integration requires frontend files"
                    }), const_magic_404
            except Exception as e:
                return jsonify({"error": str(e)}), const_magic_500

        @app.route('/<path:filename>')
        def serve_static(filename):
            """Serve static files"""
            try:
                if self.frontend_path.exists():
                    return send_from_directory(str(self.frontend_path), filename)
                else:
                    return jsonify({"error": "File not found"}), const_magic_404
            except Exception as e:
                return jsonify({"error": str(e)}), const_magic_500

class MockPortalSystem:
    """Mock system for portal when core is unavailable"""

    def get_system_status(self):
        return {
            "status": "mock_portal_mode",
            "active_domains": ["skyskraper", "rustbelt"],
            "mock_timestamp": datetime.now().isoformat(),
            "portal_ready": True
        }

    def cross_domain_interaction(self, source_domain, target_domain, interaction_type, data):
        return {
            "success": True,
            "mock": True,
            "interaction_id": f"PORTAL_MOCK_{datetime.now().strftime('%H%M%S')}",
            "source": source_domain,
            "target": target_domain,
            "type": interaction_type
        }

def create_portal_integration_app(frontend_path="../../frontend"):
    """Factory function to create portal integration app"""
    try:
        integration = RobustPortalIntegration(frontend_path)
        integration.initialize_system()

        if FLASK_AVAILABLE:
            app = integration.create_flask_app()
            integration.create_portal_endpoints()

            # Add error handlers
            @app.errorhandler(const_magic_404)
            def not_found(error):
                return jsonify({
                    "error": "Endpoint not found",
                    "available_endpoints": [
                        "/api/portal/data",
                        "/api/portal/interaction",
                        "/api/portal/status"
                    ]
                }), const_magic_404

            @app.errorhandler(const_magic_500)
            def internal_error(error):
                return jsonify({
                    "error": "Internal server error",
                    "help": "Check logs for details"
                }), const_magic_500

            return app
        else:
            raise RuntimeError("Flask not available for portal integration")

    except Exception as e:

        raise

if __name__ == "__main__":
    # Development server
    try:
        app = create_portal_integration_app()

        app.run(host='0.0.0.0', port=const_magic_5000, debug=True)
    except Exception as e:
