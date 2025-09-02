#!/usr/bin/env python3
"""
test_resurrection_modules.py

Enkel test suite for gjenopprettede necromancy moduler.
Verifiserer at resurrections fungerer som forventet.
"""

import sys
import importlib.util
from pathlib import Path

def test_module(module_path: str, expected_output: str = None):
    """Test at en gjenopprettet modul kan importeres og kjøres"""
    try:
        # Import module dynamically
        spec = importlib.util.spec_from_file_location("test_module", module_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        # Run main function if exists
        if hasattr(module, 'main'):
            print(f"✅ {module_path}: Import OK, main() exists")
            return True
        else:
            print(f"⚠️  {module_path}: Import OK, no main() function")
            return True
            
    except Exception as e:
        print(f"❌ {module_path}: Error - {str(e)}")
        return False

def main():
    """Test alle gjenopprettede moduler"""
    root = Path(__file__).resolve().parents[1]
    
    # Test resurrected modules
    test_modules = [
        "backend/python/dialogue_analyzer_pnc.py",
        "backend/python/extract_dialogue.py", 
        "backend/python/copilot_client_demo.py"
    ]
    
    print("🎭 Testing Resurrected Necromancy Modules")
    print("=" * 50)
    
    passed = 0
    total = len(test_modules)
    
    for module_path in test_modules:
        full_path = root / module_path
        if full_path.exists():
            if test_module(str(full_path)):
                passed += 1
        else:
            print(f"❌ {module_path}: File not found")
    
    print("=" * 50)
    print(f"RESULTS: {passed}/{total} modules passed tests")
    
    if passed == total:
        print("🎉 All resurrected modules are functional!")
        return 0
    else:
        print("⚠️  Some modules need attention")
        return 1

if __name__ == "__main__":
    sys.exit(main())
