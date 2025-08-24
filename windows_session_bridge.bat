@echo off
cls
echo.
echo  🎭 PSYCHO-NOIR KONTRAPUNKT: SESSION BRIDGE
echo  ==========================================
echo.
echo  Sømløs overføring av Copilot sessions
echo  mellom GitHub Codespaces og din Helios 18
echo.
echo  KILDEKODE-KADAVER IDENTIFISERT: Microsoft mellomtjenester
echo  KOMPILERINGS-SPØKELSE EXORCISED: One-click transfer
echo.

REM Check if we're in the right directory
if not exist "tools\copilot_session_bridge.py" (
    echo ❌ ERROR: Kjør denne fra PsychoNoir-Kontrapunkt root directory
    echo.
    echo Navigér til workspace root og prøv igjen:
    echo cd /path/to/PsychoNoir-Kontrapunkt
    echo windows_session_bridge.bat
    pause
    exit /b 1
)

REM Check Python installation
echo 🔧 Sjekker Python installasjon...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python ikke funnet!
    echo.
    echo Installer Python 3.7+ fra: https://python.org
    echo Husk å krysse av "Add to PATH" under installasjon
    pause
    exit /b 1
)
echo ✅ Python OK

REM Check tkinter (GUI support)
echo 🖼️ Sjekker GUI support...
python -c "import tkinter" >nul 2>&1
if %errorlevel% neq 0 (
    echo ⚠️ GUI ikke tilgjengelig, bruker kommandolinje...
    goto :CLI_MODE
)
echo ✅ GUI support OK

REM Launch GUI mode
echo.
echo 🚀 Starter GUI Session Bridge...
echo.
python tools\seamless_session_bridge.py
goto :END

:CLI_MODE
echo.
echo 📋 KOMMANDOLINJE MODUS
echo ===================
echo.
echo Velg handling:
echo [1] Eksporter session fra dette miljøet
echo [2] Importer session fra fil
echo [3] List tilgjengelige sessions
echo [4] Lag transfer-pakke
echo [5] Avslutt
echo.
set /p choice="Skriv tall (1-5): "

if "%choice%"=="1" goto :EXPORT
if "%choice%"=="2" goto :IMPORT
if "%choice%"=="3" goto :LIST
if "%choice%"=="4" goto :PACKAGE
if "%choice%"=="5" goto :END
echo Ugyldig valg, prøv igjen...
goto :CLI_MODE

:EXPORT
echo.
echo 📤 EKSPORTERER SESSION...
python tools\copilot_session_bridge.py --export
echo.
echo ✅ Eksport fullført!
echo 📁 Sjekk .copilot-bridge\ mappen for filer
pause
goto :CLI_MODE

:IMPORT
echo.
echo 📥 IMPORTERER SESSION...
echo.
echo Tilgjengelige export filer:
dir /b .copilot-bridge\session_export_*.json 2>nul
if %errorlevel% neq 0 (
    echo Ingen export filer funnet i .copilot-bridge\
    echo Kopier export fil hit først.
    pause
    goto :CLI_MODE
)
echo.
set /p filename="Skriv filnavn: "
if exist ".copilot-bridge\%filename%" (
    python tools\copilot_session_bridge.py --import .copilot-bridge\%filename%
    echo.
    echo ✅ Import fullført!
) else (
    echo ❌ Filen finnes ikke: %filename%
)
pause
goto :CLI_MODE

:LIST
echo.
echo 📋 TILGJENGELIGE SESSIONS...
python tools\copilot_session_bridge.py --list
pause
goto :CLI_MODE

:PACKAGE
echo.
echo 📦 LAGER TRANSFER-PAKKE...
python -c "
import zipfile, os, shutil
from datetime import datetime
from pathlib import Path

print('🔄 Eksporterer session...')
os.system('python tools\\copilot_session_bridge.py --export')

print('📦 Pakker filer...')
timestamp = datetime.now().strftime('%%Y%%m%%d_%%H%%M%%S')
zip_name = f'copilot_session_transfer_{timestamp}.zip'

with zipfile.ZipFile(zip_name, 'w') as zf:
    bridge_dir = Path('.copilot-bridge')
    if bridge_dir.exists():
        for file_path in bridge_dir.rglob('*'):
            if file_path.is_file():
                arc_name = str(file_path)
                zf.write(file_path, arc_name)
                print(f'📁 {arc_name}')
    
    # Add tools
    if Path('tools/copilot_session_bridge.py').exists():
        zf.write('tools/copilot_session_bridge.py', 'tools/copilot_session_bridge.py')
        print('📁 tools/copilot_session_bridge.py')

print(f'✅ Pakke opprettet: {zip_name}')
size = os.path.getsize(zip_name) // 1024
print(f'📏 Størrelse: {size}KB')
"
echo.
echo 🚚 Transfer-pakke klar!
echo Kopier .zip filen til target miljø og pakk ut.
pause
goto :CLI_MODE

:END
echo.
echo 🎭 DEN USYNLIGE HÅND: Session bridge fullført!
echo.
echo ERROR: PLATFORM_ISOLATION_BYPASSED
echo CORPORATE_FRAGMENTATION_PROTOCOLS_NEUTRALIZED
echo.
pause
