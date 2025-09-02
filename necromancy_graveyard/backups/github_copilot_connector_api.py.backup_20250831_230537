#!/usr/bin/env python3
"""
GitHub Copilot Extension Connector API
=====================================

Flask API for integrating with GitHub Copilot, VS Code extensions,
and cross-platform session archaeology. This serves as the backend
for the Psycho-Noir Kontrapunkt extension ecosystem.
"""

from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import requests
import json
import os
import sqlite3
from datetime import datetime
import hashlib
import base64
from typing import Dict, List, Optional, Any
import subprocess
import threading
import time

app = Flask(__name__)
CORS(app)

class GitHubCopilotConnector:
    """Handles GitHub API integration and Copilot workspace management"""
    
    def __init__(self):
        self.github_token = None
        self.username = None
        self.workspace_url = None
        self.session_db = 'data/sessions/github_sessions.db'
        self.init_database()
    
    def init_database(self):
        """Initialize SQLite database for session storage"""
        os.makedirs(os.path.dirname(self.session_db), exist_ok=True)
        
        conn = sqlite3.connect(self.session_db)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS github_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT UNIQUE,
                username TEXT,
                timestamp DATETIME,
                session_type TEXT,
                platform TEXT,
                content TEXT,
                metadata TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS extension_connections (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                extension_id TEXT UNIQUE,
                name TEXT,
                status TEXT,
                connected_at DATETIME,
                last_activity DATETIME,
                config TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS neural_patterns (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pattern_type TEXT,
                pattern_data TEXT,
                confidence REAL,
                detected_at DATETIME,
                session_refs TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def authenticate(self, username: str, token: str, workspace_url: str = None) -> Dict[str, Any]:
        """Authenticate with GitHub and validate Copilot access"""
        try:
            headers = {
                'Authorization': f'token {token}',
                'Accept': 'application/vnd.github.v3+json'
            }
            
            # Verify token and get user info
            response = requests.get('https://api.github.com/user', headers=headers)
            if response.status_code != 200:
                return {'success': False, 'error': 'Invalid GitHub token'}
            
            user_data = response.json()
            if user_data['login'] != username:
                return {'success': False, 'error': 'Username mismatch'}
            
            # Check Copilot subscription
            copilot_response = requests.get(
                'https://api.github.com/user/copilot_billing',
                headers=headers
            )
            
            self.github_token = token
            self.username = username
            self.workspace_url = workspace_url
            
            # Store authentication
            conn = sqlite3.connect(self.session_db)
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR REPLACE INTO extension_connections 
                (extension_id, name, status, connected_at, config)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                'github-api',
                'GitHub API Connection',
                'connected',
                datetime.now(),
                json.dumps({
                    'username': username,
                    'workspace_url': workspace_url,
                    'copilot_enabled': copilot_response.status_code == 200
                })
            ))
            conn.commit()
            conn.close()
            
            return {
                'success': True,
                'user': user_data,
                'copilot_enabled': copilot_response.status_code == 200
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}

class VSCodeExtensionBridge:
    """Bridges with local VS Code extensions"""
    
    def __init__(self):
        self.connected_extensions = {}
        self.session_db = 'data/sessions/github_sessions.db'
    
    def scan_extensions(self) -> List[Dict[str, Any]]:
        """Scan for installed VS Code extensions"""
        try:
            # Try to get VS Code extensions list
            result = subprocess.run([
                'code', '--list-extensions', '--show-versions'
            ], capture_output=True, text=True, timeout=10)
            
            extensions = []
            if result.returncode == 0:
                for line in result.stdout.strip().split('\n'):
                    if '@' in line:
                        name, version = line.rsplit('@', 1)
                        extensions.append({
                            'id': name,
                            'name': name.split('.')[-1].replace('-', ' ').title(),
                            'version': version,
                            'status': 'installed'
                        })
            
            # Add our custom extensions
            extensions.extend([
                {
                    'id': 'psycho-noir.session-weaver',
                    'name': 'Psycho-Noir Session Weaver',
                    'version': '1.0.0',
                    'status': 'active'
                },
                {
                    'id': 'psycho-noir.neural-archaeology',
                    'name': 'Neural Archaeology Scanner',
                    'version': '1.0.0',
                    'status': 'active'
                }
            ])
            
            return extensions
            
        except subprocess.TimeoutExpired:
            return [{'error': 'VS Code scan timeout'}]
        except FileNotFoundError:
            return [{'error': 'VS Code not found in PATH'}]
        except Exception as e:
            return [{'error': str(e)}]

