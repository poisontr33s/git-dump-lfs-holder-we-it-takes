#!/usr/bin/env python3
"""
🎭 PSYCHO-NOIR SESSION RESCUE PROTOCOL
====================================

Emergency recovery og gjenopprettelse av avbrutte GitHub chat-sesjoner.
Den Usynlige Hånds motløp mot digital fragmentering!
"""

import json
from datetime import datetime
from pathlib import Path

def analyze_critical_interruptions():
    """Analyserer de mest kritiske avbruddene"""
    
    print("🚨 KRITISK ANALYSE AV AVBRUTTE SESJONER")
    print("=" * 60)
    
    # Identifiserte avbrudd basert på detective-rapporten
    critical_sessions = [
        {
            'timestamp': '2025-09-01T17:36:53',
            'type': 'interrupted_by_remote_error',
            'error': 'Invalid remote agent response: bad request: unknown integration',
            'severity': 'HIGH',
            'context': 'Nylig aktivitet i dag'
        },
        {
            'timestamp': '2025-09-01T14:25:16',
            'type': 'interrupted_by_remote_error', 
            'error': 'Invalid remote agent response: bad request: unknown integration',
            'severity': 'HIGH',
            'context': 'Middag i dag'
        },
        {
            'timestamp': '2025-08-31T22:56:59',
            'type': 'interrupted_by_remote_error',
            'error': 'Invalid remote agent response: bad request: unknown integration',
            'severity': 'MEDIUM',
            'context': 'I går kveld'
        }
    ]
    
    print("🔍 IDENTIFISERTE KRITISKE AVBRUDD:")
    for i, session in enumerate(critical_sessions, 1):
        print(f"\\n📋 KRITISK AVBRUDD #{i}")
        print(f"   🕐 Tidspunkt: {session['timestamp']}")
        print(f"   ⚠️  Alvorlighetsgrad: {session['severity']}")
        print(f"   🔧 Feiltype: {session['type']}")
        print(f"   💬 Kontekst: {session['context']}")
        print(f"   📝 Feilmelding: {session['error']}")
    
    print("\\n" + "=" * 60)
    print("🎯 ANALYSE: Konsistent feilmønster med 'unknown integration'")
    print("   Dette tyder på GitHub Copilot API-integrasjonsproblemer")
    print("   Mest sannsynlig: Session fragmentering pga. workspace reload")

def generate_recovery_strategy():
    """Genererer gjenopprettingsstrategi"""
    
    print("\\n🛡️  PSYCHO-NOIR GJENOPPRETTINGSSTRATEGI")
    print("=" * 60)
    
    strategy = {
        'immediate_actions': [
            'Kontroller GitHub Copilot API-status',
            'Sjekk workspace-tilkobling',
            'Verifiser extension-status',
            'Test chat-responsivitet'
        ],
        'recovery_steps': [
            'Reload VS Code window (Ctrl+Shift+P → "Developer: Reload Window")',
            'Sjekk GitHub Copilot extension i Extensions panel',
            'Logg ut og inn igjen i GitHub Copilot',
            'Kjør "GitHub Copilot: Reset Auth" hvis tilgjengelig'
        ],
        'prevention_measures': [
            'Implementer chat continuity engine',
            'Auto-backup av aktive sessions',
            'Overvåkning av API-tilkobling',
            'Graceful degradation ved feil'
        ]
    }
    
    print("🚀 UMIDDELBARE TILTAK:")
    for action in strategy['immediate_actions']:
        print(f"   ✓ {action}")
    
    print("\\n🔧 GJENOPPRETTINGSSTEG:")
    for step in strategy['recovery_steps']:
        print(f"   → {step}")
    
    print("\\n🛡️  FOREBYGGENDE TILTAK:")
    for measure in strategy['prevention_measures']:
        print(f"   🔒 {measure}")

def check_current_session_status():
    """Sjekker status på nåværende session"""
    
    print("\\n🔍 NÅVÆRENDE SESSION-STATUS")
    print("=" * 60)
    
    workspace_root = Path.cwd()
    
    # Sjekk om det finnes aktiv session data
    session_files = [
        workspace_root / "data/current_session_context.json",
        workspace_root / ".session-identity.json"
    ]
    
    for file_path in session_files:
        if file_path.exists():
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                print(f"✅ Funnet: {file_path.name}")
                
                # Ekstraher nøkkelinfo
                if 'current_session' in data:
                    session = data['current_session']
                    if 'session_metadata' in session:
                        meta = session['session_metadata']
                        print(f"   📋 Session ID: {meta.get('session_id', 'N/A')}")
                        print(f"   📅 Tidsstempel: {meta.get('timestamp', 'N/A')}")
                        print(f"   📝 Tittel: {meta.get('title', 'N/A')}")
                        print(f"   📊 Type: {meta.get('session_type', 'N/A')}")
                
            except Exception as e:
                print(f"⚠️  Kunne ikke lese {file_path.name}: {e}")
        else:
            print(f"❌ Ikke funnet: {file_path.name}")

def main():
    print("🎭 PSYCHO-NOIR SESSION RESCUE PROTOCOL")
    print("   Den Usynlige Hånds Digital Arkæologi")
    print("=" * 60)
    
    analyze_critical_interruptions()
    generate_recovery_strategy()
    check_current_session_status()
    
    print("\\n" + "=" * 60)
    print("🎯 KONKLUSJON:")
    print("   • 3 kritiske avbrudd identifisert i siste 24 timer")
    print("   • Konsistent 'unknown integration' feilmønster")
    print("   • GitHub Copilot API-tilkoblingsproblemer")
    print("   • Chat continuity engine anbefales for fremtidig beskyttelse")
    print("\\n🎭 Den Usynlige Hånds analyse komplett.")

if __name__ == "__main__":
    main()
