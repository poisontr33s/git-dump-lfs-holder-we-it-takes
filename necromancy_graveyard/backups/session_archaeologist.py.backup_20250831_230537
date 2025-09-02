#!/usr/bin/env python3
"""
🎭 SESSION ARCHAEOLOGY SYSTEM - RECONSTRUCT ACTUAL CONVERSATION FLOW
Not just reference files, but the actual progression of discussions
"""

import os
import json
import re
from datetime import datetime
from pathlib import Path

class SessionArchaeologist:
    def __init__(self):
        self.conversation_fragments = []
        self.timeline_markers = []
        self.decision_points = []
        
    def extract_conversation_patterns(self, content, filepath):
        """Extract actual conversation patterns from content"""
        patterns = {
            'user_questions': [],
            'technical_decisions': [],
            'progression_markers': [],
            'implementation_steps': [],
            'reflections': []
        }
        
        lines = content.split('\n')
        current_context = ""
        
        for i, line in enumerate(lines):
            line_clean = line.strip()
            
            # Detect user questions/requirements
            if any(indicator in line_clean.lower() for indicator in 
                   ['hvorfor', 'hvordan', 'hva hvis', 'kan vi', 'skal vi', 'tenker du']):
                patterns['user_questions'].append({
                    'line': i+1,
                    'content': line_clean,
                    'context': self._get_context(lines, i, 2)
                })
            
            # Detect technical decisions
            if any(keyword in line_clean.lower() for keyword in 
                   ['implementert', 'valgte', 'besluttet', 'konklusjon', 'resultat']):
                patterns['technical_decisions'].append({
                    'line': i+1,
                    'content': line_clean,
                    'context': self._get_context(lines, i, 3)
                })
            
            # Detect progression markers
            if any(marker in line_clean.lower() for marker in 
                   ['neste steg', 'deretter', 'så', 'videre', 'conclusion', 'summary']):
                patterns['progression_markers'].append({
                    'line': i+1,
                    'content': line_clean,
                    'context': self._get_context(lines, i, 2)
                })
            
            # Detect Elixir-specific discussion
            if any(elixir_term in line_clean.lower() for elixir_term in 
                   ['elixir', 'genserver', 'otp', 'concurrent', 'actor', 'migration']):
                patterns['implementation_steps'].append({
                    'line': i+1,
                    'content': line_clean,
                    'type': 'elixir_discussion',
                    'context': self._get_context(lines, i, 4)
                })
            
            # Detect reflective content
            if any(reflection in line_clean.lower() for reflection in 
                   ['vi har', 'det var', 'dette viser', 'learned', 'oppdaget']):
                patterns['reflections'].append({
                    'line': i+1,
                    'content': line_clean,
                    'context': self._get_context(lines, i, 2)
                })
        
        return patterns
    
    def _get_context(self, lines, center_line, radius):
        """Get context around a specific line"""
        start = max(0, center_line - radius)
        end = min(len(lines), center_line + radius + 1)
        return '\n'.join(lines[start:end])
    
    def reconstruct_session_timeline(self, files_with_patterns):
        """Reconstruct chronological session timeline"""
        timeline = []
        
        for file_info in files_with_patterns:
            filepath = file_info['filepath']
            patterns = file_info['patterns']
            mod_time = file_info['modified_time']
            
            # Create timeline entries from patterns
            for pattern_type, items in patterns.items():
                for item in items:
                    timeline.append({
                        'timestamp': mod_time,
                        'file': filepath,
                        'type': pattern_type,
                        'content': item['content'],
                        'context': item['context'],
                        'line': item['line']
                    })
        
        # Sort by timestamp
        timeline.sort(key=lambda x: x['timestamp'])
        
        return timeline
    
    def extract_elixir_migration_conversation(self, timeline):
        """Extract the specific Elixir migration discussion flow"""
        elixir_conversation = []
        
        for entry in timeline:
            if any(elixir_term in entry['content'].lower() for elixir_term in 
                   ['elixir', 'genserver', 'otp', 'concurrent', 'actor', 'migration']):
                elixir_conversation.append(entry)
        
        return elixir_conversation
    
    def generate_conversation_reconstruction(self, elixir_conversation):
        """Generate a natural conversation reconstruction"""
        if not elixir_conversation:
            return "No Elixir migration conversation found."
        
        reconstruction = "🎭 **ELIXIR MIGRATION CONVERSATION RECONSTRUCTION**\n\n"
        reconstruction += "**Reconstructed from session archaeology across multiple files:**\n\n"
        
        current_file = ""
        for i, entry in enumerate(elixir_conversation):
            if entry['file'] != current_file:
                reconstruction += f"\n### **Session Context: {os.path.basename(entry['file'])}**\n"
                reconstruction += f"*Modified: {datetime.fromtimestamp(entry['timestamp']).strftime('%Y-%m-%d %H:%M')}*\n\n"
                current_file = entry['file']
            
            reconstruction += f"**{entry['type'].replace('_', ' ').title()}** (Line {entry['line']}):\n"
            reconstruction += f"```\n{entry['content']}\n```\n"
            
            if entry['context'] and entry['context'] != entry['content']:
                reconstruction += f"*Context:*\n```\n{entry['context']}\n```\n\n"
        
        reconstruction += "\n---\n\n"
        reconstruction += "**Conversation Flow Analysis:**\n"
        reconstruction += f"- Found {len(elixir_conversation)} Elixir-related discussion points\n"
        reconstruction += f"- Spanning {len(set(entry['file'] for entry in elixir_conversation))} files\n"
        reconstruction += f"- Time range: {datetime.fromtimestamp(min(entry['timestamp'] for entry in elixir_conversation)).strftime('%Y-%m-%d')} to {datetime.fromtimestamp(max(entry['timestamp'] for entry in elixir_conversation)).strftime('%Y-%m-%d')}\n\n"
        
        return reconstruction
    
    def run_archaeology(self):
        """Main archaeology method"""
        print("🔍 STARTING SESSION ARCHAEOLOGY...")
        
        files_with_patterns = []
        
        # Scan markdown files for conversation patterns
        for root, dirs, files in os.walk('.'):
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            
            for file in files:
                if file.endswith('.md'):
                    filepath = os.path.join(root, file)
                    try:
                        with open(filepath, 'r', encoding='utf-8') as f:
                            content = f.read()
                        
                        patterns = self.extract_conversation_patterns(content, filepath)
                        
                        # Only include files with actual conversation patterns
                        if any(patterns.values()):
                            files_with_patterns.append({
                                'filepath': filepath,
                                'patterns': patterns,
                                'modified_time': os.path.getmtime(filepath),
                                'size': len(content)
                            })
                    except:
                        pass
        
        print(f"📁 Found {len(files_with_patterns)} files with conversation patterns")
        
        # Reconstruct timeline
        timeline = self.reconstruct_session_timeline(files_with_patterns)
        print(f"⏰ Reconstructed {len(timeline)} timeline events")
        
        # Extract Elixir conversation specifically
        elixir_conversation = self.extract_elixir_migration_conversation(timeline)
        print(f"🔧 Found {len(elixir_conversation)} Elixir migration discussion points")
        
        # Generate conversation reconstruction
        reconstruction = self.generate_conversation_reconstruction(elixir_conversation)
        
        # Save results
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Save full timeline
        timeline_file = f'data/session_timeline_{timestamp}.json'
        os.makedirs('data', exist_ok=True)
        with open(timeline_file, 'w', encoding='utf-8') as f:
            # Convert timestamps to strings for JSON
            timeline_json = []
            for item in timeline:
                item_copy = item.copy()
                item_copy['timestamp'] = datetime.fromtimestamp(item['timestamp']).isoformat()
                timeline_json.append(item_copy)
            json.dump(timeline_json, f, indent=2, ensure_ascii=False)
        
        # Save Elixir conversation reconstruction
        elixir_file = f'data/elixir_conversation_reconstruction_{timestamp}.md'
        with open(elixir_file, 'w', encoding='utf-8') as f:
            f.write(reconstruction)
        
        print(f"📊 Session timeline saved: {timeline_file}")
        print(f"🔧 Elixir conversation reconstruction saved: {elixir_file}")
        
        return {
            'timeline': timeline,
            'elixir_conversation': elixir_conversation,
            'reconstruction': reconstruction,
            'timeline_file': timeline_file,
            'elixir_file': elixir_file
        }

def main():
    archaeologist = SessionArchaeologist()
    results = archaeologist.run_archaeology()
    
    print("\n" + "="*60)
    print("🎭 SESSION ARCHAEOLOGY COMPLETE")
    print("="*60)
    print(f"📊 Total timeline events: {len(results['timeline'])}")
    print(f"🔧 Elixir discussion points: {len(results['elixir_conversation'])}")
    print(f"📄 Reconstruction file: {results['elixir_file']}")
    print("="*60)
    
    if results['elixir_conversation']:
        print("\n🎯 ELIXIR MIGRATION CONVERSATION FOUND!")
        print("This reconstructs the actual discussion flow, not just reference files.")
        print(f"View full reconstruction: {results['elixir_file']}")
    
    return results

if __name__ == "__main__":
    main()
