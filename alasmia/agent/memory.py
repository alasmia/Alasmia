"""
Alasmia Memory - Complete long-term and short-term memory management

Stores user profiles, conversations, emotions, preferences, and milestones.
"""

import os
import json
from datetime import datetime
from typing import List, Dict, Optional
from pathlib import Path

try:
    from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, JSON
    from sqlalchemy.ext.declarative import declarative_base
    from sqlalchemy.orm import sessionmaker
    HAS_SQLALCHEMY = True
except ImportError:
    HAS_SQLALCHEMY = False


Base = declarative_base() if HAS_SQLALCHEMY else object


class ConversationMessage(Base):
    """SQLAlchemy model for conversation messages."""
    __tablename__ = "conversations"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(255), index=True)
    role = Column(String(50))
    content = Column(Text)
    mood = Column(String(50), nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    language = Column(String(20), default="english")


class UserPreference(Base):
    """SQLAlchemy model for user preferences."""
    __tablename__ = "user_preferences"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(255), unique=True, index=True)
    name = Column(String(255), nullable=True)
    companion_gender = Column(String(20), default="female")  # male (Alas) or female (Mia)
    language = Column(String(50), default="english")
    relationship_stage = Column(String(50), default="stranger")
    message_count = Column(Integer, default=0)
    connection_score = Column(Integer, default=0)
    first_seen = Column(DateTime, default=datetime.utcnow)
    last_seen = Column(DateTime, default=datetime.utcnow)
    preferences_json = Column(Text, nullable=True)  # JSON string
    milestones_json = Column(Text, nullable=True)  # JSON string


