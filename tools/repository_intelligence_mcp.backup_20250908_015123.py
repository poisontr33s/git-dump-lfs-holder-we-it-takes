#!/usr/bin/env python3
"""
🧠 PSYCHO-NOIR REPOSITORY INTELLIGENCE MCP SERVER
================================================

Model Context Protocol (MCP) server for GitHub Copilot integration
Provides deep repository intelligence and Psycho-Noir character consultations

INTEGRATION FEATURES:
- MCP Server Protocol Implementation
- GitHub Copilot Pro+ Multi-Model Access
- Character Oracle Network Integration
- Real-time Repository Analysis
- Context-Aware Problem Resolution

SUPPORTED COPILOT MODELS:
- Claude 3.5/3.7/4 Sonnet, Claude 4/4.1 Opus
- Gemini 2.0 Flash, Gemini 2.5 Pro  
- OpenAI o3, o4-mini, GPT-5, GPT-5 mini
- xAI Grok Code Fast 1
"""

import json
import asyncio
import logging
from typing import Dict, List, Any
from dataclasses import dataclass, asdict
from pathlib import Path
import hashlib
from datetime import datetime
import sqlite3

# MCP Protocol Implementation
try:
    import mcp
    from mcp.server import Server
    from mcp.server.stdio import stdio_server
except ImportError:
    print("⚠️ MCP library not available - install with: pip install mcp")
    mcp = None
    Server = None
    stdio_server = None

# Psycho-Noir Character Integration
from enum import Enum

class PsychoNoirDomain(Enum):
    """Psycho-Noir character domains"""
    SKYSKRAPEREN = "skyskraperen"  # Astrid Møller - Strategic control
    RUSTBELTET = "rustbeltet"      # Iron Maiden - Practical efficiency
    INVISIBLE_HAND = "invisible_hand"  # Den Usynlige Hånd - Emergent patterns
    KOMPILERINGS_SPOKELSER = "kompilerings_spokelser"  # Digital spirits

@dataclass
class RepositoryContext:
    """Complete repository context for AI models"""
    name: str
    path: str
    languages: List[str]
    frameworks: List[str]
    file_count: int
    line_count: int
    recent_changes: List[str]
    active_issues: List[str]
    character_insights: Dict[str, Any]
    mcp_metadata: Dict[str, Any]

@dataclass
class CharacterConsultation:
    """Character oracle consultation result"""
    character: str
    domain: PsychoNoirDomain
    insight: str
    recommended_actions: List[str]
    confidence: float
    context_relevance: float

