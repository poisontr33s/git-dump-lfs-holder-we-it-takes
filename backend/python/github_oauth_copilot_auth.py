#!/usr/bin/env python3
"""
GitHub OAuth Copilot-Style Authentication API
===========================================

Implements GitHub OAuth flow identical to VS Code Copilot authentication:
1. Generate device code
2. User opens GitHub on mobile/browser
3. Enters device code
4. Automatic authentication completion
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

app = Flask(__name__)
CORS(app)

# GitHub OAuth App Configuration (you'll need to create this on GitHub)
GITHUB_CLIENT_ID = "your_github_app_client_id"  # Replace with actual Client ID
GITHUB_CLIENT_SECRET = "your_github_app_client_secret"  # Replace with actual Client Secret

# Device flow storage
device_flows = {}
authenticated_sessions = {}

class GitHubOAuthDeviceFlow:
    """
    Implements GitHub Device Flow authentication exactly like VS Code Copilot
    """

    def __init__(self):
        self.base_url = "https://github.com"
        self.api_url = "https://api.github.com"

    def start_device_flow(self, scopes=None):
        """
        Start GitHub Device Flow - same as VS Code Copilot authentication
        Returns device_code and user_code for mobile authentication
        """
        if scopes is None:
            scopes = ["user:email", "read:user", "repo"]

        # GitHub Device Flow Step 1: Request device and user codes
        response = requests.post(
            f"{self.base_url}/login/device/code",
            headers={
                "Accept": "application/json",
                "User-Agent": "PsychoNoir-Kontrapunkt/1.0"
            },
            data={
                "client_id": GITHUB_CLIENT_ID,
                "scope": " ".join(scopes)
            }
        )

        if response.status_code == 200:
            data = response.json()

            # Store device flow data
            flow_id = secrets.token_urlsafe(16)
            device_flows[flow_id] = {
                "device_code": data["device_code"],
                "user_code": data["user_code"],
                "verification_uri": data["verification_uri"],
                "verification_uri_complete": data.get("verification_uri_complete"),
                "expires_in": data["expires_in"],
                "interval": data["interval"],
                "created_at": datetime.now(),
                "status": "pending"
            }

            return {
                "success": True,
                "flow_id": flow_id,
                "user_code": data["user_code"],
                "verification_uri": data["verification_uri"],
                "verification_uri_complete": data.get("verification_uri_complete"),
                "expires_in": data["expires_in"],
                "interval": data["interval"]
            }
        else:
            return {
                "success": False,
                "error": f"GitHub API error: {response.status_code}",
                "details": response.text
            }

    def poll_for_token(self, flow_id):
        """
        Poll GitHub for authentication completion
        """
        if flow_id not in device_flows:
            return {"success": False, "error": "Invalid flow ID"}

        flow_data = device_flows[flow_id]

        # Check if expired
        if datetime.now() > flow_data["created_at"] + timedelta(seconds=flow_data["expires_in"]):
            device_flows[flow_id]["status"] = "expired"
            return {"success": False, "error": "Device flow expired"}

        # Poll GitHub for token
        response = requests.post(
            f"{self.base_url}/login/oauth/access_token",
            headers={
                "Accept": "application/json",
                "User-Agent": "PsychoNoir-Kontrapunkt/1.0"
            },
            data={
                "client_id": GITHUB_CLIENT_ID,
                "device_code": flow_data["device_code"],
                "grant_type": "urn:ietf:params:oauth:grant-type:device_code"
            }
        )

        if response.status_code == 200:
            data = response.json()

            if "access_token" in data:
                # Authentication successful!
                device_flows[flow_id]["status"] = "completed"
                device_flows[flow_id]["access_token"] = data["access_token"]
                device_flows[flow_id]["token_type"] = data.get("token_type", "bearer")
                device_flows[flow_id]["scope"] = data.get("scope", "")

                # Get user information
                user_info = self.get_user_info(data["access_token"])
                device_flows[flow_id]["user"] = user_info

                # Store in authenticated sessions
                session_id = secrets.token_urlsafe(32)
                authenticated_sessions[session_id] = {
                    "access_token": data["access_token"],
                    "user": user_info,
                    "authenticated_at": datetime.now(),
                    "flow_id": flow_id
                }

                return {
                    "success": True,
                    "status": "completed",
                    "session_id": session_id,
                    "access_token": data["access_token"],
                    "user": user_info
                }

            elif data.get("error") == "authorization_pending":
                return {"success": True, "status": "pending"}

            elif data.get("error") == "slow_down":
                return {"success": True, "status": "slow_down"}

            elif data.get("error") == "expired_token":
                device_flows[flow_id]["status"] = "expired"
                return {"success": False, "error": "Device code expired"}

            elif data.get("error") == "access_denied":
                device_flows[flow_id]["status"] = "denied"
                return {"success": False, "error": "User denied access"}

            else:
                return {"success": False, "error": f"Unknown error: {data}"}

        else:
            return {"success": False, "error": f"GitHub API error: {response.status_code}"}

    def get_user_info(self, access_token):
        """Get user information from GitHub API"""
        response = requests.get(
            f"{self.api_url}/user",
            headers={
                "Authorization": f"token {access_token}",
                "Accept": "application/vnd.github.v3+json",
                "User-Agent": "PsychoNoir-Kontrapunkt/1.0"
            }
        )

        if response.status_code == 200:
            return response.json()
        else:
            return {"error": "Failed to get user info"}

    def check_copilot_access(self, access_token):
        """Check if user has GitHub Copilot access"""
        response = requests.get(
            f"{self.api_url}/user/copilot_billing",
            headers={
                "Authorization": f"token {access_token}",
                "Accept": "application/vnd.github.v3+json",
                "User-Agent": "PsychoNoir-Kontrapunkt/1.0"
            }
        )

        return response.status_code == 200

# Initialize OAuth handler
oauth_handler = GitHubOAuthDeviceFlow()

@app.route('/')
def oauth_portal():
    """Main OAuth portal page"""
    return render_template_string("""
