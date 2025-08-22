"""
Psycho-Noir Kontrapunkt Backend

A collection of modules for analyzing and processing dialogue data
within the dystopian techno-noir framework of Psycho-Noir Kontrapunkt.

This package includes:
- dialogue_analyzer_pnc: Analysis tools for conversation trees and dialogue structures
- dialogue_data_enhancer_pnc: Data enhancement and enrichment utilities  
- extract_dialogue: Database extraction and CSV generation tools
- neural_archaeology_scanner: Advanced pattern recognition for dialogue archaeology
- transmutator_de_lingua: Language transformation and processing utilities

The modules support both "Skyskraperen" (high-tech surveillance) and 
"Rustbeltet" (industrial survival) narrative domains.
"""

__version__ = "0.1.0"
__author__ = "poisontr33s"

# Core module imports for convenient access
try:
    from . import dialogue_analyzer_pnc
    from . import dialogue_data_enhancer_pnc
    from . import extract_dialogue
    
    __all__ = [
        'dialogue_analyzer_pnc',
        'dialogue_data_enhancer_pnc', 
        'extract_dialogue'
    ]
except ImportError:
    # Handle case where dependencies aren't available
    __all__ = []