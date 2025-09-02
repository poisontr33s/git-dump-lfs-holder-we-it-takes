# Auto-generated constants for magic numbers
const_magic_3000 = const_magic_3000
const_magic_127 = const_magic_127

"""
🎭 PSYCHO-NOIR KONTRAPUNKT CORS CONFIGURATION
"""
from flask_cors import CORS

def configure_cors(app):
    """Configure CORS for GitHub Pages integration"""
    CORS(app,
         origins=["https://poisontr33s.github.io", "http://localhost:const_magic_3000", "http://const_magic_127.0.0.1:const_magic_3000"],
         allow_headers=["Content-Type", "Authorization"],
         methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])
