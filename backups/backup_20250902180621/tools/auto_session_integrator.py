#!/usr/bin/env python3
"""
🎭 AUTOMATIC SESSION CONTENT INTEGRATION SYSTEM
Automatically captures and integrates missing discussions into session continuity
"""

import os
import json
import time
import hashlib
from datetime import datetime
from pathlib import Path

class AutoSessionIntegrator:
    def __init__(self):
        self.session_db_path = "data/session_content_db.json"
        self.integration_log = "data/integration_log.json"
        self.tracked_files = set()
        self.content_signatures = {}

        # Load existing database
        self.load_session_db()

    def load_session_db(self):
        """Load existing session content database"""
        if os.path.exists(self.session_db_path):
            try:
                with open(self.session_db_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.tracked_files = set(data.get('tracked_files', []))
                    self.content_signatures = data.get('content_signatures', {})
            except:
                pass

    def save_session_db(self):
        """Save session content database"""
        os.makedirs('data', exist_ok=True)
        data = {
            'tracked_files': list(self.tracked_files),
            'content_signatures': self.content_signatures,
            'last_updated': datetime.now().isoformat()
        }
        with open(self.session_db_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def get_content_signature(self, filepath):
        """Generate unique signature for file content"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            return hashlib.md5(content.encode('utf-8')).hexdigest()
        except:
            return None

    def detect_new_content(self):
        """Detect new or modified content that should be tracked"""
        new_content = []

        # Scan for markdown files with session-relevant content
        for root, dirs, files in os.walk('.'):
            # Skip hidden and system directories
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', '__pycache__']]

            for file in files:
                if file.endswith('.md'):
                    filepath = os.path.join(root, file)

                    # Check if this is a new file or content has changed
                    current_signature = self.get_content_signature(filepath)
                    if not current_signature:
                        continue

                    stored_signature = self.content_signatures.get(filepath)

                    if filepath not in self.tracked_files or stored_signature != current_signature:
                        # This is new or modified content
                        try:
                            with open(filepath, 'r', encoding='utf-8') as f:
                                content = f.read()

                            # Check if it contains technical/session content
                            if self.is_session_relevant(content):
                                new_content.append({
                                    'filepath': filepath,
                                    'content': content,
                                    'signature': current_signature,
                                    'size': len(content),
                                    'is_new': filepath not in self.tracked_files,
                                    'modified_time': os.path.getmtime(filepath)
                                })

                                # Update tracking
                                self.tracked_files.add(filepath)
                                self.content_signatures[filepath] = current_signature
                        except:
                            pass

        return new_content

    def is_session_relevant(self, content):
        """Determine if content is relevant for session tracking"""
        session_keywords = [
            'elixir', 'migration', 'implementation', 'architecture', 'framework',
            'system', 'discussion', 'session', 'conversation', 'plan', 'strategy',
            'GenServer', 'OTP', 'concurrent', 'actor', 'processing', 'optimization'
        ]

        content_lower = content.lower()
        keyword_count = sum(1 for keyword in session_keywords if keyword in content_lower)

        # Content is relevant if it has multiple technical keywords
        return keyword_count >= 3

    def create_session_summary(self, content_list):
        """Create a comprehensive session summary from detected content"""
        if not content_list:
            return None

        summary = {
            'timestamp': datetime.now().isoformat(),
            'total_files': len(content_list),
            'total_content_size': sum(item['size'] for item in content_list),
            'new_files': len([item for item in content_list if item['is_new']]),
            'modified_files': len([item for item in content_list if not item['is_new']]),
            'content_items': []
        }

        for item in content_list:
            # Extract key information from content
            lines = item['content'].split('\n')
            headers = [line for line in lines if line.startswith('#')]
            first_paragraph = ""

            for line in lines:
                if line.strip() and not line.startswith('#') and not line.startswith('```'):
                    first_paragraph = line.strip()
                    break

            summary['content_items'].append({
                'file': item['filepath'],
                'is_new': item['is_new'],
                'size': item['size'],
                'headers': headers[:5],  # First 5 headers
                'summary': first_paragraph,
                'keywords_detected': self.extract_keywords(item['content']),
                'last_modified': datetime.fromtimestamp(item['modified_time']).isoformat()
            })

        return summary

    def extract_keywords(self, content):
        """Extract relevant keywords from content"""
        keywords = [
            'elixir', 'Elixir', 'GenServer', 'OTP', 'concurrent', 'actor',
            'migration', 'architecture', 'implementation', 'system',
            'processing', 'framework', 'infrastructure', 'optimization',
            'session', 'discussion', 'plan', 'strategy', 'design'
        ]

        found_keywords = []
        content_lower = content.lower()

        for keyword in keywords:
            if keyword.lower() in content_lower:
                found_keywords.append(keyword)

        return found_keywords

    def generate_copilot_integration_prompt(self, summary):
        """Generate a prompt for integrating content into Copilot session"""
        if not summary:
            return "No new session content detected."

        prompt = f"🎭 **AUTO-DETECTED SESSION CONTENT INTEGRATION**\n\n"
        prompt += f"**Detected {summary['total_files']} files with session-relevant content:**\n\n"

        for item in summary['content_items']:
            status = "🆕 NEW" if item['is_new'] else "🔄 MODIFIED"
            prompt += f"### **{status}: {os.path.basename(item['file'])}**\n"
            prompt += f"- **Size:** {item['size']} characters\n"
            prompt += f"- **Keywords:** {', '.join(item['keywords_detected'])}\n"
            prompt += f"- **Summary:** {item['summary']}\n"

            if item['headers']:
                prompt += f"- **Key Sections:** {', '.join(item['headers'][:3])}\n"

            prompt += f"- **Last Modified:** {item['last_modified']}\n\n"

        prompt += f"**Integration Request:**\n"
        prompt += f"Please incorporate these {summary['total_files']} technical discussions into the active session context for:\n"
        prompt += f"- Continuity tracking and reference\n"
        prompt += f"- Future optimization and development\n"
        prompt += f"- Cross-session knowledge retention\n\n"

        return prompt

    def log_integration(self, summary, prompt):
        """Log the integration for audit trail"""
        integration_entry = {
            'timestamp': datetime.now().isoformat(),
            'summary': summary,
            'prompt_generated': prompt,
            'integration_id': hashlib.md5(str(summary).encode()).hexdigest()[:8]
        }

        # Load existing log
        integration_history = []
        if os.path.exists(self.integration_log):
            try:
                with open(self.integration_log, 'r', encoding='utf-8') as f:
                    integration_history = json.load(f)
            except:
                pass

        integration_history.append(integration_entry)

        # Save updated log
        os.makedirs('data', exist_ok=True)
        with open(self.integration_log, 'w', encoding='utf-8') as f:
            json.dump(integration_history, f, indent=2, ensure_ascii=False)

        return integration_entry['integration_id']

    def run_auto_integration(self):
        """Main method to run automatic session content integration"""

        # Detect new content
        new_content = self.detect_new_content()

        if not new_content:

            return None

        print(f"🎯 Detected {len(new_content)} files with session content")

        # Create summary
        summary = self.create_session_summary(new_content)

        # Generate integration prompt
        prompt = self.generate_copilot_integration_prompt(summary)

        # Log integration
        integration_id = self.log_integration(summary, prompt)

        # Save updated database
        self.save_session_db()

        # Save integration prompt
        prompt_file = f"data/auto_integration_prompt_{integration_id}.md"
        with open(prompt_file, 'w', encoding='utf-8') as f:
            f.write(prompt)

        # Display summary

        return {
            'summary': summary,
            'prompt': prompt,
            'integration_id': integration_id,
            'prompt_file': prompt_file
        }

def main():
    integrator = AutoSessionIntegrator()
    result = integrator.run_auto_integration()

    if result:

    return result

if __name__ == "__main__":
    main()
