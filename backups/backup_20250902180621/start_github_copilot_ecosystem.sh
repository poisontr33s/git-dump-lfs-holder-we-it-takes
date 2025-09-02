#!/bin/bash

# 🚀 Psycho-Noir Kontrapunkt - GitHub Copilot Extension Connector Startup
# ========================================================================
# 
# This script launches the complete ecosystem for GitHub Copilot integration
# and cross-platform session archaeology.

echo "🎭 Starting Psycho-Noir Kontrapunkt Extension Ecosystem..."
echo "========================================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

# Check prerequisites
print_status "Checking prerequisites..."

# Check Python
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is required but not installed"
    exit 1
fi

# Check Node.js (for VS Code extension development)
if ! command -v node &> /dev/null; then
    print_warning "Node.js not found. VS Code extension features may be limited."
else
    print_success "Node.js found: $(node --version)"
fi

# Check VS Code
if ! command -v code &> /dev/null; then
    print_warning "VS Code not found in PATH. Extension installation may require manual setup."
else
    print_success "VS Code found: $(code --version | head -1)"
fi

# Create necessary directories
print_status "Setting up directory structure..."
mkdir -p data/sessions
mkdir -p data/archaeology
mkdir -p data/patterns
mkdir -p logs
mkdir -p vscode-extension/out

# Install Python dependencies
print_status "Installing Python dependencies..."
pip3 install -r backend/requirements.txt --quiet
if [ $? -eq 0 ]; then
    print_success "Python dependencies installed"
else
    print_error "Failed to install Python dependencies"
    exit 1
fi

# Install Node.js dependencies (if Node.js is available)
if command -v npm &> /dev/null; then
    print_status "Installing Node.js dependencies for VS Code extension..."
    cd vscode-extension
    npm install --silent
    if [ $? -eq 0 ]; then
        print_success "Node.js dependencies installed"
    else
        print_warning "Some Node.js dependencies may have failed to install"
    fi
    cd ..
fi

# Start the GitHub Copilot Connector API
print_status "Starting GitHub Copilot Connector API..."
python3 backend/python/github_copilot_connector_api.py &
API_PID=$!

# Wait for API to start
sleep 3

# Check if API is running
if curl -s http://localhost:5000/api/status > /dev/null; then
    print_success "GitHub Copilot Connector API is running on http://localhost:5000"
else
    print_error "Failed to start GitHub Copilot Connector API"
    kill $API_PID 2>/dev/null
    exit 1
fi

# Start the frontend HTTP server
print_status "Starting frontend server..."
cd frontend
if command -v npx &> /dev/null; then
    npx http-server . -p 8080 --silent &
    FRONTEND_PID=$!
    sleep 2
    
    if curl -s http://localhost:8080 > /dev/null; then
        print_success "Frontend server is running on http://localhost:8080"
    else
        print_warning "Frontend server may not be running properly"
    fi
else
    print_warning "npx not available. Frontend server not started."
    print_warning "You can manually serve frontend files or use Python: python3 -m http.server 8080"
fi
cd ..

# Create VS Code extension package (if tools are available)
if command -v npx &> /dev/null && [ -d "vscode-extension/node_modules" ]; then
    print_status "Building VS Code extension..."
    cd vscode-extension
    npx tsc -p . 2>/dev/null
    if [ $? -eq 0 ]; then
        print_success "VS Code extension built successfully"
        
        # Try to package the extension
        if command -v vsce &> /dev/null; then
            print_status "Packaging VS Code extension..."
            vsce package --quiet
            if [ $? -eq 0 ]; then
                print_success "VS Code extension packaged as .vsix file"
                print_status "Install with: code --install-extension *.vsix"
            fi
        else
            print_warning "vsce not found. Install with: npm install -g vsce"
        fi
    else
        print_warning "TypeScript compilation had issues. Extension may still work."
    fi
    cd ..
else
    print_warning "Skipping VS Code extension build (missing dependencies)"
fi

# Display startup summary
echo ""
echo -e "${PURPLE}🎭 PSYCHO-NOIR KONTRAPUNKT ECOSYSTEM STATUS${NC}"
echo "=============================================="
echo ""
echo -e "${BLUE}🔗 GitHub Copilot Connector API:${NC} http://localhost:5000"
echo -e "${BLUE}🌐 Frontend Portal:${NC} http://localhost:8080"
echo -e "${BLUE}📊 API Status:${NC} http://localhost:5000/api/status"
echo -e "${BLUE}🧠 Neural Patterns:${NC} http://localhost:5000/api/patterns/neural"
echo ""
echo -e "${GREEN}🚀 SYSTEM READY FOR GITHUB COPILOT INTEGRATION!${NC}"
echo ""

# Show GitHub integration instructions
echo -e "${YELLOW}📋 NEXT STEPS FOR GITHUB COPILOT INTEGRATION:${NC}"
echo "1. Open the connector portal: http://localhost:5000"
echo "2. Enter your GitHub username (e.g., poisontr33s)"
echo "3. Generate a GitHub Personal Access Token with 'copilot' scope"
echo "4. Paste the token (ghp_...) in the authentication form"
echo "5. Connect to your Copilot Workspace URL"
echo ""

# VS Code extension instructions
if [ -f "vscode-extension/*.vsix" ]; then
    echo -e "${YELLOW}🧩 VS CODE EXTENSION READY:${NC}"
    echo "Install the extension with:"
    echo "  code --install-extension vscode-extension/*.vsix"
    echo ""
elif [ -d "vscode-extension/out" ]; then
    echo -e "${YELLOW}🧩 VS CODE EXTENSION (DEV MODE):${NC}"
    echo "1. Open VS Code in the vscode-extension folder"
    echo "2. Press F5 to launch Extension Development Host"
    echo "3. Use Ctrl+Shift+P and search for 'Psycho-Noir' commands"
    echo ""
fi

# Show session archaeology instructions
echo -e "${YELLOW}🔍 SESSION ARCHAEOLOGY READY:${NC}"
echo "• Export sessions from Google AI Studio as JSON"
echo "• Import them via the portal or VS Code extension"
echo "• Watch as neural patterns are detected across platforms"
echo "• Use the archaeology mode to discover hidden connections"
echo ""

# Create a cleanup function
cleanup() {
    echo ""
    print_status "Shutting down Psycho-Noir Kontrapunkt ecosystem..."
    
    if [ ! -z "$API_PID" ]; then
        kill $API_PID 2>/dev/null
        print_status "API server stopped"
    fi
    
    if [ ! -z "$FRONTEND_PID" ]; then
        kill $FRONTEND_PID 2>/dev/null
        print_status "Frontend server stopped"
    fi
    
    print_success "Ecosystem shutdown complete"
    exit 0
}

# Set up signal handlers for graceful shutdown
trap cleanup SIGINT SIGTERM

# Keep the script running
print_status "System running. Press Ctrl+C to stop."
echo ""
echo -e "${BLUE}📊 Real-time logs:${NC}"
echo "API: tail -f logs/api.log"
echo "Archaeology: tail -f logs/archaeology.log"
echo ""

# Monitor the system
while true; do
    sleep 10
    
    # Check if API is still running
    if ! curl -s http://localhost:5000/api/status > /dev/null; then
        print_error "API server appears to have stopped"
        break
    fi
    
    # Optional: Display live statistics
    if [ $(($(date +%s) % 60)) -eq 0 ]; then
        print_status "System health check passed - $(date)"
    fi
done

# If we get here, something went wrong
cleanup
