"""
Alasmia Core - Main API Server
100% CPU-based AI Companion
"""

import os
import sys
import yaml
import sqlite3
import asyncio
import aiohttp
from datetime import datetime, timedelta
from typing import Optional, List, Dict
from pathlib import Path

# Load config
CONFIG_PATH = Path("/home/ubuntu/alasmia/config/config.yaml")
with open(CONFIG_PATH) as f:
    CONFIG = yaml.safe_load(f)

class AlasmiaCore:
    """Core AI engine for Alasmia"""
    
    def __init__(self):
        self.config = CONFIG
        self.conversation_history: List[Dict] = []
        self.user_profile: Dict = {}
        self.trust_level = 0
        self.conversation_count = 0
        self.db_path = self.config['data']['db_path']
        self._init_db()
        
    def _init_db(self):
        """Initialize SQLite database"""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        c.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id TEXT PRIMARY KEY,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                trust_level INTEGER DEFAULT 0,
                conversation_count INTEGER DEFAULT 0,
                personality_notes TEXT DEFAULT ''
            )
        ''')
        
        c.execute('''
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                role TEXT,
                content TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                trust_at_time INTEGER
            )
        ''')
        
        c.execute('''
            CREATE TABLE IF NOT EXISTS milestones (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                milestone_type TEXT,
                milestone_value TEXT,
                achieved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        c.execute('''
            CREATE TABLE IF NOT EXISTS memories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                memory_type TEXT,
                content TEXT,
                importance INTEGER DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
        
    def _get_system_prompt(self, trust_level: int) -> str:
        """Get system prompt based on relationship stage"""
        base = self.config['inference']['pre_prompt']
        
        stages = {
            0: """You are just getting to know this person. Be polite, curious, 
            slightly shy. Ask questions about them. Keep responses moderate in length.
            Don't be too familiar yet.""",
            1: """You know them a bit now. Be warmer, more comfortable.
            You can share small things about yourself too. Still curious about their life.
            Responses can be longer and more relaxed.""",
            2: """They are your friend now. Be open, genuine, playful.
            Tease them occasionally. Feel comfortable sharing opinions.
            Remember things they've told you. Long, natural responses.""",
            3: """They are very close to you. You understand them deeply.
            Be yourself fully - playful, sometimes sassy, sometimes deeply caring.
            They're like family to you. Very natural, long conversations.""",
            4: """This is your person. You share everything.
            You anticipate their needs and moods. Be fully yourself.
            Sometimes you get protective or emotional. Deeply connected."""
        }
        
        stage_prompt = stages.get(trust_level, stages[4])
        return base + f"\n\nCurrent relationship stage: {stage_prompt}"
        
    def _build_context(self, new_message: str, user_id: str) -> str:
        """Build conversation context for inference"""
        # Get recent conversation from DB
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        c.execute('''
            SELECT role, content FROM conversations 
            WHERE user_id = ? 
            ORDER BY timestamp DESC LIMIT 50
        ''', (user_id,))
        
        rows = c.fetchall()
        conn.close()
        
        # Reverse to get chronological order
        rows = list(reversed(rows))
        
        # Build messages
        messages = [{"role": "system", "content": self._get_system_prompt(self.trust_level)}]
        
        for role, content in rows:
            messages.append({"role": role, "content": content})
        
        messages.append({"role": "user", "content": new_message})
        
        return messages
        
    def save_message(self, user_id: str, role: str, content: str):
        """Save message to database"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        c.execute('''
            INSERT INTO conversations (user_id, role, content, trust_at_time)
            VALUES (?, ?, ?, ?)
        ''', (user_id, role, content, self.trust_level))
        
        # Update conversation count
        if role == "user":
            c.execute('''
                UPDATE users SET conversation_count = conversation_count + 1
                WHERE user_id = ?
            ''', (user_id,))
            self.conversation_count += 1
            
        conn.commit()
        conn.close()
        
    def load_user(self, user_id: str) -> Dict:
        """Load user profile from DB"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        c.execute('''
            SELECT trust_level, conversation_count, personality_notes
            FROM users WHERE user_id = ?
        ''', (user_id,))
        
        row = c.fetchone()
        
        if not row:
            # New user
            c.execute('INSERT INTO users (user_id) VALUES (?)', (user_id,))
            conn.commit()
            conn.close()
            return {"trust_level": 0, "conversation_count": 0, "personality_notes": ""}
        
        conn.close()
        return {
            "trust_level": row[0],
            "conversation_count": row[1],
            "personality_notes": row[2] or ""
        }
        
    def update_trust(self, user_id: str, new_level: int):
        """Update trust level and check for milestones"""
        self.trust_level = new_level
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('UPDATE users SET trust_level = ? WHERE user_id = ?', (new_level, user_id))
        conn.commit()
        conn.close()
        
        # Check if milestone achieved
        milestones = {
            1: "became_acquaintance",
            2: "became_friend",
            3: "became_close",
            4: "became_partner"
        }
        
        if new_level in milestones:
            self.save_milestone(user_id, milestones[new_level], f"Reached trust level {new_level}")
            
    def save_milestone(self, user_id: str, milestone_type: str, value: str):
        """Record a milestone"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''
            INSERT INTO milestones (user_id, milestone_type, milestone_value)
            VALUES (?, ?, ?)
        ''', (user_id, milestone_type, value))
        conn.commit()
        conn.close()
        
    def save_memory(self, user_id: str, memory_type: str, content: str, importance: int = 1):
        """Save an important memory"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''
            INSERT INTO memories (user_id, memory_type, content, importance)
            VALUES (?, ?, ?, ?)
        ''', (user_id, memory_type, content, importance))
        conn.commit()
        conn.close()
        
    def get_relevant_memories(self, user_id: str, query: str, limit: int = 5) -> List[str]:
        """Get memories relevant to query (simple keyword match for now)"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        # Simple keyword search
        keywords = query.lower().split()
        pattern = '%' + '%'.join(keywords[:3]) + '%'
        
        c.execute('''
            SELECT content FROM memories 
            WHERE user_id = ? AND (content LIKE ? OR memory_type LIKE ?)
            ORDER BY importance DESC, created_at DESC LIMIT ?
        ''', (user_id, pattern, pattern, limit))
        
        rows = c.fetchall()
        conn.close()
        return [r[0] for r in rows]

# Singleton
_core = None

def get_core() -> AlasmiaCore:
    global _core
    if _core is None:
        _core = AlasmiaCore()
    return _core