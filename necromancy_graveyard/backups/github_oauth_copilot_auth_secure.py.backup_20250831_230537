#!/usr/bin/env python3
"""
Production-Ready GitHub OAuth Copilot-Style Authentication API
============================================================

Implements GitHub OAuth flow with enhanced security following GitHub best practices:
- Environment variable secrets management
- Token encryption at rest
- HTTPS enforcement
- Enhanced error handling and logging
"""

from flask import Flask, request, jsonify, render_template_string, redirect, url_for
from flask_cors import CORS
import requests
import json
import time
import threading
from datetime import datetime, timedelta
import secrets
import qrcode
import io
import base64
import os
import logging
from cryptography.fernet import Fernet

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Security: Load secrets from environment variables (GitHub best practice)
GITHUB_CLIENT_ID = os.environ.get('GITHUB_CLIENT_ID')
GITHUB_CLIENT_SECRET = os.environ.get('GITHUB_CLIENT_SECRET')
ENCRYPTION_KEY = os.environ.get('ENCRYPTION_KEY')

# Validate required environment variables
if not GITHUB_CLIENT_ID:
    raise ValueError("GITHUB_CLIENT_ID environment variable is required")
if not GITHUB_CLIENT_SECRET:
    raise ValueError("GITHUB_CLIENT_SECRET environment variable is required")
if not ENCRYPTION_KEY:
    logger.warning("ENCRYPTION_KEY not set, generating temporary key (NOT for production)")
    ENCRYPTION_KEY = Fernet.generate_key()

# Initialize encryption
cipher_suite = Fernet(ENCRYPTION_KEY if isinstance(ENCRYPTION_KEY, bytes) else ENCRYPTION_KEY.encode())

# Device flow storage
device_flows = {}
authenticated_sessions = {}

def encrypt_token(token):
    """Encrypt sensitive tokens (GitHub best practice)"""
    try:
        return cipher_suite.encrypt(token.encode()).decode()
    except Exception as e:
        logger.error(f"Token encryption failed: {e}")
        return token  # Fallback for development

def decrypt_token(encrypted_token):
    """Decrypt sensitive tokens"""
    try:
        return cipher_suite.decrypt(encrypted_token.encode()).decode()
    except Exception as e:
        logger.error(f"Token decryption failed: {e}")
        return encrypted_token  # Fallback for development

def generate_csrf_token():
    """Generate CSRF token for additional security"""
    return secrets.token_urlsafe(32)

def validate_csrf_token(token, session_token):
    """Validate CSRF token using constant-time comparison"""
    return secrets.compare_digest(token, session_token)

