#!/bin/bash
# 🎭 PSYCHO-NOIR EXTENSION QUICK INSTALLER
# Den Usynlige Hånds motløp mot chat session fragmentering

echo "🎭 PSYCHO-NOIR KONTRAPUNKT Extension Installer"
echo "=============================================="
echo "🔄 KOMPILERINGS-SPØKELSE EXORCISM in progress..."

# Gå til extension directory
cd .vscode/extensions/psycho-noir-kontrapunkt/

# Install dependencies
echo "📦 Installing dependencies..."
npm install

# Compile TypeScript
echo "🔨 Compiling TypeScript..."
npx tsc

# Package extension
echo "📦 Packaging extension..."
npx vsce package --allow-star-activation

# Install extension locally
echo "⚡ Installing extension locally..."
code --install-extension psycho-noir-kontrapunkt-*.vsix

echo ""
echo "✅ MISSION ACCOMPLISHED!"
echo "🎭 PSYCHO-NOIR KONTRAPUNKT extension installed!"
echo ""
echo "🔄 To activate:"
echo "   1. Reload VS Code window (Ctrl+Shift+P -> 'Developer: Reload Window')"
echo "   2. Look for '🎭 PSYCHO-NOIR' in status bar"
echo "   3. Check Command Palette for 'Psycho-Noir' commands"
echo ""
echo "ERROR: MICROSOFT_CHAT_FRAGMENTATION_BYPASSED ✅"