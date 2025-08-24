@echo off
REM 🎭 PSYCHO-NOIR SESSION DETECTOR FOR WINDOWS 11
REM Universal chat session continuity - no dependencies!

title Psycho-Noir Session Detector
color 0A

echo.
echo 🎭 PSYCHO-NOIR SESSION DETECTOR
echo ===============================
echo Windows 11 Universal Edition
echo.

REM Detect environment
echo 📍 ENVIRONMENT DETECTION:
echo Platform: %OS% %PROCESSOR_ARCHITECTURE%
echo User: %USERNAME%
echo Host: %COMPUTERNAME%
echo Workspace: %CD%
echo.

REM Check for Node.js (VS Code usually has it)
where node >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo ✅ Node.js detected - running advanced detector...
    node universal_session_detector.js
    goto :end
) else (
    echo ⚠️ Node.js not found - using basic detection...
)

REM Basic detection without Node.js
echo.
echo 🔍 BASIC SESSION DETECTION:
echo ============================

if exist ".copilot-bridge" (
    echo ✅ Found .copilot-bridge directory
    echo.
    echo 📁 Session files:
    dir /b ".copilot-bridge\session_export_*.json" 2>nul
    if %ERRORLEVEL% EQU 0 (
        echo.
        echo 💬 EXISTING SESSIONS DETECTED!
        echo.
        echo 🎯 TO CONTINUE YOUR CHAT:
        echo 1. Open VS Code in this workspace
        echo 2. Open GitHub Copilot Chat (Ctrl+Shift+I)
        echo 3. Say: "Continue our previous work on [topic]"
        echo 4. Reference specific features you were working on
        echo.
        echo 🔧 ADVANCED OPTIONS:
        echo • Run: session_detector.html in browser for full analysis
        echo • Use VS Code Command Palette: "🎭 Check Session Continuity"
    ) else (
        echo 📝 Directory exists but no session files found
    )
) else (
    echo ✨ No existing sessions found. Starting fresh!
    echo.
    echo 🆕 NEW SESSION SETUP:
    echo 1. This will be your first session in this workspace
    echo 2. Open VS Code and start working
    echo 3. Chat sessions will be automatically tracked
)

echo.
echo 🎭 SESSION DETECTOR OPTIONS:
echo ============================
echo.
echo 1. Open HTML Session Detector (recommended)
echo 2. Try Node.js detector (if Node.js available)
echo 3. Show manual instructions
echo 4. Exit
echo.
set /p choice="Choose option (1-4): "

if "%choice%"=="1" (
    echo 🌐 Opening HTML detector...
    start "" "session_detector.html"
    goto :end
)

if "%choice%"=="2" (
    echo 🔧 Trying Node.js detector...
    node universal_session_detector.js 2>nul
    if %ERRORLEVEL% NEQ 0 (
        echo ❌ Node.js not available or script failed
        echo 💡 Try option 1 (HTML detector) instead
    )
    goto :end
)

if "%choice%"=="3" (
    echo.
    echo 📖 MANUAL CHAT CONTINUATION INSTRUCTIONS:
    echo =========================================
    echo.
    echo If you have existing chat sessions from another environment:
    echo.
    echo 1. LOCATE SESSION FILES:
    echo    • Look for files named: session_export_YYYYMMDD_HHMMSS.json
    echo    • Usually in: .copilot-bridge/ directory
    echo    • Or in downloads from GitHub Codespaces
    echo.
    echo 2. COPY TO THIS WORKSPACE:
    echo    • Create .copilot-bridge\ directory if it doesn't exist
    echo    • Copy session files there
    echo    • Run this detector again
    echo.
    echo 3. CONTINUE CHAT IN VS CODE:
    echo    • Open GitHub Copilot Chat panel
    echo    • Reference your previous work context
    echo    • Example: "Continue the VS Code extension we were building"
    echo.
    echo 4. USE HTML DETECTOR FOR ANALYSIS:
    echo    • Open session_detector.html in any browser
    echo    • Drag and drop session files for detailed analysis
    echo.
    goto :end
)

:end
echo.
echo 🎭 Den Usynlige Hånd: SESSION_DETECTION_COMPLETE!
echo.
pause