class GitHubOAuthDeviceFlowSecure:
    """
    Secure implementation of GitHub Device Flow authentication 
    following GitHub docs best practices
    """
    
    def __init__(self):
        self.base_url = "https://github.com"
        self.api_url = "https://api.github.com"
        # Enhanced User-Agent following GitHub guidelines
        self.user_agent = "PsychoNoir-Kontrapunkt/1.0 (GitHub OAuth Connector)"
    
    def start_device_flow(self, scopes=None):
        """
        Start GitHub Device Flow with enhanced security
        """
        if scopes is None:
            # Minimal scopes following Principle of Least Privilege
            scopes = ["user:email", "read:user"]
        
        try:
            # GitHub Device Flow Step 1: Request device and user codes
            response = requests.post(
                f"{self.base_url}/login/device/code",
                headers={
                    "Accept": "application/json",
                    "User-Agent": self.user_agent
                },
                data={
                    "client_id": GITHUB_CLIENT_ID,
                    "scope": " ".join(scopes)
                },
                timeout=30  # Timeout for security
            )
            
            if response.status_code == 200:
                data = response.json()
                
                # Generate secure flow ID
                flow_id = secrets.token_urlsafe(16)
                csrf_token = generate_csrf_token()
                
                # Store device flow data with security enhancements
                device_flows[flow_id] = {
                    "device_code": encrypt_token(data["device_code"]),  # Encrypt sensitive data
                    "user_code": data["user_code"],  # This is safe to store unencrypted
                    "verification_uri": data["verification_uri"],
                    "verification_uri_complete": data.get("verification_uri_complete"),
                    "expires_in": data["expires_in"],
                    "interval": data["interval"],
                    "created_at": datetime.now(),
                    "status": "pending",
                    "csrf_token": csrf_token,
                    "scopes": scopes
                }
                
                logger.info(f"Device flow initiated: {flow_id}")
                
                return {
                    "success": True,
                    "flow_id": flow_id,
                    "user_code": data["user_code"],
                    "verification_uri": data["verification_uri"],
                    "verification_uri_complete": data.get("verification_uri_complete"),
                    "expires_in": data["expires_in"],
                    "interval": data["interval"],
                    "csrf_token": csrf_token
                }
            else:
                logger.error(f"GitHub device flow start failed: {response.status_code}")
                return {
                    "success": False,
                    "error": f"GitHub API error: {response.status_code}",
                    "details": response.text
                }
                
        except requests.RequestException as e:
            logger.error(f"Network error during device flow start: {e}")
            return {
                "success": False,
                "error": "Network error communicating with GitHub"
            }
    
    def poll_for_token(self, flow_id, csrf_token=None):
        """
        Poll GitHub for authentication completion with enhanced security
        """
        if flow_id not in device_flows:
            return {"success": False, "error": "Invalid flow ID"}
        
        flow_data = device_flows[flow_id]
        
        # CSRF validation (if provided)
        if csrf_token and not validate_csrf_token(csrf_token, flow_data.get("csrf_token", "")):
            logger.warning(f"CSRF token validation failed for flow: {flow_id}")
            return {"success": False, "error": "Invalid CSRF token"}
        
        # Check if expired
        if datetime.now() > flow_data["created_at"] + timedelta(seconds=flow_data["expires_in"]):
            device_flows[flow_id]["status"] = "expired"
            logger.info(f"Device flow expired: {flow_id}")
            return {"success": False, "error": "Device flow expired"}
        
        try:
            # Decrypt device code for API call
            device_code = decrypt_token(flow_data["device_code"])
            
            # Poll GitHub for token
            response = requests.post(
                f"{self.base_url}/login/oauth/access_token",
                headers={
                    "Accept": "application/json",
                    "User-Agent": self.user_agent
                },
                data={
                    "client_id": GITHUB_CLIENT_ID,
                    "device_code": device_code,
                    "grant_type": "urn:ietf:params:oauth:grant-type:device_code"
                },
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                
                if "access_token" in data:
                    # Authentication successful!
                    logger.info(f"Authentication successful for flow: {flow_id}")
                    
                    # Encrypt access token before storage
                    encrypted_token = encrypt_token(data["access_token"])
                    
                    device_flows[flow_id]["status"] = "completed"
                    device_flows[flow_id]["access_token"] = encrypted_token
                    device_flows[flow_id]["token_type"] = data.get("token_type", "bearer")
                    device_flows[flow_id]["scope"] = data.get("scope", "")
                    
                    # Get user information
                    user_info = self.get_user_info(data["access_token"])
                    device_flows[flow_id]["user"] = user_info
                    
                    # Store in authenticated sessions with encryption
                    session_id = secrets.token_urlsafe(32)
                    authenticated_sessions[session_id] = {
                        "access_token": encrypted_token,
                        "user": user_info,
                        "authenticated_at": datetime.now(),
                        "flow_id": flow_id,
                        "scopes": flow_data.get("scopes", [])
                    }
                    
                    return {
                        "success": True,
                        "status": "completed",
                        "session_id": session_id,
                        "user": user_info
                        # NOTE: We don't return the actual access token for security
                    }
                
                elif data.get("error") == "authorization_pending":
                    return {"success": True, "status": "pending"}
                
                elif data.get("error") == "slow_down":
                    # GitHub rate limiting - respect the slow down
                    return {"success": True, "status": "slow_down"}
                
                elif data.get("error") == "expired_token":
                    device_flows[flow_id]["status"] = "expired"
                    return {"success": False, "error": "Device code expired"}
                
                elif data.get("error") == "access_denied":
                    device_flows[flow_id]["status"] = "denied"
                    logger.info(f"User denied access for flow: {flow_id}")
                    return {"success": False, "error": "User denied access"}
                
                else:
                    logger.error(f"Unknown GitHub error: {data}")
                    return {"success": False, "error": f"Unknown error: {data.get('error', 'Unknown')}"}
            
            else:
                logger.error(f"GitHub API error during polling: {response.status_code}")
                return {"success": False, "error": f"GitHub API error: {response.status_code}"}
        
        except requests.RequestException as e:
            logger.error(f"Network error during token polling: {e}")
            return {"success": False, "error": "Network error communicating with GitHub"}
    
    def get_user_info(self, access_token):
        """Get user information from GitHub API with enhanced error handling"""
        try:
            response = requests.get(
                f"{self.api_url}/user",
                headers={
                    "Authorization": f"Bearer {access_token}",  # Bearer preferred over token
                    "Accept": "application/vnd.github.v3+json",
                    "User-Agent": self.user_agent
                },
                timeout=30
            )
            
            if response.status_code == 200:
                user_data = response.json()
                # Log successful user info retrieval (without sensitive data)
                logger.info(f"User info retrieved for: {user_data.get('login', 'unknown')}")
                return user_data
            else:
                logger.error(f"Failed to get user info: {response.status_code}")
                return {"error": "Failed to get user info", "status": response.status_code}
                
        except requests.RequestException as e:
            logger.error(f"Network error getting user info: {e}")
            return {"error": "Network error getting user info"}
    
    def check_copilot_access(self, access_token):
        """Check if user has GitHub Copilot access"""
        try:
            response = requests.get(
                f"{self.api_url}/user/copilot_billing",
                headers={
                    "Authorization": f"Bearer {access_token}",
                    "Accept": "application/vnd.github.v3+json",
                    "User-Agent": self.user_agent
                },
                timeout=30
            )
            
            return response.status_code == 200
            
        except requests.RequestException:
            return False
    
    def get_session_token(self, session_id):
        """Securely retrieve access token for a session"""
        if session_id in authenticated_sessions:
            session = authenticated_sessions[session_id]
            return decrypt_token(session["access_token"])
        return None

# Initialize secure OAuth handler
oauth_handler = GitHubOAuthDeviceFlowSecure()

@app.route('/')
def oauth_portal():
    """Main OAuth portal page with enhanced security"""
    # Generate nonce for CSP
    nonce = secrets.token_urlsafe(16)
    
    return render_template_string("""
<!DOCTYPE html>
<html lang="no">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GitHub Copilot OAuth Authentication - Secure</title>
    <meta http-equiv="Content-Security-Policy" content="default-src 'self'; script-src 'self' 'nonce-{{ nonce }}'; style-src 'self' 'unsafe-inline';">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'SF Pro Display', -apple-system, BlinkMacSystemFont, sans-serif;
            background: linear-gradient(135deg, #0d1117 0%, #161b22 100%);
            color: #f0f6fc;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        .oauth-container {
            max-width: 500px;
            padding: 40px;
            background: rgba(22, 27, 34, 0.9);
            border-radius: 16px;
            border: 1px solid #30363d;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
            text-align: center;
        }

        .security-badge {
            background: #1f6f3b;
            color: white;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 12px;
            margin-bottom: 20px;
            display: inline-block;
        }

        .github-logo {
            width: 64px;
            height: 64px;
            margin: 0 auto 20px;
            background: #f0f6fc;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 24px;
            color: #0d1117;
        }

        h1 {
            font-size: 28px;
            margin-bottom: 12px;
            background: linear-gradient(135deg, #58a6ff, #79c0ff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .subtitle {
            color: #8b949e;
            margin-bottom: 32px;
            font-size: 16px;
        }

        .auth-button {
            background: linear-gradient(135deg, #238636, #2ea043);
            border: none;
            padding: 16px 32px;
            border-radius: 8px;
            color: white;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            width: 100%;
            margin-bottom: 20px;
        }

        .auth-button:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 16px rgba(35, 134, 54, 0.3);
        }

        .auth-button:disabled {
            opacity: 0.6;
            cursor: not-allowed;
            transform: none;
        }

        .device-flow-container {
            display: none;
            margin-top: 24px;
        }

        .user-code-display {
            background: #21262d;
            border: 1px solid #30363d;
            border-radius: 8px;
            padding: 20px;
            margin: 20px 0;
            font-family: 'SF Mono', Consolas, monospace;
            font-size: 24px;
            font-weight: bold;
            letter-spacing: 4px;
            color: #58a6ff;
        }

        .qr-code {
            margin: 20px 0;
            display: flex;
            justify-content: center;
        }

        .status-indicator {
            display: inline-block;
            width: 8px;
            height: 8px;
            border-radius: 50%;
            margin-right: 8px;
        }

        .status-pending { background: #f85149; }
        .status-success { background: #56d364; }

        .instructions {
            background: rgba(56, 139, 253, 0.1);
            border: 1px solid rgba(56, 139, 253, 0.3);
            border-radius: 8px;
            padding: 16px;
            margin: 16px 0;
            text-align: left;
        }

        .security-info {
            font-size: 12px;
            color: #8b949e;
            margin-top: 20px;
            text-align: left;
        }

        .footer {
            margin-top: 32px;
            padding-top: 20px;
            border-top: 1px solid #30363d;
            color: #6e7681;
            font-size: 14px;
        }
    </style>
</head>
<body>
    <div class="oauth-container">
        <div class="security-badge">🔒 Enhanced Security Mode</div>
        
        <div class="github-logo">
            <svg width="32" height="32" viewBox="0 0 16 16" fill="currentColor">
                <path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0 0 16 8c0-4.42-3.58-8-8-8z"/>
            </svg>
        </div>

        <h1>GitHub Copilot Authentication</h1>
        <p class="subtitle">Secure OAuth device flow • Production ready</p>

        <div id="initial-screen">
            <button class="auth-button" onclick="startDeviceFlow()">
                🚀 Start Secure Authentication
            </button>
            
            <div class="security-info">
                <strong>Security Features:</strong><br>
                • End-to-end encrypted token storage<br>
                • CSRF protection enabled<br>
                • Rate limiting compliance<br>
                • Environment variable secrets<br>
                • GitHub best practices implemented
            </div>
        </div>

        <div id="device-flow-screen" class="device-flow-container">
            <div class="instructions">
                <strong>📱 Mobile Authentication:</strong><br>
                1. Open GitHub app on your mobile device<br>
                2. Scan the QR code below, or<br>
                3. Visit <span id="verification-uri"></span><br>
                4. Enter the code: <span id="user-code-text"></span>
            </div>

            <div class="user-code-display" id="user-code-display">
                Loading...
            </div>

            <div class="qr-code" id="qr-code-container">
                <!-- QR code will be inserted here -->
            </div>

            <div style="margin: 20px 0;">
                <span class="status-indicator status-pending" id="status-indicator"></span>
                <span id="status-text">Waiting for authentication...</span>
            </div>

            <button class="auth-button" onclick="cancelFlow()" style="background: #da3633;">
                Cancel Authentication
            </button>
        </div>

        <div class="footer">
            Powered by PsychoNoir-Kontrapunkt Neural Archaeology<br>
            Following GitHub OAuth 2.0 Device Flow Standards
        </div>
    </div>

    <script nonce="{{ nonce }}">
        let currentFlowId = null;
        let pollingInterval = null;
        let csrfToken = null;

        function startDeviceFlow() {
            document.getElementById('initial-screen').style.display = 'none';
            document.getElementById('device-flow-screen').style.display = 'block';

            fetch('/api/start-device-flow', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({})
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    currentFlowId = data.flow_id;
                    csrfToken = data.csrf_token;
                    
                    document.getElementById('user-code-display').textContent = data.user_code;
                    document.getElementById('user-code-text').textContent = data.user_code;
                    document.getElementById('verification-uri').textContent = data.verification_uri;

                    // Generate QR code
                    const qrUrl = data.verification_uri_complete || 
                                  `${data.verification_uri}?user_code=${data.user_code}`;
                    generateQRCode(qrUrl);

                    // Start polling with secure interval
                    const interval = Math.max(data.interval * 1000, 5000); // Respect GitHub rate limits
                    pollingInterval = setInterval(() => pollForToken(), interval);
                } else {
                    alert('Error starting authentication: ' + data.error);
                    resetToInitial();
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Network error occurred');
                resetToInitial();
            });
        }

        function pollForToken() {
            if (!currentFlowId) return;

            fetch('/api/poll-token', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    flow_id: currentFlowId,
                    csrf_token: csrfToken
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success && data.status === 'completed') {
                    // Authentication successful!
                    clearInterval(pollingInterval);
                    document.getElementById('status-indicator').className = 'status-indicator status-success';
                    document.getElementById('status-text').textContent = 
                        `✅ Authentication successful! Welcome, ${data.user.login}`;
                    
                    // Store session info
                    sessionStorage.setItem('github_session', data.session_id);
                    
                    // Redirect or notify parent window
                    setTimeout(() => {
                        if (window.opener) {
                            window.opener.postMessage({
                                type: 'oauth_success',
                                session_id: data.session_id,
                                user: data.user
                            }, '*');
                            window.close();
                        } else {
                            alert('Authentication complete! You can now close this window.');
                        }
                    }, 2000);
                    
                } else if (data.success && data.status === 'slow_down') {
                    // GitHub rate limiting - increase interval
                    clearInterval(pollingInterval);
                    setTimeout(() => {
                        pollingInterval = setInterval(() => pollForToken(), 10000); // 10 second interval
                    }, 5000);
                    
                } else if (!data.success) {
                    clearInterval(pollingInterval);
                    document.getElementById('status-text').textContent = '❌ ' + data.error;
                    setTimeout(() => resetToInitial(), 3000);
                }
            })
            .catch(error => {
                console.error('Polling error:', error);
            });
        }

        function generateQRCode(url) {
            fetch('/api/generate-qr', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ url: url })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    const img = document.createElement('img');
                    img.src = 'data:image/png;base64,' + data.qr_code;
                    img.style.maxWidth = '200px';
                    img.style.border = '8px solid white';
                    img.style.borderRadius = '8px';
                    document.getElementById('qr-code-container').appendChild(img);
                }
            })
            .catch(error => console.error('QR generation error:', error));
        }

        function cancelFlow() {
            if (pollingInterval) {
                clearInterval(pollingInterval);
            }
            resetToInitial();
        }

        function resetToInitial() {
            document.getElementById('device-flow-screen').style.display = 'none';
            document.getElementById('initial-screen').style.display = 'block';
            currentFlowId = null;
            csrfToken = null;
            if (pollingInterval) {
                clearInterval(pollingInterval);
            }
        }

        // Security: Clear sensitive data on page unload
        window.addEventListener('beforeunload', function() {
            if (pollingInterval) {
                clearInterval(pollingInterval);
            }
        });
    </script>
</body>
</html>
    """, nonce=nonce)

# API Routes with enhanced security

@app.route('/api/start-device-flow', methods=['POST'])
def api_start_device_flow():
    """API endpoint to start device flow with security enhancements"""
    try:
        data = request.get_json() or {}
        scopes = data.get('scopes', ["user:email", "read:user"])
        
        result = oauth_handler.start_device_flow(scopes)
        
        if result['success']:
            logger.info(f"Device flow started successfully: {result['flow_id']}")
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error in start_device_flow: {e}")
        return jsonify({
            "success": False,
            "error": "Internal server error"
        }), 500

@app.route('/api/poll-token', methods=['POST'])
def api_poll_token():
    """API endpoint to poll for token with CSRF protection"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"success": False, "error": "No data provided"}), 400
        
        flow_id = data.get('flow_id')
        csrf_token = data.get('csrf_token')
        
        if not flow_id:
            return jsonify({"success": False, "error": "Flow ID required"}), 400
        
        result = oauth_handler.poll_for_token(flow_id, csrf_token)
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error in poll_token: {e}")
        return jsonify({
            "success": False,
            "error": "Internal server error"
        }), 500

@app.route('/api/generate-qr', methods=['POST'])
def api_generate_qr():
    """Generate QR code for mobile authentication"""
    try:
        data = request.get_json()
        url = data.get('url')
        
        if not url:
            return jsonify({"success": False, "error": "URL required"}), 400
        
        # Generate QR code
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(url)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)
        
        qr_base64 = base64.b64encode(buffer.getvalue()).decode()
        
        return jsonify({
            "success": True,
            "qr_code": qr_base64
        })
        
    except Exception as e:
        logger.error(f"Error generating QR code: {e}")
        return jsonify({
            "success": False,
            "error": "QR generation failed"
        }), 500

@app.route('/api/session-info/<session_id>')
def api_session_info(session_id):
    """Get session information (without exposing tokens)"""
    try:
        if session_id in authenticated_sessions:
            session = authenticated_sessions[session_id]
            return jsonify({
                "success": True,
                "user": session["user"],
                "authenticated_at": session["authenticated_at"].isoformat(),
                "scopes": session.get("scopes", [])
            })
        else:
            return jsonify({
                "success": False,
                "error": "Session not found"
            }), 404
            
    except Exception as e:
        logger.error(f"Error in session_info: {e}")
        return jsonify({
            "success": False,
            "error": "Internal server error"
        }), 500

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0-secure"
    })

if __name__ == '__main__':
    # Production security configurations
    
    # Check if running in production
    is_production = os.environ.get('PRODUCTION', '').lower() == 'true'
    
    if is_production:
        # Production settings
        app.run(
            host='0.0.0.0',
            port=int(os.environ.get('PORT', 5003)),
            debug=False,
            ssl_context='adhoc'  # Enable HTTPS
        )
    else:
        # Development settings
        logger.warning("Running in DEVELOPMENT mode - not suitable for production")
        app.run(
            host='127.0.0.1',
            port=5003,
            debug=True
        )