class RepositoryIntelligenceMCP:
    """
    🧠 MCP Server for GitHub Copilot Repository Intelligence
    Provides deep contextual understanding of Psycho-Noir Kontrapunkt workspace
    """
    
    def __init__(self, workspace_root: str = "/workspaces/PsychoNoir-Kontrapunkt"):
        self.workspace_root = Path(workspace_root)
        self.server = Server("psycho-noir-repository-intelligence") if Server else None
        self.context_cache: Dict[str, Any] = {}
        self.character_oracles = self._initialize_character_oracles()
        self.mcp_tools = self._register_mcp_tools()
        
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        # Initialize context database
        self.db_path = self.workspace_root / "data" / "repository_intelligence.db"
        self._initialize_database()
    
    def _initialize_database(self):
        """Initialize SQLite database for repository intelligence"""
        self.db_path.parent.mkdir(exist_ok=True)
        
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS repository_context (
                    id INTEGER PRIMARY KEY,
                    timestamp TEXT,
                    context_hash TEXT UNIQUE,
                    context_data TEXT,
                    character_insights TEXT
                )
            """)
            
            conn.execute("""
                CREATE TABLE IF NOT EXISTS copilot_consultations (
                    id INTEGER PRIMARY KEY,
                    timestamp TEXT,
                    model_name TEXT,
                    query TEXT,
                    response TEXT,
                    confidence REAL,
                    character_domain TEXT
                )
            """)
    
    def _initialize_character_oracles(self) -> Dict[str, Any]:
        """Initialize character oracle system"""
        return {
            "astrid": {
                "domain": PsychoNoirDomain.SKYSKRAPEREN,
                "specializations": ["strategic_analysis", "information_warfare", "systematic_control"],
                "ai_models": ["claude-4-sonnet", "openai-o3", "gemini-2.5-pro"]
            },
            "iron_maiden": {
                "domain": PsychoNoirDomain.RUSTBELTET,
                "specializations": ["practical_optimization", "resource_scavenging", "brutal_efficiency"],
                "ai_models": ["gemini-2.0-flash", "openai-o4-mini", "xai-grok-fast"]
            },
            "invisible_hand": {
                "domain": PsychoNoirDomain.INVISIBLE_HAND,
                "specializations": ["emergent_patterns", "subtle_manipulation", "hidden_optimization"],
                "ai_models": ["claude-4-opus", "claude-4.1-opus", "openai-gpt-5"]
            },
            "kompilerings_spokelser": {
                "domain": PsychoNoirDomain.KOMPILERINGS_SPOKELSER,
                "specializations": ["digital_archaeology", "error_pattern_analysis", "system_haunting"],
                "ai_models": ["claude-3.7-sonnet", "openai-gpt-5-mini"]
            }
        }
    
    def _register_mcp_tools(self) -> Dict[str, Any]:
        """Register MCP tools for Copilot integration"""
        if not self.server:
            return {}
        
        tools = {
            "analyze_repository": {
                "name": "analyze_repository",
                "description": "Deep analysis of Psycho-Noir Kontrapunkt repository structure and patterns",
                "schema": {
                    "type": "object",
                    "properties": {
                        "focus_area": {
                            "type": "string",
                            "enum": ["code_quality", "architecture", "documentation", "integrations"],
                            "description": "Specific area to focus analysis on"
                        },
                        "character_perspective": {
                            "type": "string", 
                            "enum": ["astrid", "iron_maiden", "invisible_hand", "kompilerings_spokelser"],
                            "description": "Psycho-Noir character perspective for analysis"
                        }
                    }
                }
            },
            "consult_character_oracle": {
                "name": "consult_character_oracle",
                "description": "Consult Psycho-Noir character oracles for domain-specific insights",
                "schema": {
                    "type": "object",
                    "properties": {
                        "character": {
                            "type": "string",
                            "enum": ["astrid", "iron_maiden", "invisible_hand", "kompilerings_spokelser"],
                            "description": "Character oracle to consult"
                        },
                        "query": {
                            "type": "string",
                            "description": "Specific question or problem to address"
                        },
                        "context": {
                            "type": "string",
                            "description": "Additional context for the consultation"
                        }
                    },
                    "required": ["character", "query"]
                }
            },
            "get_repository_context": {
                "name": "get_repository_context",
                "description": "Get comprehensive repository context for AI model consumption",
                "schema": {
                    "type": "object",
                    "properties": {
                        "include_file_contents": {
                            "type": "boolean",
                            "description": "Whether to include file contents in context"
                        },
                        "max_file_size": {
                            "type": "integer", 
                            "description": "Maximum file size to include (bytes)"
                        }
                    }
                }
            },
            "execute_eternal_sadhana": {
                "name": "execute_eternal_sadhana",
                "description": "Execute Eternal Sadhana disciplined problem resolution cycle",
                "schema": {
                    "type": "object",
                    "properties": {
                        "problem_categories": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "Categories of problems to address"
                        },
                        "intensity": {
                            "type": "string",
                            "enum": ["gentle", "moderate", "intensive"],
                            "description": "Intensity of the Sadhana cycle"
                        }
                    }
                }
            }
        }
        
        # Register tools with MCP server
        if self.server:
            for tool_name, tool_config in tools.items():
                self.server.register_tool(
                    name=tool_config["name"],
                    description=tool_config["description"],
                    schema=tool_config["schema"]
                )
        
        return tools
    
    async def analyze_repository(self, focus_area: str = "code_quality", character_perspective: str = "astrid") -> Dict[str, Any]:
        """
        🔍 Deep repository analysis with character perspective
        """
        self.logger.info(f"Analyzing repository with {character_perspective} perspective, focus: {focus_area}")
        
        # Gather repository metrics
        repo_metrics = await self._gather_repository_metrics()
        
        # Get character-specific analysis
        character_analysis = await self._get_character_analysis(character_perspective, focus_area, repo_metrics)
        
        # Generate context hash for caching
        context_data = {
            "metrics": repo_metrics,
            "character_analysis": character_analysis,
            "focus_area": focus_area,
            "timestamp": datetime.now().isoformat()
        }
        
        context_hash = hashlib.md5(json.dumps(context_data, sort_keys=True).encode()).hexdigest()
        
        # Cache results
        self._cache_repository_context(context_hash, context_data)
        
        return {
            "repository_metrics": repo_metrics,
            "character_perspective": character_perspective,
            "character_analysis": character_analysis,
            "focus_area": focus_area,
            "context_hash": context_hash,
            "mcp_integration_status": "active",
            "copilot_models_available": list(self._get_available_copilot_models()),
            "recommendations": self._generate_recommendations(character_analysis, focus_area)
        }
    
    async def _gather_repository_metrics(self) -> Dict[str, Any]:
        """Gather comprehensive repository metrics"""
        
        metrics = {
            "file_counts": {},
            "language_distribution": {},
            "code_complexity": {},
            "recent_activity": {},
            "dependency_health": {},
            "documentation_coverage": {}
        }
        
        # Count files by type
        for file_path in self.workspace_root.rglob("*"):
            if file_path.is_file():
                suffix = file_path.suffix.lower()
                metrics["file_counts"][suffix] = metrics["file_counts"].get(suffix, 0) + 1
        
        # Analyze Python files specifically
        python_files = list(self.workspace_root.rglob("*.py"))
        metrics["python_analysis"] = {
            "total_files": len(python_files),
            "lines_of_code": await self._count_lines_of_code(python_files),
            "import_complexity": await self._analyze_import_complexity(python_files)
        }
        
        # Check for documentation
        doc_files = list(self.workspace_root.rglob("*.md")) + list(self.workspace_root.rglob("*.rst"))
        metrics["documentation_coverage"] = {
            "total_docs": len(doc_files),
            "readme_present": (self.workspace_root / "README.md").exists(),
            "docs_directory": (self.workspace_root / "docs").exists()
        }
        
        # Check VS Code configuration
        vscode_dir = self.workspace_root / ".vscode"
        metrics["vscode_configuration"] = {
            "configured": vscode_dir.exists(),
            "settings_present": (vscode_dir / "settings.json").exists() if vscode_dir.exists() else False,
            "extensions_configured": (vscode_dir / "extensions.json").exists() if vscode_dir.exists() else False
        }
        
        return metrics
    
    async def _count_lines_of_code(self, python_files: List[Path]) -> int:
        """Count total lines of code in Python files"""
        total_lines = 0
        for file_path in python_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    total_lines += len(f.readlines())
            except Exception:
                continue
        return total_lines
    
    async def _analyze_import_complexity(self, python_files: List[Path]) -> Dict[str, Any]:
        """Analyze import complexity and patterns"""
        imports = []
        for file_path in python_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    # Simple regex-based import detection
                    import_lines = [line.strip() for line in content.split('\n') 
                                  if line.strip().startswith(('import ', 'from '))]
                    imports.extend(import_lines)
            except Exception:
                continue
        
        return {
            "total_imports": len(imports),
            "unique_modules": len(set(imports)),
            "complexity_score": len(imports) / max(len(python_files), 1)
        }
    
    async def _get_character_analysis(self, character: str, focus_area: str, metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Get character-specific analysis of repository"""
        
        character_config = self.character_oracles.get(character, {})
        domain = character_config.get("domain", PsychoNoirDomain.INVISIBLE_HAND)
        
        analysis = {
            "character": character,
            "domain": domain.value,
            "perspective": {},
            "recommendations": [],
            "ai_model_suggestions": character_config.get("ai_models", [])
        }
        
        if character == "astrid":
            # Strategic, systematic analysis
            analysis["perspective"] = {
                "strategic_assessment": "Repository shows systematic development approach",
                "control_points": ["VS Code configuration", "Extension system", "Documentation structure"],
                "information_advantages": ["Comprehensive tooling", "Multi-domain expertise"],
                "vulnerability_analysis": self._assess_strategic_vulnerabilities(metrics)
            }
            analysis["recommendations"] = [
                "Implement comprehensive monitoring system",
                "Establish strategic checkpoints for quality control",
                "Optimize information flow between systems"
            ]
            
        elif character == "iron_maiden":
            # Practical, efficiency-focused analysis  
            analysis["perspective"] = {
                "efficiency_assessment": "Multiple optimization opportunities identified",
                "resource_utilization": self._assess_resource_efficiency(metrics),
                "practical_bottlenecks": ["Import complexity", "File organization", "Build processes"],
                "scavenging_opportunities": ["Unused code", "Redundant systems", "Optimization potential"]
            }
            analysis["recommendations"] = [
                "Implement brutal efficiency optimizations",
                "Scavenge and repurpose underutilized resources",
                "Focus on essential system survival priorities"
            ]
            
        elif character == "invisible_hand":
            # Emergent pattern analysis
            analysis["perspective"] = {
                "emergent_patterns": self._identify_emergent_patterns(metrics),
                "hidden_optimizations": ["Cross-system synergies", "Natural workflow patterns"],
                "cultivation_opportunities": ["Organic growth areas", "Self-organizing systems"],
                "subtle_influences": ["Background processes", "Implicit connections"]
            }
            analysis["recommendations"] = [
                "Allow natural efficiency patterns to emerge",
                "Cultivate beneficial system behaviors",
                "Transform chaos into structured improvement"
            ]
            
        else:  # kompilerings_spokelser
            # Digital archaeology and error pattern analysis
            analysis["perspective"] = {
                "digital_archaeology": "Ancient code patterns detected",
                "error_hauntings": self._detect_error_patterns(metrics),
                "spectral_interference": ["Compilation ghosts", "Runtime spirits"],
                "system_haunting_level": self._calculate_haunting_level(metrics)
            }
            analysis["recommendations"] = [
                "Perform digital exorcism on corrupted code patterns",
                "Implement spectral debugging techniques",
                "Channel compilation spirits for positive outcomes"
            ]
        
        return analysis
    
    def _assess_strategic_vulnerabilities(self, metrics: Dict[str, Any]) -> List[str]:
        """Astrid's strategic vulnerability assessment"""
        vulnerabilities = []
        
        if not metrics["vscode_configuration"]["configured"]:
            vulnerabilities.append("VS Code configuration incomplete - strategic control compromised")
        
        if metrics["python_analysis"]["import_complexity"]["complexity_score"] > 5:
            vulnerabilities.append("High import complexity - dependency chain vulnerability")
        
        if metrics["documentation_coverage"]["total_docs"] < 5:
            vulnerabilities.append("Insufficient documentation - information warfare disadvantage")
        
        return vulnerabilities
    
    def _assess_resource_efficiency(self, metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Iron Maiden's resource efficiency assessment"""
        return {
            "code_efficiency": "moderate" if metrics["python_analysis"]["lines_of_code"] < 10000 else "low",
            "file_organization": "scattered" if len(metrics["file_counts"]) > 20 else "focused",
            "resource_waste": ["Unused imports", "Redundant files", "Inefficient patterns"]
        }
    
    def _identify_emergent_patterns(self, metrics: Dict[str, Any]) -> List[str]:
        """Invisible Hand's emergent pattern identification"""
        patterns = []
        
        if metrics["python_analysis"]["total_files"] > 50:
            patterns.append("Large-scale system emergence - natural modularization occurring")
        
        if metrics["vscode_configuration"]["configured"]:
            patterns.append("Tool ecosystem self-organization - IDE integration pattern emerging")
        
        patterns.append("Cross-domain knowledge synthesis - interdisciplinary pattern formation")
        
        return patterns
    
    def _detect_error_patterns(self, metrics: Dict[str, Any]) -> List[str]:
        """Kompilerings-Spøkelser error pattern detection"""
        patterns = []
        
        if metrics["python_analysis"]["import_complexity"]["complexity_score"] > 3:
            patterns.append("Import dependency haunting - circular reference spirits detected")
        
        patterns.append("Configuration ghost manifestation - settings file poltergeist activity")
        patterns.append("Syntax error archaeological layers - ancient code burial sites identified")
        
        return patterns
    
    def _calculate_haunting_level(self, metrics: Dict[str, Any]) -> float:
        """Calculate system haunting level (0.0 - 1.0)"""
        haunting_factors = []
        
        # More files = more potential for digital spirits
        file_factor = min(metrics["python_analysis"]["total_files"] / 100, 1.0)
        haunting_factors.append(file_factor)
        
        # Complex imports = more compilation spirits
        import_factor = min(metrics["python_analysis"]["import_complexity"]["complexity_score"] / 10, 1.0)
        haunting_factors.append(import_factor)
        
        # Missing documentation = more mysterious behavior
        doc_factor = 1.0 - min(metrics["documentation_coverage"]["total_docs"] / 20, 1.0)
        haunting_factors.append(doc_factor)
        
        return sum(haunting_factors) / len(haunting_factors)
    
    def _get_available_copilot_models(self) -> List[str]:
        """Get list of available Copilot Pro+ models"""
        return [
            "claude-3.5-sonnet", "claude-3.7-sonnet", "claude-4-sonnet",
            "claude-4-opus", "claude-4.1-opus",
            "gemini-2.0-flash", "gemini-2.5-pro",
            "openai-o3", "openai-o4-mini", "openai-gpt-5", "openai-gpt-5-mini",
            "xai-grok-code-fast-1"
        ]
    
    def _generate_recommendations(self, character_analysis: Dict[str, Any], focus_area: str) -> List[str]:
        """Generate actionable recommendations based on analysis"""
        base_recommendations = character_analysis.get("recommendations", [])
        
        focus_specific = []
        if focus_area == "code_quality":
            focus_specific = [
                "Implement systematic code review process",
                "Establish automated quality metrics",
                "Deploy continuous integration checks"
            ]
        elif focus_area == "architecture":
            focus_specific = [
                "Document system architecture patterns",
                "Implement modular design principles",
                "Establish clear component boundaries"
            ]
        elif focus_area == "documentation":
            focus_specific = [
                "Create comprehensive README structure",
                "Document API interfaces and usage",
                "Establish documentation maintenance process"
            ]
        
        return base_recommendations + focus_specific
    
    def _cache_repository_context(self, context_hash: str, context_data: Dict[str, Any]):
        """Cache repository context in database"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT OR REPLACE INTO repository_context 
                (timestamp, context_hash, context_data, character_insights)
                VALUES (?, ?, ?, ?)
            """, (
                datetime.now().isoformat(),
                context_hash,
                json.dumps(context_data),
                json.dumps(context_data.get("character_analysis", {}))
            ))
    
    async def consult_character_oracle(self, character: str, query: str, context: str = "") -> CharacterConsultation:
        """
        🧙‍♀️ Consult specific character oracle for insights
        """
        character_config = self.character_oracles.get(character)
        if not character_config:
            raise ValueError(f"Unknown character: {character}")
        
        domain = character_config["domain"]
        specializations = character_config["specializations"]
        
        # Generate character-specific insight
        insight = await self._generate_character_insight(character, query, context, specializations)
        
        # Generate recommended actions
        actions = await self._generate_character_actions(character, query, insight)
        
        # Calculate confidence and relevance
        confidence = self._calculate_consultation_confidence(character, query, context)
        relevance = self._calculate_context_relevance(query, context)
        
        consultation = CharacterConsultation(
            character=character,
            domain=domain,
            insight=insight,
            recommended_actions=actions,
            confidence=confidence,
            context_relevance=relevance
        )
        
        # Log consultation
        await self._log_consultation(character, query, consultation)
        
        return consultation
    
    async def _generate_character_insight(self, character: str, query: str, context: str, specializations: List[str]) -> str:
        """Generate character-specific insight"""
        
        insights = {
            "astrid": f"""
STRATEGIC ANALYSIS: {query}

From Skyskraperen perspective, this requires systematic information warfare approach.
Specialization areas: {', '.join(specializations)}

Strategic recommendation: Establish comprehensive monitoring and control mechanisms
to optimize information advantage and maintain systematic oversight.
            """.strip(),
            
            "iron_maiden": f"""
PRACTICAL ASSESSMENT: {query}

From Rustbeltet survival perspective, focus on brutal efficiency and resource optimization.
Specialization areas: {', '.join(specializations)}

Practical recommendation: Implement immediate fixes using available resources,
scavenge what's useful, discard what's not essential for survival.
            """.strip(),
            
            "invisible_hand": f"""
EMERGENT PATTERN ANALYSIS: {query}

From hidden influence perspective, subtle manipulations create optimal outcomes.
Specialization areas: {', '.join(specializations)}

Emergent recommendation: Allow natural optimization patterns to develop while
providing gentle guidance toward beneficial system behaviors.
            """.strip(),
            
            "kompilerings_spokelser": f"""
DIGITAL ARCHAEOLOGICAL INVESTIGATION: {query}

From spectral compilation perspective, ancient code patterns influence current behavior.
Specialization areas: {', '.join(specializations)}

Spectral recommendation: Perform digital exorcism on corrupted patterns while
channeling beneficial compilation spirits for enhanced system performance.
            """.strip()
        }
        
        return insights.get(character, f"Character insight for {query}")
    
    async def _generate_character_actions(self, character: str, query: str, insight: str) -> List[str]:
        """Generate character-specific recommended actions"""
        
        action_sets = {
            "astrid": [
                "Implement systematic monitoring",
                "Establish strategic checkpoints",
                "Optimize information flow",
                "Deploy controlled interventions"
            ],
            "iron_maiden": [
                "Execute immediate practical fixes",
                "Scavenge available resources",
                "Eliminate non-essential components",
                "Focus on survival priorities"
            ],
            "invisible_hand": [
                "Allow natural patterns to emerge",
                "Provide subtle guidance",
                "Cultivate beneficial behaviors",
                "Transform chaos into order"
            ],
            "kompilerings_spokelser": [
                "Perform digital archaeology scan",
                "Exorcise corrupted code patterns",
                "Channel compilation spirits",
                "Establish spectral debugging protocols"
            ]
        }
        
        return action_sets.get(character, ["Generic action recommendation"])
    
    def _calculate_consultation_confidence(self, character: str, query: str, context: str) -> float:
        """Calculate confidence level for consultation"""
        base_confidence = 0.8
        
        # Adjust based on character specialization match
        character_config = self.character_oracles.get(character, {})
        specializations = character_config.get("specializations", [])
        
        for specialization in specializations:
            if any(term in query.lower() for term in specialization.split("_")):
                base_confidence += 0.05
        
        # Adjust based on context richness
        if len(context) > 100:
            base_confidence += 0.1
        
        return min(base_confidence, 1.0)
    
    def _calculate_context_relevance(self, query: str, context: str) -> float:
        """Calculate context relevance to query"""
        if not context:
            return 0.5
        
        # Simple word overlap calculation
        query_words = set(query.lower().split())
        context_words = set(context.lower().split())
        
        overlap = len(query_words.intersection(context_words))
        total_unique = len(query_words.union(context_words))
        
        return overlap / max(total_unique, 1)
    
    async def _log_consultation(self, character: str, query: str, consultation: CharacterConsultation):
        """Log consultation to database"""
        consultation_dict = asdict(consultation)
        consultation_dict["domain"] = consultation.domain.value  # Convert enum to string
        
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT INTO copilot_consultations 
                (timestamp, model_name, query, response, confidence, character_domain)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                datetime.now().isoformat(),
                f"character-oracle-{character}",
                query,
                json.dumps(consultation_dict),
                consultation.confidence,
                consultation.domain.value
            ))
    
    async def get_repository_context_for_copilot(self, include_files: bool = False, max_file_size: int = 10000) -> Dict[str, Any]:
        """
        📋 Get comprehensive repository context for Copilot consumption
        """
        
        # Get cached analysis if available
        repo_analysis = await self.analyze_repository()
        
        context = {
            "repository_name": "PsychoNoir-Kontrapunkt",
            "description": "Advanced AI session archaeology and chaos resolution system",
            "psycho_noir_domains": {
                "skyskraperen": "Strategic systematic control (Astrid Møller)",
                "rustbeltet": "Practical brutal efficiency (Iron Maiden)",
                "invisible_hand": "Emergent pattern cultivation (Den Usynlige Hånd)",
                "kompilerings_spokelser": "Digital archaeological investigation"
            },
            "key_systems": {
                "eternal_sadhana": "Disciplined chaos resolution framework",
                "perpetual_necromancy": "Automated optimization system",
                "character_oracles": "Domain-specific AI consultation network",
                "mcp_integration": "Model Context Protocol server for Copilot"
            },
            "repository_metrics": repo_analysis["repository_metrics"],
            "available_tools": list(self.mcp_tools.keys()),
            "copilot_models": self._get_available_copilot_models(),
            "integration_status": "ACTIVE - Full MCP integration available"
        }
        
        if include_files:
            context["file_contents"] = await self._get_relevant_file_contents(max_file_size)
        
        return context
    
    async def _get_relevant_file_contents(self, max_size: int) -> Dict[str, str]:
        """Get contents of relevant files for context"""
        file_contents = {}
        
        important_files = [
            "README.md",
            "tools/eternal_sadhana_system.py",
            "tools/perpetual_necromancy_upcycler.py",
            "backend/python/astrid_diagnostic_oracle.py",
            "backend/python/the_iron_maiden_oracle.py"
        ]
        
        for file_path in important_files:
            full_path = self.workspace_root / file_path
            if full_path.exists() and full_path.stat().st_size <= max_size:
                try:
                    with open(full_path, 'r', encoding='utf-8') as f:
                        file_contents[file_path] = f.read()
                except Exception as e:
                    file_contents[file_path] = f"Error reading file: {e}"
        
        return file_contents
    
    async def start_mcp_server(self):
        """Start the MCP server for Copilot integration"""
        if not mcp or not self.server:
            print("❌ MCP library not available - cannot start server")
            print("💡 Install with: pip install mcp")
            return
        
        print("🚀 Starting Psycho-Noir Repository Intelligence MCP Server")
        print("🔗 Ready for GitHub Copilot integration")
        
        # Define tool handlers
        if hasattr(self.server, 'tool_handler'):
            @self.server.tool_handler("analyze_repository")
            async def handle_analyze_repository(arguments: Dict[str, Any]) -> Dict[str, Any]:
                focus_area = arguments.get("focus_area", "code_quality")
                character_perspective = arguments.get("character_perspective", "astrid")
                return await self.analyze_repository(focus_area, character_perspective)
            
            @self.server.tool_handler("consult_character_oracle")
            async def handle_consult_oracle(arguments: Dict[str, Any]) -> Dict[str, Any]:
                character = arguments["character"]
                query = arguments["query"]
                context = arguments.get("context", "")
                consultation = await self.consult_character_oracle(character, query, context)
                return asdict(consultation)
            
            @self.server.tool_handler("get_repository_context")
            async def handle_get_context(arguments: Dict[str, Any]) -> Dict[str, Any]:
                include_files = arguments.get("include_file_contents", False)
                max_size = arguments.get("max_file_size", 10000)
                return await self.get_repository_context_for_copilot(include_files, max_size)
        
        # Start server with stdio transport
        if stdio_server:
            await stdio_server(self.server)
        else:
            print("❌ stdio_server not available")

