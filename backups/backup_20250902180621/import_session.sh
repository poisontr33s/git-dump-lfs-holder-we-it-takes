#!/bin/bash
# Copilot Session Import Script
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <export_file.json>"
    echo "Available exports:"
    ls .copilot-bridge/session_export_*.json 2>/dev/null || echo "  No exports found"
    exit 1
fi

echo "🎭 Importing Copilot Session..."
cd "$(dirname "$0")/.."
python3 tools/copilot_session_bridge.py --import "$1"
echo "✅ Import complete!"