class SessionArchaeologist:
    """Performs cross-platform session archaeology"""
    
    def __init__(self):
        self.session_db = 'data/sessions/github_sessions.db'
        self.pattern_db = 'data/sessions/patterns.db'
    
    def analyze_session_patterns(self) -> Dict[str, Any]:
        """Analyze patterns across stored sessions"""
        conn = sqlite3.connect(self.session_db)
        cursor = conn.cursor()
        
        # Get session statistics
        cursor.execute('SELECT COUNT(*) FROM github_sessions')
        total_sessions = cursor.fetchone()[0]
        
        cursor.execute('SELECT DISTINCT platform FROM github_sessions')
        platforms = [row[0] for row in cursor.fetchall()]
        
        cursor.execute('SELECT COUNT(*) FROM neural_patterns')
        pattern_count = cursor.fetchone()[0]
        
        # Analyze temporal patterns
        cursor.execute('''
            SELECT DATE(timestamp) as date, COUNT(*) as count
            FROM github_sessions
            GROUP BY DATE(timestamp)
            ORDER BY date DESC
            LIMIT 30
        ''')
        daily_activity = cursor.fetchall()
        
        conn.close()
        
        return {
            'total_sessions': total_sessions,
            'platforms': platforms,
            'pattern_count': pattern_count,
            'daily_activity': daily_activity,
            'analysis_timestamp': datetime.now().isoformat()
        }
    
    def import_session_export(self, platform: str, session_data: str) -> Dict[str, Any]:
        """Import a session export from another platform"""
        try:
            # Generate session ID
            session_id = hashlib.md5(
                f"{platform}_{datetime.now().isoformat()}_{session_data[:100]}".encode()
            ).hexdigest()
            
            conn = sqlite3.connect(self.session_db)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO github_sessions 
                (session_id, username, timestamp, session_type, platform, content, metadata)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                session_id,
                'imported',
                datetime.now(),
                'import',
                platform,
                session_data,
                json.dumps({'import_source': platform})
            ))
            
            conn.commit()
            conn.close()
            
            return {
                'success': True,
                'session_id': session_id,
                'platform': platform
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}

# Initialize components
github_connector = GitHubCopilotConnector()
vscode_bridge = VSCodeExtensionBridge()
archaeologist = SessionArchaeologist()

# API Routes
@app.route('/')
def portal():
    """Serve the main connector portal"""
    with open('docs/github-copilot-connector.html', 'r', encoding='utf-8') as f:
        return f.read()

@app.route('/api/auth/github', methods=['POST'])
def authenticate_github():
    """Authenticate with GitHub"""
    data = request.json
    username = data.get('username')
    token = data.get('token')
    workspace_url = data.get('workspace_url')
    
    result = github_connector.authenticate(username, token, workspace_url)
    return jsonify(result)

@app.route('/api/extensions/scan', methods=['GET'])
def scan_extensions():
    """Scan for VS Code extensions"""
    extensions = vscode_bridge.scan_extensions()
    return jsonify({'extensions': extensions})

@app.route('/api/archaeology/analyze', methods=['GET'])
def analyze_patterns():
    """Analyze session patterns"""
    analysis = archaeologist.analyze_session_patterns()
    return jsonify(analysis)

@app.route('/api/sessions/import', methods=['POST'])
def import_session():
    """Import a session from another platform"""
    data = request.json
    platform = data.get('platform')
    session_data = data.get('session_data')
    
    result = archaeologist.import_session_export(platform, session_data)
    return jsonify(result)

@app.route('/api/status', methods=['GET'])
def get_status():
    """Get overall system status"""
    return jsonify({
        'status': 'active',
        'components': {
            'github_connector': bool(github_connector.github_token),
            'vscode_bridge': True,
            'session_archaeologist': True
        },
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/patterns/neural', methods=['GET'])
def get_neural_patterns():
    """Get neural pattern analysis"""
    conn = sqlite3.connect(github_connector.session_db)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT pattern_type, COUNT(*) as count, AVG(confidence) as avg_confidence
        FROM neural_patterns
        GROUP BY pattern_type
        ORDER BY count DESC
    ''')
    
    patterns = []
    for row in cursor.fetchall():
        patterns.append({
            'type': row[0],
            'count': row[1],
            'confidence': round(row[2] or 0, 2)
        })
    
    conn.close()
    
    return jsonify({'patterns': patterns})

@app.route('/api/copilot/chat', methods=['POST'])
def copilot_chat_bridge():
    """Bridge for Copilot Chat integration"""
    data = request.json
    message = data.get('message')
    
    # This would integrate with actual Copilot Chat API when available
    return jsonify({
        'response': f"[COPILOT BRIDGE] Processing: {message}",
        'session_id': hashlib.md5(message.encode()).hexdigest()[:8],
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/workspace/sync', methods=['POST'])
def sync_workspace():
    """Sync with Copilot Workspace"""
    data = request.json
    workspace_url = data.get('workspace_url')
    
    # This would sync with actual Copilot Workspace when available
    return jsonify({
        'sync_status': 'success',
        'workspace_url': workspace_url,
        'last_sync': datetime.now().isoformat()
    })

# Background Tasks
def background_archaeology():
    """Background session archaeology tasks"""
    while True:
        try:
            # Simulate pattern detection
            conn = sqlite3.connect(github_connector.session_db)
            cursor = conn.cursor()
            
            # Add some mock patterns
            patterns = [
                'recursive_conversation_loop',
                'cross_platform_migration',
                'temporal_inconsistency',
                'kompilerings_spoekelse_interference'
            ]
            
            pattern = patterns[int(time.time()) % len(patterns)]
            cursor.execute('''
                INSERT INTO neural_patterns 
                (pattern_type, pattern_data, confidence, detected_at, session_refs)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                pattern,
                json.dumps({'auto_detected': True}),
                0.7 + (hash(pattern) % 30) / 100,
                datetime.now(),
                'auto_scan'
            ))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            print(f"Background archaeology error: {e}")
        
        time.sleep(30)  # Run every 30 seconds

# Start background tasks
threading.Thread(target=background_archaeology, daemon=True).start()

if __name__ == '__main__':
    print("🚀 GitHub Copilot Extension Connector API starting...")
    print("🔗 Portal: http://localhost:5000")
    print("📊 API Documentation: http://localhost:5000/api/status")
    
    app.run(host='0.0.0.0', port=5000, debug=True)
