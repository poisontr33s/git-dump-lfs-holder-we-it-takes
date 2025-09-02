#!/usr/bin/env python3

import json
import sys
from datetime import datetime
from pathlib import Path

# Auto-generated constants for magic numbers
const_magic_300 = 300
const_ten = 10

"""
🎭 PSYCHO-NOIR CODESPACES SESSION IMPORTER
Specialized tool for importing mobile sessions into GitHub Codespaces PWA environment
"""

class CodespacesSessionImporter:
    def __init__(self):
        self.workspace_root = Path.cwd()
        self.mobile_session_file = self.workspace_root / "data" / "current_session_context.json"
        self.session_files = list((self.workspace_root / "data" / "sessions").glob("*.json"))

    def extract_mobile_session_summary(self):
        """Extracts key points from mobile session for Copilot Chat context"""
        if not self.mobile_session_file.exists():

            return None

        with open(self.mobile_session_file, 'r', encoding='utf-8') as f:
            session_data = json.load(f)

        # Extract key information
        session_metadata = session_data.get("current_session", {}).get("session_metadata", {})
        achievements = session_data.get("current_session", {}).get("technical_achievements", [])

        summary = {
            "session_id": session_metadata.get("session_id"),
            "timestamp": session_metadata.get("timestamp"),
            "conversation_length": session_metadata.get("conversation_length"),
            "session_type": session_metadata.get("session_type"),
            "key_achievements": achievements[:const_ten],  # Top const_ten achievements
            "total_achievements": len(achievements)
        }

        return summary

    def generate_copilot_context_prompt(self):
        """Generates a context prompt that can be pasted into Copilot Chat"""
        summary = self.extract_mobile_session_summary()
        if not summary:
            return None

        prompt = f"""🎭 **iPHONE CODESPACES SESSION RESTORATION REQUEST**

**Context:** I was working on the Psycho-Noir Kontrapunkt project on my iPhone using a CUSTOM MOBILE PORTAL through GitHub Codespaces preview URL. The session data has been preserved in the backend but is not visible in the current standard Codespaces interface.

**iPhone Session Architecture:**
- **Access Method:** iPhone Safari → GitHub Codespaces Preview → Custom Mobile Portal (`mobile.html`)
- **Codespace Name:** fictional-parakeet-wrggxgxq949w35gq4
- **Mobile Portal:** Custom Psycho-Noir interface optimized for touch
- **Session Storage:** Backend Codespaces container + databases

**Mobile Session Details:**
- **Session ID:** {summary['session_id']}
- **Date:** {summary['timestamp']}
- **Conversations:** {summary['conversation_length']} exchanges
- **Type:** {summary['session_type']}
- **Achievements:** {summary['total_achievements']} technical milestones

**Key Technical Achievements from iPhone Session:**
"""

        for i, achievement in enumerate(summary['key_achievements'], 1):
            achievement_type = achievement.get('type', 'unknown')
            description = achievement.get('description', 'No description')
            level = achievement.get('level', 'N/A')

            if achievement_type == 'level_implementation':
                prompt += f"{i}. **Level {level}:** {description}\n"
            else:
                prompt += f"{i}. **{achievement_type.title()}:** {description}\n"

        prompt += """
**Files and Systems Created in Mobile Session:**
- Session Archaeology Engine (`backend/python/session_archaeology_engine.py`)
- Mobile Neural Interface (`LVL2_Frontend_Evolution/mobile_neural_interface.html`)
- VS Code Extension (`vscode-extension/`)
- Multiple database files and configuration systems

**Request:** Please help me continue this work by:
1. Understanding the context of these achievements
2. Identifying next logical steps
3. Helping me resume development where I left off on mobile

**Current Status:** All mobile session files have been merged into this Codespaces environment and are available in the workspace.
"""

        return prompt

    def create_session_summary_file(self):
        """Creates a markdown summary file for easy reference"""
        summary = self.extract_mobile_session_summary()
        if not summary:
            return None

        markdown_content = f"""# 🎭 Mobile Session Summary - Psycho-Noir Kontrapunkt

**Generated:** {datetime.now().isoformat()}
**Original Session:** {summary['session_id']}
**Mobile Timestamp:** {summary['timestamp']}

## Session Overview
- **Type:** {summary['session_type']}
- **Duration:** {summary['conversation_length']} conversations
- **Achievements:** {summary['total_achievements']} technical milestones

## Key Technical Achievements

"""

        for i, achievement in enumerate(summary['key_achievements'], 1):
            achievement_type = achievement.get('type', 'unknown')
            description = achievement.get('description', 'No description')
            level = achievement.get('level', 'N/A')

            markdown_content += f"### {i}. {achievement_type.title()}"
            if level != 'N/A':
                markdown_content += f" (Level {level})"
            markdown_content += f"\n{description}\n\n"

        markdown_content += """## How to Use This Summary

1. **Copy the context prompt below and paste it into GitHub Copilot Chat**
2. **Reference specific achievements when asking follow-up questions**
3. **Use the session ID for detailed queries about specific implementations**

## Context Prompt for Copilot Chat

```
"""
        context_prompt = self.generate_copilot_context_prompt()
        if context_prompt:
            markdown_content += context_prompt
        markdown_content += """
```

## Next Steps

- [ ] Review mobile session achievements
- [ ] Identify current development priorities
- [ ] Resume work on incomplete features
- [ ] Test imported systems in Codespaces environment

---
*Generated by Psycho-Noir Session Archaeology System*
"""

        summary_file = self.workspace_root / "MOBILE_SESSION_SUMMARY.md"
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write(markdown_content)

        return summary_file

    def run_import(self):
        """Main import process"""

        # Check mobile session availability

        print(f"📂 Additional sessions: {len(self.session_files)} files")

        if not self.mobile_session_file.exists():

            return False

        # Generate summary and context
        summary_file = self.create_session_summary_file()
        context_prompt = self.generate_copilot_context_prompt()

        if summary_file and context_prompt:

            print("1. Open GitHub Copilot Chat (Ctrl+Shift+I)")

            print(context_prompt[:const_magic_300] + "..." if len(context_prompt) > const_magic_300 else context_prompt)

            return True
        else:

            return False

if __name__ == "__main__":
    importer = CodespacesSessionImporter()
    success = importer.run_import()
    sys.exit(0 if success else 1)
