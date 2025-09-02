#!/bin/bash
# GitHub Copilot Chat Log Import Script

echo "🎭 COPILOT CHAT BRIDGE - Import Sessions"
echo "Environment: $(date)"

BRIDGE_DIR=".copilot-bridge"

if [ ! -d "$BRIDGE_DIR" ]; then
    echo "❌ No bridge directory found"
    exit 1
fi

echo "📥 Available sessions:"
ls -la "$BRIDGE_DIR"/*.json 2>/dev/null || echo "No session files found"

echo "💡 Manual restoration required:"
echo "1. Copy session content from .copilot-bridge/ files"
echo "2. Reference in current chat session"
echo "3. Use workspace files for context continuity"
