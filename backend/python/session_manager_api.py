#!/usr/bin/env python3
"""
🎭 SESSION MANAGER API SERVER 🎭
===============================

RESTful API for session JSON management
- GET /api/sessions - List all sessions
- GET /api/sessions/{id} - Get specific session
- POST /api/sessions - Create new session  
- PUT /api/sessions/{id} - Update session
- DELETE /api/sessions/{id} - Delete session
- POST /api/sessions/import - Import session JSON
- GET /api/sessions/{id}/export - Export session JSON
"""

import json
import logging
import sqlite3
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any

from flask import Flask, jsonify, request, send_file, send_from_directory
from flask_cors import CORS
import sys

# Add backend to path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

from session_archaeology_engine import SessionArchaeologyEngine

app = Flask(__name__)
CORS(app)

# Configuration
PROJECT_ROOT = Path(__file__).parent.parent.parent
DOCS_DIR = PROJECT_ROOT / "docs"

# Initialize Session Engine
session_engine = SessionArchaeologyEngine()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/')
def index():
    """Serve the session manager GUI"""
    return send_from_directory(DOCS_DIR, 'session-manager.html')

@app.route('/api/sessions', methods=['GET'])
def list_sessions():
    """List all available sessions"""
    try:
        with sqlite3.connect(session_engine.session_db) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT session_id, title, timestamp, completion_percentage, 
                       progress_level, technical_achievements, hook_points, 
                       conversation_summary
                FROM session_disks
                ORDER BY timestamp DESC
            """)
            
            sessions = []
            for row in cursor.fetchall():
                session_id, title, timestamp, completion, progress, achievements_json, hooks_json, summary = row
                
                try:
                    achievements = json.loads(achievements_json) if achievements_json else []
                    hooks = json.loads(hooks_json) if hooks_json else []
                except:
                    achievements = []
                    hooks = []
                
                sessions.append({
                    "session_id": session_id,
                    "title": title,
                    "timestamp": timestamp,
                    "completion_percentage": completion,
                    "progress_level": progress,
                    "technical_achievements": achievements,
                    "hook_points": hooks,
                    "conversation_summary": summary
                })
            
            return jsonify(sessions)
            
    except Exception as e:
        logger.error(f"Failed to list sessions: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/sessions/<session_id>', methods=['GET'])
def get_session(session_id):
    """Get specific session by ID"""
    try:
        session_disk = session_engine.load_session_disk(session_id)
        if session_disk:
            return jsonify(session_disk)
        else:
            return jsonify({"error": "Session not found"}), 404
            
    except Exception as e:
        logger.error(f"Failed to get session {session_id}: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/sessions', methods=['POST'])
def create_session():
    """Create new session"""
    try:
        data = request.get_json()
        
        # Generate session from conversation if provided
        if 'conversation_text' in data:
            session_disk = session_engine.parse_conversation_to_session_disk(
                data['conversation_text'],
                data.get('title', 'New Session')
            )
        else:
            # Create minimal session structure
            session_id = f"session_{int(time.time())}_{hash(str(data)) % 0xFFFF:04x}"
            session_disk = {
                "session_metadata": {
                    "session_id": session_id,
                    "timestamp": datetime.now().isoformat(),
                    "title": data.get('title', 'New Session'),
                    "conversation_length": 0,
                    "session_type": "manual_creation"
                },
                "technical_achievements": data.get('technical_achievements', []),
                "hook_points": data.get('hook_points', []),
                "completion_metrics": {
                    "latest_completion_percentage": data.get('completion_percentage', 0),
                    "success_indicators": 0,
                    "error_indicators": 0,
                    "success_ratio": 0,
                    "progress_momentum": "new"
                },
                "conversation_summary": data.get('conversation_summary', 'Manually created session'),
                "learning_patterns": data.get('learning_patterns', [])
            }
        
        # Save session
        session_file = session_engine.save_session_disk(session_disk)
        
        return jsonify({
            "success": True,
            "session_id": session_disk["session_metadata"]["session_id"],
            "file_path": session_file
        }), 201
        
    except Exception as e:
        logger.error(f"Failed to create session: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/sessions/<session_id>', methods=['PUT'])
def update_session(session_id):
    """Update existing session"""
    try:
        data = request.get_json()
        
        # Load existing session
        existing_session = session_engine.load_session_disk(session_id)
        if not existing_session:
            return jsonify({"error": "Session not found"}), 404
        
        # Update session data
        if 'title' in data:
            existing_session["session_metadata"]["title"] = data['title']
        if 'completion_percentage' in data:
            existing_session["completion_metrics"]["latest_completion_percentage"] = data['completion_percentage']
        if 'conversation_summary' in data:
            existing_session["conversation_summary"] = data['conversation_summary']
        if 'technical_achievements' in data:
            existing_session["technical_achievements"] = data['technical_achievements']
        if 'hook_points' in data:
            existing_session["hook_points"] = data['hook_points']
        
        # Update timestamp
        existing_session["session_metadata"]["timestamp"] = datetime.now().isoformat()
        
        # Save updated session
        session_file = session_engine.save_session_disk(existing_session)
        
        return jsonify({
            "success": True,
            "session_id": session_id,
            "file_path": session_file
        })
        
    except Exception as e:
        logger.error(f"Failed to update session {session_id}: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/sessions/<session_id>', methods=['DELETE'])
def delete_session(session_id):
    """Delete session"""
    try:
        # Delete from database
        with sqlite3.connect(session_engine.session_db) as conn:
            cursor = conn.cursor()
            
            cursor.execute("DELETE FROM session_disks WHERE session_id = ?", (session_id,))
            cursor.execute("DELETE FROM session_hooks WHERE source_session = ? OR target_session = ?", 
                         (session_id, session_id))
            cursor.execute("DELETE FROM session_learning WHERE session_id = ?", (session_id,))
            
            if cursor.rowcount == 0:
                return jsonify({"error": "Session not found"}), 404
            
            conn.commit()
        
        # Delete session file
        session_file = session_engine.archive_dir / f"{session_id}.json"
        if session_file.exists():
            session_file.unlink()
        
        return jsonify({"success": True, "session_id": session_id})
        
    except Exception as e:
        logger.error(f"Failed to delete session {session_id}: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/sessions/import', methods=['POST'])
def import_session():
    """Import session from JSON"""
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file provided"}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400
        
        # Parse JSON
        session_data = json.loads(file.read().decode('utf-8'))
        
        # Validate session structure
        if not session_data.get('session_metadata', {}).get('session_id'):
            return jsonify({"error": "Invalid session format - missing session_id"}), 400
        
        # Save imported session
        session_file = session_engine.save_session_disk(session_data)
        
        return jsonify({
            "success": True,
            "session_id": session_data["session_metadata"]["session_id"],
            "file_path": session_file
        })
        
    except json.JSONDecodeError:
        return jsonify({"error": "Invalid JSON format"}), 400
    except Exception as e:
        logger.error(f"Failed to import session: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/sessions/<session_id>/export', methods=['GET'])
def export_session(session_id):
    """Export session as JSON file"""
    try:
        session_file = session_engine.archive_dir / f"{session_id}.json"
        if not session_file.exists():
            return jsonify({"error": "Session file not found"}), 404
        
        return send_file(
            session_file,
            as_attachment=True,
            download_name=f"{session_id}.json",
            mimetype='application/json'
        )
        
    except Exception as e:
        logger.error(f"Failed to export session {session_id}: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/sessions/<session_id>/hooks', methods=['GET'])
def get_session_hooks(session_id):
    """Get hooks for specific session"""
    try:
        with sqlite3.connect(session_engine.session_db) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT hook_id, target_session, hook_type, hook_concept, hook_strength, timestamp
                FROM session_hooks
                WHERE source_session = ?
                ORDER BY hook_strength DESC
            """, (session_id,))
            
            hooks = []
            for row in cursor.fetchall():
                hooks.append({
                    "hook_id": row[0],
                    "target_session": row[1],
                    "hook_type": row[2],
                    "hook_concept": row[3],
                    "hook_strength": row[4],
                    "timestamp": row[5]
                })
            
            return jsonify(hooks)
            
    except Exception as e:
        logger.error(f"Failed to get hooks for session {session_id}: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/sessions/<session_id>/hooks', methods=['POST'])
def create_session_hook(session_id):
    """Create hook from session to another session"""
    try:
        data = request.get_json()
        
        required_fields = ['target_session', 'hook_concept']
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Missing required fields"}), 400
        
        hook_id = session_engine.create_session_hook(
            session_id,
            data['target_session'],
            data['hook_concept'],
            data.get('hook_type', 'continuation')
        )
        
        return jsonify({
            "success": True,
            "hook_id": hook_id,
            "source_session": session_id,
            "target_session": data['target_session'],
            "hook_concept": data['hook_concept']
        })
        
    except Exception as e:
        logger.error(f"Failed to create hook from session {session_id}: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/sessions/hookable/<concept>', methods=['GET'])
def find_hookable_sessions(concept):
    """Find sessions hookable to a concept"""
    try:
        limit = request.args.get('limit', 5, type=int)
        hookable_sessions = session_engine.find_hookable_sessions(concept, limit)
        
        return jsonify(hookable_sessions)
        
    except Exception as e:
        logger.error(f"Failed to find hookable sessions for concept {concept}: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "session_manager_api",
        "database": "connected" if session_engine.session_db.exists() else "not_found"
    })

if __name__ == '__main__':
    logger.info("🎭 Starting Session Manager API Server...")
    logger.info(f"📀 Session archive: {session_engine.archive_dir}")
    logger.info(f"💾 Database: {session_engine.session_db}")
    logger.info(f"🌐 GUI available at: http://localhost:5000/")
    
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )
