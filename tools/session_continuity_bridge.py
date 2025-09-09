#!/usr/bin/env python3
"""
🌊 SESSION CONTINUITY BRIDGE

Komplett system for å linke sammen retroactive analysis, real-time tracking,
og cross-platform session continuity for optimal development flow.
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
import subprocess

class SessionContinuityBridge:
    """
    Master controller for session tracking og optimization across all platforms
    """
    
    def __init__(self, workspace_path: str = "/workspaces/PsychoNoir-Kontrapunkt"):
        self.workspace_path = Path(workspace_path)
        self.data_dir = self.workspace_path / "data"
        self.session_db_path = self.data_dir / "session_continuity_database.json"
        
        # Initialize session database
        self.session_database = self.load_session_database()
        
        # Track active sessions
        self.active_sessions = {}
        
        print("🌊 Session Continuity Bridge initialized")
    
    def load_session_database(self) -> Dict[str, Any]:
        """Load eller create session database"""
        if self.session_db_path.exists():
            with open(self.session_db_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            return {
                'optimization_chains': {},
                'cross_platform_links': {},
                'implementation_tracking': {},
                'decision_genealogy': {},
                'created': datetime.now().isoformat()
            }
    
    def save_session_database(self):
        """Save session database til disk"""
        self.data_dir.mkdir(exist_ok=True)
        with open(self.session_db_path, 'w', encoding='utf-8') as f:
            json.dump(self.session_database, f, indent=2, ensure_ascii=False)
    
    def register_session(self, 
                        session_id: str, 
                        platform: str, 
                        session_data: Dict[str, Any],
                        parent_session: Optional[str] = None) -> str:
        """
        Register ny session i continuity database
        """
        registration = {
            'session_id': session_id,
            'platform': platform,
            'registered_timestamp': datetime.now().isoformat(),
            'parent_session': parent_session,
            'child_sessions': [],
            'session_metadata': session_data,
            'optimization_score': self.calculate_session_optimization_score(session_data),
            'continuity_links': [],
            'implementation_status': 'active'
        }
        
        # Link til parent session
        if parent_session and parent_session in self.session_database['sessions']:
            self.session_database['sessions'][parent_session]['child_sessions'].append(session_id)
        
        self.session_database['sessions'][session_id] = registration
        self.save_session_database()
        
        print(f"✅ Session registered: {session_id} ({platform})")
        return session_id
    
    def create_continuity_link(self, 
                             from_session: str, 
                             to_session: str, 
                             link_type: str,
                             context: str = ""):
        """
        Create explicit continuity link between sessions
        """
        link = {
            'from_session': from_session,
            'to_session': to_session,
            'link_type': link_type,  # 'continuation', 'optimization', 'implementation', 'reference'
            'context': context,
            'created': datetime.now().isoformat()
        }
        
        if from_session in self.session_database['sessions']:
            self.session_database['sessions'][from_session]['continuity_links'].append(link)
        
        if to_session in self.session_database['sessions']:
            self.session_database['sessions'][to_session]['continuity_links'].append({
                **link,
                'direction': 'incoming'
            })
        
        self.save_session_database()
        print(f"🔗 Continuity link created: {from_session} → {to_session} ({link_type})")
    
    def track_implementation_progress(self, 
                                    session_id: str, 
                                    implementation_item: str,
                                    status: str):
        """
        Track implementation progress from decisions
        """
        if session_id not in self.session_database['implementation_tracking']:
            self.session_database['implementation_tracking'][session_id] = {}
        
        self.session_database['implementation_tracking'][session_id][implementation_item] = {
            'status': status,  # 'planned', 'in_progress', 'completed', 'abandoned'
            'timestamp': datetime.now().isoformat(),
            'session_origin': session_id
        }
        
        self.save_session_database()
        print(f"📋 Implementation tracked: {implementation_item} = {status}")
    
    def analyze_decision_genealogy(self, concept: str) -> Dict[str, Any]:
        """
        Trace genealogy av specific concept across sessions
        """
        genealogy = {
            'concept': concept,
            'origin_sessions': [],
            'evolution_chain': [],
            'current_status': 'unknown',
            'optimization_trajectory': []
        }
        
        for session_id, session_data in self.session_database['sessions'].items():
            session_content = json.dumps(session_data).lower()
            
            if concept.lower() in session_content:
                genealogy['origin_sessions'].append({
                    'session_id': session_id,
                    'platform': session_data.get('platform', 'unknown'),
                    'timestamp': session_data.get('registered_timestamp', ''),
                    'optimization_score': session_data.get('optimization_score', 0)
                })
        
        genealogy['origin_sessions'].sort(key=lambda x: x['timestamp'])
        genealogy['evolution_chain'] = [s['session_id'] for s in genealogy['origin_sessions']]
        
        return genealogy
    
    def generate_optimization_recommendations(self) -> List[Dict[str, Any]]:
        """
        Generate optimization recommendations basert på session analysis
        """
        recommendations = []
        
        high_value_sessions = [
            (sid, sdata) for sid, sdata in self.session_database['sessions'].items()
            if sdata.get('optimization_score', 0) > 0.7
        ]
        
        # Identify incomplete implementations
        incomplete_implementations = []
        for session_id, implementations in self.session_database['implementation_tracking'].items():
            for item, status_data in implementations.items():
                if status_data['status'] in ['planned', 'in_progress']:
                    incomplete_implementations.append({
                        'item': item,
                        'session': session_id,
                        'status': status_data['status'],
                        'age_days': (datetime.now() - datetime.fromisoformat(status_data['timestamp'])).days
                    })
        
        # Generate recommendations
        if incomplete_implementations:
            recommendations.append({
                'type': 'implementation_urgency',
                'priority': 'high',
                'title': 'Complete Pending Implementations',
                'details': f"{len(incomplete_implementations)} pending implementations found",
                'actions': [impl['item'] for impl in incomplete_implementations[:5]]
            })
        
        if high_value_sessions:
            latest_high_value = max(high_value_sessions, key=lambda x: x[1].get('registered_timestamp', ''))
            recommendations.append({
                'type': 'continue_high_value',
                'priority': 'medium',
                'title': 'Continue High-Value Session',
                'details': f"Session {latest_high_value[0]} had optimization score {latest_high_value[1].get('optimization_score', 0):.2f}",
                'actions': ['Resume development', 'Review decisions', 'Implement next steps']
            })
        
        return recommendations
    
    def calculate_session_optimization_score(self, session_data: Dict[str, Any]) -> float:
        """
        Calculate overall optimization score for session
        """
        score = 0.0
        
        # Base score from content analysis
        if 'optimization_score' in session_data:
            score += session_data['optimization_score'] * 0.4
        
        # Implementation ratio
        if 'implementation_ratio' in session_data:
            score += session_data['implementation_ratio'] * 0.3
        
        # Decision tracking
        if 'decision_points' in session_data:
            decision_count = len(session_data['decision_points'])
            score += min(decision_count / 10, 0.2)  # Max 0.2 for decisions
        
        # Technical depth
        if 'technical_depth' in session_data:
            depth_score = {'high': 0.1, 'medium': 0.05, 'low': 0.0}
            score += depth_score.get(session_data['technical_depth'], 0)
        
        return min(score, 1.0)
    
    def import_mobile_session(self, mobile_session_path: str) -> str:
        """
        Import mobile session into continuity system
        """
        try:
            with open(mobile_session_path, 'r', encoding='utf-8') as f:
                mobile_data = json.load(f)
            
            session_id = f"mobile_{mobile_data.get('session_id', 'unknown')}"
            
            # Register mobile session
            self.register_session(
                session_id=session_id,
                platform='mobile_codespaces',
                session_data=mobile_data
            )
            
            print(f"📱 Mobile session imported: {session_id}")
            return session_id
            
        except Exception as e:
            print(f"❌ Error importing mobile session: {e}")
            return ""
    
    def import_retroactive_analysis(self, analysis_path: str) -> str:
        """
        Import retroactive analysis into continuity system
        """
        try:
            with open(analysis_path, 'r', encoding='utf-8') as f:
                analysis_data = json.load(f)
            
            # Register each analyzed file as session
            imported_sessions = []
            
            for file_analysis in analysis_data.get('files_analyzed', []):
                file_path = Path(file_analysis['file_path']).name
                session_id = f"retroactive_{file_path}_{int(datetime.now().timestamp())}"
                
                self.register_session(
                    session_id=session_id,
                    platform='retroactive_analysis',
                    session_data=file_analysis
                )
                
                imported_sessions.append(session_id)
            
            print(f"📊 Retroactive analysis imported: {len(imported_sessions)} sessions")
            return f"batch_{len(imported_sessions)}_sessions"
            
        except Exception as e:
            print(f"❌ Error importing retroactive analysis: {e}")
            return ""
    
    def generate_session_continuity_report(self) -> Dict[str, Any]:
        """
        Generate comprehensive session continuity report
        """
        total_sessions = len(self.session_database['sessions'])
        platforms = {}
        optimization_scores = []
        
        for session_data in self.session_database['sessions'].values():
            platform = session_data.get('platform', 'unknown')
            platforms[platform] = platforms.get(platform, 0) + 1
            
            opt_score = session_data.get('optimization_score', 0)
            if opt_score > 0:
                optimization_scores.append(opt_score)
        
        avg_optimization = sum(optimization_scores) / len(optimization_scores) if optimization_scores else 0
        
        # Implementation tracking summary
        total_implementations = 0
        completed_implementations = 0
        
        for implementations in self.session_database['implementation_tracking'].values():
            for status_data in implementations.values():
                total_implementations += 1
                if status_data['status'] == 'completed':
                    completed_implementations += 1
        
        implementation_completion_rate = completed_implementations / total_implementations if total_implementations > 0 else 0
        
        report = {
            'report_timestamp': datetime.now().isoformat(),
            'session_overview': {
                'total_sessions': total_sessions,
                'platforms': platforms,
                'average_optimization_score': avg_optimization,
                'high_value_sessions': len([s for s in optimization_scores if s > 0.7])
            },
            'implementation_tracking': {
                'total_implementations': total_implementations,
                'completed_implementations': completed_implementations,
                'completion_rate': implementation_completion_rate,
                'pending_implementations': total_implementations - completed_implementations
            },
            'continuity_health': {
                'linked_sessions': len([s for s in self.session_database['sessions'].values() if s.get('continuity_links')]),
                'orphaned_sessions': len([s for s in self.session_database['sessions'].values() if not s.get('continuity_links') and not s.get('parent_session')]),
                'continuity_ratio': 0.0  # Calculate based on linked vs total
            },
            'recommendations': self.generate_optimization_recommendations()
        }
        
        # Calculate continuity ratio
        linked_sessions = report['continuity_health']['linked_sessions']
        report['continuity_health']['continuity_ratio'] = linked_sessions / total_sessions if total_sessions > 0 else 0
        
        return report
    
    def create_copilot_chat_import_prompt(self, target_sessions: List[str] = None) -> str:
        """
        Create optimized import prompt for Copilot Chat basert på session tracking
        """
        if not target_sessions:
            # Select highest value sessions automatically
            high_value_sessions = [
                (sid, sdata) for sid, sdata in self.session_database['sessions'].items()
                if sdata.get('optimization_score', 0) > 0.6
            ]
            high_value_sessions.sort(key=lambda x: x[1].get('optimization_score', 0), reverse=True)
            target_sessions = [sid for sid, _ in high_value_sessions[:3]]  # Top 3
        
        prompt_sections = [
            "🎭 **COMPREHENSIVE SESSION RESTORATION**",
            "",
            "**Context:** I need to restore and continue my development work with full session tracking context.",
            "",
            "**Session Continuity Overview:**"
        ]
        
        for session_id in target_sessions:
            if session_id in self.session_database['sessions']:
                session = self.session_database['sessions'][session_id]
                prompt_sections.extend([
                    f"",
                    f"### **Session: {session_id}**",
                    f"- **Platform:** {session.get('platform', 'unknown')}",
                    f"- **Optimization Score:** {session.get('optimization_score', 0):.2%}",
                    f"- **Timestamp:** {session.get('registered_timestamp', 'unknown')}",
                    f"- **Implementation Status:** {session.get('implementation_status', 'unknown')}"
                ])
                
                metadata = session.get('session_metadata', {})
                if 'key_concepts' in metadata:
                    prompt_sections.append(f"- **Key Concepts:** {', '.join(metadata['key_concepts'][:5])}")
                
                if 'decision_points' in metadata:
                    decision_count = len(metadata['decision_points'])
                    prompt_sections.append(f"- **Decision Points:** {decision_count} tracked decisions")
        
        # Add implementation tracking
        prompt_sections.extend([
            "",
            "### **Implementation Backlog:**"
        ])
        
        pending_implementations = []
        for session_id, implementations in self.session_database['implementation_tracking'].items():
            for item, status_data in implementations.items():
                if status_data['status'] in ['planned', 'in_progress']:
                    pending_implementations.append(f"- **{item}** ({status_data['status']})")
        
        if pending_implementations:
            prompt_sections.extend(pending_implementations[:5])
        else:
            prompt_sections.append("- No pending implementations")
        
        # Add optimization recommendations
        recommendations = self.generate_optimization_recommendations()
        if recommendations:
            prompt_sections.extend([
                "",
                "### **Optimization Recommendations:**"
            ])
            
            for rec in recommendations[:3]:
                prompt_sections.append(f"- **{rec['title']}** ({rec['priority']} priority)")
        
        prompt_sections.extend([
            "",
            "**Ready to continue development with full session tracking context!**"
        ])
        
        return '\n'.join(prompt_sections)

def main():
    """
    Demonstration av Session Continuity Bridge
    """
    bridge = SessionContinuityBridge()
    
    print("🌊 SESSION CONTINUITY BRIDGE DEMO")
    print("=" * 50)
    
    # Import existing retroactive analysis
    analysis_path = "/workspaces/PsychoNoir-Kontrapunkt/data/session_content_analysis.json"
    if Path(analysis_path).exists():
        bridge.import_retroactive_analysis(analysis_path)
    
    # Import any live sessions
    live_sessions_dir = Path("/workspaces/PsychoNoir-Kontrapunkt/data/live_sessions")
    if live_sessions_dir.exists():
        for session_file in live_sessions_dir.glob("*.json"):
            print(f"📱 Importing live session: {session_file.name}")
    
    # Generate continuity report
    report = bridge.generate_session_continuity_report()
    
    print(f"\n📊 SESSION CONTINUITY REPORT:")
    print(f"  Total sessions: {report['session_overview']['total_sessions']}")
    print(f"  Average optimization: {report['session_overview']['average_optimization_score']:.2%}")
    print(f"  Implementation completion: {report['implementation_tracking']['completion_rate']:.2%}")
    print(f"  Continuity ratio: {report['continuity_health']['continuity_ratio']:.2%}")
    
    import_prompt = bridge.create_copilot_chat_import_prompt()
    
    prompt_path = Path("/workspaces/PsychoNoir-Kontrapunkt/COPILOT_CHAT_IMPORT_PROMPT.md")
    with open(prompt_path, 'w', encoding='utf-8') as f:
        f.write(import_prompt)
    
    print(f"\n✅ Copilot Chat import prompt saved: {prompt_path}")
    print(f"\n🎯 RECOMMENDATIONS:")
    for rec in report['recommendations'][:3]:
        print(f"  {rec['priority'].upper()}: {rec['title']}")
    
    return bridge

if __name__ == "__main__":
    main()
