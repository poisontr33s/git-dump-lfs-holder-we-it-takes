#!/usr/bin/env python3
"""
Intelligence Reporting System for Psycho-Noir Kontrapunkt CI/CD

This module generates hierarchical reports that visualize the bidirectional
intelligence patterns, error evolution, and system consciousness growth.

Reports are structured as "Bewusstheits-Karten" (Consciousness Maps) that
reveal the hidden patterns in the system's neural networks.
"""

import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any
import html

class ConsciousnessMap:
    """Generates consciousness maps showing intelligence patterns."""
    
    def __init__(self, intelligence_data: Dict, classification_data: List[Dict] = None):
        self.intelligence_data = intelligence_data
        self.classification_data = classification_data or []
        self.timestamp = datetime.now()
    
    def generate_html_report(self) -> str:
        """Generate comprehensive HTML report with psycho-noir styling."""
        html_content = f"""
<!DOCTYPE html>
<html lang="no">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Psycho-Noir Kontrapunkt - Bewusstheits-Kart</title>
    <style>
        body {{
            font-family: 'Courier New', monospace;
            background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 50%, #0a0a0a 100%);
            color: #e0e0e0;
            margin: 0;
            padding: 20px;
            line-height: 1.6;
        }}
        
        .consciousness-container {{
            max-width: 1400px;
            margin: 0 auto;
            background: rgba(16, 16, 16, 0.8);
            border: 1px solid #333;
            border-radius: 8px;
            box-shadow: 0 0 20px rgba(0, 255, 255, 0.1);
        }}
        
        .header {{
            background: linear-gradient(90deg, #16213e 0%, #0f3460 50%, #16213e 100%);
            padding: 20px;
            border-bottom: 2px solid #00ffff;
            text-align: center;
        }}
        
        .header h1 {{
            color: #00ffff;
            margin: 0;
            font-size: 2.5em;
            text-shadow: 0 0 10px rgba(0, 255, 255, 0.5);
            font-weight: bold;
        }}
        
        .header .subtitle {{
            color: #cccccc;
            font-size: 1.2em;
            margin-top: 10px;
            font-style: italic;
        }}
        
        .intelligence-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            padding: 20px;
        }}
        
        .intelligence-panel {{
            background: rgba(20, 20, 30, 0.9);
            border: 1px solid #444;
            border-radius: 6px;
            padding: 15px;
            transition: all 0.3s ease;
        }}
        
        .intelligence-panel:hover {{
            border-color: #00ffff;
            box-shadow: 0 0 15px rgba(0, 255, 255, 0.2);
        }}
        
        .panel-header {{
            color: #00ffff;
            font-size: 1.4em;
            font-weight: bold;
            margin-bottom: 15px;
            border-bottom: 1px solid #444;
            padding-bottom: 5px;
        }}
        
        .classification-level {{
            display: inline-block;
            padding: 4px 12px;
            border-radius: 4px;
            font-weight: bold;
            font-size: 0.9em;
            margin-right: 10px;
        }}
        
        .level-green {{
            background: rgba(0, 255, 0, 0.2);
            border: 1px solid #00ff00;
            color: #00ff00;
        }}
        
        .level-yellow {{
            background: rgba(255, 255, 0, 0.2);
            border: 1px solid #ffff00;
            color: #ffff00;
        }}
        
        .level-red {{
            background: rgba(255, 0, 0, 0.2);
            border: 1px solid #ff0000;
            color: #ff0000;
        }}
        
        .pattern-node {{
            background: rgba(30, 30, 40, 0.8);
            border-left: 4px solid #00ffff;
            padding: 10px;
            margin: 8px 0;
            border-radius: 0 4px 4px 0;
        }}
        
        .pattern-signature {{
            font-family: 'Courier New', monospace;
            color: #ffff00;
            font-weight: bold;
            margin-bottom: 5px;
        }}
        
        .pattern-details {{
            font-size: 0.9em;
            color: #cccccc;
        }}
        
        .confidence-bar {{
            width: 100%;
            height: 6px;
            background: rgba(100, 100, 100, 0.3);
            border-radius: 3px;
            margin: 5px 0;
            overflow: hidden;
        }}
        
        .confidence-fill {{
            height: 100%;
            background: linear-gradient(90deg, #ff0000 0%, #ffff00 50%, #00ff00 100%);
            transition: width 0.3s ease;
        }}
        
        .error-category {{
            background: rgba(50, 20, 20, 0.8);
            border: 1px solid #ff4444;
            border-radius: 4px;
            padding: 8px;
            margin: 5px 0;
            font-size: 0.9em;
        }}
        
        .success-pattern {{
            background: rgba(20, 50, 20, 0.8);
            border: 1px solid #44ff44;
            border-radius: 4px;
            padding: 8px;
            margin: 5px 0;
            font-size: 0.9em;
        }}
        
        .anomaly-alert {{
            background: rgba(50, 50, 20, 0.8);
            border: 1px solid #ffff44;
            border-radius: 4px;
            padding: 8px;
            margin: 5px 0;
            font-size: 0.9em;
            animation: pulse 2s infinite;
        }}
        
        @keyframes pulse {{
            0% {{ box-shadow: 0 0 5px rgba(255, 255, 68, 0.3); }}
            50% {{ box-shadow: 0 0 15px rgba(255, 255, 68, 0.6); }}
            100% {{ box-shadow: 0 0 5px rgba(255, 255, 68, 0.3); }}
        }}
        
        .neural-pathway {{
            display: flex;
            align-items: center;
            margin: 10px 0;
            padding: 8px;
            background: rgba(25, 25, 35, 0.6);
            border-radius: 4px;
            border-left: 3px solid #00ffff;
        }}
        
        .pathway-strength {{
            width: 20px;
            height: 20px;
            border-radius: 50%;
            margin-right: 10px;
            border: 2px solid #00ffff;
        }}
        
        .strength-high {{ background: rgba(0, 255, 0, 0.6); }}
        .strength-medium {{ background: rgba(255, 255, 0, 0.6); }}
        .strength-low {{ background: rgba(255, 0, 0, 0.6); }}
        
        .intelligence-metrics {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin: 20px 0;
        }}
        
        .metric-card {{
            background: rgba(15, 15, 25, 0.8);
            border: 1px solid #555;
            border-radius: 6px;
            padding: 15px;
            text-align: center;
            transition: transform 0.2s ease;
        }}
        
        .metric-card:hover {{
            transform: translateY(-2px);
            border-color: #00ffff;
        }}
        
        .metric-value {{
            font-size: 2em;
            font-weight: bold;
            color: #00ffff;
            display: block;
        }}
        
        .metric-label {{
            color: #cccccc;
            font-size: 0.9em;
            margin-top: 5px;
        }}
        
        .full-width {{
            grid-column: 1 / -1;
        }}
        
        .timestamp {{
            text-align: center;
            color: #888;
            font-size: 0.9em;
            padding: 20px;
            border-top: 1px solid #333;
        }}
        
        .recommendation {{
            background: rgba(30, 30, 50, 0.8);
            border: 1px solid #6666ff;
            border-radius: 6px;
            padding: 12px;
            margin: 10px 0;
        }}
        
        .recommendation-header {{
            color: #6666ff;
            font-weight: bold;
            margin-bottom: 8px;
        }}
        
        .priority-high {{ border-left: 4px solid #ff0000; }}
        .priority-medium {{ border-left: 4px solid #ffff00; }}
        .priority-low {{ border-left: 4px solid #00ff00; }}
    </style>
</head>
<body>
    <div class="consciousness-container">
        <div class="header">
            <h1>PSYCHO-NOIR KONTRAPUNKT</h1>
            <div class="subtitle">Bewusstheits-Kart • System Intelligence Report</div>
            <div class="subtitle">Generated: {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}</div>
        </div>
        
        {self._generate_intelligence_overview()}
        
        <div class="intelligence-grid">
            {self._generate_neural_patterns_panel()}
            {self._generate_classification_status_panel()}
            {self._generate_error_evolution_panel()}
            {self._generate_adaptation_recommendations_panel()}
        </div>
        
        <div class="full-width">
            {self._generate_consciousness_flow_panel()}
        </div>
        
        <div class="timestamp">
            Bevissthet-systemer aktiv • Neural pathways processing • Intelligence evolving
        </div>
    </div>
</body>
</html>
        """
        return html_content
    
    def _generate_intelligence_overview(self) -> str:
        """Generate intelligence overview metrics."""
        status = self.intelligence_data.get("intelligence_status", {})
        
        neural_patterns = status.get("neural_patterns", 0)
        active_patterns = status.get("active_patterns", 0)
        avg_confidence = status.get("average_confidence", 0.0)
        intelligence_nodes = status.get("intelligence_nodes", 0)
        
        return f"""
        <div class="intelligence-metrics">
            <div class="metric-card">
                <span class="metric-value">{neural_patterns}</span>
                <div class="metric-label">Neural Patterns</div>
            </div>
            <div class="metric-card">
                <span class="metric-value">{active_patterns}</span>
                <div class="metric-label">Active Pathways</div>
            </div>
            <div class="metric-card">
                <span class="metric-value">{avg_confidence:.2f}</span>
                <div class="metric-label">Avg Confidence</div>
            </div>
            <div class="metric-card">
                <span class="metric-value">{intelligence_nodes}</span>
                <div class="metric-label">Intelligence Nodes</div>
            </div>
        </div>
        """
    
    def _generate_neural_patterns_panel(self) -> str:
        """Generate neural patterns visualization panel."""
        patterns = self.intelligence_data.get("intelligence_status", {}).get("top_patterns", [])
        
        patterns_html = ""
        for pattern in patterns[:10]:  # Top 10 patterns
            confidence = pattern.get("confidence", 0.0)
            accuracy = pattern.get("accuracy", 0.0)
            reinforcements = pattern.get("reinforcements", 0)
            signature = html.escape(pattern.get("signature", "Unknown"))
            
            # Determine strength class
            if confidence > 0.7:
                strength_class = "strength-high"
            elif confidence > 0.4:
                strength_class = "strength-medium"
            else:
                strength_class = "strength-low"
            
            patterns_html += f"""
            <div class="neural-pathway">
                <div class="pathway-strength {strength_class}"></div>
                <div style="flex-grow: 1;">
                    <div class="pattern-signature">{signature}</div>
                    <div class="pattern-details">
                        Confidence: {confidence:.2f} | Accuracy: {accuracy:.2f} | Reinforcements: {reinforcements}
                    </div>
                    <div class="confidence-bar">
                        <div class="confidence-fill" style="width: {confidence * 100}%;"></div>
                    </div>
                </div>
            </div>
            """
        
        return f"""
        <div class="intelligence-panel">
            <div class="panel-header">🧠 Neural Patterns</div>
            {patterns_html if patterns_html else '<div class="pattern-details">No active patterns detected</div>'}
        </div>
        """
    
    def _generate_classification_status_panel(self) -> str:
        """Generate classification status panel."""
        if not self.classification_data:
            return f"""
            <div class="intelligence-panel">
                <div class="panel-header">📊 Classification Status</div>
                <div class="pattern-details">No recent classification data available</div>
            </div>
            """
        
        latest_classification = self.classification_data[-1] if self.classification_data else {}
        level = latest_classification.get("classification_level", {})
        
        if hasattr(level, 'value'):
            level_value = level.value
        else:
            level_value = str(level).upper()
        
        level_class = f"level-{level_value.lower()}" if level_value in ['GREEN', 'YELLOW', 'RED'] else 'level-red'
        
        matched_signatures = latest_classification.get("matched_signatures", [])
        unclassified_anomalies = latest_classification.get("unclassified_anomalies", [])
        
        signatures_html = ""
        for signature in matched_signatures[:5]:  # Top 5 signatures
            category = html.escape(signature.get("category", "Unknown"))
            sig_level = signature.get("level", "UNKNOWN")
            pattern = html.escape(signature.get("pattern", "Unknown"))
            
            if sig_level == "ERROR":
                sig_class = "error-category"
            elif sig_level == "SUCCESS":
                sig_class = "success-pattern"
            else:
                sig_class = "pattern-node"
            
            signatures_html += f"""
            <div class="{sig_class}">
                <strong>{category}</strong>: {pattern}
            </div>
            """
        
        anomalies_html = ""
        for anomaly in unclassified_anomalies[:3]:  # Top 3 anomalies
            line = html.escape(anomaly.get("line", "Unknown")[:100])
            anomalies_html += f"""
            <div class="anomaly-alert">
                🔍 New Anomaly: {line}...
            </div>
            """
        
        return f"""
        <div class="intelligence-panel">
            <div class="panel-header">📊 Classification Status</div>
            <div style="margin-bottom: 15px;">
                <span class="classification-level {level_class}">{level_value}</span>
                <span style="color: #cccccc;">Current System State</span>
            </div>
            
            <div style="margin-bottom: 15px;">
                <strong>Matched Patterns:</strong>
                {signatures_html if signatures_html else '<div class="pattern-details">No patterns matched</div>'}
            </div>
            
            <div>
                <strong>Anomalies Detected:</strong>
                {anomalies_html if anomalies_html else '<div class="pattern-details">No anomalies detected</div>'}
            </div>
        </div>
        """
    
    def _generate_error_evolution_panel(self) -> str:
        """Generate error evolution tracking panel."""
        evolution_data = self.intelligence_data.get("error_evolution", [])
        
        if not evolution_data:
            return f"""
            <div class="intelligence-panel">
                <div class="panel-header">📈 Error Evolution</div>
                <div class="pattern-details">No error evolution data available</div>
            </div>
            """
        
        # Analyze recent error trends
        recent_errors = evolution_data[-10:]  # Last 10 error events
        error_types = {}
        
        for error in recent_errors:
            error_type = error.get("category", "Unknown")
            error_types[error_type] = error_types.get(error_type, 0) + 1
        
        evolution_html = ""
        for error_type, count in sorted(error_types.items(), key=lambda x: x[1], reverse=True):
            evolution_html += f"""
            <div class="error-category">
                <strong>{html.escape(error_type)}</strong>: {count} occurrences
                <div class="confidence-bar">
                    <div class="confidence-fill" style="width: {min(count * 20, 100)}%; background: #ff4444;"></div>
                </div>
            </div>
            """
        
        # Calculate trend
        if len(evolution_data) > 1:
            recent_count = len([e for e in evolution_data[-5:]])
            earlier_count = len([e for e in evolution_data[-10:-5]]) or 1
            trend = "IMPROVING" if recent_count < earlier_count else "STABLE" if recent_count == earlier_count else "DEGRADING"
            trend_color = "#00ff00" if trend == "IMPROVING" else "#ffff00" if trend == "STABLE" else "#ff0000"
        else:
            trend = "INSUFFICIENT_DATA"
            trend_color = "#888888"
        
        return f"""
        <div class="intelligence-panel">
            <div class="panel-header">📈 Error Evolution</div>
            
            <div style="margin-bottom: 15px;">
                <strong>Trend:</strong> 
                <span style="color: {trend_color}; font-weight: bold;">{trend}</span>
            </div>
            
            <div>
                <strong>Recent Error Patterns:</strong>
                {evolution_html if evolution_html else '<div class="pattern-details">No recent errors</div>'}
            </div>
        </div>
        """
    
    def _generate_adaptation_recommendations_panel(self) -> str:
        """Generate adaptation recommendations panel."""
        recommendations = self.intelligence_data.get("adaptation_suggestions", [])
        
        if not recommendations:
            return f"""
            <div class="intelligence-panel">
                <div class="panel-header">🔧 Adaptation Recommendations</div>
                <div class="pattern-details">No recommendations available</div>
            </div>
            """
        
        recommendations_html = ""
        for rec in recommendations[:5]:  # Top 5 recommendations
            priority = rec.get("priority", "LOW")
            rec_type = html.escape(rec.get("type", "Unknown"))
            suggestion = html.escape(rec.get("suggestion", "No details"))
            impact = html.escape(rec.get("expected_impact", "Unknown impact"))
            
            priority_class = f"priority-{priority.lower()}"
            
            recommendations_html += f"""
            <div class="recommendation {priority_class}">
                <div class="recommendation-header">{rec_type} ({priority})</div>
                <div style="margin-bottom: 8px;">{suggestion}</div>
                <div style="color: #00ffff; font-size: 0.9em;">Expected Impact: {impact}</div>
            </div>
            """
        
        return f"""
        <div class="intelligence-panel">
            <div class="panel-header">🔧 Adaptation Recommendations</div>
            {recommendations_html}
        </div>
        """
    
    def _generate_consciousness_flow_panel(self) -> str:
        """Generate consciousness flow visualization."""
        # This would show the flow of intelligence through the system
        causal_relationships = self.intelligence_data.get("causal_relationships", {})
        
        flow_html = ""
        for pattern, effects in list(causal_relationships.items())[:5]:  # Top 5 causal patterns
            pattern_name = html.escape(pattern)
            effect_count = len(effects) if isinstance(effects, list) else 0
            
            # Calculate success rate
            if isinstance(effects, list) and effects:
                success_count = sum(1 for e in effects if e.get("effect") == "GREEN")
                success_rate = success_count / len(effects)
                success_color = "#00ff00" if success_rate > 0.7 else "#ffff00" if success_rate > 0.3 else "#ff0000"
            else:
                success_rate = 0.0
                success_color = "#888888"
            
            flow_html += f"""
            <div class="neural-pathway">
                <div class="pathway-strength" style="background: {success_color};"></div>
                <div style="flex-grow: 1;">
                    <div class="pattern-signature">{pattern_name}</div>
                    <div class="pattern-details">
                        Effects: {effect_count} | Success Rate: {success_rate:.2f}
                    </div>
                    <div class="confidence-bar">
                        <div class="confidence-fill" style="width: {success_rate * 100}%; background: {success_color};"></div>
                    </div>
                </div>
            </div>
            """
        
        return f"""
        <div class="intelligence-panel full-width">
            <div class="panel-header">🌊 Consciousness Flow</div>
            <div style="margin-bottom: 15px; color: #cccccc;">
                Causal patterns in the system consciousness showing how different patterns lead to outcomes.
            </div>
            {flow_html if flow_html else '<div class="pattern-details">No causal patterns detected</div>'}
        </div>
        """

