#!/usr/bin/env python3
"""
🔗 GitHub API + Chat Session Bridge - Pro+ Enhanced
Direct GitHub API integration with chat session for autonomous orchestration

CLAUDINE SIN'CLAIRE 3.7 TEMPORAL ENHANCED - GitHub Pro+ Sophistication
"""

import json
import asyncio
from datetime import datetime
from pathlib import Path

class GitHubProBridge:
    """
    GitHub Pro+ bridge for autonomous repository management
    Uses gh CLI with direct GitHub API integration
    """
    
    def __init__(self, session_id=None):
        self.session_id = session_id or f"gh-pro-bridge-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        self.command_history = []
        self.bridge_status = "GITHUB_PRO_ACTIVE"
        
    async def gh_api_call(self, endpoint: str, method="GET", data=None) -> dict:
        """
        Make GitHub API calls using gh CLI
        """
        try:
            cmd = ['gh', 'api', endpoint]
            if method != "GET":
                cmd.extend(['--method', method])
            if data:
                cmd.extend(['--input', '-'])
            
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                stdin=asyncio.subprocess.PIPE if data else None
            )
            
            input_data = json.dumps(data).encode() if data else None
            stdout, stderr = await process.communicate(input=input_data)
            
            if process.returncode == 0:
                return {
                    "data": json.loads(stdout.decode()),
                    "endpoint": endpoint,
                    "timestamp": datetime.now().isoformat()
                }
            else:
                return {
                    "error": stderr.decode(),
                    "endpoint": endpoint,
                    "timestamp": datetime.now().isoformat()
                }
                
        except Exception as e:
            return {
                "error": str(e),
                "endpoint": endpoint,
                "timestamp": datetime.now().isoformat()
            }
    
    async def analyze_repository_insights(self) -> dict:
        """
        Analyze repository using GitHub API insights
        """
        repo = "poisontr33s/PsychoNoir-Kontrapunkt"
        
        print(f"🔍 Analyzing repository: {repo}")
        
        # Get repository details
        repo_info = await self.gh_api_call(f"repos/{repo}")
        
        # Get recent commits
        commits = await self.gh_api_call(f"repos/{repo}/commits?per_page=10")
        
        # Get issues
        issues = await self.gh_api_call(f"repos/{repo}/issues?state=all&per_page=20")
        
        # Get repository languages
        languages = await self.gh_api_call(f"repos/{repo}/languages")
        
        # Get repository topics
        topics = await self.gh_api_call(f"repos/{repo}/topics")
        
        workflows = await self.gh_api_call(f"repos/{repo}/actions/workflows")
        
        analysis = {
            "session_id": self.session_id,
            "repository": repo,
            "timestamp": datetime.now().isoformat(),
            "repository_info": repo_info,
            "recent_commits": commits,
            "issues": issues,
            "languages": languages,
            "topics": topics,
            "workflows": workflows
        }
        
        return analysis
    
    async def create_intelligent_issue(self, title: str, body: str, labels=None) -> dict:
        """
        Create an issue using GitHub API
        """
        repo = "poisontr33s/PsychoNoir-Kontrapunkt"
        
        issue_data = {
            "title": title,
            "body": body
        }
        
        if labels:
            issue_data["labels"] = labels
        
        result = await self.gh_api_call(f"repos/{repo}/issues", method="POST", data=issue_data)
        
        print(f"📝 Created issue: {title}")
        return result
    
    async def autonomous_repository_management(self) -> dict:
        """
        Perform autonomous repository management tasks
        """
        print("🏴‍☠️ AUTONOMOUS GITHUB PRO+ REPOSITORY MANAGEMENT")
        print("=" * 60)
        
        # Get comprehensive repository analysis
        analysis = await self.analyze_repository_insights()
        
        # Extract insights
        repo_data = analysis.get("repository_info", {}).get("data", {})
        commits_data = analysis.get("recent_commits", {}).get("data", [])
        issues_data = analysis.get("issues", {}).get("data", [])
        languages_data = analysis.get("languages", {}).get("data", {})
        
        # Generate insights
        insights = {
            "repository_size": repo_data.get("size", 0),
            "stars": repo_data.get("stargazers_count", 0),
            "forks": repo_data.get("forks_count", 0),
            "open_issues": repo_data.get("open_issues_count", 0),
            "primary_language": repo_data.get("language", "Unknown"),
            "recent_commits_count": len(commits_data),
            "total_issues": len(issues_data),
            "languages_breakdown": languages_data
        }
        
        print(f"📊 Repository size: {insights['repository_size']} KB")
        print(f"⭐ Stars: {insights['stars']}")
        print(f"🔄 Forks: {insights['forks']}")
        print(f"🐛 Open issues: {insights['open_issues']}")
        print(f"🐍 Primary language: {insights['primary_language']}")
        print(f"📝 Recent commits: {insights['recent_commits_count']}")
        
        if insights['open_issues'] > 5:
            await self.create_intelligent_issue(
                "🤖 Autonomous Repository Management Alert",
                f"""## 🔍 Autonomous Analysis Report
                
Repository has {insights['open_issues']} open issues requiring attention.

### 📊 Current Statistics:
- **Size**: {insights['repository_size']} KB  
- **Primary Language**: {insights['primary_language']}
- **Recent Commits**: {insights['recent_commits_count']}
- **Open Issues**: {insights['open_issues']}

### 🎯 Recommended Actions:
1. Review and triage open issues
2. Update documentation 
3. Consider issue cleanup automation

---
*Generated by Autonomous GitHub Pro+ Bridge - {datetime.now().isoformat()}*
                """,
                labels=["automation", "maintenance"]
            )
        
        # Save comprehensive analysis
        log_path = self.save_session_log({
            "analysis": analysis,
            "insights": insights,
            "autonomous_actions": "Issue created for high issue count" if insights['open_issues'] > 5 else "No actions needed"
        })
        
        return {
            "insights": insights,
            "analysis": analysis,
            "log_path": str(log_path)
        }
    
    def save_session_log(self, data: dict, filename: str | None = None):
        """
        Save session data to JSON file
        """
        if not filename:
            filename = f"gh_pro_session_{self.session_id}.json"
        
        output_path = Path(f"/workspaces/PsychoNoir-Kontrapunkt/data/generert/{filename}")
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"💾 Session saved to: {output_path}")
        return output_path

# Direct execution demo
async def autonomous_github_pro_demo():
    """
    Demonstrate autonomous GitHub Pro+ integration
    """
    bridge = GitHubProBridge()
    
    # Execute autonomous repository management
    results = await bridge.autonomous_repository_management()
    
    print(f"\n🎭 BRIDGE STATUS: {bridge.bridge_status}")
    print(f"📊 API calls made: {len(bridge.command_history)}")
    print(f"💾 Analysis complete: {results['log_path']}")
    
    return results

if __name__ == "__main__":
    asyncio.run(autonomous_github_pro_demo())
