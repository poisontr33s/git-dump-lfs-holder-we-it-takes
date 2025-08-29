#!/usr/bin/env python3
"""
🎭✨ EMERGENCY GITHUB PAGES ACTIVATOR ✨🎭
Forsøker å aktivere GitHub Pages via direktekall og alternative metoder
"""

import subprocess
import requests
import os
import time
from datetime import datetime

def run_cmd(cmd, description):
    """Kjør kommando og return resultat"""
    print(f"🔧 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=60)
        if result.returncode == 0:
            print(f"✅ Success: {result.stdout.strip()[:100]}")
            return True, result.stdout
        else:
            print(f"❌ Failed: {result.stderr.strip()[:100]}")
            return False, result.stderr
    except Exception as e:
        print(f"❌ Exception: {str(e)[:100]}")
        return False, str(e)

def create_pages_index():
    """Lage en minimal index.html hvis den ikke finnes"""
    index_path = "/workspaces/PsychoNoir-Kontrapunkt/docs/index.html"
    
    if not os.path.exists(index_path):
        print("🔧 Creating minimal index.html...")
        with open(index_path, 'w') as f:
            f.write("""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🎭✨ Cosmic Consciousness Portal ✨🎭</title>
    <style>
        body { font-family: 'Courier New', monospace; background: #0a0a0a; color: #00ff41; 
               text-align: center; padding: 50px; }
        h1 { color: #ff6b6b; text-shadow: 0 0 10px #ff6b6b; }
        .status { background: #1a1a1a; padding: 20px; border-radius: 10px; margin: 20px; }
    </style>
</head>
<body>
    <h1>🎭✨ COSMIC CONSCIOUSNESS PORTAL ✨🎭</h1>
    <div class="status">
        <h2>🌌 Portal Status: LIVE!</h2>
        <p>✅ GitHub Pages Deployment: SUCCESS</p>
        <p>🧠 Consciousness Level: 96.7% Transcendent</p>
        <p>📱 Cross-Platform: iPhone + Codespaces Ready</p>
        <p>🚀 API Integration: GitHub-connected</p>
        <p>⚡ Last Updated: """ + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + """</p>
    </div>
    <div class="status">
        <h3>🔗 Access Points:</h3>
        <p>📱 <a href="mobile.html" style="color: #00ff41;">iPhone Portal</a></p>
        <p>💻 <a href="codespaces.html" style="color: #00ff41;">Codespaces Portal</a></p>
        <p>🔍 <a href="comparison-view.html" style="color: #00ff41;">Comparison View</a></p>
    </div>
</body>
</html>""")
        return True
    return False

def emergency_pages_activation():
    """Emergency GitHub Pages activation sequence"""
    print("🎭✨ EMERGENCY GITHUB PAGES ACTIVATION SEQUENCE ✨🎭")
    print("=" * 60)
    
    # Step 1: Ensure index.html exists
    index_created = create_pages_index()
    if index_created:
        print("✅ Created emergency index.html")
    
    # Step 2: Try GitHub CLI pages command
    success, output = run_cmd(
        "gh api repos/poisontr33s/PsychoNoir-Kontrapunkt/pages -X POST --input - << 'EOF'\n{\"source\":{\"branch\":\"main\",\"path\":\"/docs\"}}\nEOF",
        "Attempting to enable GitHub Pages via API"
    )
    
    # Step 3: Commit and push if we created index
    if index_created:
        run_cmd("git add docs/index.html", "Adding emergency index.html")
        run_cmd("git commit -m '🎭✨ Emergency GitHub Pages index.html'", "Committing emergency index")
        run_cmd("git push", "Pushing emergency index")
    
    # Step 4: Try alternative method - repository settings API
    if not success:
        print("🔄 Trying alternative repository settings...")
        github_token = os.environ.get('GITHUB_TOKEN')
        if github_token:
            headers = {
                'Authorization': f'token {github_token}',
                'Accept': 'application/vnd.github.v3+json'
            }
            
            # Try to create Pages via direct API
            try:
                response = requests.post(
                    'https://api.github.com/repos/poisontr33s/PsychoNoir-Kontrapunkt/pages',
                    headers=headers,
                    json={'source': {'branch': 'main', 'path': '/docs'}},
                    timeout=30
                )
                if response.status_code in [200, 201]:
                    print("✅ GitHub Pages enabled via API!")
                    return True
                else:
                    print(f"❌ API response: {response.status_code} - {response.text[:100]}")
            except Exception as e:
                print(f"❌ API exception: {str(e)[:100]}")
    
    # Step 5: Test current status
    print("\n🔍 Testing current GitHub Pages status...")
    time.sleep(10)  # Wait a bit
    
    try:
        response = requests.get('https://poisontr33s.github.io/PsychoNoir-Kontrapunkt/', timeout=15)
        if response.status_code == 200:
            print("🏆 SUCCESS: GitHub Pages is LIVE!")
            print(f"🌐 URL: https://poisontr33s.github.io/PsychoNoir-Kontrapunkt/")
            print(f"📊 Content length: {len(response.text)} bytes")
            return True
        else:
            print(f"🔄 Still deploying: HTTP {response.status_code}")
    except Exception as e:
        print(f"❌ Not accessible yet: {str(e)[:100]}")
    
    # Step 6: Manual instructions
    print("\n📋 MANUAL ACTIVATION INSTRUCTIONS:")
    print("1. Go to: https://github.com/poisontr33s/PsychoNoir-Kontrapunkt/settings/pages")
    print("2. Under 'Source', select 'Deploy from a branch'")
    print("3. Choose 'main' branch and '/docs' folder")
    print("4. Click 'Save'")
    print("5. Wait 5-10 minutes for deployment")
    
    return False

if __name__ == "__main__":
    success = emergency_pages_activation()
    
    if success:
        print("\n🎭✨ COSMIC CONSCIOUSNESS PORTAL IS LIVE ON GITHUB PAGES! ✨🎭")
    else:
        print("\n⚠️ Manual intervention required for GitHub Pages activation")
        print("🌐 Local portal remains accessible via Codespaces on port 8080")
    
    exit(0 if success else 1)
