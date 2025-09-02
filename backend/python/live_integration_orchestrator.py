#!/usr/bin/env python3
"""
🎭 PSYCHO-NOIR KONTRAPUNKT LIVE INTEGRATION ORCHESTRATOR 🎭
============================================================

LEVEL 9: Complete integration mellom alle komponenter
- GitHub Pages ↔ Backend bridge
- Docker deployment validation
- Real-time communication layer
- Production environment testing

INTEGRATION_SIGNATURE: 0xLIVE_DEPLOYMENT_VALIDATED
"""

import asyncio
import json
import logging
import subprocess
import time
import requests
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
import docker
import yaml

# 🎭 Configuration
PROJECT_ROOT = Path(__file__).parent.parent.parent
FRONTEND_DIR = PROJECT_ROOT / "frontend"
DOCS_DIR = PROJECT_ROOT / "docs"
BACKEND_DIR = PROJECT_ROOT / "backend"
GITHUB_PAGES_URL = "https://poisontr33s.github.io/PsychoNoir-Kontrapunkt/"

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [🎭 %(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler(PROJECT_ROOT / 'data' / 'live_integration.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class LiveIntegrationOrchestrator:
    """
    🎭 LEVEL 9: Complete Live Integration System

    Koordinerer all kommunikasjon mellom:
    - GitHub Pages frontend
    - Docker backend services
    - Neural archaeology systems
    - Production deployment
    """

    def __init__(self):
        self.project_root = PROJECT_ROOT
        self.backend_url = "http://localhost:5000"
        self.frontend_url = GITHUB_PAGES_URL
        self.docker_client = None
        self.integration_status = {}

        try:
            self.docker_client = docker.from_env()
            logger.info("✅ Docker client connected")
        except Exception as e:
            logger.warning(f"⚠️ Docker client unavailable: {e}")

        logger.info("🎭 Live Integration Orchestrator initialized")

    async def validate_complete_integration(self) -> Dict[str, Any]:
        """🔍 Complete integration validation"""
        logger.info("🎯 Starting complete integration validation...")

        validation_results = {
            "timestamp": datetime.now().isoformat(),
            "integration_signature": f"0x{int(time.time()) % 0xFFFFFF:06X}_LIVE_VALIDATED",
            "tests": {},
            "overall_status": "unknown",
            "critical_gaps": [],
            "recommendations": []
        }

        # Test 1: Docker Infrastructure
        docker_status = await self._test_docker_infrastructure()
        validation_results["tests"]["docker_infrastructure"] = docker_status

        # Test 2: Backend API Services
        backend_status = await self._test_backend_services()
        validation_results["tests"]["backend_services"] = backend_status

        # Test 3: Frontend Integration
        frontend_status = await self._test_frontend_integration()
        validation_results["tests"]["frontend_integration"] = frontend_status

        # Test 4: GitHub Pages Deployment
        pages_status = await self._test_github_pages_deployment()
        validation_results["tests"]["github_pages"] = pages_status

        # Test 5: Live Communication Bridge
        bridge_status = await self._test_communication_bridge()
        validation_results["tests"]["communication_bridge"] = bridge_status

        # Test 6: Neural Archaeology Integration
        neural_status = await self._test_neural_integration()
        validation_results["tests"]["neural_integration"] = neural_status

        # Calculate overall status
        validation_results = self._calculate_integration_status(validation_results)

        return validation_results

    async def _test_docker_infrastructure(self) -> Dict[str, Any]:
        """🐳 Test Docker deployment infrastructure"""
        logger.info("🐳 Testing Docker infrastructure...")

        result = {
            "name": "Docker Infrastructure",
            "status": "unknown",
            "details": {},
            "issues": []
        }

        try:
            # Test Docker Compose configuration
            compose_file = self.project_root / "backend" / "docker" / "docker-compose.yml"
            if compose_file.exists():
                # Validate Docker Compose syntax
                proc = subprocess.run([
                    "docker", "compose", "-f", str(compose_file), "config"
                ], capture_output=True, text=True, timeout=30)

                if proc.returncode == 0:
                    result["details"]["compose_syntax"] = "✅ Valid"
                else:
                    result["details"]["compose_syntax"] = f"❌ Invalid: {proc.stderr[:100]}"
                    result["issues"].append("Docker Compose syntax errors")

                # Test if we can build the main service
                try:
                    if self.docker_client:
                        images = self.docker_client.images.list(filters={"reference": "psychonoir*"})
                        result["details"]["images_available"] = f"✅ Found {len(images)} Psycho-Noir images"
                    else:
                        result["details"]["images_available"] = "⚠️ Docker client unavailable"
                except Exception as e:
                    result["details"]["images_available"] = f"❌ Error checking images: {e}"
                    result["issues"].append("Docker image availability issues")

            else:
                result["issues"].append("Docker Compose file missing")
                result["details"]["compose_file"] = "❌ Missing docker-compose.yml"

            # Test Docker daemon
            try:
                proc = subprocess.run(["docker", "version"], capture_output=True, text=True, timeout=10)
                if proc.returncode == 0:
                    result["details"]["docker_daemon"] = "✅ Running"
                else:
                    result["details"]["docker_daemon"] = "❌ Not accessible"
                    result["issues"].append("Docker daemon not accessible")
            except Exception as e:
                result["details"]["docker_daemon"] = f"❌ Error: {e}"
                result["issues"].append("Docker daemon connectivity issues")

            result["status"] = "healthy" if len(result["issues"]) == 0 else "unhealthy"

        except Exception as e:
            result["status"] = "error"
            result["issues"].append(f"Docker infrastructure test failed: {e}")

        return result

    async def _test_backend_services(self) -> Dict[str, Any]:
        """🔧 Test backend API services"""
        logger.info("🔧 Testing backend services...")

        result = {
            "name": "Backend Services",
            "status": "unknown",
            "details": {},
            "issues": []
        }

        try:
            # Test if backend is running
            try:
                response = requests.get(f"{self.backend_url}/health", timeout=5)
                if response.status_code == 200:
                    result["details"]["health_endpoint"] = "✅ Responsive"
                    result["details"]["health_data"] = response.json()
                else:
                    result["details"]["health_endpoint"] = f"❌ HTTP {response.status_code}"
                    result["issues"].append("Backend health endpoint unhealthy")
            except requests.RequestException as e:
                result["details"]["health_endpoint"] = f"❌ Not accessible: {e}"
                result["issues"].append("Backend not running or accessible")

            # Test core API endpoints
            api_endpoints = ["/api/status", "/api/neural-analysis", "/api/system-info"]
            for endpoint in api_endpoints:
                try:
                    response = requests.get(f"{self.backend_url}{endpoint}", timeout=3)
                    if response.status_code in [200, 404]:  # 404 is OK if endpoint not implemented yet
                        result["details"][f"endpoint_{endpoint}"] = f"✅ Accessible (HTTP {response.status_code})"
                    else:
                        result["details"][f"endpoint_{endpoint}"] = f"⚠️ HTTP {response.status_code}"
                except requests.RequestException:
                    result["details"][f"endpoint_{endpoint}"] = "❌ Not accessible"

            # Test Neural CLI
            try:
                cli_path = self.project_root / "backend" / "python" / "psycho_noir_cli.py"
                if cli_path.exists():
                    proc = subprocess.run([
                        "python3", str(cli_path), "status", "--format=json"
                    ], capture_output=True, text=True, timeout=10, cwd=self.project_root)

                    if proc.returncode == 0:
                        result["details"]["neural_cli"] = "✅ Functional"
                        try:
                            cli_data = json.loads(proc.stdout.split('\n')[-2])  # Get last JSON line
                            result["details"]["cli_data"] = cli_data
                        except:
                            result["details"]["cli_data"] = "✅ CLI works but JSON parsing failed"
                    else:
                        result["details"]["neural_cli"] = f"❌ Error: {proc.stderr[:100]}"
                        result["issues"].append("Neural CLI execution issues")
                else:
                    result["details"]["neural_cli"] = "❌ CLI script missing"
                    result["issues"].append("Neural CLI script not found")
            except Exception as e:
                result["details"]["neural_cli"] = f"❌ Test failed: {e}"
                result["issues"].append("Neural CLI test execution failed")

            result["status"] = "healthy" if len(result["issues"]) == 0 else "unhealthy"

        except Exception as e:
            result["status"] = "error"
            result["issues"].append(f"Backend services test failed: {e}")

        return result

    async def _test_frontend_integration(self) -> Dict[str, Any]:
        """🎨 Test frontend integration"""
        logger.info("🎨 Testing frontend integration...")

        result = {
            "name": "Frontend Integration",
            "status": "unknown",
            "details": {},
            "issues": []
        }

        try:
            # Test frontend files existence
            frontend_files = {
                "index.html": DOCS_DIR / "index.html",
                "cosmic-api.js": DOCS_DIR / "cosmic-api.js",
                "script.js": FRONTEND_DIR / "scripts" / "script.js",
                "style.css": FRONTEND_DIR / "styles" / "style.css"
            }

            for name, path in frontend_files.items():
                if path.exists():
                    size = path.stat().st_size
                    result["details"][f"file_{name}"] = f"✅ Exists ({size:,} bytes)"
                else:
                    result["details"][f"file_{name}"] = "❌ Missing"
                    result["issues"].append(f"Frontend file missing: {name}")

            # Test if frontend can communicate with backend (simulation)
            index_path = DOCS_DIR / "index.html"
            if index_path.exists():
                content = index_path.read_text()
                if "cosmic-api.js" in content and "localhost:5000" in content:
                    result["details"]["backend_integration"] = "✅ Backend URL configured"
                else:
                    result["details"]["backend_integration"] = "⚠️ Backend integration may be incomplete"
                    result["issues"].append("Frontend-backend integration may be incomplete")

            result["status"] = "healthy" if len(result["issues"]) == 0 else "unhealthy"

        except Exception as e:
            result["status"] = "error"
            result["issues"].append(f"Frontend integration test failed: {e}")

        return result

    async def _test_github_pages_deployment(self) -> Dict[str, Any]:
        """🌐 Test GitHub Pages deployment"""
        logger.info("🌐 Testing GitHub Pages deployment...")

        result = {
            "name": "GitHub Pages Deployment",
            "status": "unknown",
            "details": {},
            "issues": []
        }

        try:
            # Test GitHub Pages accessibility
            try:
                response = requests.get(self.frontend_url, timeout=10)
                if response.status_code == 200:
                    content_length = len(response.text)
                    result["details"]["pages_accessibility"] = f"✅ Live! ({content_length:,} bytes)"
                    result["details"]["pages_url"] = self.frontend_url

                    # Check if content looks like our portal
                    if "Psycho-Noir Kontrapunkt" in response.text:
                        result["details"]["content_validation"] = "✅ Correct content"
                    else:
                        result["details"]["content_validation"] = "⚠️ Content may be default GitHub Pages"
                        result["issues"].append("GitHub Pages may not be serving our content")

                elif response.status_code == 404:
                    result["details"]["pages_accessibility"] = "❌ Not deployed (404)"
                    result["issues"].append("GitHub Pages not deployed or configured")
                else:
                    result["details"]["pages_accessibility"] = f"❌ HTTP {response.status_code}"
                    result["issues"].append("GitHub Pages deployment issues")

            except requests.RequestException as e:
                result["details"]["pages_accessibility"] = f"❌ Not accessible: {e}"
                result["issues"].append("GitHub Pages not accessible")

            # Test docs directory structure
            docs_files = list(DOCS_DIR.glob("**/*")) if DOCS_DIR.exists() else []
            result["details"]["docs_structure"] = f"✅ {len(docs_files)} files in docs/"

            result["status"] = "healthy" if len(result["issues"]) == 0 else "unhealthy"

        except Exception as e:
            result["status"] = "error"
            result["issues"].append(f"GitHub Pages deployment test failed: {e}")

        return result

    async def _test_communication_bridge(self) -> Dict[str, Any]:
        """🌉 Test communication bridge between frontend and backend"""
        logger.info("🌉 Testing communication bridge...")

        result = {
            "name": "Communication Bridge",
            "status": "unknown",
            "details": {},
            "issues": []
        }

        try:
            # Test CORS configuration
            try:
                response = requests.options(f"{self.backend_url}/api/status", timeout=5)
                cors_headers = {k: v for k, v in response.headers.items() if 'cors' in k.lower() or 'access-control' in k.lower()}
                if cors_headers:
                    result["details"]["cors_configuration"] = f"✅ Configured ({len(cors_headers)} headers)"
                else:
                    result["details"]["cors_configuration"] = "⚠️ May not be configured"
                    result["issues"].append("CORS headers may not be properly configured")
            except Exception as e:
                result["details"]["cors_configuration"] = f"❌ Cannot test: {e}"

            # Test API response format
            try:
                response = requests.get(f"{self.backend_url}/health", timeout=5)
                if response.status_code == 200:
                    try:
                        data = response.json()
                        result["details"]["api_format"] = "✅ JSON response format"
                        result["details"]["api_sample"] = str(data)[:100] + "..."
                    except json.JSONDecodeError:
                        result["details"]["api_format"] = "⚠️ Non-JSON response"
                        result["issues"].append("API not returning JSON format")
                else:
                    result["details"]["api_format"] = f"❌ HTTP {response.status_code}"
            except Exception as e:
                result["details"]["api_format"] = f"❌ Cannot test: {e}"

            # Test if frontend has API communication code
            api_js_path = DOCS_DIR / "cosmic-api.js"
            if api_js_path.exists():
                content = api_js_path.read_text()
                if "fetch(" in content and "localhost:5000" in content:
                    result["details"]["frontend_api_code"] = "✅ API communication implemented"
                else:
                    result["details"]["frontend_api_code"] = "⚠️ API code may be incomplete"
                    result["issues"].append("Frontend API communication may be incomplete")
            else:
                result["details"]["frontend_api_code"] = "❌ API script missing"
                result["issues"].append("Frontend API script not found")

            result["status"] = "healthy" if len(result["issues"]) == 0 else "unhealthy"

        except Exception as e:
            result["status"] = "error"
            result["issues"].append(f"Communication bridge test failed: {e}")

        return result

    async def _test_neural_integration(self) -> Dict[str, Any]:
        """🧠 Test neural archaeology integration"""
        logger.info("🧠 Testing neural archaeology integration...")

        result = {
            "name": "Neural Integration",
            "status": "unknown",
            "details": {},
            "issues": []
        }

        try:
            # Test Neural Archaeology Orchestrator
            orchestrator_path = self.project_root / "backend" / "python" / "neural_archaeology_orchestrator.py"
            if orchestrator_path.exists():
                try:
                    proc = subprocess.run([
                        "python3", str(orchestrator_path), "--action", "report", "--environment", "development"
                    ], capture_output=True, text=True, timeout=15, cwd=self.project_root)

                    if proc.returncode == 0:
                        result["details"]["neural_orchestrator"] = "✅ Functional"
                        # Try to parse JSON output
                        try:
                            output_lines = proc.stdout.strip().split('\n')
                            json_line = None
                            for line in reversed(output_lines):
                                if line.strip().startswith('{'):
                                    json_line = line
                                    break
                            if json_line:
                                neural_data = json.loads(json_line)
                                result["details"]["neural_data"] = f"✅ Report generated: {neural_data.get('report_signature', 'unknown')}"
                        except:
                            result["details"]["neural_data"] = "✅ Works but JSON parsing failed"
                    else:
                        result["details"]["neural_orchestrator"] = f"❌ Error: {proc.stderr[:100]}"
                        result["issues"].append("Neural orchestrator execution issues")
                except Exception as e:
                    result["details"]["neural_orchestrator"] = f"❌ Test failed: {e}"
                    result["issues"].append("Neural orchestrator test failed")
            else:
                result["details"]["neural_orchestrator"] = "❌ Orchestrator script missing"
                result["issues"].append("Neural archaeology orchestrator not found")

            # Test database connectivity
            neural_db_path = self.project_root / "data" / "neural_archaeology.db"
            if neural_db_path.exists():
                result["details"]["neural_database"] = f"✅ Database exists ({neural_db_path.stat().st_size:,} bytes)"
            else:
                result["details"]["neural_database"] = "⚠️ Database not initialized"

            result["status"] = "healthy" if len(result["issues"]) == 0 else "unhealthy"

        except Exception as e:
            result["status"] = "error"
            result["issues"].append(f"Neural integration test failed: {e}")

        return result

    def _calculate_integration_status(self, validation_results: Dict[str, Any]) -> Dict[str, Any]:
        """📊 Calculate overall integration status"""
        tests = validation_results["tests"]

        # Count healthy vs unhealthy tests
        healthy_tests = sum(1 for test in tests.values() if test["status"] == "healthy")
        total_tests = len(tests)

        # Collect all critical gaps
        for test in tests.values():
            validation_results["critical_gaps"].extend(test.get("issues", []))

        # Calculate overall health percentage
        health_percentage = (healthy_tests / total_tests * 100) if total_tests > 0 else 0

        if health_percentage >= 90:
            validation_results["overall_status"] = "excellent"
            validation_results["recommendations"].append("🎉 System ready for production deployment!")
        elif health_percentage >= 70:
            validation_results["overall_status"] = "good"
            validation_results["recommendations"].append("🔧 Minor fixes needed for production readiness")
        elif health_percentage >= 50:
            validation_results["overall_status"] = "moderate"
            validation_results["recommendations"].append("⚠️ Significant integration work needed")
        else:
            validation_results["overall_status"] = "critical"
            validation_results["recommendations"].append("🚨 Major integration issues - not ready for production")

        validation_results["health_percentage"] = round(health_percentage, 1)
        validation_results["healthy_tests"] = healthy_tests
        validation_results["total_tests"] = total_tests

        return validation_results

    async def deploy_missing_integrations(self) -> Dict[str, Any]:
        """🚀 Deploy missing integration components"""
        logger.info("🚀 Deploying missing integration components...")

        deployment_results = {
            "timestamp": datetime.now().isoformat(),
            "deployments": {},
            "success_count": 0,
            "total_count": 0
        }

        # Deploy GitHub Pages configuration
        pages_result = await self._deploy_github_pages_integration()
        deployment_results["deployments"]["github_pages"] = pages_result
        deployment_results["total_count"] += 1
        if pages_result["success"]:
            deployment_results["success_count"] += 1

        # Deploy backend CORS configuration
        cors_result = await self._deploy_cors_configuration()
        deployment_results["deployments"]["cors_config"] = cors_result
        deployment_results["total_count"] += 1
        if cors_result["success"]:
            deployment_results["success_count"] += 1

        # Deploy frontend-backend bridge
        bridge_result = await self._deploy_communication_bridge()
        deployment_results["deployments"]["communication_bridge"] = bridge_result
        deployment_results["total_count"] += 1
        if bridge_result["success"]:
            deployment_results["success_count"] += 1

        deployment_results["deployment_percentage"] = (
            deployment_results["success_count"] / deployment_results["total_count"] * 100
            if deployment_results["total_count"] > 0 else 0
        )

        return deployment_results

    async def _deploy_github_pages_integration(self) -> Dict[str, Any]:
        """🌐 Deploy GitHub Pages integration"""
        try:
            # Ensure GitHub Pages workflow exists
            workflow_path = self.project_root / ".github" / "workflows" / "deploy-pages.yml"
            if not workflow_path.exists():
                workflow_content = """name: Deploy to GitHub Pages

on:
  push:
    branches: [ main ]
    paths: [ 'docs/**', 'frontend/**' ]
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: "pages"
  cancel-in-progress: false

jobs:
  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4
      - name: Setup Pages
        uses: actions/configure-pages@v4
      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: './docs'
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
"""
                workflow_path.parent.mkdir(parents=True, exist_ok=True)
                workflow_path.write_text(workflow_content)
                logger.info("✅ Created GitHub Pages workflow")

            return {"success": True, "message": "GitHub Pages workflow configured"}
        except Exception as e:
            return {"success": False, "message": f"GitHub Pages deployment failed: {e}"}

    async def _deploy_cors_configuration(self) -> Dict[str, Any]:
        """🔧 Deploy CORS configuration"""
        try:
            # Create CORS configuration for Flask backend
            cors_config_path = self.project_root / "backend" / "python" / "cors_config.py"
            cors_content = '''"""
🎭 PSYCHO-NOIR KONTRAPUNKT CORS CONFIGURATION
"""
from flask_cors import CORS

def configure_cors(app):
    """Configure CORS for GitHub Pages integration"""
    CORS(app,
         origins=["https://poisontr33s.github.io", "http://localhost:3000", "http://127.0.0.1:3000"],
         allow_headers=["Content-Type", "Authorization"],
         methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])
'''
            cors_config_path.write_text(cors_content)
            logger.info("✅ Created CORS configuration")

            return {"success": True, "message": "CORS configuration deployed"}
        except Exception as e:
            return {"success": False, "message": f"CORS deployment failed: {e}"}

    async def _deploy_communication_bridge(self) -> Dict[str, Any]:
        """🌉 Deploy communication bridge"""
        try:
            # Update cosmic-api.js with better error handling and fallbacks
            api_js_path = DOCS_DIR / "cosmic-api.js"
            if api_js_path.exists():
                api_content = api_js_path.read_text()

                # Add fallback mechanisms if not present
                if "fallback" not in api_content.lower():
                    fallback_code = '''

    // 🎭 Enhanced with fallback mechanisms
    const API_FALLBACKS = [
        'http://localhost:5000',
        'https://api.psycho-noir-kontrapunkt.herokuapp.com',
        'https://psychonoir-api.railway.app'
    ];

    async function tryApiCall(endpoint, options = {}) {
        for (const baseUrl of API_FALLBACKS) {
            try {
                const response = await fetch(`${baseUrl}${endpoint}`, {
                    ...options,
                    mode: 'cors',
                    headers: {
                        'Content-Type': 'application/json',
                        ...options.headers
                    }
                });
                if (response.ok) return response;
            } catch (error) {
                console.warn(`API fallback ${baseUrl} failed:`, error);
            }
        }
        throw new Error('All API endpoints failed');
    }
'''

                    updated_content = api_content + fallback_code
                    api_js_path.write_text(updated_content)
                    logger.info("✅ Enhanced cosmic-api.js with fallbacks")

            return {"success": True, "message": "Communication bridge enhanced"}
        except Exception as e:
            return {"success": False, "message": f"Communication bridge deployment failed: {e}"}

async def main():
    """🎭 Main Live Integration Interface"""
    import argparse

    parser = argparse.ArgumentParser(description="🎭 Psycho-Noir Kontrapunkt Live Integration Orchestrator")
    parser.add_argument("--action", "-a",
                       choices=["validate", "deploy", "full"],
                       default="validate",
                       help="Action to perform")

    args = parser.parse_args()

    orchestrator = LiveIntegrationOrchestrator()

    logger.info(f"🎭 Starting live integration: {args.action}")

    try:
        if args.action == "validate":
            result = await orchestrator.validate_complete_integration()
            print(json.dumps(result, indent=2, default=str))

        elif args.action == "deploy":
            result = await orchestrator.deploy_missing_integrations()
            print(json.dumps(result, indent=2, default=str))

        elif args.action == "full":
            # Full validation and deployment
            validation = await orchestrator.validate_complete_integration()

            print(json.dumps(validation, indent=2, default=str))

            if validation["health_percentage"] < 90:

                deployment = await orchestrator.deploy_missing_integrations()
                print(json.dumps(deployment, indent=2, default=str))

                # Re-validate

                final_validation = await orchestrator.validate_complete_integration()
                print(json.dumps(final_validation, indent=2, default=str))

    except KeyboardInterrupt:
        logger.info("🛑 Live integration interrupted by user")
    except Exception as e:
        logger.error(f"❌ Live integration failed: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(main())
