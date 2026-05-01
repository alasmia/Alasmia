"""
Alasmia Memory - Long-term and Short-term Memory Management

Handles conversation storage, user preferences, and semantic search.
"""

import os
import json
from datetime import datetime
from typing import List, Dict, Optional, Tuple
from pathlib import Path

from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

Base = declarative_base()


class ConversationMessage(Base):
    """SQLAlchemy model for conversation messages."""
    __tablename__ = "conversations"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(255), index=True)
    role = Column(String(50))  # "user" or "assistant"
    content = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)
    language = Column(String(20), default="hinglish")


class UserPreference(Base):
    """SQLAlchemy model for user preferences."""
    __tablename__ = "user_preferences"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(255), unique=True, index=True)
    name = Column(String(255), nullable=True)
    language = Column(String(50), default="hinglish")
    relationship_stage = Column(String(50), default="stranger")
    message_count = Column(Integer, default=0)
    first_seen = Column(DateTime, default=datetime.utcnow)
    last_seen = Column(DateTime, default=datetime.utcnow)
    personality_prefs = Column(Text, nullable=True)  # JSON string


class MemoryManager:
    """Manages both short-term and long-term memory."""
    
    def __init__(self):
        """Initialize memory manager with database."""
        db_path = os.getenv("MEMORY_DB_PATH", "./data/alasmia.db")
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        
        self.engine = create_engine(f"sqlite:///{db_path}", echo=False)
        Base.metadata.create_all(self.engine)
        
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        
        # Short-term memory (in-memory cache)
        self.short_term: Dict[str, List[Dict]] = {}
    
    def add_message(
        self,
        user_id: str,
        role: str,
        content: str,
        language: str = "hinglish"
    ) -> None:
        """Add a message to conversation history."""
        message = ConversationMessage(
            user_id=user_id,
            role=role,
            content=content,
            language=language
        )
        self.session.add(message)
        self.session.commit()
        
        # Update short-term cache
        if user_id not in self.short_term:
            self.short_term[user_id] = []
        self.short_term[user_id].append({
            "role": role,
            "content": content
        })
        
        # Update user message count
        self.increment_message_count(user_id)
    
    def get_conversation(
        self,
        user_id: str,
        limit: int = 50
    ) -> List[Dict[str, str]]:
        """Get recent conversation history for a user."""
        messages = (
            self.session.query(ConversationMessage)
            .filter_by(user_id=user_id)
            .order_by(ConversationMessage.timestamp.desc())
            .limit(limit)
            .all()
        )
        
        # Return in chronological order (oldest first)
        return [
            {"role": m.role, "content": m.content}
            for m in reversed(messages)
        ]
    
    def get_user_info(self, user_id: str) -> Optional[Dict]:
        """Get user information and preferences."""
        user = (
            self.session.query(UserPreference)
            .filter_by(user_id=user_id)
            .first()
        )
        
        if not user:
            return None
        
        return {
            "name": user.name,
            "language": user.language,
            "relationship_stage": user.relationship_stage,
            "message_count": user.message_count,
            "first_seen": user.first_seen.isoformat() if user.first_seen else None,
            "last_seen": user.last_seen.isoformat() if user.last_seen else None,
            "personality_prefs": json.loads(user.personality_prefs or "{}")
        }
    
    def create_user(
        self,
        user_id: str,
        name: Optional[str] = None,
        language: str = "hinglish"
    ) -> None:
        """Create a new user profile."""
        user = UserPreference(
            user_id=user_id,
            name=name,
            language=language,
            relationship_stage="stranger",
            message_count=0
        )
        self.session.add(user)
        self.session.commit()
    
    def update_user_name(self, user_id: str, name: str) -> None:
        """Update user's name."""
        user = self.get_or_create_user(user_id)
        user.name = name
        self.session.commit()
    
    def update_user_language(self, user_id: str, language: str) -> None:
        """Update user's preferred language."""
        user = self.get_or_create_user(user_id)
        user.language = language
        self.session.commit()
    
    def update_relationship_stage(self, user_id: str, stage: str) -> None:
        """Update user's relationship stage."""
        valid_stages = ["stranger", "acquaintance", "friend", "close", "partner"]
        if stage not in valid_stages:
            raise ValueError(f"Invalid stage. Must be one of: {valid_stages}")
        
        user = self.get_or_create_user(user_id)
        user.relationship_stage = stage
        self.session.commit()
    
    def increment_message_count(self, user_id: str) -> None:
        """Increment user's message count and update last_seen."""
        user = self.get_or_create_user(user_id)
        user.message_count += 1
        user.last_seen = datetime.utcnow()
        self.session.commit()
        
        # Auto-progress relationship stage based on message count
        self._check_stage_progression(user)
    
    def _check_stage_progression(self, user) -> None:
        """Check and update relationship stage based on message count."""
        count = user.message_count
        current = user.relationship_stage
        
        # Progression thresholds
        new_stage = None
        if current == "stranger" and count >= 10:
            new_stage = "acquaintance"
        elif current == "acquaintance" and count >= 50:
            new_stage = "friend"
        elif current == "friend" and count >= 200:
            new_stage = "close"
        elif current == "close" and count >= 500:
            new_stage = "partner"
        
        if new_stage:
            user.relationship_stage = new_stage
            self.session.commit()
    
    def get_or_create_user(self, user_id: str) -> UserPreference:
        """Get existing user or create new one."""
        user = (
            self.session.query(UserPreference)
            .filter_by(user_id=user_id)
            .first()
        )
        
        if not user:
            user = UserPreference(user_id=user_id)
            self.session.add(user)
            self.session.commit()
        
        return user
    
    def save_personality_prefs(
        self,
        user_id: str,
        prefs: Dict
    ) -> None:
        """Save personality preferences as JSON."""
        user = self.get_or_create_user(user_id)
        user.personality_prefs = json.dumps(prefs)
        self.session.commit()
    
    def clear_conversation(self, user_id: str) -> None:
        """Clear conversation history for a user (keeps profile)."""
        (
            self.session.query(ConversationMessage)
            .filter_by(user_id=user_id)
            .delete()
        )
        self.session.commit()
        
        # Clear short-term cache
        if user_id in self.short_term:
            del self.short_term[user_id]
    
    def close(self) -> None:
        """Close database session."""
        self.session.close()
