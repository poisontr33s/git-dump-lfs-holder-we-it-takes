"""
🎭 PSYCHO-NOIR KONTRAPUNKT CORS CONFIGURATION
"""
from flask_cors import CORS

def configure_cors(app):
    """Configure CORS for GitHub Pages integration"""
    CORS(app, 
         origins=["https://poisontr33s.github.io", "http://localhost:3000", "http://127.0.0.1:3000"],
         allow_headers=["Content-Type", "Authorization"],
         methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])
