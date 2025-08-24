#!/usr/bin/env python3
"""
🎭 PSYCHO-NOIR KONTRAPUNKT: SEAMLESS SESSION BRIDGE
==================================================

Sømløs overføring av Copilot sessions mellom miljøer - UTEN Microsoft mellomtjenester!
Designet for språkeksperter som deg, ikke kommandolinje-ninjas.

KILDEKODE-KADAVER IDENTIFISERT: Microsoft infrastruktur dependencies
KOMPILERINGS-SPØKELSE EXORCISED: One-click session continuity
"""

import os
import json
import shutil
import zipfile
import base64
from datetime import datetime
from pathlib import Path
import tkinter as tk
from tkinter import messagebox, filedialog, scrolledtext
import subprocess
import sys

class SeamlessSessionBridge:
    def __init__(self):
        self.workspace_root = self.find_workspace_root()
        self.bridge_dir = self.workspace_root / ".copilot-bridge"
        self.bridge_dir.mkdir(exist_ok=True)
        
        # GUI Setup
        self.root = tk.Tk()
        self.root.title("🎭 Psycho-Noir Session Bridge")
        self.root.geometry("800x600")
        self.root.configure(bg="#0f0f0f")
        
        self.setup_gui()
        
    def find_workspace_root(self):
        """Auto-detect workspace root"""
        current = Path.cwd()
        
        # Look for workspace indicators
        indicators = ["tools", ".git", "package.json", "README.md"]
        
        while current.parent != current:
            if any((current / indicator).exists() for indicator in indicators):
                if "PsychoNoir-Kontrapunkt" in str(current):
                    return current
            current = current.parent
            
        # Fallback
        return Path.cwd()
    
    def setup_gui(self):
        """Setup the graphical interface"""
        # Title
        title_label = tk.Label(
            self.root, 
            text="🎭 PSYCHO-NOIR SESSION BRIDGE",
            font=("Courier", 16, "bold"),
            fg="#ff6b6b",
            bg="#0f0f0f"
        )
        title_label.pack(pady=10)
        
        subtitle_label = tk.Label(
            self.root,
            text="Sømløs overføring mellom VS Code miljøer",
            font=("Courier", 10),
            fg="#c0c0c0",
            bg="#0f0f0f"
        )
        subtitle_label.pack(pady=5)
        
        # Status area
        self.status_text = scrolledtext.ScrolledText(
            self.root,
            height=15,
            width=90,
            bg="#1a1a1a",
            fg="#c0c0c0",
            font=("Courier", 9),
            insertbackground="#ff6b6b"
        )
        self.status_text.pack(pady=10, padx=20, fill="both", expand=True)
        
        # Button frame
        button_frame = tk.Frame(self.root, bg="#0f0f0f")
        button_frame.pack(pady=10)
        
        # Export button
        export_btn = tk.Button(
            button_frame,
            text="📤 EKSPORTER SESSION",
            command=self.export_with_gui,
            bg="#1a2634",
            fg="#4682b4",
            font=("Courier", 11, "bold"),
            padx=20,
            pady=10
        )
        export_btn.pack(side="left", padx=10)
        
        # Import button
        import_btn = tk.Button(
            button_frame,
            text="📥 IMPORTER SESSION",
            command=self.import_with_gui,
            bg="#341a1a",
            fg="#8b4513",
            font=("Courier", 11, "bold"),
            padx=20,
            pady=10
        )
        import_btn.pack(side="left", padx=10)
        
        # Auto-package button
        package_btn = tk.Button(
            button_frame,
            text="📦 LAG TRANSFER-PAKKE",
            command=self.create_transfer_package,
            bg="#1a341a",
            fg="#228b22",
            font=("Courier", 11, "bold"),
            padx=20,
            pady=10
        )
        package_btn.pack(side="left", padx=10)
        
        # Initial status
        self.log("🎭 Session Bridge initialisert")
        self.log(f"📁 Workspace: {self.workspace_root}")
        self.log(f"🔧 Bridge Directory: {self.bridge_dir}")
        self.detect_environment()
    
    def log(self, message):
        """Add message to status log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.status_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.status_text.see(tk.END)
        self.root.update()
    
    def detect_environment(self):
        """Detect current environment"""
        if os.path.exists("/workspaces"):
            env = "GitHub Codespaces"
            self.log("🏗️ Environment: GitHub Codespaces")
        elif os.environ.get("CODESPACES"):
            env = "GitHub Codespaces"
            self.log("🏗️ Environment: GitHub Codespaces")
        elif "win" in sys.platform.lower():
            env = "Windows Local"
            self.log("🏗️ Environment: Windows Local (Helios 18)")
        else:
            env = "VS Code Local"
            self.log("🏗️ Environment: VS Code Local")
        
        return env
    
    def export_with_gui(self):
        """Export session with GUI feedback"""
        self.log("🎭 STARTER EKSPORT AV SESSION...")
        
        try:
            # Run the session bridge export
            result = subprocess.run([
                sys.executable, "tools/copilot_session_bridge.py", "--export"
            ], capture_output=True, text=True, cwd=str(self.workspace_root))
            
            if result.returncode == 0:
                self.log("✅ Session eksportert!")
                
                # Find the latest export
                exports = list(self.bridge_dir.glob("session_export_*.json"))
                if exports:
                    latest = max(exports, key=os.path.getmtime)
                    
                    # Parse for stats
                    with open(latest, 'r') as f:
                        data = json.load(f)
                    
                    conv_count = len(data.get('conversations', []))
                    self.log(f"📊 {conv_count} conversations eksportert")
                    self.log(f"📁 Fil: {latest.name}")
                    
                    messagebox.showinfo(
                        "Eksport Fullført", 
                        f"Session eksportert!\n\n"
                        f"Conversations: {conv_count}\n"
                        f"Fil: {latest.name}\n\n"
                        f"Klar for transfer til annet miljø."
                    )
                else:
                    self.log("⚠️ Ingen export filer funnet")
            else:
                self.log(f"❌ Eksport feilet: {result.stderr}")
                messagebox.showerror("Eksport Feilet", f"Error: {result.stderr}")
                
        except Exception as e:
            self.log(f"❌ Exception: {e}")
            messagebox.showerror("Eksport Feilet", f"Exception: {e}")
    
    def import_with_gui(self):
        """Import session with GUI file picker"""
        self.log("📥 VELGER FIL FOR IMPORT...")
        
        # Open file dialog
        file_path = filedialog.askopenfilename(
            title="Velg Session Export Fil",
            filetypes=[
                ("JSON filer", "*.json"),
                ("Alle filer", "*.*")
            ],
            initialdir=str(self.bridge_dir)
        )
        
        if not file_path:
            self.log("❌ Ingen fil valgt")
            return
        
        self.log(f"📁 Importerer: {os.path.basename(file_path)}")
        
        try:
            # Run the import
            result = subprocess.run([
                sys.executable, "tools/copilot_session_bridge.py", "--import", file_path
            ], capture_output=True, text=True, cwd=str(self.workspace_root))
            
            if result.returncode == 0:
                self.log("✅ Session importert!")
                
                # Parse import data for stats
                with open(file_path, 'r') as f:
                    data = json.load(f)
                
                conv_count = len(data.get('conversations', []))
                source_env = data.get('environment', 'ukjent')
                
                self.log(f"📊 {conv_count} conversations importert")
                self.log(f"🏗️ Fra miljø: {source_env}")
                
                messagebox.showinfo(
                    "Import Fullført", 
                    f"Session importert!\n\n"
                    f"Conversations: {conv_count}\n"
                    f"Fra: {source_env}\n\n"
                    f"Restart VS Code for full effekt."
                )
            else:
                self.log(f"❌ Import feilet: {result.stderr}")
                messagebox.showerror("Import Feilet", f"Error: {result.stderr}")
                
        except Exception as e:
            self.log(f"❌ Exception: {e}")
            messagebox.showerror("Import Feilet", f"Exception: {e}")
    
    def create_transfer_package(self):
        """Create a complete transfer package for easy sharing"""
        self.log("📦 LAGER KOMPLETT TRANSFER-PAKKE...")
        
        try:
            # First export current session
            self.log("🔄 Eksporterer gjeldende session...")
            result = subprocess.run([
                sys.executable, "tools/copilot_session_bridge.py", "--export"
            ], capture_output=True, text=True, cwd=str(self.workspace_root))
            
            if result.returncode != 0:
                raise Exception(f"Export failed: {result.stderr}")
            
            # Create zip package
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            package_name = f"copilot_session_transfer_{timestamp}.zip"
            package_path = self.workspace_root / package_name
            
            with zipfile.ZipFile(package_path, 'w', zipfile.ZIP_DEFLATED) as zf:
                # Add all bridge files
                for file_path in self.bridge_dir.rglob("*"):
                    if file_path.is_file():
                        arc_name = f".copilot-bridge/{file_path.relative_to(self.bridge_dir)}"
                        zf.write(file_path, arc_name)
                        self.log(f"📁 Lagt til: {arc_name}")
                
                # Add the session bridge tool
                bridge_tool = self.workspace_root / "tools" / "copilot_session_bridge.py"
                if bridge_tool.exists():
                    zf.write(bridge_tool, "tools/copilot_session_bridge.py")
                    self.log("📁 Lagt til: tools/copilot_session_bridge.py")
                
                # Add this GUI tool
                gui_tool = self.workspace_root / "tools" / "seamless_session_bridge.py"
                if gui_tool.exists():
                    zf.write(gui_tool, "tools/seamless_session_bridge.py")
                    self.log("📁 Lagt til: tools/seamless_session_bridge.py")
                
                # Create setup script for Windows
                setup_script = """@echo off