<!DOCTYPE html>
<html lang="no">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GitHub Copilot OAuth Authentication</title>
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

        .github-logo {
            width: 64px;
            height: 64px;
            margin: 0 auto 20px;
            background: #f0f6fc;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 32px;
            color: #0d1117;
        }

        h1 {
            font-size: 28px;
            margin-bottom: 10px;
            color: #f0f6fc;
        }

        .subtitle {
            color: #8b949e;
            margin-bottom: 30px;
            font-size: 16px;
        }

        .auth-status {
            padding: 20px;
            border-radius: 12px;
            margin-bottom: 20px;
            border: 1px solid #30363d;
        }

        .status-waiting {
            background: rgba(248, 149, 25, 0.1);
            border-color: #f89519;
        }

        .status-success {
            background: rgba(35, 134, 54, 0.1);
            border-color: #238636;
        }

        .status-error {
            background: rgba(248, 81, 73, 0.1);
            border-color: #f85149;
        }

        .device-code {
            font-family: 'SF Mono', 'Monaco', monospace;
            font-size: 24px;
            font-weight: bold;
            letter-spacing: 4px;
            margin: 20px 0;
            padding: 15px;
            background: rgba(13, 17, 23, 0.8);
            border-radius: 8px;
            border: 2px dashed #30363d;
            color: #58a6ff;
        }

        .btn {
            background: linear-gradient(135deg, #238636 0%, #2ea043 100%);
            border: none;
            border-radius: 12px;
            padding: 16px 32px;
            color: white;
            font-weight: 600;
            font-size: 16px;
            cursor: pointer;
            transition: all 0.3s ease;
            margin: 10px;
            text-decoration: none;
            display: inline-block;
        }

        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(35, 134, 54, 0.4);
        }

        .btn-mobile {
            background: linear-gradient(135deg, #1f6feb 0%, #58a6ff 100%);
        }

        .qr-code {
            margin: 20px auto;
            max-width: 200px;
            padding: 10px;
            background: white;
            border-radius: 8px;
        }

        .instructions {
            background: rgba(13, 17, 23, 0.6);
            border-radius: 8px;
            padding: 20px;
            margin: 20px 0;
            text-align: left;
        }

        .step {
            margin: 10px 0;
            padding-left: 20px;
            position: relative;
        }

        .step::before {
            content: "→";
            position: absolute;
            left: 0;
            color: #58a6ff;
            font-weight: bold;
        }

        .spinner {
            display: inline-block;
            width: 20px;
            height: 20px;
            border: 3px solid #30363d;
            border-radius: 50%;
            border-top-color: #58a6ff;
            animation: spin 1s ease-in-out infinite;
            margin-right: 10px;
        }

        @keyframes spin {
            to { transform: rotate(360deg); }
        }

        .user-info {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 15px;
            margin: 20px 0;
        }

        .avatar {
            width: 48px;
            height: 48px;
            border-radius: 50%;
            border: 2px solid #30363d;
        }
    </style>
</head>
<body>
    <div class="oauth-container">
        <div class="github-logo">🐙</div>
        <h1>GitHub Copilot Authentication</h1>
        <p class="subtitle">Akkurat som VS Code - bruk GitHub mobilappen!</p>

        <div id="auth-status" class="auth-status status-waiting" style="display: none;">
            <div id="status-content"></div>
        </div>

        <div id="device-code-section" style="display: none;">
            <div class="instructions">
                <div class="step">Åpne GitHub mobilappen eller gå til github.com/login/device</div>
                <div class="step">Skriv inn denne koden:</div>
            </div>

            <div id="device-code" class="device-code"></div>

            <div class="instructions">
                <div class="step">Eller skann QR-koden:</div>
            </div>

            <div id="qr-code" class="qr-code" style="display: none;"></div>

            <a id="mobile-link" class="btn btn-mobile" target="_blank" style="display: none;">
                📱 Åpne i GitHub Mobilapp
            </a>
        </div>

        <div id="success-section" style="display: none;">
            <div class="auth-status status-success">
                <div id="success-content"></div>
            </div>
            <div id="user-info" class="user-info"></div>
            <button class="btn" onclick="proceedToCopilot()">🚀 Fortsett til Copilot Portal</button>
        </div>

        <button id="start-auth" class="btn" onclick="startAuthentication()">
            🔐 Start GitHub Authentication
        </button>

        <div id="error-section" style="display: none;">
            <div class="auth-status status-error">
                <div id="error-content"></div>
            </div>
            <button class="btn" onclick="retryAuthentication()">🔄 Prøv Igjen</button>
        </div>
    </div>

    <script>
        let currentFlowId = null;
        let pollInterval = null;

        async function startAuthentication() {
            const startBtn = document.getElementById('start-auth');
            startBtn.style.display = 'none';

            const statusDiv = document.getElementById('auth-status');
            const statusContent = document.getElementById('status-content');

            statusDiv.style.display = 'block';
            statusDiv.className = 'auth-status status-waiting';
            statusContent.innerHTML = '<div class="spinner"></div>Starter GitHub Device Flow...';

            try {
                const response = await fetch('/api/oauth/start', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' }
                });

                const data = await response.json();

                if (data.success) {
                    currentFlowId = data.flow_id;
                    showDeviceCode(data);
                    startPolling();
                } else {
                    showError(data.error);
                }
            } catch (error) {
                showError('Nettverksfeil: ' + error.message);
            }
        }

        function showDeviceCode(data) {
            const statusContent = document.getElementById('status-content');
            const deviceCodeSection = document.getElementById('device-code-section');
            const deviceCodeDiv = document.getElementById('device-code');
            const mobileLink = document.getElementById('mobile-link');

            statusContent.innerHTML = '<div class="spinner"></div>Venter på autentisering...';
            deviceCodeSection.style.display = 'block';
            deviceCodeDiv.textContent = data.user_code;

            if (data.verification_uri_complete) {
                mobileLink.href = data.verification_uri_complete;
                mobileLink.style.display = 'inline-block';

                // Generate QR code for mobile convenience
                generateQRCode(data.verification_uri_complete);
            }
        }

        function generateQRCode(url) {
            // For simplicity, we'll use a QR code service
            const qrDiv = document.getElementById('qr-code');
            qrDiv.innerHTML = `<img src="https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=${encodeURIComponent(url)}" alt="QR Code">`;
            qrDiv.style.display = 'block';
        }

        function startPolling() {
            pollInterval = setInterval(async () => {
                try {
                    const response = await fetch(`/api/oauth/poll/${currentFlowId}`);
                    const data = await response.json();

                    if (data.success && data.status === 'completed') {
                        clearInterval(pollInterval);
                        showSuccess(data);
                    } else if (!data.success) {
                        clearInterval(pollInterval);
                        showError(data.error);
                    }
                    // Continue polling for 'pending' and 'slow_down' statuses
                } catch (error) {
                    clearInterval(pollInterval);
                    showError('Polling error: ' + error.message);
                }
            }, 5000); // Poll every 5 seconds
        }

        function showSuccess(data) {
            document.getElementById('auth-status').style.display = 'none';
            document.getElementById('device-code-section').style.display = 'none';

            const successSection = document.getElementById('success-section');
            const successContent = document.getElementById('success-content');
            const userInfo = document.getElementById('user-info');

            successSection.style.display = 'block';
            successContent.innerHTML = '✅ GitHub autentisering vellykket!';

            if (data.user && data.user.login) {
                userInfo.innerHTML = `
                    <img src="${data.user.avatar_url}" alt="Avatar" class="avatar">
                    <div>
                        <div style="font-weight: bold;">${data.user.name || data.user.login}</div>
                        <div style="color: #8b949e;">@${data.user.login}</div>
                    </div>
                `;
            }

            // Store session for redirect
            localStorage.setItem('github_session_id', data.session_id);
        }

        function showError(error) {
            document.getElementById('auth-status').style.display = 'none';
            document.getElementById('device-code-section').style.display = 'none';

            const errorSection = document.getElementById('error-section');
            const errorContent = document.getElementById('error-content');

            errorSection.style.display = 'block';
            errorContent.textContent = error;
        }

        function retryAuthentication() {
            location.reload();
        }

        function proceedToCopilot() {
            const sessionId = localStorage.getItem('github_session_id');
            if (sessionId) {
                window.location.href = `/copilot-portal?session=${sessionId}`;
            } else {
                window.location.href = '/copilot-portal';
            }
        }
    </script>
