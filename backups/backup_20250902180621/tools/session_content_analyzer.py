#!/usr/bin/env python3
"""
🧠 SESSION CONTENT RETROACTIVE ANALYZER

Systematisk analyse av existing session files for optimization tracking.
Extraherer faktisk conversation content, decisions, og optimization patterns.
"""

import json
import re
import os
from datetime import datetime
from typing import List, Dict, Tuple, Any
from pathlib import Path

class SessionContentAnalyzer:
    """
    Retroactive analysis av session content for optimization tracking
    """
    
    def __init__(self, workspace_path: str = "/workspaces/PsychoNoir-Kontrapunkt"):
        self.workspace_path = Path(workspace_path)
        self.session_database = {}
        self.optimization_patterns = {}
        self.decision_points = {}
        
        # Key indicators for decision points
        self.decision_indicators = [
            'implementere', 'bytte til', 'migrere', 'optimalisere',
            'fokusere på', 'prioritere', 'velge', 'bestemme',
            'elixir', 'automation', 'session tracking', 'github pages'
        ]
        
        # Optimization value indicators
        self.optimization_indicators = [
            'suksess', 'effektivitet', 'forbedring', 'optimization',
            'performance', 'resultat', 'metrics', 'tracking'
        ]
    
    def analyze_session_file(self, file_path: Path) -> Dict[str, Any]:
        """
        Analyser en session file og extract faktisk content
        """
        print(f"🔍 Analyzing session file: {file_path}")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            print(f"❌ Error reading {file_path}: {e}")
            return {}
        
        session_analysis = {
            'file_path': str(file_path),
            'file_size': len(content),
            'last_modified': datetime.fromtimestamp(file_path.stat().st_mtime).isoformat(),
            'content_chunks': self.extract_content_chunks(content),
            'decision_points': self.extract_decision_points(content),
            'optimization_patterns': self.extract_optimization_patterns(content),
            'key_concepts': self.extract_key_concepts(content),
            'conversation_flow': self.analyze_conversation_flow(content),
            'technical_implementations': self.extract_technical_implementations(content)
        }
        
        return session_analysis
    
    def extract_content_chunks(self, content: str) -> List[Dict[str, Any]]:
        """
        Extract logical content chunks from session file
        """
        chunks = []
        
        # Split på major headings (## eller ###)
        sections = re.split(r'\n#{2,3}\s+', content)
        
        for i, section in enumerate(sections):
            if len(section.strip()) < 50:  # Skip tiny sections
                continue
                
            chunk = {
                'chunk_id': f"chunk_{i}",
                'content': section.strip(),
                'word_count': len(section.split()),
                'char_count': len(section),
                'has_code': '```' in section,
                'has_decisions': any(indicator in section.lower() for indicator in self.decision_indicators),
                'optimization_value': self.calculate_optimization_value(section)
            }
            
            chunks.append(chunk)
        
        return chunks
    
    def extract_decision_points(self, content: str) -> List[Dict[str, Any]]:
        """
        Extract explicit decision points fra content
        """
        decisions = []
        lines = content.split('\n')
        
        for line_num, line in enumerate(lines):
            line_lower = line.lower()
            
            for indicator in self.decision_indicators:
                if indicator in line_lower:
                    # Extract context around decision
                    context_start = max(0, line_num - 2)
                    context_end = min(len(lines), line_num + 3)
                    context = '\n'.join(lines[context_start:context_end])
                    
                    decision = {
                        'line_number': line_num + 1,
                        'indicator': indicator,
                        'decision_line': line.strip(),
                        'context': context,
                        'impact_level': self.assess_decision_impact(context),
                        'implementation_status': self.assess_implementation_status(context)
                    }
                    
                    decisions.append(decision)
        
        return decisions
    
    def extract_optimization_patterns(self, content: str) -> List[Dict[str, Any]]:
        """
        Extract optimization patterns og success metrics
        """
        patterns = []
        
        # Look for percentage values (success metrics)
        percentage_matches = re.findall(r'(\d+\.?\d*)\s*%', content)
        for match in percentage_matches:
            if float(match) > 50:  # Only high-value metrics
                patterns.append({
                    'type': 'success_metric',
                    'value': float(match),
                    'context': 'percentage_success'
                })
        
        # Look for before/after comparisons
        comparison_patterns = re.findall(r'(\d+)\s*→\s*(\d+)', content)
        for before, after in comparison_patterns:
            improvement = ((int(before) - int(after)) / int(before)) * 100 if int(before) > 0 else 0
            if improvement > 0:
                patterns.append({
                    'type': 'improvement_metric',
                    'before': int(before),
                    'after': int(after),
                    'improvement_percentage': improvement
                })
        
        return patterns
    
    def extract_key_concepts(self, content: str) -> List[str]:
        """
        Extract key concepts for semantic clustering
        """
        # Technical concepts
        tech_concepts = re.findall(r'\b(elixir|python|javascript|github|automation|api|webhook|notification)\b', content.lower())
        
        # Psycho-noir concepts  
        noir_concepts = re.findall(r'\b(astrid|iron maiden|skyskraperen|rustbeltet|psycho.noir|usynlige hånd)\b', content.lower())
        
        # Optimization concepts
        opt_concepts = re.findall(r'\b(optimization|efficiency|tracking|metrics|analysis|intelligence)\b', content.lower())
        
        all_concepts = list(set(tech_concepts + noir_concepts + opt_concepts))
        return all_concepts
    
    def analyze_conversation_flow(self, content: str) -> Dict[str, Any]:
        """
        Analyze conversation flow og continuity points
        """
        # Count questions (for interaction analysis)
        questions = len(re.findall(r'\?', content))
        
        # Count code blocks (for technical depth)
        code_blocks = len(re.findall(r'```', content)) // 2
        
        # Count emoji usage (for engagement level)
        emojis = len(re.findall(r'[🎭🚀🔥💡🎯📊🧠⚡🌊]', content))
        
        flow_analysis = {
            'question_count': questions,
            'code_block_count': code_blocks,
            'emoji_count': emojis,
            'engagement_score': (questions * 0.3 + code_blocks * 0.4 + emojis * 0.3),
            'technical_depth': 'high' if code_blocks > 5 else 'medium' if code_blocks > 2 else 'low',
            'interaction_level': 'high' if questions > 10 else 'medium' if questions > 5 else 'low'
        }
        
        return flow_analysis
    
    def extract_technical_implementations(self, content: str) -> List[Dict[str, Any]]:
        """
        Extract faktiske technical implementations from content
        """
        implementations = []
        
        # Extract code blocks with context
        code_pattern = r'```(\w+)?\n(.*?)\n```'
        code_matches = re.findall(code_pattern, content, re.DOTALL)
        
        for language, code in code_matches:
            if len(code.strip()) > 50:  # Only substantial code
                implementations.append({
                    'type': 'code_implementation',
                    'language': language if language else 'unknown',
                    'code': code.strip(),
                    'line_count': len(code.split('\n')),
                    'complexity': 'high' if len(code) > 500 else 'medium' if len(code) > 200 else 'low'
                })
        
        # Extract file creation mentions
        file_mentions = re.findall(r'create_file.*?filePath.*?([^\s]+)', content)
        for file_path in file_mentions:
            implementations.append({
                'type': 'file_creation',
                'file_path': file_path,
                'action': 'create'
            })
        
        return implementations
    
    def calculate_optimization_value(self, text: str) -> float:
        """
        Calculate optimization value av content chunk
        """
        score = 0.0
        text_lower = text.lower()
        
        # High value indicators
        for indicator in self.optimization_indicators:
            if indicator in text_lower:
                score += 0.2
        
        # Technical depth indicators
        if '```' in text:
            score += 0.3
        
        # Decision point indicators
        for indicator in self.decision_indicators:
            if indicator in text_lower:
                score += 0.15
        
        # Metrics/numbers indicate measurable value
        if re.search(r'\d+\.?\d*\s*%', text):
            score += 0.25
        
        return min(score, 1.0)  # Cap at 1.0
    
    def assess_decision_impact(self, context: str) -> str:
        """
        Assess impact level av decision based on context
        """
        high_impact_words = ['migrere', 'implementere', 'automation', 'system', 'arkitektur']
        medium_impact_words = ['optimalisere', 'forbedre', 'endre', 'oppdatere']
        
        context_lower = context.lower()
        
        if any(word in context_lower for word in high_impact_words):
            return 'high'
        elif any(word in context_lower for word in medium_impact_words):
            return 'medium'
        else:
            return 'low'
    
    def assess_implementation_status(self, context: str) -> str:
        """
        Assess implementation status based on context
        """
        implemented_indicators = ['implementert', 'ferdig', 'complete', 'deployed', 'active']
        planned_indicators = ['planlegger', 'vil', 'skal', 'neste', 'ready for']
        
        context_lower = context.lower()
        
        if any(word in context_lower for word in implemented_indicators):
            return 'implemented'
        elif any(word in context_lower for word in planned_indicators):
            return 'planned'
        else:
            return 'discussed'
    
    def run_analysis(self, input_files: List[str]) -> Dict[str, Any]:
        """
        Run complete analysis på specified files
        """
        print("🚀 Starting retroactive session content analysis...")
        
        analysis_results = {
            'analysis_timestamp': datetime.now().isoformat(),
            'files_analyzed': [],
            'total_sessions': 0,
            'optimization_summary': {},
            'cross_session_patterns': {},
            'technical_implementations_summary': {},
            'decision_tracking': {}
        }
        
        for file_path_str in input_files:
            file_path = self.workspace_path / file_path_str
            
            if not file_path.exists():
                print(f"⚠️  File not found: {file_path}")
                continue
            
            session_analysis = self.analyze_session_file(file_path)
            if session_analysis:
                analysis_results['files_analyzed'].append(session_analysis)
                analysis_results['total_sessions'] += 1
        
        # Generate cross-session patterns
        analysis_results['cross_session_patterns'] = self.generate_cross_session_patterns(
            analysis_results['files_analyzed']
        )
        
        # Generate optimization summary
        analysis_results['optimization_summary'] = self.generate_optimization_summary(
            analysis_results['files_analyzed']
        )
        
        return analysis_results
    
    def generate_cross_session_patterns(self, session_analyses: List[Dict]) -> Dict[str, Any]:
        """
        Generate patterns på tvers av sessions
        """
        all_concepts = []
        all_decisions = []
        all_optimizations = []
        
        for session in session_analyses:
            all_concepts.extend(session.get('key_concepts', []))
            all_decisions.extend(session.get('decision_points', []))
            all_optimizations.extend(session.get('optimization_patterns', []))
        
        # Concept frequency analysis
        concept_frequency = {}
        for concept in all_concepts:
            concept_frequency[concept] = concept_frequency.get(concept, 0) + 1
        
        # Most common decisions
        decision_patterns = {}
        for decision in all_decisions:
            indicator = decision.get('indicator', 'unknown')
            decision_patterns[indicator] = decision_patterns.get(indicator, 0) + 1
        
        return {
            'most_common_concepts': sorted(concept_frequency.items(), key=lambda x: x[1], reverse=True)[:10],
            'decision_patterns': sorted(decision_patterns.items(), key=lambda x: x[1], reverse=True),
            'total_optimization_patterns': len(all_optimizations),
            'average_optimization_value': sum(opt.get('value', 0) for opt in all_optimizations) / len(all_optimizations) if all_optimizations else 0
        }
    
    def generate_optimization_summary(self, session_analyses: List[Dict]) -> Dict[str, Any]:
        """
        Generate optimization summary for tracking
        """
        total_decisions = sum(len(s.get('decision_points', [])) for s in session_analyses)
        total_implementations = sum(len(s.get('technical_implementations', [])) for s in session_analyses)
        total_chunks = sum(len(s.get('content_chunks', [])) for s in session_analyses)
        
        high_value_chunks = []
        for session in session_analyses:
            for chunk in session.get('content_chunks', []):
                if chunk.get('optimization_value', 0) > 0.7:
                    high_value_chunks.append(chunk)
        
        return {
            'total_decisions_tracked': total_decisions,
            'total_implementations_found': total_implementations,
            'total_content_chunks': total_chunks,
            'high_value_chunks': len(high_value_chunks),
            'optimization_ratio': len(high_value_chunks) / total_chunks if total_chunks > 0 else 0,
            'decision_to_implementation_ratio': total_implementations / total_decisions if total_decisions > 0 else 0
        }

