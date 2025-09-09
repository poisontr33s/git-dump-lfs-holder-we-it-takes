#!/usr/bin/env python3

import os
import json
import time

const_magic_3600 = 3600
const_magic_300 = 300
const_magic_48 = 48
const_magic_24 = 24

"""
🎭 MISSING CONTENT DETECTOR - Find Lost Discussions & Interactions
Detects content that exists in workspace but isn't captured in session logs
"""
import re
from datetime import datetime, timedelta

class MissingContentDetector:
    def __init__(self):
        self.technical_keywords = [
            'elixir', 'Elixir', 'GenServer', 'OTP', 'concurrent', 'actor',
            'migration', 'architecture', 'implementation', 'system',
            'processing', 'framework', 'infrastructure', 'refactor',
            'optimize', 'performance', 'scalability', 'deployment'
        ]

        self.session_indicators = [
            'session', 'discussion', 'conversation', 'chat', 'interaction',
            'requirement', 'specification', 'plan', 'strategy', 'decision'
        ]

    def scan_recent_modifications(self, hours=const_magic_24):
        """Scan for files modified in last N hours"""
        cutoff_time = time.time() - (hours * const_magic_3600)
        recent_files = []

        for root, dirs, files in os.walk('.'):
            # Skip hidden and system directories
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', '__pycache__']]

            for file in files:
                if file.endswith(('.md', '.py', '.json', '.txt', '.yml', '.yaml')):
                    filepath = os.path.join(root, file)
                    try:
                        stat = os.stat(filepath)
                        if stat.st_mtime > cutoff_time:
                            recent_files.append({
                                'path': filepath,
                                'modified': datetime.fromtimestamp(stat.st_mtime),
                                'size': stat.st_size
                            })
                    except:
                        pass

        return sorted(recent_files, key=lambda x: x['modified'], reverse=True)

    def analyze_technical_discussions(self, files):
        """Analyze files for technical discussions"""
        technical_discussions = []

        for file_info in files:
            filepath = file_info['path']
            if not filepath.endswith('.md'):
                continue

            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()

                found_keywords = [kw for kw in self.technical_keywords if kw in content]
                session_indicators = [si for si in self.session_indicators if si in content]

                if found_keywords:
                    # Extract key sections
                    lines = content.split('\n')
                    key_sections = []

                    for i, line in enumerate(lines):
                        if any(kw in line for kw in found_keywords):
                            # Extract context around keyword
                            start = max(0, i-2)
                            end = min(len(lines), i+3)
                            context = '\n'.join(lines[start:end])
                            key_sections.append({
                                'line': i+1,
                                'context': context,
                                'keywords': [kw for kw in found_keywords if kw in line]
                            })

                    technical_discussions.append({
                        'file': filepath,
                        'modified': file_info['modified'],
                        'size': file_info['size'],
                        'keywords_found': found_keywords,
                        'session_indicators': session_indicators,
                        'key_sections': key_sections,
                        'content_preview': content[:const_magic_300] + '...' if len(content) > const_magic_300 else content,
                        'is_session_related': len(session_indicators) > 0
                    })
            except:
                pass

        return technical_discussions

    def detect_missing_sessions(self):
        """Main detection method"""

        # Scan recent files
        recent_files = self.scan_recent_modifications(const_magic_48)  # Last const_magic_48 hours
        print(f"📁 Found {len(recent_files)} recently modified files")

        technical_discussions = self.analyze_technical_discussions(recent_files)
        print(f"🎯 Found {len(technical_discussions)} files with technical content")

        # Identify high-priority missing content
        high_priority = []
        for disc in technical_discussions:
            if disc['is_session_related'] and len(disc['keywords_found']) >= 3:
                high_priority.append(disc)

        print(f"🚨 Found {len(high_priority)} high-priority missing discussions")

        return {
            'recent_files': recent_files,
            'technical_discussions': technical_discussions,
            'high_priority_missing': high_priority,
            'summary': {
                'total_recent_files': len(recent_files),
                'technical_files': len(technical_discussions),
                'session_related': len([d for d in technical_discussions if d['is_session_related']]),
                'high_priority': len(high_priority)
            }
        }

    def save_detection_report(self, results):
        """Save detection results"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_file = f'data/missing_content_report_{timestamp}.json'

        # Ensure data directory exists
        os.makedirs('data', exist_ok=True)

        json_results = self._prepare_for_json(results)

        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(json_results, f, indent=2, ensure_ascii=False)

        return report_file

    def _prepare_for_json(self, obj):
        """Convert datetime objects to strings for JSON serialization"""
        if isinstance(obj, dict):
            return {k: self._prepare_for_json(v) for k, v in obj.items()}
            return [self._prepare_for_json(item) for item in obj]
            return obj.isoformat()
        else:
            return obj

    def generate_recovery_prompt(self, results):
        """Generate a prompt for recovering missing content"""
        high_priority = results['high_priority_missing']

        if not high_priority:
            return "No high-priority missing content detected."

        prompt = "🎭 **MISSING CONTENT RECOVERY PROMPT**\n\n"
        prompt += f"**Detected {len(high_priority)} missing discussions that should be in session logs:**\n\n"

        for i, disc in enumerate(high_priority, 1):
            prompt += f"### **{i}. {os.path.basename(disc['file'])}**\n"
            prompt += f"- **Modified:** {disc['modified']}\n"
            prompt += f"- **Keywords:** {', '.join(disc['keywords_found'])}\n"
            prompt += f"- **Content Preview:**\n```\n{disc['content_preview']}\n```\n\n"

        prompt += "**Action Required:**\n"
        prompt += "These discussions contain technical implementation details that should be captured in session continuity for future reference and optimization.\n\n"

        return prompt

def main():
    detector = MissingContentDetector()
    results = detector.detect_missing_sessions()

    # Print summary

    # Save report
    report_file = detector.save_detection_report(results)

    if results['high_priority_missing']:
        recovery_prompt = detector.generate_recovery_prompt(results)

        # Save recovery prompt
        prompt_file = f"data/missing_content_recovery_prompt_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        with open(prompt_file, 'w', encoding='utf-8') as f:
            f.write(recovery_prompt)

    return results

if __name__ == "__main__":
    main()
