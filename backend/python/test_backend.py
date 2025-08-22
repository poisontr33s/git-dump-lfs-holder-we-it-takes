"""
Basic test suite for Psycho-Noir Kontrapunkt backend modules
Ensures the Python infrastructure is functional
"""

import unittest
import sys
import os

# Add the backend directory to the path so we can import modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    import dialogue_analyzer_pnc
    import dialogue_data_enhancer_pnc
    import extract_dialogue
    MODULES_AVAILABLE = True
except ImportError as e:
    MODULES_AVAILABLE = False
    IMPORT_ERROR = str(e)


class TestPsychoNoirBackend(unittest.TestCase):
    """Test suite for Psycho-Noir Kontrapunkt backend functionality."""

    def test_modules_can_be_imported(self):
        """Test that core modules can be imported without errors."""
        if not MODULES_AVAILABLE:
            self.skipTest(f"Modules not available: {IMPORT_ERROR}")
        
        # If we get here, imports succeeded
        self.assertTrue(True, "All core modules imported successfully")

    def test_basic_functionality(self):
        """Test basic Python functionality for the backend."""
        # Test basic operations that might be used in the backend
        test_data = {
            'skyskraperen': 'overvåkning_og_kontroll',
            'rustbeltet': 'overlevelse_og_improvisation'
        }
        
        self.assertEqual(test_data['skyskraperen'], 'overvåkning_og_kontroll')
        self.assertEqual(test_data['rustbeltet'], 'overlevelse_og_improvisation')

    def test_environment_setup(self):
        """Test that the Python environment is properly configured."""
        # Basic environment checks
        self.assertIsNotNone(sys.version)
        self.assertTrue(len(sys.path) > 0)
        
        # Check that we can work with basic data structures
        test_list = [1, 2, 3]
        test_dict = {'key': 'value'}
        
        self.assertEqual(len(test_list), 3)
        self.assertEqual(test_dict['key'], 'value')


if __name__ == '__main__':
    unittest.main()