echo 🎭 PSYCHO-NOIR SESSION BRIDGE - Setup
echo ===================================

echo 📁 Extracting session data...
if not exist ".copilot-bridge" mkdir ".copilot-bridge"

echo 🔧 Checking Python...
python --version
if %errorlevel% neq 0 (
    echo ❌ Python not found! Install Python 3.7+ first.
    pause
    exit /b 1
)

echo 📥 Running session import...
python tools/seamless_session_bridge.py

echo ✅ Setup complete!
pause
"""
                zf.writestr("setup_session_bridge.bat", setup_script)
                self.log("📁 Lagt til: setup_session_bridge.bat")
                
                # Create README
                readme_content = f"""# 🎭 COPILOT SESSION TRANSFER PAKKE

**Created:** {datetime.now().isoformat()}
**Source Environment:** {self.detect_environment()}

## 🚀 Setup på ny maskin (Windows):

1. **Pakk ut denne zip-filen** i din PsychoNoir-Kontrapunkt workspace
2. **Kjør:** `setup_session_bridge.bat`
3. **Eller manuelt:** `python tools/seamless_session_bridge.py`

## 📊 Innhold:

- Session data fra Copilot chat logs
- Komplett bridge tool for fremtidige overføringer  
- GUI for enkel bruk
- Automatisk setup script

