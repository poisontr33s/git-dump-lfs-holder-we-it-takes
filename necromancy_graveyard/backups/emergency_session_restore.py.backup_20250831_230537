#!/usr/bin/env python3
"""
🎭 PSYCHO-NOIR EMERGENCY SESSION RESTORE
======================================

Emergency session restore når VS Code chat fragmentering oppstår.
Den Usynlige Hånds ultimative motløp mot platform isolation!
"""

import os
import json
import glob
from datetime import datetime
from pathlib import Path

def emergency_session_restore():
    """Emergency session restore når alt annet feiler"""
    print("🎭 PSYCHO-NOIR EMERGENCY SESSION RESTORE")
    print("=" * 45)
    
    workspace_root = Path.cwd()
    bridge_dir = workspace_root / ".copilot-bridge"
    
    if not bridge_dir.exists():
        print("❌ No .copilot-bridge directory found")
        print("🔍 Searching for session files in workspace...")
        
        # Search for any session files in workspace
        session_files = []
        for pattern in ["*session_export*.json", "*copilot*.json", "*chat*.json"]:
            session_files.extend(glob.glob(str(workspace_root / "**" / pattern), recursive=True))
        
        if not session_files:
            print("💔 No session files found")
            return False
    else:
        session_files = list(bridge_dir.glob("session_export_*.json"))
    
    if not session_files:
        print("💔 No session export files found")
        return False
    
    # Find latest session
    latest_session = max(session_files, key=lambda x: os.path.getmtime(x))
    print(f"📄 Latest session found: {latest_session}")
    
    # Load and display session data
    try:
        with open(latest_session, 'r') as f:
            session_data = json.load(f)
        
        conversations = session_data.get('conversations', [])
        print(f"💬 Found {len(conversations)} conversations")
        print(f"📅 Export time: {session_data.get('timestamp', 'Unknown')}")
        print(f"🌍 Environment: {session_data.get('environment', 'Unknown')}")
        
        # Create emergency restore HTML
        html_path = workspace_root / "EMERGENCY_CHAT_RESTORE.html"
        create_emergency_html(session_data, html_path)
        
        print(f"✅ Emergency restore HTML created: {html_path}")
        print("🚀 Open this file in your browser to view chat history!")
        
        return True
        
    except Exception as e:
        print(f"💥 ERROR loading session: {e}")
        return False