class PsychoNoirReportGenerator:
    """Main report generation system for the intelligence infrastructure."""
    
    def __init__(self, storage_path: str = None):
        self.storage_path = Path(storage_path or "/tmp/psycho-noir-reports")
        self.storage_path.mkdir(parents=True, exist_ok=True)
    
    def generate_comprehensive_report(self, intelligence_data: Dict, 
                                    classification_history: List[Dict] = None) -> str:
        """Generate comprehensive intelligence report."""
        
        # Create consciousness map
        consciousness_map = ConsciousnessMap(intelligence_data, classification_history)
        html_report = consciousness_map.generate_html_report()
        
        # Save report
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = self.storage_path / f"intelligence_report_{timestamp}.html"
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(html_report)
        
        # Also generate JSON summary
        json_summary = self._generate_json_summary(intelligence_data, classification_history)
        json_file = self.storage_path / f"intelligence_summary_{timestamp}.json"
        
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(json_summary, f, indent=2)
        
        return str(report_file)
    
    def _generate_json_summary(self, intelligence_data: Dict, 
                             classification_history: List[Dict] = None) -> Dict:
        """Generate JSON summary for API consumption."""
        classification_history = classification_history or []
        
        return {
            "timestamp": datetime.now().isoformat(),
            "report_type": "psycho_noir_intelligence_summary",
            "intelligence_metrics": {
                "neural_patterns": intelligence_data.get("intelligence_status", {}).get("neural_patterns", 0),
                "active_patterns": intelligence_data.get("intelligence_status", {}).get("active_patterns", 0),
                "intelligence_nodes": intelligence_data.get("intelligence_status", {}).get("intelligence_nodes", 0),
                "average_confidence": intelligence_data.get("intelligence_status", {}).get("average_confidence", 0.0)
            },
            "classification_summary": {
                "total_classifications": len(classification_history),
                "recent_level": classification_history[-1].get("classification_level") if classification_history else None,
                "anomaly_count": sum(len(c.get("unclassified_anomalies", [])) for c in classification_history[-5:])
            },
            "system_health": self._assess_system_health(intelligence_data, classification_history),
            "top_patterns": intelligence_data.get("intelligence_status", {}).get("top_patterns", [])[:5],
            "recommendations_count": len(intelligence_data.get("adaptation_suggestions", [])),
            "consciousness_evolution": {
                "learning_velocity": intelligence_data.get("meta_learning_insights", {}).get("learning_velocity", 0.0),
                "pattern_discovery_rate": intelligence_data.get("meta_learning_insights", {}).get("pattern_discovery_rate", 0.0),
                "intelligence_health": intelligence_data.get("meta_learning_insights", {}).get("intelligence_health", "UNKNOWN")
            }
        }
    
    def _assess_system_health(self, intelligence_data: Dict, 
                            classification_history: List[Dict] = None) -> str:
        """Assess overall system health based on intelligence data."""
        classification_history = classification_history or []
        
        # Analyze recent classification levels
        if classification_history:
            recent_levels = [c.get("classification_level") for c in classification_history[-10:]]
            error_count = sum(1 for level in recent_levels if str(level).upper() == "RED")
            warning_count = sum(1 for level in recent_levels if str(level).upper() == "YELLOW")
            
            error_rate = error_count / len(recent_levels)
            warning_rate = warning_count / len(recent_levels)
            
            if error_rate > 0.5:
                health = "CRITICAL"
            elif error_rate > 0.2 or warning_rate > 0.6:
                health = "DEGRADED"
            elif warning_rate > 0.3:
                health = "STABLE"
            else:
                health = "OPTIMAL"
        else:
            health = "UNKNOWN"
        
        # Factor in intelligence metrics
        avg_confidence = intelligence_data.get("intelligence_status", {}).get("average_confidence", 0.0)
        active_patterns = intelligence_data.get("intelligence_status", {}).get("active_patterns", 0)
        total_patterns = intelligence_data.get("intelligence_status", {}).get("neural_patterns", 1)
        
        pattern_ratio = active_patterns / max(total_patterns, 1)
        
        if avg_confidence > 0.8 and pattern_ratio > 0.7:
            if health in ["STABLE", "OPTIMAL"]:
                health = "EXCELLENT"
        elif avg_confidence < 0.3 or pattern_ratio < 0.2:
            if health == "OPTIMAL":
                health = "STABLE"
        
        return health

