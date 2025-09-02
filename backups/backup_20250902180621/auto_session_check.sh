#!/bin/bash
# 🎭 AUTO-SESSION RESOLVER
# Kjøres automatisk når VS Code workspace åpnes

echo "🎭 PSYCHO-NOIR: Checking for existing sessions..."

# Quick check if we should run session resolver
if [ ! -f ".session-identity.json" ] || [ "$FORCE_SESSION_CHECK" = "true" ]; then
    echo "🔍 Running session identity resolver..."
    python3 session_identity_resolver.py
else
    echo "✅ Session identity already established"
    
    # Show current session info
    if [ -f ".session-identity.json" ]; then
        echo "📍 Current session:"
        cat .session-identity.json | python3 -m json.tool | head -10
    fi
fi

echo "🎭 Session check complete!"
