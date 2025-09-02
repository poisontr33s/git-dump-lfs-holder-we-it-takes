#!/usr/bin/env python3
"""
🎭 PSYCHO-NOIR KONTRAPUNKT: SMART SESSION INSTALLER
==================================================

Intelligent installer som tilpasser seg ditt system på Helios 18.
Detekterer automatisk hva som er tilgjengelig og velger beste tilnærming.

KILDEKODE-KADAVER IDENTIFISERT: Complex dependency requirements  
KOMPILERINGS-SPØKELSE EXORCISED: Adaptive installation strategy
"""

import os
import sys
import subprocess
import platform
from pathlib import Path
import json

class SmartSessionInstaller:
    def __init__(self):
        self.system_info = self.detect_system()
        self.capabilities = self.check_capabilities()
        
    def detect_system(self):
        """Detect system information"""
        info = {
            "platform": platform.system(),
            "architecture": platform.architecture()[0],
            "python_version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
            "is_helios": self.detect_helios(),
            "is_codespaces": os.path.exists("/workspaces") or os.environ.get("CODESPACES"),
            "vscode_available": self.check_vscode()
        }
        
        return info
    
    def detect_helios(self):
        """Try to detect if running on Helios 18 system"""
        indicators = [
            "Helios" in platform.node(),
            "RTX 4090" in str(subprocess.run(["wmic", "path", "win32_VideoController", "get", "name"], 
                                            capture_output=True, text=True, shell=True).stdout) if platform.system() == "Windows" else False,
            "14900" in platform.processor()
        ]
        
        return any(indicators)
    
    def check_vscode(self):
        """Check if VS Code is available"""
        try:
            result = subprocess.run(["code", "--version"], capture_output=True)
            return result.returncode == 0
        except:
            return False
    
    def check_capabilities(self):
        """Check what capabilities are available"""
        caps = {
            "gui": False,
            "cli": True,  # Always assume CLI works
            "zip_support": False,
            "file_dialogs": False,
            "notifications": False
        }
        
        # Check GUI support
        try:
            import tkinter
            caps["gui"] = True
            caps["file_dialogs"] = True
            
            # Test if we can actually create windows
            try:
                root = tkinter.Tk()
                root.withdraw()  # Hide window
                caps["notifications"] = True
                root.destroy()
            except:
                caps["gui"] = False
        except ImportError:
            pass
        
        # Check zip support
        try:
            import zipfile
            caps["zip_support"] = True
        except ImportError:
            pass
        
        return caps
    
    def print_system_info(self):
        """Print detected system information"""
        print("🎭 PSYCHO-NOIR SESSION INSTALLER")
        print("================================")
        print()
        print("🖥️ SYSTEM DETECTION:")
        print(f"   Platform: {self.system_info['platform']} {self.system_info['architecture']}")
        print(f"   Python: {self.system_info['python_version']}")
        print(f"   Helios 18: {'✅' if self.system_info['is_helios'] else '❌'}")
        print(f"   Codespaces: {'✅' if self.system_info['is_codespaces'] else '❌'}")
        print(f"   VS Code: {'✅' if self.system_info['vscode_available'] else '❌'}")
        print()
        print("🔧 CAPABILITIES:")
        print(f"   GUI Support: {'✅' if self.capabilities['gui'] else '❌'}")
        print(f"   File Dialogs: {'✅' if self.capabilities['file_dialogs'] else '❌'}")
        print(f"   ZIP Support: {'✅' if self.capabilities['zip_support'] else '❌'}")
        print(f"   Notifications: {'✅' if self.capabilities['notifications'] else '❌'}")
        print()
    
    def recommend_approach(self):
        """Recommend best approach based on capabilities"""
        print("🎯 RECOMMENDED APPROACH:")
        print("========================")
        
        if self.capabilities["gui"] and self.capabilities["file_dialogs"]:
            print("✨ OPTIMAL: GUI Bridge med full funksjonalitet")
            print("   • Bruk: python tools/seamless_session_bridge.py")
            print("   • Eller: dobbeltklikk windows_session_bridge.bat")
            print("   • GUI gir enklest brukeropplevelse")
            approach = "gui"
            
        elif self.capabilities["zip_support"]:
            print("🔧 GOOD: CLI Bridge med ZIP transfer")
            print("   • Bruk: windows_session_bridge.bat")
            print("   • Eller: python tools/copilot_session_bridge.py")
            print("   • Kommandolinje med veiledning")
            approach = "cli_enhanced"
            
        else:
            print("⚠️ BASIC: Manual transfer anbefales")
            print("   • Installer zipfile support: pip install zipfile")
            print("   • Eller manual kopiering av .copilot-bridge/ mappe")
            approach = "manual"
        
        print()
        return approach
    
    def create_optimal_launcher(self):
        """Create launcher script optimized for detected system"""
        approach = self.recommend_approach()
        
        if approach == "gui":
            self.create_gui_launcher()
        elif approach == "cli_enhanced":
            self.create_cli_launcher()
        else:
            self.create_manual_instructions()
    
    def create_gui_launcher(self):
        """Create optimized GUI launcher"""
        launcher_content = f"""#!/usr/bin/env python3
# Auto-generated optimal launcher for {self.system_info['platform']}

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from tools.seamless_session_bridge import SeamlessSessionBridge
    
    print("🎭 Starting Psycho-Noir Session Bridge (GUI Mode)")
    bridge = SeamlessSessionBridge()
    bridge.run()
    
except ImportError as e:
    print(f"❌ GUI libraries not available: {{e}}")
    print("🔄 Falling back to CLI mode...")
    
    from tools.copilot_session_bridge import CopilotSessionBridge
    bridge = CopilotSessionBridge()
    bridge.scan_environment()
    bridge.export_session()

except Exception as e:
    print(f"❌ Error: {{e}}")
    input("Press Enter to continue...")
"""
        
        with open("start_session_bridge.py", "w") as f:
            f.write(launcher_content)
        
        print("✅ Optimal launcher opprettet: start_session_bridge.py")
    
    def create_cli_launcher(self):
        """Create enhanced CLI launcher"""
        print("✅ CLI launcher allerede tilgjengelig: windows_session_bridge.bat")
    
    def create_manual_instructions(self):
        """Create manual transfer instructions"""
        instructions = """
# 🎭 MANUAL SESSION TRANSFER GUIDE

## På Helios 18 (Windows):

### Steg 1: Forbered environment
```cmd
cd /path/to/PsychoNoir-Kontrapunkt
python -m pip install --user zipfile
```

### Steg 2: Eksporter session (fra Codespaces)
```cmd
python tools/copilot_session_bridge.py --export
```

### Steg 3: Kopier .copilot-bridge/ mappen
- Fra Codespaces: Last ned hele .copilot-bridge/ mappen
- Til Helios 18: Plasser i workspace root

### Steg 4: Import session
```cmd
python tools/copilot_session_bridge.py --import .copilot-bridge/session_export_*.json
```

### Steg 5: Restart VS Code
- Restart VS Code for å se importert session data
"""
        
        with open("MANUAL_TRANSFER_GUIDE.md", "w") as f:
            f.write(instructions)
        
        print("✅ Manual guide opprettet: MANUAL_TRANSFER_GUIDE.md")
    
    def install_missing_dependencies(self):
        """Try to install missing dependencies"""
        print("🔧 INSTALLING MISSING DEPENDENCIES:")
        print("===================================")
        
        if not self.capabilities["gui"]:
            print("📦 Attempting to install tkinter...")
            if self.system_info["platform"] == "Windows":
                print("   ℹ️ tkinter should be included with Python on Windows")
                print("   ℹ️ If missing, reinstall Python with 'tcl/tk and IDLE' option")
            else:
                try:
                    subprocess.run([sys.executable, "-m", "pip", "install", "tk"], check=True)
                    print("   ✅ tkinter installation attempted")
                except:
                    print("   ❌ tkinter installation failed")
        
        if not self.capabilities["zip_support"]:
            print("📦 Installing zipfile support...")
            try:
                subprocess.run([sys.executable, "-m", "pip", "install", "--user", "zipfile"], check=True)
                print("   ✅ zipfile installed")
            except:
                print("   ❌ zipfile installation failed")

def main():
    installer = SmartSessionInstaller()
    installer.print_system_info()
    installer.install_missing_dependencies()
    installer.create_optimal_launcher()
    
    print()
    print("🎭 DEN USYNLIGE HÅND: Installation complete!")
    print()
    print("ERROR: DEPENDENCY_COMPLEXITY_BYPASSED")
    print("MICROSOFT_COMPATIBILITY_MAZE_NAVIGATED")
    print()

if __name__ == "__main__":
    main()
