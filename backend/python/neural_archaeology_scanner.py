#!/usr/bin/env python3

# Auto-generated constants for magic numbers
const_magic_50 = 50
const_ten = 10

"""
Neural Archaeology Scanner
-------------------------
Et verktøy for å grave i VS Codes digitale katakomber og kartlegge AI-modellenes spor.
Del av Psycho-Noir Kontrapunkt-rammeverket.
"""

import os
import json
from pathlib import Path
import tkinter as tk
from tkinter import ttk
from datetime import datetime
import shutil

class NeuralArchaeologyScanner:
    def __init__(self):
        self.VSCODE_STORAGE_PATH = os.path.expandvars(r"%APPDATA%\Code\User\workspaceStorage")
        self.root = tk.Tk()
        self.root.title("Neural Archaeology Scanner")
        self.root.geometry("1200x800")
        self.setup_ui()

    def setup_ui(self):
        """Etablerer brukergrensesnittet for nevral arkeologi."""
        # Stil-konfigurasjon
        style = ttk.Style()
        style.configure("Neural.TFrame", background="#1a1a1a")
        style.configure("Neural.TLabel",
                       background="#1a1a1a",
                       foreground="#00ff00",
                       font=("Courier", const_ten))
        style.configure("Neural.TButton",
                       background="#2a2a2a",
                       foreground="#00ff00")

        # Hovedramme
        main_frame = ttk.Frame(self.root, style="Neural.TFrame")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=const_ten, pady=const_ten)

        # Workspace-liste
        self.workspace_frame = ttk.Frame(main_frame, style="Neural.TFrame")
        self.workspace_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        workspace_label = ttk.Label(self.workspace_frame,
                                  text="DETEKTERTE DATASFÆRER (WORKSPACES)",
                                  style="Neural.TLabel")
        workspace_label.pack(pady=5)

        self.workspace_list = tk.Listbox(self.workspace_frame,
                                       bg="#1a1a1a",
                                       fg="#00ff00",
                                       selectmode=tk.SINGLE,
                                       font=("Courier", const_ten))
        self.workspace_list.pack(fill=tk.BOTH, expand=True, pady=5)
        self.workspace_list.bind('<<ListboxSelect>>', self.on_workspace_select)

        # Chat-historikk og modell-info
        info_frame = ttk.Frame(main_frame, style="Neural.TFrame")
        info_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # AI-modeller
        models_label = ttk.Label(info_frame,
                               text="IDENTIFISERTE AI-KONSTRUKTER",
                               style="Neural.TLabel")
        models_label.pack(pady=5)

        self.models_text = tk.Text(info_frame,
                                 bg="#1a1a1a",
                                 fg="#00ff00",
                                 height=const_ten,
                                 font=("Courier", const_ten))
        self.models_text.pack(fill=tk.X, pady=5)

        # Chat-historikk
        history_label = ttk.Label(info_frame,
                                text="ARKIVERTE DIALOGER",
                                style="Neural.TLabel")
        history_label.pack(pady=5)

        self.history_text = tk.Text(info_frame,
                                  bg="#1a1a1a",
                                  fg="#00ff00",
                                  font=("Courier", const_ten))
        self.history_text.pack(fill=tk.BOTH, expand=True, pady=5)

        # Kontrollknapper
        control_frame = ttk.Frame(info_frame, style="Neural.TFrame")
        control_frame.pack(fill=tk.X, pady=5)

        export_btn = ttk.Button(control_frame,
                              text="EKSPORTER DIALOGER",
                              command=self.export_selected_chats,
                              style="Neural.TButton")
        export_btn.pack(side=tk.LEFT, padx=5)

        import_btn = ttk.Button(control_frame,
                              text="IMPORTER DIALOGER",
                              command=self.import_chats,
                              style="Neural.TButton")
        import_btn.pack(side=tk.LEFT, padx=5)

    def scan_workspaces(self):
        """Scanner workspaceStorage etter digitale artefakter."""
        try:
            workspaces = []
            for workspace_dir in os.listdir(self.VSCODE_STORAGE_PATH):
                workspace_path = os.path.join(self.VSCODE_STORAGE_PATH, workspace_dir)
                if os.path.isdir(workspace_path):
                    workspace_json = os.path.join(workspace_path, "workspace.json")
                    if os.path.exists(workspace_json):
                        with open(workspace_json, 'r', encoding='utf-8') as f:
                            try:
                                data = json.load(f)
                                folder = data.get('folder', 'Ukjent lokasjon')
                                workspaces.append((folder, workspace_path))
                            except json.JSONDecodeError:
                                continue

            # Oppdater workspace-listen
            self.workspace_list.delete(0, tk.END)
            for folder, _ in sorted(workspaces):
                self.workspace_list.insert(tk.END, folder)

            return "SKANNING FULLFØRT: {} DATASFÆRER IDENTIFISERT".format(len(workspaces))
        except Exception as e:
            return f"FEIL UNDER SKANNING: {str(e)}"

    def on_workspace_select(self, event):
        """Håndterer valg av workspace fra listen."""
        if not self.workspace_list.curselection():
            return

        selected = self.workspace_list.get(self.workspace_list.curselection())
        workspace_path = None

        # Finn workspace-stien
        for workspace_dir in os.listdir(self.VSCODE_STORAGE_PATH):
            workspace_path = os.path.join(self.VSCODE_STORAGE_PATH, workspace_dir)
            if os.path.isdir(workspace_path):
                workspace_json = os.path.join(workspace_path, "workspace.json")
                if os.path.exists(workspace_json):
                    with open(workspace_json, 'r', encoding='utf-8') as f:
                        try:
                            data = json.load(f)
                            if data.get('folder') == selected:
                                break
                        except json.JSONDecodeError:
                            continue

        if workspace_path:
            self.analyze_workspace(workspace_path)

    def analyze_workspace(self, workspace_path):
        """Analyserer en valgt workspace for AI-modeller og chat-historikk."""
        # Tøm tidligere resultater
        self.models_text.delete('1.0', tk.END)
        self.history_text.delete('1.0', tk.END)

        # Sjekk etter chat-sesjoner
        chat_dir = os.path.join(workspace_path, "chatSessions")
        if os.path.exists(chat_dir):
            detected_models = set()  # Unike modeller
            for chat_file in os.listdir(chat_dir):
                if chat_file.endswith('.json'):
                    chat_path = os.path.join(chat_dir, chat_file)
                    try:
                        with open(chat_path, 'r', encoding='utf-8') as f:
                            chat_data = json.load(f)

                            # Ekstraher AI-modell-informasjon
                            if 'requests' in chat_data:
                                for request in chat_data.get('requests', []):
                                    # Sjekk agent/modell info i request
                                    if 'agent' in request:
                                        agent = request['agent']
                                        if 'name' in agent:
                                            detected_models.add(f"AGENT: {agent['name']}")
                                        if 'extensionDisplayName' in agent:
                                            detected_models.add(f"EXTENSION: {agent['extensionDisplayName']}")

                                    # Sjekk etter modellnavn i response
                                    if 'response' in request:
                                        responses = request['response']
                                        for resp in responses:
                                            if isinstance(resp, dict) and 'model' in resp:
                                                detected_models.add(f"MODEL: {resp['model']}")

                            # Vis chat-historikk sammendrag
                            self.history_text.insert(tk.END,
                                f"DIALOG-ARKIV: {chat_file}\n")
                            num_messages = len(chat_data.get('requests', [])) if 'requests' in chat_data else 0
                            self.history_text.insert(tk.END,
                                f"INTERAKSJONER: {num_messages}\n")
                            self.history_text.insert(tk.END,
                                f"SIST MODIFISERT: {datetime.fromtimestamp(os.path.getmtime(chat_path))}\n")
                            self.history_text.insert(tk.END, "-" * const_magic_50 + "\n")

                    except Exception as e:
                        self.history_text.insert(tk.END, f"FEIL VED LESING AV {chat_file}: {str(e)}\n")

            # Vis alle unike modeller
            for model in sorted(detected_models):
                self.models_text.insert(tk.END, f"{model}\n")

    def export_selected_chats(self):
        """Eksporterer valgte chat-sesjoner til en backup-mappe."""
        if not self.workspace_list.curselection():
            return

        selected = self.workspace_list.get(self.workspace_list.curselection())
        export_dir = os.path.join(os.path.expanduser("~"), "neural_archaeology_exports")
        os.makedirs(export_dir, exist_ok=True)

        # Finn workspace-stien
        for workspace_dir in os.listdir(self.VSCODE_STORAGE_PATH):
            workspace_path = os.path.join(self.VSCODE_STORAGE_PATH, workspace_dir)
            if os.path.isdir(workspace_path):
                workspace_json = os.path.join(workspace_path, "workspace.json")
                if os.path.exists(workspace_json):
                    with open(workspace_json, 'r', encoding='utf-8') as f:
                        try:
                            data = json.load(f)
                            if data.get('folder') == selected:
                                chat_dir = os.path.join(workspace_path, "chatSessions")
                                if os.path.exists(chat_dir):
                                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                                    backup_dir = os.path.join(export_dir, f"backup_{timestamp}")
                                    shutil.copytree(chat_dir, backup_dir)
                                    self.history_text.insert(tk.END,
                                        f"\nDIALOGER EKSPORTERT TIL: {backup_dir}\n")
                                break
                        except json.JSONDecodeError:
                            continue

    def import_chats(self):
        """Importerer chat-sesjoner fra backup."""

        pass

    def run(self):
        """Starter skanningen og GUI-loopen."""
        status = self.scan_workspaces()

        self.root.mainloop()

if __name__ == "__main__":
    scanner = NeuralArchaeologyScanner()
    scanner.run()
