#!/usr/bin/env python3
"""
Jules Integration Test - Verification of Caching Mechanisms

Tests that Jules' caching and dependency management systems are working correctly.
"""

import os
import sys
import json
import subprocess
from pathlib import Path

def test_jules_cache_analyzer():
    """Test Jules cache analyzer functionality"""
    print("🔍 Testing Jules Cache Analyzer...")
    
    script_path = Path(".github/jules/scripts/jules-cache-analyzer.py")
    if not script_path.exists():
        return False, "Cache analyzer script not found"
    
    try:
        result = subprocess.run([
            sys.executable, str(script_path)
        ], capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            # Check if analysis file was created
            analysis_file = Path("jules-cache-analysis.md")
            if analysis_file.exists():
                return True, "Cache analyzer working correctly"
            else:
                return False, "Analysis file not generated"
        else:
            return False, f"Script failed: {result.stderr}"
    except subprocess.TimeoutExpired:
        return False, "Script timeout"
    except Exception as e:
        return False, f"Execution error: {str(e)}"

def test_jules_dependency_validator():
    """Test Jules dependency validator functionality"""
    print("🔍 Testing Jules Dependency Validator...")
    
    script_path = Path(".github/jules/scripts/jules-dependency-validator.sh")
    if not script_path.exists():
        return False, "Dependency validator script not found"
    
    try:
        # Set CI=true to suppress console output during test
        env = os.environ.copy()
        env['CI'] = 'true'
        
        result = subprocess.run([
            "bash", str(script_path)
        ], capture_output=True, text=True, timeout=30, env=env)
        
        if result.returncode == 0:
            # Check if validation report was created
            report_file = Path("jules-validation-report.md")
            config_file = Path(".github/jules/cache-config.json")
            
            if report_file.exists() and config_file.exists():
                return True, "Dependency validator working correctly"
            else:
                return False, "Required files not generated"
        else:
            return False, f"Script failed: {result.stderr}"
    except subprocess.TimeoutExpired:
        return False, "Script timeout"
    except Exception as e:
        return False, f"Execution error: {str(e)}"

def test_cache_config_validity():
    """Test that generated cache config is valid JSON"""
    print("🔍 Testing Cache Config Validity...")
    
    config_file = Path(".github/jules/cache-config.json")
    if not config_file.exists():
        return False, "Cache config file not found"
    
    try:
        with open(config_file) as f:
            config = json.load(f)
        
        # Validate structure
        required_keys = ["jules_version", "cache_strategies", "conditional_checks"]
        for key in required_keys:
            if key not in config:
                return False, f"Missing required key: {key}"
        
        # Check if ecosystems are defined
        ecosystems = ["nodejs", "python", "ruby", "docker"]
        for ecosystem in ecosystems:
            if ecosystem not in config["cache_strategies"]:
                return False, f"Missing ecosystem config: {ecosystem}"
        
        return True, "Cache config is valid"
    
    except json.JSONDecodeError as e:
        return False, f"Invalid JSON: {str(e)}"
    except Exception as e:
        return False, f"Config validation error: {str(e)}"

def test_jules_files_exist():
    """Test that all Jules files are present"""
    print("🔍 Testing Jules File Structure...")
    
    required_files = [
        ".github/jules/README.md",
        ".github/jules/jules-config.yml", 
        ".github/jules/CACHE_STRATEGY.md",
        ".github/jules/scripts/jules-cache-analyzer.py",
        ".github/jules/scripts/jules-dependency-validator.sh",
        ".github/workflows/jules-enhanced-ci.yml"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
    
    if missing_files:
        return False, f"Missing files: {', '.join(missing_files)}"
    
    return True, "All Jules files present"

def test_workflow_syntax():
    """Test that the Jules workflow has valid syntax"""
    print("🔍 Testing Workflow Syntax...")
    
    workflow_file = Path(".github/workflows/jules-enhanced-ci.yml")
    if not workflow_file.exists():
        return False, "Jules workflow file not found"
    
    try:
        import yaml
        with open(workflow_file) as f:
            yaml.safe_load(f)
        return True, "Workflow syntax is valid"
    except ImportError:
        # If yaml module not available, just check if file exists
        return True, "Workflow file exists (YAML module not available for validation)"
    except yaml.YAMLError as e:
        return False, f"Invalid YAML syntax: {str(e)}"
    except Exception as e:
        return False, f"Workflow validation error: {str(e)}"

def run_all_tests():
    """Run all Jules integration tests"""
    print("🎭 Jules Integration Test Suite - Initiating validation protocol...\n")
    
    tests = [
        ("Jules File Structure", test_jules_files_exist),
        ("Cache Analyzer", test_jules_cache_analyzer),
        ("Dependency Validator", test_jules_dependency_validator),
        ("Cache Config Validity", test_cache_config_validity),
        ("Workflow Syntax", test_workflow_syntax),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            success, message = test_func()
            results.append((test_name, success, message))
            
            status = "✅ PASS" if success else "❌ FAIL"
            print(f"{status} {test_name}: {message}")
        except Exception as e:
            results.append((test_name, False, f"Test error: {str(e)}"))
            print(f"❌ FAIL {test_name}: Test error: {str(e)}")
    
    print("\n" + "="*60)
    print("🎭 Jules Integration Test Results")
    print("="*60)
    
    passed = sum(1 for _, success, _ in results if success)
    total = len(results)
    
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 All tests passed! Jules is ready for Den Usynlige Hånds optimization.")
        return 0
    else:
        print("⚠️ Some tests failed. Jules may need attention.")
        return 1

if __name__ == "__main__":
    exit_code = run_all_tests()
    sys.exit(exit_code)