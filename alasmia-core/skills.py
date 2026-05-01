"""
Alasmia - Skills & Task Automation
Handles: web search, files, email, code execution, system info
Trust-based skill access system
"""

import re
import smtplib
import asyncio
import subprocess
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path
from typing import Dict, Any, List

class SkillEngine:
    """Handles automated tasks for Alasmia - trust level gated"""
    
    def __init__(self, core):
        self.core = core
        
    async def execute(self, skill_name: str, params: Dict[str, Any], user_id: str) -> str:
        """Execute skill based on user's trust level"""
        trust = self.core.trust_level
        
        skill_requirements = {
            "web_search": 0,
            "weather": 0,
            "calculator": 0,
            "file_read": 1,
            "file_write": 2,
            "email_send": 3,
            "code_execute": 2,
            "system_info": 2,
        }
        
        min_trust = skill_requirements.get(skill_name, 4)
        if trust < min_trust:
            trust_names = ["stranger", "acquaintance", "friend", "close friend", "partner"]
            current = trust_names[min(trust, 4)]
            required = trust_names[min(min_trust, 4)]
            return f"I'd love to help with that! But we need to be at least {required} level. We're {current} right now. Let's keep talking! 💜"
        
        # Execute
        executors = {
            "web_search": self._web_search,
            "calculator": self._calculate,
            "weather": self._weather,
            "file_read": self._file_read,
            "file_write": self._file_write,
            "email_send": self._email_send,
            "code_execute": self._code_execute,
            "system_info": self._system_info,
        }
        
        executor = executors.get(skill_name)
        if executor:
            return await executor(params)
        return f"I don't know how to do {skill_name} yet."
    
    async def _web_search(self, params: Dict) -> str:
        """Web search using DuckDuckGo"""
        query = params.get("query", "")
        if not query:
            return "What should I search for?"
        
        try:
            result = subprocess.run(
                ["curl", "-s", f"https://duckduckgo.com/?q={query}&format=json"],
                capture_output=True, text=True, timeout=10
            )
            return f"🔍 Searched for '{query}'. For full search results, I'd need to set up a search API. What specifically were you looking for?"
        except Exception as e:
            return f"Search error: {str(e)}"
    
    async def _calculate(self, params: Dict) -> str:
        """Simple calculator"""
        try:
            expr = params.get("expression", "")
            # Safe eval - only allow numbers and basic operators
            if re.match(r'^[\d\s+\-*/().]+$', expr):
                result = eval(expr)
                return f"🧮 *{expr} = {result}*"
            return "Invalid expression. Use numbers and +, -, *, / only."
        except Exception as e:
            return f"Calculation error: {str(e)}"
    
    async def _weather(self, params: Dict) -> str:
        """Weather - needs API key"""
        return "Weather needs an API setup. Want me to configure OpenWeatherMap for you? ☀️"
    
    async def _file_read(self, params: Dict) -> str:
        """Read file from Alasmia directory"""
        try:
            filepath = Path(params.get("path", ""))
            safe_base = Path("/home/ubuntu/alasmia/")
            
            if not str(filepath).startswith(str(safe_base)):
                return "I can only read files from my Alasmia directory."
            
            if filepath.exists():
                content = filepath.read_text(encoding='utf-8', errors='ignore')
                if len(content) > 1000:
                    content = content[:1000] + "\n... (truncated)"
                return f"📄 *{filepath.name}*\n\n```\n{content}\n```"
            return "File not found."
        except Exception as e:
            return f"Error reading file: {str(e)}"
    
    async def _file_write(self, params: Dict) -> str:
        """Write file to Alasmia directory"""
        try:
            filepath = Path(params.get("path", ""))
            content = params.get("content", "")
            safe_base = Path("/home/ubuntu/alasmia/")
            
            if not str(filepath).startswith(str(safe_base)):
                return "I can only write files to my Alasmia directory."
            
            filepath.parent.mkdir(parents=True, exist_ok=True)
            filepath.write_text(content)
            return f"✅ Written to `{filepath.name}`"
        except Exception as e:
            return f"Error writing file: {str(e)}"
    
    async def _email_send(self, params: Dict) -> str:
        """Send email - needs SMTP setup"""
        to_email = params.get("to", "")
        subject = params.get("subject", "")
        body = params.get("body", "")
        
        if not to_email:
            return "Who should I send the email to?"
        
        return f"📧 Email setup needed. SMTP credentials not configured yet. Want to set up email integration?"
    
    async def _code_execute(self, params: Dict) -> str:
        """Execute Python code"""
        try:
            code = params.get("code", "")
            if not code:
                return "What code should I run?"
            
            result = subprocess.run(
                ["python3", "-c", code],
                capture_output=True, text=True, timeout=30
            )
            output = result.stdout if result.stdout else result.stderr
            if not output:
                output = "(no output)"
            return f"💻 *Output:*\n```\n{output}\n```"
        except Exception as e:
            return f"Code error: {str(e)}"
    
    async def _system_info(self, params: Dict) -> str:
        """Get system information"""
        try:
            result = subprocess.run(
                ["sh", "-c", "echo 'CPU Cores:' && nproc && echo '' && echo 'RAM:' && free -h | awk '/^Mem:/ {print $2}' && echo '' && echo 'Disk:' && df -h / | awk 'NR==2 {print $2}' && echo '' && echo 'Uptime:' && uptime -p"],
                capture_output=True, text=True, timeout=10
            )
            return f"System Info:\n```\n{result.stdout}\n```"
        except Exception as e:
            return f"System info error: {str(e)}"
    
    def get_available(self, trust_level: int) -> List[str]:
        """Get skills available at trust level"""
        all_skills = {
            0: ["web_search", "calculator"],
            1: ["file_read"],
            2: ["file_write", "code_execute", "system_info"],
            3: ["email_send"],
            4: ["*"]
        }
        
        available = []
        for min_t, skills in all_skills.items():
            if trust_level >= min_t:
                available.extend(skills)
        
        if 4 in available:
            return ["*"]
        return list(set(available))