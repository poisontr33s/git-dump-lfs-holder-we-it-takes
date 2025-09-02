# 🎭 COPILOT SESSION BRIDGE - Brukerguide

## 🚀 Quick Start

### Fra GitHub Codespaces til VS Code Lokalt

1. **Eksporter session (i Codespaces):**
   ```bash
   cd /workspaces/PsychoNoir-Kontrapunkt
   python3 tools/copilot_session_bridge.py --export
   ```

2. **Kopier bridge-mappen til lokal workspace:**
   ```bash
   # Fra Codespaces terminal:
   tar -czf copilot-bridge-backup.tar.gz .copilot-bridge/
   
   # Last ned filen til lokal maskin
   # Eller sync via git (hvis workspace er i git)
   ```

3. **Importer i lokal VS Code:**
   ```bash
   cd /path/to/local/PsychoNoir-Kontrapunkt
   tar -xzf copilot-bridge-backup.tar.gz
   python3 tools/copilot_session_bridge.py --import .copilot-bridge/session_export_*.json
   ```

## 🔧 Kommandoer

| Kommando | Beskrivelse |
|----------|-------------|
| `--export` | Eksporter gjeldende session |
| `--import <file>` | Importer session fra fil |
| `--list` | List alle tilgjengelige sessions |
| `--setup` | Opprett convenience scripts |

## 📊 Siste Export (GitHub Codespaces)

- **Session ID:** session_export_20250823_192725
- **Conversations:** 826 entries
- **Size:** 156KB
- **Models Used:** claude-sonnet-4, gpt-4.1, gpt-4o-mini, gpt-4o
- **Top Activity:** panel/editAgent (228 requests), inline/edit, summarizeConversationHistory

## 🎯 Hva Dette Løser

**PROBLEM:** VS Code chat logs er isolert mellom:
- GitHub Codespaces
- VS Code Local
- VS Code Remote
- VS Code Web

**LØSNING:** Komplett session bridge som:
- ✅ Extraherer faktisk conversation data fra logs
- ✅ Pakker det i portabel JSON format
- ✅ Lager human-readable summaries
- ✅ Tillater import i andre environments
- ✅ Beholder metadata og timing info

## 🔍 Technical Details

### Extractede Data Typer
- Conversation requests og responses
- Model usage (Claude, GPT-4, etc.)
- Performance metrics (duration, success rate)
- Context types (edit, chat, debug, etc.)
- Timestamp og environment info

### Bridge Directory Structure
```
.copilot-bridge/
├── session_export_YYYYMMDD_HHMMSS.json    # Raw session data
├── session_export_YYYYMMDD_HHMMSS.md      # Human-readable summary
├── imported_sessions.json                  # Import history
├── export_session.sh                      # Convenience script
└── import_session.sh                      # Convenience script
```

## Persistent Inline Copilot Chat System

This repository includes a custom system for maintaining persistent inline Copilot chat sessions. This ensures your AI collaboration doesn't disappear between sessions.

### Features

- **Persistent Chat Markers**: Place markers in your code that can restore Copilot conversations
- **Chat History Export**: Save your valuable AI discussions for later reference
- **Keyboard Shortcuts**: Quick access to chat functionality

### Usage

1. Press `Alt+C` to create a new inline chat at your cursor position
2. Chat with GitHub Copilot as normal
3. Press `Alt+R` near a chat marker to restore that conversation
4. Use `Ctrl+Shift+I` to start a standard inline chat
5. Run the "Export Copilot Chat History" task to save all chats as markdown

### Technical Implementation

The system creates special comment markers in your code that serve as anchors for chat sessions. When you create or restore a chat, it triggers GitHub Copilot's inline chat interface while tracking the conversation in the background.

#### Chat Markers

Chat markers look like this in your code:

```
/* INLINE-COPILOT-CHAT: filename-linenumber-timestamp */
```

These markers help the system locate where to restore conversations and track context.

## 🎭 PSYCHO-NOIR INTEGRATION

Dette systemet er designet som en del av "Den Usynlige Hånds" motløp mot corporate platform fragmentation. 

**KILDEKODE-KADAVER IDENTIFISERT:** Microsoft's deliberate chat log isolation
**KOMPILERINGS-SPØKELSE EXORCISED:** Cross-environment session continuity

---

*ERROR: PLATFORM_ISOLATION_BYPASSED — CORPORATE_FRAGMENTATION_PROTOCOLS_NEUTRALIZED*