class MemoryManager:
    """
    Manages complete user memory including:
    - User profiles
    - Conversation history
    - Emotional events
    - Preferences
    - Milestones
    """
    
    def __init__(self):
        """Initialize memory manager."""
        db_path = os.getenv("MEMORY_DB_PATH", "./data/alasmia.db")
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        
        if HAS_SQLALCHEMY:
            self.engine = create_engine(f"sqlite:///{db_path}", echo=False)
            Base.metadata.create_all(self.engine)
            Session = sessionmaker(bind=self.engine)
            self.session = Session()
        else:
            self.session = None
            self.engine = None
        
        # File-based fallback
        self.data_dir = Path("./data")
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.memory_file = self.data_dir / "memory.json"
        self.memory = self._load_memory()
    
    def _load_memory(self) -> dict:
        """Load memory from file (fallback)."""
        if self.memory_file.exists():
            with open(self.memory_file, 'r') as f:
                return json.load(f)
        return {"users": {}, "conversations": {}}
    
    def _save_memory(self):
        """Save memory to file."""
        with open(self.memory_file, 'w') as f:
            json.dump(self.memory, f, indent=2)
    
    # ========== USER MANAGEMENT ==========
    
    def create_user(self, user_id: str, name: str = None, language: str = "english", companion_gender: str = "female"):
        """Create a new user profile."""
        if self.session and HAS_SQLALCHEMY:
            user = UserPreference(
                user_id=user_id,
                name=name,
                language=language,
                companion_gender=companion_gender,
                relationship_stage="stranger",
                message_count=0,
                first_seen=datetime.utcnow(),
                last_seen=datetime.utcnow()
            )
            self.session.add(user)
            self.session.commit()
        
        # Also save to file
        if user_id not in self.memory["users"]:
            self.memory["users"][user_id] = {
                "name": name,
                "companion_gender": companion_gender,
                "language": language,
                "relationship_stage": "stranger",
                "message_count": 0,
                "connection_score": 0,
                "first_seen": datetime.utcnow().isoformat(),
                "last_seen": datetime.utcnow().isoformat(),
                "milestones": [],
                "preferences": {}
            }
            self.memory["conversations"][user_id] = []
            self._save_memory()
    
    def get_user_info(self, user_id: str) -> Optional[Dict]:
        """Get user information."""
        if self.session and HAS_SQLALCHEMY:
            user = self.session.query(UserPreference).filter_by(user_id=user_id).first()
            if user:
                return {
                    "name": user.name,
                    "companion_gender": user.companion_gender,
                    "language": user.language,
                    "relationship_stage": user.relationship_stage,
                    "message_count": user.message_count,
                    "connection_score": user.connection_score,
                    "first_seen": user.first_seen.isoformat() if user.first_seen else None,
                    "last_seen": user.last_seen.isoformat() if user.last_seen else None,
                    "milestones": json.loads(user.milestones_json or "[]"),
                    "preferences": json.loads(user.preferences_json or "{}")
                }
        
        # File fallback
        return self.memory["users"].get(user_id)
    
    def update_user(self, user_id: str, updates: Dict):
        """Update user information."""
        if self.session and HAS_SQLALCHEMY:
            user = self.session.query(UserPreference).filter_by(user_id=user_id).first()
            if user:
                for key, value in updates.items():
                    if hasattr(user, key):
                        setattr(user, key, value)
                user.last_seen = datetime.utcnow()
                self.session.commit()
        
        # File fallback
        if user_id in self.memory["users"]:
            self.memory["users"][user_id].update(updates)
            self.memory["users"][user_id]["last_seen"] = datetime.utcnow().isoformat()
            self._save_memory()
    
    def get_or_create_user(self, user_id: str) -> any:
        """Get existing user or create new one."""
        info = self.get_user_info(user_id)
        if not info:
            self.create_user(user_id)
            return self.get_user_info(user_id)
        return info
    
    # ========== CONVERSATION MANAGEMENT ==========
    
    def add_message(self, user_id: str, role: str, content: str, mood: str = None, language: str = "english"):
        """Add a message to conversation history."""
        if self.session and HAS_SQLALCHEMY:
            msg = ConversationMessage(
                user_id=user_id,
                role=role,
                content=content,
                mood=mood,
                language=language,
                timestamp=datetime.utcnow()
            )
            self.session.add(msg)
        
        # Also save to file
        if user_id not in self.memory["conversations"]:
            self.memory["conversations"][user_id] = []
        
        self.memory["conversations"][user_id].append({
            "role": role,
            "content": content,
            "mood": mood,
            "timestamp": datetime.utcnow().isoformat(),
            "language": language
        })
        
        # Update message count
        if role == "user":
            self.increment_message_count(user_id)
        
        self._save_memory()
    
    def get_conversation(self, user_id: str, limit: int = 50) -> List[Dict]:
        """Get recent conversation history."""
        if self.session and HAS_SQLALCHEMY:
            messages = (
                self.session.query(ConversationMessage)
                .filter_by(user_id=user_id)
                .order_by(ConversationMessage.timestamp.desc())
                .limit(limit)
                .all()
            )
            return [{"role": m.role, "content": m.content, "mood": m.mood} for m in reversed(messages)]
        
        # File fallback
        conv = self.memory["conversations"].get(user_id, [])
        return list(reversed(conv[-limit:]))
    
    def clear_conversation(self, user_id: str):
        """Clear conversation history."""
        if self.session and HAS_SQLALCHEMY:
            self.session.query(ConversationMessage).filter_by(user_id=user_id).delete()
            self.session.commit()
        
        # File fallback
        if user_id in self.memory["conversations"]:
            self.memory["conversations"][user_id] = []
            self._save_memory()
    
    def increment_message_count(self, user_id: str):
        """Increment user's message count and check stage progression."""
        info = self.get_user_info(user_id)
        if info:
            new_count = info.get("message_count", 0) + 1
            self.update_user(user_id, {"message_count": new_count})
            
            # Auto-progress stage
            self._check_stage_progression(user_id, new_count)
    
    def _check_stage_progression(self, user_id: str, message_count: int):
        """Check and update relationship stage based on message count."""
        thresholds = {"acquaintance": 10, "friend": 50, "close": 200, "partner": 500}
        
        info = self.get_user_info(user_id)
        current_stage = info.get("relationship_stage", "stranger") if info else "stranger"
        
        for stage, threshold in thresholds.items():
            if message_count >= threshold:
                current_idx = ["stranger", "acquaintance", "friend", "close", "partner"].index(current_stage)
                new_idx = ["stranger", "acquaintance", "friend", "close", "partner"].index(stage)
                
                if new_idx > current_idx:
                    self.update_relationship_stage(user_id, stage)
                    break
    
    def update_relationship_stage(self, user_id: str, stage: str):
        """Update user's relationship stage."""
        valid_stages = ["stranger", "acquaintance", "friend", "close", "partner"]
        if stage not in valid_stages:
            return
        
        self.update_user(user_id, {"relationship_stage": stage})
    
    # ========== PREFERENCES ==========
    
    def save_preference(self, user_id: str, key: str, value: any):
        """Save a user preference."""
        info = self.get_user_info(user_id)
        if info:
            prefs = info.get("preferences", {})
            prefs[key] = value
            self.update_user(user_id, {"preferences": prefs})
    
    def get_preference(self, user_id: str, key: str, default: any = None) -> any:
        """Get a user preference."""
        info = self.get_user_info(user_id)
        if info:
            return info.get("preferences", {}).get(key, default)
        return default
    
    # ========== MILESTONES ==========
    
    def add_milestone(self, user_id: str, milestone: str):
        """Record a milestone achievement."""
        info = self.get_user_info(user_id)
        if info:
            milestones = info.get("milestones", [])
            if milestone not in milestones:
                milestones.append({
                    "milestone": milestone,
                    "timestamp": datetime.utcnow().isoformat()
                })
                self.update_user(user_id, {"milestones": milestones})
    
    def get_milestones(self, user_id: str) -> List[Dict]:
        """Get user's milestone achievements."""
        info = self.get_user_info(user_id)
        return info.get("milestones", []) if info else []
    
    # ========== CLEANUP ==========
    
    def close(self):
        """Close database session."""
        if self.session:
            self.session.close()
