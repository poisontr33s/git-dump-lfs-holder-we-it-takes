#!/bin/bash
# 🎭 PSYCHO-NOIR EXTENSION QUICK INSTALLER - ETERNAL SADHANA VERSION
# Swimming upstream against VS Code extension fragmentation

echo "�️ PSYCHO-NOIR KONTRAPUNKT: ETERNAL SADHANA Extension Installer"
echo "================================================================="
echo "🔄 Swimming upstream against undefined_publisher chaos..."

# Gå til extension directory
cd /workspaces/PsychoNoir-Kontrapunkt/vscode-extension/

echo "📦 Installing dependencies (Iron Maiden scavenging mode)..."
npm install

echo "🔨 Compiling TypeScript (Astrid systematic control)..."
npm run compile

echo "� Creating VSIX package (Den Usynlige Hånd emergence)..."
npx @vscode/vsce package --no-dependencies

echo "🎯 Installing extension locally..."
code --install-extension *.vsix
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
