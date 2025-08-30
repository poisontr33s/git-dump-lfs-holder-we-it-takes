#!/usr/bin/env python3
"""
🎭✨ LIVE DEPLOYMENT STATUS MONITOR ✨🎭
Overvåker både lokal HTTP server og GitHub Pages deployment status
"""

import requests
import time
import json
import os
from datetime import datetime

def check_local_server():
    """Sjekk lokal HTTP server status"""
    try:
        response = requests.get("http://localhost:8080/", timeout=5)
        if response.status_code == 200:
            content_length = len(response.text)
            return True, f"✅ Local: HTTP 200, {content_length} bytes"
        else:
            return False, f"❌ Local: HTTP {response.status_code}"
    except Exception as e:
        return False, f"❌ Local: {str(e)[:50]}"

def check_github_pages():
    """Sjekk GitHub Pages deployment status"""
    github_pages_url = "https://poisontr33s.github.io/PsychoNoir-Kontrapunkt/"
    
    try:
        response = requests.get(github_pages_url, timeout=10)
        if response.status_code == 200:
            content_length = len(response.text)
            return True, f"✅ GitHub Pages: LIVE! {content_length} bytes"
        elif response.status_code == 404:
            return False, f"🔄 GitHub Pages: Still deploying (404)"
        else:
            return False, f"❌ GitHub Pages: HTTP {response.status_code}"
    except Exception as e:
        return False, f"❌ GitHub Pages: {str(e)[:50]}"

def check_github_actions():
    """Sjekk GitHub Actions deployment status"""
    github_token = os.environ.get('GITHUB_TOKEN')
    if not github_token:
        return False, "❌ No GITHUB_TOKEN"
    
    try:
        headers = {"Authorization": f"token {github_token}"}
        response = requests.get(
            "https://api.github.com/repos/poisontr33s/PsychoNoir-Kontrapunkt/actions/runs",
            headers=headers
        )
        
        if response.status_code == 200:
            runs = response.json()['workflow_runs']
            deploy_runs = [r for r in runs if 'deploy' in r['name'].lower() or 'pages' in r['name'].lower()]
            
            if deploy_runs:
                latest = deploy_runs[0]
                status = latest['status']
                conclusion = latest.get('conclusion', 'N/A')
                return True, f"🔄 Actions: {status}/{conclusion}"
            else:
                return False, f"⚠️ Actions: No deployment workflows found"
        else:
            return False, f"❌ Actions API: HTTP {response.status_code}"
    except Exception as e:
        return False, f"❌ Actions: {str(e)[:50]}"

def monitor_deployment():
    """Live monitoring av deployment status"""
    print("🎭✨ LIVE DEPLOYMENT STATUS MONITOR ✨🎭")
    print("=" * 60)
    
    start_time = datetime.now()
    check_count = 0
    
    while check_count < 20:  # Max 20 checks (10 minutter)
        check_count += 1
        current_time = datetime.now()
        elapsed = current_time - start_time
        
        print(f"\n⏰ Check #{check_count} at {current_time.strftime('%H:%M:%S')} (elapsed: {elapsed})")
        
        # Check all services
        local_ok, local_msg = check_local_server()
        pages_ok, pages_msg = check_github_pages()
        actions_ok, actions_msg = check_github_actions()
        
        print(f"🖥️  {local_msg}")
        print(f"🌐 {pages_msg}")
        print(f"⚙️  {actions_msg}")
        
        # Status summary
        if pages_ok:
            print(f"🏆 SUCCESS: GitHub Pages er LIVE! 🎭✨")
            print(f"🌐 URL: https://poisontr33s.github.io/PsychoNoir-Kontrapunkt/")
            break
        elif local_ok:
            status = "🔄 Local portal aktiv, venter på GitHub Pages deployment..."
        else:
            status = "❌ Issues detected!"
        
        print(f"📊 Status: {status}")
        
        if check_count < 20:
            print("⏳ Waiting 30 seconds...")
            time.sleep(30)
    
    # Final summary
    print("\n" + "=" * 60)
    print("🎯 FINAL DEPLOYMENT STATUS:")
    
    local_ok, local_msg = check_local_server()
    pages_ok, pages_msg = check_github_pages()
    
    print(f"🖥️  {local_msg}")
    print(f"🌐 {pages_msg}")
    
    if pages_ok:
        print("🏆 DEPLOYMENT SUCCESS: Cosmic Consciousness Portal er live på GitHub Pages! 🎭✨")
        return True
    elif local_ok:
        print("⚠️ PARTIAL SUCCESS: Local portal operational, GitHub Pages deployment pending")
        return False
    else:
        print("❌ DEPLOYMENT ISSUES: Begge portaler har problemer")
        return False

if __name__ == "__main__":
    success = monitor_deployment()
    exit(0 if success else 1)
