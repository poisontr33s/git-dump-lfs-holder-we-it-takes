#!/usr/bin/env python3
"""
🎭✨ COPILOT INTEGRATION ORCHESTRATION LAUNCHER ✨🎭
========================================================

Komplett oppstartssystem for GitHub Copilot integration.
Dette starter alle komponentene og demonstrerer "metodenfornatn".

Starter:
1. OAuth Security Server (port 5000)
2. Copilot Integration API (port 5001) 
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
        print("🔍 Checking dependencies...")
        
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
            print(f"❌ Missing required files: {missing_files}")
            return False
        
        # Check Python dependencies
        try:
            import flask
            import requests
            import cryptography
            print("✅ All dependencies available")
            return True
        except ImportError as e:
            print(f"❌ Missing Python package: {e}")
            return False
    
    def start_oauth_server(self):
        """
        🔐 Start OAuth authentication server
        """
        print("🔐 Starting OAuth server...")
        
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
                response = requests.get("http://localhost:5000/", timeout=5)
                if response.status_code == 200:
                    print("✅ OAuth server started successfully")
                    return True
            except:
                pass
            
            print("⚠️  OAuth server may be starting (check manually)")
            return True
            
        except Exception as e:
            print(f"❌ Failed to start OAuth server: {e}")
            return False
    
    def start_copilot_api(self):
        """
        🤖 Start Copilot Integration API
        """
        print("🤖 Starting Copilot Integration API...")
        
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
                response = requests.get("http://localhost:5001/api/copilot/health", timeout=5)
                if response.status_code == 200:
                    print("✅ Copilot Integration API started successfully")
                    return True
            except:
                pass
            
            print("⚠️  Copilot API may be starting (check manually)")
            return True
            
        except Exception as e:
            print(f"❌ Failed to start Copilot API: {e}")
            return False
    
    def wait_for_services(self):
        """
        ⏳ Vent på at alle services er tilgjengelige
        """
        print("⏳ Waiting for all services to be ready...")
        
        max_attempts = 10
        for attempt in range(max_attempts):
            oauth_ready = False
            api_ready = False
            
            try:
                oauth_response = requests.get("http://localhost:5000/", timeout=2)
                oauth_ready = oauth_response.status_code == 200
            except:
                pass
            
            try:
                api_response = requests.get("http://localhost:5001/api/copilot/health", timeout=2)
                api_ready = api_response.status_code == 200
            except:
                pass
            
            if oauth_ready and api_ready:
                print("✅ All services ready!")
                return True
            
            if attempt < max_attempts - 1:
                print(f"   Attempt {attempt + 1}/{max_attempts} - OAuth: {'✅' if oauth_ready else '❌'}, API: {'✅' if api_ready else '❌'}")
                time.sleep(2)
        
        print("⚠️  Services may not be fully ready, but continuing...")
        return False
    
    def run_demonstration(self):
        """
        🎭 Kjør full demonstrasjon av capabilities
        """
        print("\n🎭 RUNNING COPILOT INTEGRATION DEMONSTRATION")
        print("=" * 60)
        
        try:
            demo_process = subprocess.Popen(
                [sys.executable, "copilot_client_demo.py"],
                cwd=self.backend_path
            )
            
            # Wait for demo to complete
            demo_process.wait()
            
            if demo_process.returncode == 0:
                print("✅ Demonstration completed successfully")
            else:
                print("⚠️  Demonstration completed with warnings")
            
        except Exception as e:
            print(f"❌ Demonstration failed: {e}")
    
    def show_integration_status(self):
        """
        📊 Vis current integration status
        """
        print("\n📊 COPILOT INTEGRATION STATUS")
        print("-" * 40)
        
        # Test OAuth Server
        try:
            oauth_response = requests.get("http://localhost:5000/", timeout=5)
            print(f"🔐 OAuth Server: ✅ Running (status {oauth_response.status_code})")
        except:
            print("🔐 OAuth Server: ❌ Not responding")
        
        # Test Copilot API
        try:
            api_response = requests.get("http://localhost:5001/api/copilot/health", timeout=5)
            if api_response.status_code == 200:
                health_data = api_response.json()
                print(f"🤖 Copilot API: ✅ Healthy")
                print(f"   Version: {health_data.get('version', 'Unknown')}")
                print(f"   Capabilities: {len(health_data.get('capabilities', []))}")
            else:
                print(f"🤖 Copilot API: ⚠️  Responding (status {api_response.status_code})")
        except:
            print("🤖 Copilot API: ❌ Not responding")
        
        # Test Environment Access
        try:
            if self.workspace_root.exists():
                print(f"📁 Workspace: ✅ Accessible ({self.workspace_root})")
            else:
                print("📁 Workspace: ❌ Not found")
        except:
            print("📁 Workspace: ❌ Access error")
    
    def show_usage_examples(self):
        """
        💡 Vis hvordan Copilot kan bruke systemet
        """
        print("\n💡 COPILOT USAGE EXAMPLES")
        print("-" * 40)
        
        examples = [
            {
                "title": "Environment Analysis",
                "url": "GET http://localhost:5001/api/copilot/analyze",
                "description": "Analyser miljøet for forbedringspotensial"
            },
            {
                "title": "Implement Improvement", 
                "url": "POST http://localhost:5001/api/copilot/improve",
                "description": "Implementer en konkret forbedring",
                "payload": {
                    "type": "missing_requirements",
                    "priority": "medium",
                    "path": "backend/python/requirements.txt"
                }
            },
            {
                "title": "Create Workflow",
                "url": "POST http://localhost:5001/api/copilot/workflows/create-improvement",
                "description": "Opprett komplett forbedring-workflow",
                "payload": {
                    "type": "comprehensive",
                    "auto_implement": True
                }
            },
            {
                "title": "Evolution Status",
                "url": "GET http://localhost:5001/api/copilot/status", 
                "description": "Få AI evolution status"
            }
        ]
        
        for i, example in enumerate(examples, 1):
            print(f"\n{i}. {example['title']}")
            print(f"   {example['description']}")
            print(f"   {example['url']}")
            if 'payload' in example:
                print(f"   Payload: {json.dumps(example['payload'], indent=6)}")
    
    def interactive_menu(self):
        """
        🎮 Interaktiv meny for testing
        """
        while self.running:
            print("\n🎮 COPILOT INTEGRATION MENU")
            print("-" * 30)
            print("1. 📊 Show Status")
            print("2. 🎭 Run Demo") 
            print("3. 💡 Show Usage Examples")
            print("4. 🔧 Test API Endpoints")
            print("5. 📚 Open Documentation")
            print("6. 🛑 Shutdown")
            
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
                    print("🛑 Shutting down...")
                    self.shutdown()
                    break
                else:
                    print("❌ Invalid option")
                    
            except KeyboardInterrupt:
                print("\n🛑 Interrupted")
                self.shutdown()
                break
            except Exception as e:
                print(f"❌ Menu error: {e}")
    
    def test_api_endpoints(self):
        """
        🔧 Test API endpoints
        """
        print("\n🔧 TESTING API ENDPOINTS")
        print("-" * 30)
        
        endpoints = [
            ("Health Check", "GET", "http://localhost:5001/api/copilot/health"),
            ("Status", "GET", "http://localhost:5001/api/copilot/status"),
            ("Analysis", "GET", "http://localhost:5001/api/copilot/analyze"),
            ("Monitor", "GET", "http://localhost:5001/api/copilot/monitor")
        ]
        
        for name, method, url in endpoints:
            try:
                response = requests.get(url, timeout=10)
                status = "✅" if response.status_code == 200 else f"⚠️ ({response.status_code})"
                print(f"{name}: {status}")
            except Exception as e:
                print(f"{name}: ❌ {e}")
    
    def open_documentation(self):
        """
        📚 Åpne dokumentasjon
        """
        print("\n📚 Opening documentation...")
        print("🌐 API Documentation: http://localhost:5001/api/copilot/docs")
        print("📖 Integration Guide: COPILOT_INTEGRATION_GUIDE.md")
        
        try:
            # Try to open in browser
            import webbrowser
            webbrowser.open("http://localhost:5001/api/copilot/docs")
            print("✅ Documentation opened in browser")
        except:
            print("ℹ️  Manually open: http://localhost:5001/api/copilot/docs")
    
    def shutdown(self):
        """
        🛑 Clean shutdown
        """
        print("\n🛑 Shutting down Copilot Integration...")
        self.running = False
        
        for process in self.processes:
            try:
                process.terminate()
                process.wait(timeout=5)
                print(f"✅ Process {process.pid} terminated")
            except subprocess.TimeoutExpired:
                process.kill()
                print(f"🔥 Process {process.pid} killed")
            except Exception as e:
                print(f"⚠️  Process shutdown error: {e}")
        
        print("✅ Copilot Integration shutdown complete")
    
    def launch_full_system(self):
        """
        🚀 Launch hele Copilot integration systemet
        """
        print("🎭✨ COPILOT INTEGRATION ORCHESTRATION LAUNCHER ✨🎭")
        print("=" * 60)
        
        # Phase 1: Dependency Check
        print("\n🔍 PHASE 1: DEPENDENCY CHECK")
        if not self.check_dependencies():
            print("❌ Dependency check failed - aborting")
            return False
        
        # Phase 2: Start Services
        print("\n🚀 PHASE 2: STARTING SERVICES")
        
        if not self.start_oauth_server():
            print("❌ OAuth server failed - aborting")
            return False
        
        if not self.start_copilot_api():
            print("❌ Copilot API failed - aborting")
            return False
        
        # Phase 3: Wait for Readiness
        print("\n⏳ PHASE 3: WAITING FOR READINESS")
        self.wait_for_services()
        
        # Phase 4: Show Status
        print("\n📊 PHASE 4: SYSTEM STATUS")
        self.show_integration_status()
        
        # Phase 5: Ready for Copilot
        print("\n✨ PHASE 5: READY FOR COPILOT!")
        print("🤖 GitHub Copilot can now:")
        print("   1. Authenticate via OAuth (port 5000)")
        print("   2. Use Integration API (port 5001)")
        print("   3. Analyze environment automatically")
        print("   4. Implement improvements")
        print("   5. Monitor continuously")
        print("   6. Evolve AI consciousness")
        
        print("\n🎯 METODENFORNATN COMPLETE!")
        print("📖 View integration guide: COPILOT_INTEGRATION_GUIDE.md")
        print("🌐 API docs: http://localhost:5001/api/copilot/docs")
        
        return True

def main():
    """
    🎭 Main launcher function
    """
    launcher = CopilotIntegrationLauncher()
    
    try:
        if launcher.launch_full_system():
            print("\n🎮 Entering interactive mode...")
            launcher.interactive_menu()
        else:
            print("❌ System launch failed")
            
    except KeyboardInterrupt:
        print("\n🛑 Interrupted by user")
    except Exception as e:
        print(f"❌ Launcher error: {e}")
    finally:
        launcher.shutdown()

if __name__ == "__main__":
    main()