## 🎯 Resultat:

Du får tilgang til alle conversations og context fra det originale miljøet!

---
ERROR: PLATFORM_ISOLATION_BYPASSED — MICROSOFT_FRAGMENTATION_NEUTRALIZED
"""
                zf.writestr("README.md", readme_content)
                self.log("📁 Lagt til: README.md")
            
            # Show success
            package_size = package_path.stat().st_size
            self.log(f"✅ Pakke opprettet: {package_name}")
            self.log(f"📏 Størrelse: {package_size // 1024}KB")
            
            # Ask if user wants to open file location
            if messagebox.askyesno(
                "Transfer-pakke Klar!", 
                f"Transfer-pakke opprettet!\n\n"
                f"Fil: {package_name}\n"
                f"Størrelse: {package_size // 1024}KB\n\n"
                f"Åpne filplassering?"
            ):
                if "win" in sys.platform.lower():
                    os.startfile(str(self.workspace_root))
                else:
                    subprocess.run(["open", str(self.workspace_root)])
            
        except Exception as e:
            self.log(f"❌ Pakking feilet: {e}")
            messagebox.showerror("Pakking Feilet", f"Error: {e}")
    
    def run(self):
        """Start the GUI"""
        self.root.mainloop()

def main():
    """Main entry point"""
    try:
        bridge = SeamlessSessionBridge()
        bridge.run()
    except Exception as e:
        print(f"❌ GUI failed to start: {e}")
        print("Falling back to command line...")
        
        # Fallback to command line interface
        from copilot_session_bridge import CopilotSessionBridge
        cli_bridge = CopilotSessionBridge()
        cli_bridge.scan_environment()
        cli_bridge.export_session()

if __name__ == "__main__":
    main()