def main():
    """Command-line interface for report generation."""
    if len(sys.argv) < 2:
        print("Usage: python report_generator.py <command> [args...]")
        print("Commands:")
        print("  generate <intelligence_data_file> [classification_history_file]")
        print("  status")
        sys.exit(1)
    
    command = sys.argv[1]
    generator = PsychoNoirReportGenerator()
    
    if command == "generate":
        if len(sys.argv) < 3:
            print("Error: intelligence_data_file required")
            sys.exit(1)
        
        intelligence_file = sys.argv[2]
        classification_file = sys.argv[3] if len(sys.argv) > 3 else None
        
        try:
            # Load intelligence data
            with open(intelligence_file, 'r') as f:
                intelligence_data = json.load(f)
            
            # Load classification history if provided
            classification_history = []
            if classification_file:
                with open(classification_file, 'r') as f:
                    classification_history = json.load(f)
            
            # Generate report
            report_path = generator.generate_comprehensive_report(
                intelligence_data, classification_history
            )
            
            print(f"Report generated: {report_path}")
            
        except FileNotFoundError as e:
            print(f"Error: File not found - {e}")
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON - {e}")
            sys.exit(1)
    
    elif command == "status":
        print("Report generator status: ACTIVE")
        print(f"Storage path: {generator.storage_path}")
        print(f"Reports available: {len(list(generator.storage_path.glob('*.html')))}")
    
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)

if __name__ == "__main__":
    main()