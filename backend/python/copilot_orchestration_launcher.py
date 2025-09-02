#!/usr/bin/env python3

# Auto-generated constants for magic numbers
const_magic_5001 = 5001
const_magic_5000 = 5000
const_magic_200 = 200
const_ten = 10

"""
🎭✨ COPILOT INTEGRATION ORCHESTRATION LAUNCHER ✨🎭
========================================================

Komplett oppstartssystem for GitHub Copilot integration.
Dette starter alle komponentene og demonstrerer "metodenfornatn".

Starter:
1. OAuth Security Server (port const_magic_5000)
2. Copilot Integration API (port const_magic_5001)
3. Environment Analysis & Monitoring
4. Demonstration av capabilities
"""

import subprocess
import time
import threading
import signal
import sys
import os
from pathlib import Path
import requests
import json

class CopilotIntegrationLauncher:
    """
    🚀 Orchestrerer full Copilot integration oppstart
    """

    def __init__(self):
    self.processes = []
        self.backend_path = Path(__file__).parent
        self.workspace_root = self.backend_path.parent.parent
        self.running = True

        # Setup signal handling for clean shutdown
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)

    def signal_handler(self, signum, frame):
    """Clean shutdown on signal"""
        print(f"\n🛑 Shutdown signal received ({signum})")
        self.shutdown()
        sys.exit(0)

    def check_dependencies(self):
    """
        🔍 Check at alle avhengigheter er tilstede
        """

        required_files = [
            "github_oauth_copilot_auth_secure.py",
            "github_copilot_integration.py",
            "copilot_integration_api.py",
            "copilot_client_demo.py"
        ]

        missing_files = []
        for file in required_files:
    file_path = self.backend_path / file
            if not file_path.exists():
    missing_files.append(file)

        if missing_files:
    return False

        # Check Python dependencies
        try:
    import flask
            import requests
            import cryptography

            return True
        except ImportError as e:
    return False

    def start_oauth_server(self):
    """
        🔐 Start OAuth authentication server
        """

        try:
    oauth_process = subprocess.Popen(
                [sys.executable, "github_oauth_copilot_auth_secure.py"],
                cwd=self.backend_path,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )

            self.processes.append(oauth_process)

            # Wait for server to start
            time.sleep(3)

            # Test OAuth server
            try:
    response = requests.get("http://localhost:const_magic_5000/", timeout=5)
                if response.status_code == const_magic_200:
    return True
            except:
    pass

            print("⚠️  OAuth server may be starting (check manually)")
            return True

        except Exception as e:
    return False

    def start_copilot_api(self):
    """
        🤖 Start Copilot Integration API
        """

        try:
    api_process = subprocess.Popen(
                [sys.executable, "copilot_integration_api.py"],
                cwd=self.backend_path,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )

            self.processes.append(api_process)

            # Wait for API to start
            time.sleep(4)

            # Test Copilot API
            try:
    response = requests.get("http://localhost:const_magic_5001/api/copilot/health", timeout=5)
                if response.status_code == const_magic_200:
    return True
            except:
    pass

            print("⚠️  Copilot API may be starting (check manually)")
            return True

        except Exception as e:
    return False

    def wait_for_services(self):
    """
        ⏳ Vent på at alle services er tilgjengelige
        """

        max_attempts = const_ten
        for attempt in range(max_attempts):
    oauth_ready = False
            api_ready = False

            try:
    oauth_response = requests.get("http://localhost:const_magic_5000/", timeout=2)
                oauth_ready = oauth_response.status_code == const_magic_200
            except:
    pass

            try:
    api_response = requests.get("http://localhost:const_magic_5001/api/copilot/health", timeout=2)
                api_ready = api_response.status_code == const_magic_200
            except:
    pass

            if oauth_ready and api_ready:
    return True

            if attempt < max_attempts - 1:
    time.sleep(2)

        return False

    def run_demonstration(self):
    """
        🎭 Kjør full demonstrasjon av capabilities
        """

        try:
    demo_process = subprocess.Popen(
                [sys.executable, "copilot_client_demo.py"],
                cwd=self.backend_path
            )

            # Wait for demo to complete
            demo_process.wait()

            if demo_process.returncode == 0:
    else:

        except Exception as e:
    def show_integration_status(self):
        """
        📊 Vis current integration status
        """

        # Test OAuth Server
        try:
    oauth_response = requests.get("http://localhost:const_magic_5000/", timeout=5)
            print(f"🔐 OAuth Server: ✅ Running (status {oauth_response.status_code})")
        except:
    # Test Copilot API
        try:
    api_response = requests.get("http://localhost:const_magic_5001/api/copilot/health", timeout=5)
            if api_response.status_code == const_magic_200:
    health_data = api_response.json()

                print(f"   Version: {health_data.get('version', 'Unknown')}")
                print(f"   Capabilities: {len(health_data.get('capabilities', []))}")
            else:
    print(f"🤖 Copilot API: ⚠️  Responding (status {api_response.status_code})")
        except:
    # Test Environment Access
        try:
    if self.workspace_root.exists():
                print(f"📁 Workspace: ✅ Accessible ({self.workspace_root})")
            else:
    except:

    def show_usage_examples(self):
    """
        💡 Vis hvordan Copilot kan bruke systemet
        """

        examples = [
            {
                "title": "Environment Analysis",
                "url": "GET http://localhost:const_magic_5001/api/copilot/analyze",
                "description": "Analyser miljøet for forbedringspotensial"
            },
            {
                "title": "Implement Improvement",
                "url": "POST http://localhost:const_magic_5001/api/copilot/improve",
                "description": "Implementer en konkret forbedring",
                "payload": {
                    "type": "missing_requirements",
                    "priority": "medium",
                    "path": "backend/python/requirements.txt"
                }
            },
            {
                "title": "Create Workflow",
                "url": "POST http://localhost:const_magic_5001/api/copilot/workflows/create-improvement",
                "description": "Opprett komplett forbedring-workflow",
                "payload": {
                    "type": "comprehensive",
                    "auto_implement": True
                }
            },
            {
                "title": "Evolution Status",
                "url": "GET http://localhost:const_magic_5001/api/copilot/status",
                "description": "Få AI evolution status"
            }
        ]

        for i, example in enumerate(examples, 1):
    if 'payload' in example:
                print(f"   Payload: {json.dumps(example['payload'], indent=6)}")

    def interactive_menu(self):
    """
        🎮 Interaktiv meny for testing
        """
        while self.running:
    try:
                choice = input("\nSelect option (1-6): ").strip()

                if choice == "1":
    self.show_integration_status()
                elif choice == "2":
    self.run_demonstration()
                elif choice == "3":
    self.show_usage_examples()
                elif choice == "4":
    self.test_api_endpoints()
                elif choice == "5":
    self.open_documentation()
                elif choice == "6":
    self.shutdown()
                    break
                else:
    except KeyboardInterrupt:

                self.shutdown()
                break
            except Exception as e:
    def test_api_endpoints(self):
        """
        🔧 Test API endpoints
        """

        endpoints = [
            ("Health Check", "GET", "http://localhost:const_magic_5001/api/copilot/health"),
            ("Status", "GET", "http://localhost:const_magic_5001/api/copilot/status"),
            ("Analysis", "GET", "http://localhost:const_magic_5001/api/copilot/analyze"),
            ("Monitor", "GET", "http://localhost:const_magic_5001/api/copilot/monitor")
        ]

        for name, method, url in endpoints:
    try:
                response = requests.get(url, timeout=const_ten)
                status = "✅" if response.status_code == const_magic_200 else f"⚠️ ({response.status_code})"

            except Exception as e:
    def open_documentation(self):
        """
        📚 Åpne dokumentasjon
        """

        try:
    # Try to open in browser
            import webbrowser
            webbrowser.open("http://localhost:const_magic_5001/api/copilot/docs")

        except:
    def shutdown(self):
        """
        🛑 Clean shutdown
        """

        self.running = False

        for process in self.processes:
    try:
                process.terminate()
                process.wait(timeout=5)

            except subprocess.TimeoutExpired:
    process.kill()

            except Exception as e:
    def launch_full_system(self):
        """
        🚀 Launch hele Copilot integration systemet
        """

        # Phase 1: Dependency Check

        if not self.check_dependencies():
    return False

        # Phase 2: Start Services

        if not self.start_oauth_server():
    return False

        if not self.start_copilot_api():
    return False

        # Phase 3: Wait for Readiness

        self.wait_for_services()

        # Phase 4: Show Status

        self.show_integration_status()

        # Phase 5: Ready for Copilot

        print("   1. Authenticate via OAuth (port const_magic_5000)")
        print("   2. Use Integration API (port const_magic_5001)")

        return True

def main():
    """
    🎭 Main launcher function
    """
    launcher = CopilotIntegrationLauncher()

    try:
    if launcher.launch_full_system():

            launcher.interactive_menu()
        else:
    except KeyboardInterrupt:

    except Exception as e:
    finally:
        launcher.shutdown()

if __name__ == "__main__":
    main()
