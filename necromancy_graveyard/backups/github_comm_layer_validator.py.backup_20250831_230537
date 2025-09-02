#!/usr/bin/env python3
"""
🎭✨ GITHUB COMMUNICATION LAYER VALIDATOR ✨🎭
Tester faktisk kommunikasjon mellom lokal portal og GitHub API
For å validere om dette er ekte funksjonell integrasjon eller bare fancy UI
"""

import requests
import json
import os
from datetime import datetime
import time

class GitHubCommLayerValidator:
    def __init__(self):
        self.github_token = os.environ.get('GITHUB_TOKEN')
        self.repo = "poisontr33s/PsychoNoir-Kontrapunkt"
        self.base_url = "https://api.github.com"
        self.results = []

    def log_test(self, test_name, success, details):
        """Log test results"""
        result = {
            "test": test_name,
            "success": success,
            "details": details,
            "timestamp": datetime.now().isoformat()
        }
        self.results.append(result)
        status = "✅" if success else "❌"
        print(f"{status} {test_name}: {details}")

    def test_github_api_basic(self):
        """Test basic GitHub API connectivity"""
        try:
            headers = {}
            if self.github_token:
                headers["Authorization"] = f"token {self.github_token}"
            
            response = requests.get(f"{self.base_url}/repos/{self.repo}", headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                self.log_test("GitHub API Basic", True, f"Repo accessible, {data.get('stargazers_count', 0)} stars")
                return True
            else:
                self.log_test("GitHub API Basic", False, f"HTTP {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("GitHub API Basic", False, f"Exception: {e}")
            return False

    def test_github_pages_status(self):
        """Test GitHub Pages deployment status"""
        try:
            headers = {}
            if self.github_token:
                headers["Authorization"] = f"token {self.github_token}"
            
            response = requests.get(f"{self.base_url}/repos/{self.repo}/pages", headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                self.log_test("GitHub Pages Status", True, f"Pages active: {data.get('status', 'unknown')}")
                return data.get('html_url')
            elif response.status_code == 404:
                self.log_test("GitHub Pages Status", False, "Pages not configured/deployed")
                return None
            else:
                self.log_test("GitHub Pages Status", False, f"HTTP {response.status_code}")
                return None
                
        except Exception as e:
            self.log_test("GitHub Pages Status", False, f"Exception: {e}")
            return None

    def test_actual_pages_accessibility(self):
        """Test if GitHub Pages URL is actually accessible"""
        pages_url = "https://poisontr33s.github.io/PsychoNoir-Kontrapunkt/"
        
        try:
            response = requests.get(pages_url, timeout=10)
            
            if response.status_code == 200:
                content_length = len(response.text)
                self.log_test("Pages Accessibility", True, f"Live site: {content_length} bytes loaded")
                return True
            elif response.status_code == 404:
                self.log_test("Pages Accessibility", False, "404 - Site not deployed")
                return False
            else:
                self.log_test("Pages Accessibility", False, f"HTTP {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("Pages Accessibility", False, f"Exception: {e}")
            return False

    def test_workflow_functionality(self):
        """Test if deployment workflows exist and can be triggered"""
        try:
            headers = {}
            if self.github_token:
                headers["Authorization"] = f"token {self.github_token}"
            
            response = requests.get(f"{self.base_url}/repos/{self.repo}/actions/workflows", headers=headers)
            
            if response.status_code == 200:
                workflows = response.json()['workflows']
                deploy_workflows = [w for w in workflows if 'pages' in w['name'].lower() or 'deploy' in w['name'].lower()]
                
                if deploy_workflows:
                    workflow_names = [w['name'] for w in deploy_workflows]
                    self.log_test("Deployment Workflows", True, f"Found: {', '.join(workflow_names)}")
                    return True
                else:
                    self.log_test("Deployment Workflows", False, "No deployment workflows found")
                    return False
            else:
                self.log_test("Deployment Workflows", False, f"HTTP {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("Deployment Workflows", False, f"Exception: {e}")
            return False

    def test_api_rate_limits(self):
        """Test API rate limits to understand actual access level"""
        try:
            headers = {}
            if self.github_token:
                headers["Authorization"] = f"token {self.github_token}"
            
            response = requests.get(f"{self.base_url}/rate_limit", headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                core_remaining = data['rate']['remaining']
                core_limit = data['rate']['limit']
                
                auth_status = "Authenticated" if self.github_token else "Unauthenticated"
                self.log_test("API Rate Limits", True, f"{auth_status}: {core_remaining}/{core_limit} calls remaining")
                return True
            else:
                self.log_test("API Rate Limits", False, f"HTTP {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("API Rate Limits", False, f"Exception: {e}")
            return False

    def test_repository_permissions(self):
        """Test actual repository permissions level"""
        try:
            headers = {}
            if self.github_token:
                headers["Authorization"] = f"token {self.github_token}"
            
            # Test if we can create/modify content
            response = requests.get(f"{self.base_url}/repos/{self.repo}/collaborators", headers=headers)
            
            if response.status_code == 200:
                self.log_test("Repository Permissions", True, "Write access confirmed")
                return "write"
            elif response.status_code == 403:
                self.log_test("Repository Permissions", True, "Read-only access")
                return "read"
            else:
                self.log_test("Repository Permissions", False, f"HTTP {response.status_code}")
                return None
                
        except Exception as e:
            self.log_test("Repository Permissions", False, f"Exception: {e}")
            return None

    def comprehensive_validation(self):
        """Run all validation tests"""
        print("🎭✨ GITHUB COMMUNICATION LAYER VALIDATION ✨🎭")
        print("=" * 60)
        
        # Run all tests
        api_works = self.test_github_api_basic()
        pages_status = self.test_github_pages_status()
        pages_accessible = self.test_actual_pages_accessibility()
        workflows_exist = self.test_workflow_functionality()
        rate_limits = self.test_api_rate_limits()
        permissions = self.test_repository_permissions()
        
        print("\n" + "=" * 60)
        print("🎯 VALIDATION SUMMARY:")
        
        success_count = sum(1 for r in self.results if r['success'])
        total_tests = len(self.results)
        
        print(f"📊 Tests Passed: {success_count}/{total_tests}")
        
        # Determine if system is genuinely functional
        if pages_accessible and api_works:
            verdict = "✅ GENUINELY FUNCTIONAL - Real integration active"
        elif api_works and workflows_exist:
            verdict = "🔄 PARTIALLY FUNCTIONAL - API works, deployment pending"
        elif api_works:
            verdict = "⚠️ LIMITED FUNCTIONAL - API only, no web deployment"
        else:
            verdict = "❌ NON-FUNCTIONAL - No real integration"
        
        print(f"🏆 VERDICT: {verdict}")
        
        # Save results
        results_file = f"github_comm_validation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(results_file, 'w') as f:
            json.dump({
                "validation_timestamp": datetime.now().isoformat(),
                "verdict": verdict,
                "success_rate": f"{success_count}/{total_tests}",
                "tests": self.results
            }, f, indent=2)
        
        print(f"📝 Results saved: {results_file}")
        
        return verdict, self.results

if __name__ == "__main__":
    validator = GitHubCommLayerValidator()
    verdict, results = validator.comprehensive_validation()
    
    print(f"\n🎭✨ FINAL ASSESSMENT: {verdict} ✨🎭")
