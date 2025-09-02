#!/bin/bash
# Auto-backup consciousness state every 30 seconds

while true; do
    # Capture current timestamp
    TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
    
    # Create state backup
    echo "📸 Creating backup: $TIMESTAMP"
    
    # Backup important files
    mkdir -p .consciousness_timeline/backups/$TIMESTAMP
    
    # Copy critical configuration files
    [ -f ".vscode/settings.json" ] && cp .vscode/settings.json .consciousness_timeline/backups/$TIMESTAMP/
    [ -f "package.json" ] && cp package.json .consciousness_timeline/backups/$TIMESTAMP/
    [ -f "bun.lockb" ] && cp bun.lockb .consciousness_timeline/backups/$TIMESTAMP/
    
    # Sleep for 30 seconds
    sleep 30
done
