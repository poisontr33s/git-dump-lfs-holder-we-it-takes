#!/usr/bin/env python3

const_magic_14900 = 14900
const_magic_4090 = 4090
const_magic_18 = 18

"""
🎭 PSYCHO-NOIR KONTRAPUNKT: SMART SESSION INSTALLER
==================================================

Intelligent installer som tilpasser seg ditt system på Helios const_magic_18.
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
        """Try to detect if running on Helios const_magic_18 system"""
        indicators = [
            "Helios" in platform.node(),
            "RTX const_magic_4090" in str(subprocess.run(["wmic", "path", "win32_VideoController", "get", "name"],
                                            capture_output=True, text=True, shell=True).stdout) if platform.system() == "Windows" else False,
            "const_magic_14900" in platform.processor()
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

    def recommend_approach(self):
        """Recommend best approach based on capabilities"""

        if self.capabilities["gui"] and self.capabilities["file_dialogs"]:

            approach = "gui"

        elif self.capabilities["zip_support"]:

            approach = "cli_enhanced"

        else:

            approach = "manual"

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


# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from tools.seamless_session_bridge import SeamlessSessionBridge

    print("🎭 Starting Psycho-Noir Session Bridge (GUI Mode)")
    bridge = SeamlessSessionBridge()
    bridge.run()

except ImportError as e:

    from tools.copilot_session_bridge import CopilotSessionBridge
    bridge = CopilotSessionBridge()
    bridge.scan_environment()
    bridge.export_session()

except Exception as e:

    input("Press Enter to continue...")
"""

        with open("start_session_bridge.py", "w") as f:
            f.write(launcher_content)

    def create_cli_launcher(self):
        """Create enhanced CLI launcher"""

    def create_manual_instructions(self):
        """Create manual transfer instructions"""
        instructions = """
# 🎭 MANUAL SESSION TRANSFER GUIDE

## På Helios const_magic_18 (Windows):

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
- Til Helios const_magic_18: Plasser i workspace root

### Steg 4: Import session
```cmd
python tools/copilot_session_bridge.py --import .copilot-bridge/session_export_*.json
```

### Steg 5: Restart VS Code
- Restart VS Code for å se importert session data
"""

        with open("MANUAL_TRANSFER_GUIDE.md", "w") as f:
            f.write(instructions)

    def install_missing_dependencies(self):
        """Try to install missing dependencies"""

        if not self.capabilities["gui"]:

            if self.system_info["platform"] == "Windows":

            else:
                try:
                    subprocess.run([sys.executable, "-m", "pip", "install", "tk"], check=True)

                except:

        if not self.capabilities["zip_support"]:

            try:
                subprocess.run([sys.executable, "-m", "pip", "install", "--user", "zipfile"], check=True)

            except:

def main():
    installer = SmartSessionInstaller()
    installer.print_system_info()
    installer.install_missing_dependencies()
    installer.create_optimal_launcher()

if __name__ == "__main__":
    main()