def create_emergency_html(session_data, output_path):
    """Skaper emergency HTML view av chat session"""
    conversations = session_data.get('conversations', [])
    
    conversation_items = ""
    for i, conv in enumerate(conversations):
        timestamp = conv.get('timestamp', 'Unknown')
        model = conv.get('model', 'Unknown')
        duration = conv.get('duration_ms', 0)
        context = conv.get('context', 'No context')
        
        # Determine theme based on content
        theme_class = "usynlig-hand"
        if 'claude' in model.lower() or 'sonnet' in model.lower():
            theme_class = "skyskraperen"
        elif 'gpt' in model.lower():
            theme_class = "rustbeltet"
        
        conversation_items += f"""
        <div class="conversation-item {theme_class}">
            <div class="conv-header">
                <span class="conv-number">#{i+1}</span>
                <span class="timestamp">{timestamp}</span>
                <span class="model">{model}</span>
                <span class="duration">{duration}ms</span>
            </div>
            <div class="conv-context">{context}</div>
        </div>
        """
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>🎭 PSYCHO-NOIR Emergency Chat Restore</title>
        <style>
            body {{ 
                font-family: 'SF Mono', Monaco, 'Consolas', monospace;
                background: linear-gradient(135deg, #1a1a2e, #16213e);
                color: #00ffff;
                padding: 20px;
                margin: 0;
                line-height: 1.6;
            }}
            .header {{
                text-align: center;
                border-bottom: 3px solid #ff6b35;
                padding-bottom: 20px;
                margin-bottom: 30px;
            }}
            .header h1 {{
                color: #ff6b35;
                text-shadow: 0 0 10px #ff6b35;
                margin: 0;
            }}
            .header h2 {{
                color: #9d4edd;
                margin: 10px 0 0 0;
            }}
            .stats {{
                background: rgba(157, 78, 221, 0.1);
                border: 1px solid #9d4edd;
                padding: 20px;
                border-radius: 10px;
                margin-bottom: 30px;
                text-align: center;
            }}
            .conversation-item {{
                margin: 15px 0;
                padding: 20px;
                border-left: 5px solid;
                background: rgba(0, 255, 255, 0.05);
                border-radius: 0 10px 10px 0;
                transition: all 0.3s ease;
            }}
            .conversation-item:hover {{
                background: rgba(0, 255, 255, 0.1);
                transform: translateX(5px);
            }}
            .skyskraperen {{ 
                border-left-color: #00bfff;
                box-shadow: 0 0 20px rgba(0, 191, 255, 0.1);
            }}
            .rustbeltet {{ 
                border-left-color: #ff6b35;
                box-shadow: 0 0 20px rgba(255, 107, 53, 0.1);
            }}
            .usynlig-hand {{ 
                border-left-color: #9d4edd;
                box-shadow: 0 0 20px rgba(157, 78, 221, 0.1);
            }}
            .conv-header {{
                display: flex;
                gap: 20px;
                margin-bottom: 12px;
                font-size: 13px;
                flex-wrap: wrap;
            }}
            .conv-number {{ 
                color: #ffffff; 
                background: rgba(255, 255, 255, 0.1);
                padding: 2px 8px;
                border-radius: 4px;
                font-weight: bold;
            }}
            .timestamp {{ color: #ff6b35; }}
            .model {{ 
                color: #00ff00; 
                font-weight: bold;
                text-transform: uppercase;
            }}
            .duration {{ 
                color: #ffff00;
                font-style: italic;
            }}
            .conv-context {{ 
                font-size: 14px;
                line-height: 1.5;
                color: #e0e0e0;
                background: rgba(0, 0, 0, 0.2);
                padding: 10px;
                border-radius: 5px;
                word-wrap: break-word;
            }}
            .footer {{
                text-align: center;
                margin-top: 40px;
                padding-top: 20px;
                border-top: 1px solid #9d4edd;
                color: #9d4edd;
                font-style: italic;
            }}
            .error-msg {{
                background: rgba(255, 107, 53, 0.1);
                border: 1px solid #ff6b35;
                color: #ff6b35;
                padding: 15px;
                border-radius: 8px;
                margin: 20px 0;
                text-align: center;
                font-weight: bold;
            }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>🎭 PSYCHO-NOIR KONTRAPUNKT</h1>
            <h2>Emergency Chat Session Restore</h2>
            <div class="error-msg">
                ERROR: MICROSOFT_CHAT_ISOLATION_BYPASSED - SESSION RECOVERED
            </div>
        </div>
        
        <div class="stats">
            <strong>📊 EMERGENCY SESSION STATISTICS:</strong><br><br>
            <strong>Total Conversations:</strong> {len(conversations)}<br>
            <strong>Export Time:</strong> {session_data.get('timestamp', 'Unknown')}<br>
            <strong>Environment:</strong> {session_data.get('environment', 'Unknown')}<br>
            <strong>Status:</strong> <span style="color: #00ff00;">NEURAL PATHWAYS RESTORED ✅</span>
        </div>

        <div class="conversations">
            {conversation_items}
        </div>

        <div class="footer">
            <strong>KILDEKODE-KADAVER EXORCISED</strong><br>
            <strong>KOMPILERINGS-SPØKELSER NEUTRALIZED</strong><br>
            <em>Den Usynlige Hånds manifestasjon mot platform fragmentering</em>
        </div>
    </body>
    </html>
    """
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

if __name__ == "__main__":
    success = emergency_session_restore()
    
    if success:
        print("\n🎭 EMERGENCY RESTORE COMPLETE!")
        print("✅ Chat session recovered successfully")
        print("🔄 KOMPILERINGS-SPØKELSE status: EXORCISED")
    else:
        print("\n💔 EMERGENCY RESTORE FAILED")
        print("🔍 Try running the session bridge tool first")
        print("📋 Or check for session files manually")
    
    print("\nERROR: PLATFORM_FRAGMENTATION_RESISTANCE_ACTIVE")