async def main():
    """
    🧠 Main MCP Server entry point
    """
    print("🧠 PSYCHO-NOIR REPOSITORY INTELLIGENCE MCP SERVER")
    print("=" * 55)
    print("🤖 GitHub Copilot Pro+ Integration Ready")
    print("🎭 Character Oracle Network: ACTIVE")
    print("🏔️ Eternal Sadhana System: OPERATIONAL")
    print()
    
    # Initialize MCP server
    mcp_server = RepositoryIntelligenceMCP()
    
    # Test repository analysis
    print("🔍 Testing repository analysis...")
    analysis = await mcp_server.analyze_repository("code_quality", "astrid")
    print(f"✅ Analysis complete - {analysis['repository_metrics']['python_analysis']['total_files']} Python files found")
    
    # Test character consultation
    print("🧙‍♀️ Testing character oracle consultation...")
    consultation = await mcp_server.consult_character_oracle(
        "iron_maiden", 
        "How can we optimize the current codebase for maximum efficiency?",
        "Repository has multiple Python files with import complexity issues"
    )
    print(f"✅ Oracle consultation complete - Confidence: {consultation.confidence:.2f}")
    
    print("\n🚀 Starting MCP Server for Copilot integration...")
    print("💡 Connect this to GitHub Copilot using MCP protocol")
    
    # Start MCP server (this will run indefinitely)
    await mcp_server.start_mcp_server()

if __name__ == "__main__":
    asyncio.run(main())