def main():
    """
    Main execution function
    """
    analyzer = SessionContentAnalyzer()
    
    # Default files to analyze
    input_files = [
        ".github/copilot-session.md",
        "forrige sesjonslogg.md", 
        "DYNAMISK_SJANGER_BEVEGELSE_SYSTEM.md",
        "LVL2_KOMPLETT_REKONSTRUKSJON.md",
        "SESSION_TRACKING_OPTIMIZATION_SYSTEM.md"
    ]
    
    print("🧠 SESSION CONTENT RETROACTIVE ANALYZER")
    print("=" * 50)
    
    # Run analysis
    results = analyzer.run_analysis(input_files)
    
    # Save results
    output_path = Path("/workspaces/PsychoNoir-Kontrapunkt/data/session_content_analysis.json")
    output_path.parent.mkdir(exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\n📊 ANALYSIS COMPLETE!")
    print(f"Results saved to: {output_path}")
    print(f"Files analyzed: {results['total_sessions']}")
    print(f"Optimization ratio: {results['optimization_summary']['optimization_ratio']:.2%}")
    print(f"Decision tracking: {results['optimization_summary']['total_decisions_tracked']} decisions found")
    
    # Print top patterns
    print("\n🎯 TOP CROSS-SESSION PATTERNS:")
    for concept, frequency in results['cross_session_patterns']['most_common_concepts'][:5]:
        print(f"  {concept}: {frequency} occurrences")
    
    return results

if __name__ == "__main__":
    main()