</body>
</html>
    """)

@app.route('/api/oauth/start', methods=['POST'])
def start_oauth_flow():
    """Start GitHub Device Flow"""
    result = oauth_handler.start_device_flow()
    return jsonify(result)

@app.route('/api/oauth/poll/<flow_id>')
def poll_oauth_status(flow_id):
    """Poll for OAuth completion"""
    result = oauth_handler.poll_for_token(flow_id)
    return jsonify(result)

@app.route('/api/oauth/status/<session_id>')
def get_oauth_status(session_id):
    """Get current authentication status"""
    if session_id in authenticated_sessions:
        session = authenticated_sessions[session_id]
        return jsonify({
            "authenticated": True,
            "user": session["user"],
            "authenticated_at": session["authenticated_at"].isoformat()
        })
    else:
        return jsonify({"authenticated": False})

@app.route('/copilot-portal')
def copilot_portal():
    """Redirect to main Copilot portal after authentication"""
    session_id = request.args.get('session')

    if session_id and session_id in authenticated_sessions:
        # User is authenticated, show the full portal
        return redirect('http://127.0.0.1:5001')
    else:
        # Not authenticated, redirect back to OAuth
        return redirect('/')

@app.route('/api/github/user/<session_id>')
def get_github_user(session_id):
    """Get GitHub user info for authenticated session"""
    if session_id not in authenticated_sessions:
        return jsonify({"error": "Not authenticated"}), 401

    session = authenticated_sessions[session_id]

    # Check Copilot access
    has_copilot = oauth_handler.check_copilot_access(session["access_token"])

    return jsonify({
        "user": session["user"],
        "has_copilot": has_copilot,
        "access_token": session["access_token"]  # In production, don't expose this
    })

if __name__ == '__main__':

    app.run(host='0.0.0.0', port=5002, debug=True)
