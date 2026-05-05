"""
Alasmia State Manager - Handles user session state and context
"""

import json
from typing import Dict, Optional, Any
from datetime import datetime


class StateManager:
    """
    Manages user session state, current context, active modes,
    and user preferences including language.
    """
    
    def __init__(self, user_id: str = "default"):
        """Initialize state manager for a user."""
        self.user_id = user_id
        self.state = {
            "user_id": user_id,
            "current_mode": "normal",  # normal, comfort, celebration, quiet, deep, playful
            "conversation_depth": 0,  # 0-10 scale
            "last_mood": None,
            "last_topic": None,
            "active_reminders": [],
            "context_stack": [],  # Recent conversation context
            "pending_language_switch": None,
            "session_start": datetime.utcnow().isoformat(),
            # LANGUAGE SETTINGS
            "user_language": None,  # e.g., "English", "Mandarin Chinese", "Hindi", "Arabic"
            "language_confirmed": False,  # True once user confirms their language
            "first_interaction": True,  # For initial language setup
        }
    
    def set_mode(self, mode: str):
        """Set current interaction mode."""
        valid_modes = ["normal", "comfort", "celebration", "quiet", "deep", "playful"]
        if mode in valid_modes:
            self.state["current_mode"] = mode
    
    def get_mode(self) -> str:
        """Get current interaction mode."""
        return self.state.get("current_mode", "normal")
    
    def update_mood(self, mood: str):
        """Update detected mood."""
        self.state["last_mood"] = mood
        
        # Auto-trigger modes based on mood
        if mood in ["sad", "down", "upset", "angry"]:
            self.set_mode("comfort")
        elif mood in ["happy", "excited", "celebrating"]:
            self.set_mode("celebration")
    
    def set_language(self, language: str):
        """Set user's preferred language."""
        self.state["user_language"] = language
        self.state["language_confirmed"] = True
        self.state["first_interaction"] = False
    
    def get_language(self) -> Optional[str]:
        """Get user's preferred language."""
        return self.state.get("user_language")
    
    def is_language_confirmed(self) -> bool:
        """Check if user's language preference is confirmed."""
        return self.state.get("language_confirmed", False)
    
    def push_context(self, context: str):
        """Add to conversation context stack."""
        self.state["context_stack"].append({
            "context": context,
            "timestamp": datetime.utcnow().isoformat()
        })
        # Keep only last 10 contexts
        if len(self.state["context_stack"]) > 10:
            self.state["context_stack"].pop(0)
    
    def get_context_summary(self) -> str:
        """Get summary of recent context."""
        contexts = self.state.get("context_stack", [])
        if not contexts:
            return ""
        return f"Recent: {', '.join([c['context'] for c in contexts[-3:]])}"
    
    def add_reminder(self, reminder: Dict):
        """Add a reminder."""
        self.state["active_reminders"].append(reminder)
    
    def clear_reminders(self):
        """Clear all reminders."""
        self.state["active_reminders"] = []
    
    def get_state(self) -> Dict:
        """Get complete state."""
        return self.state.copy()
    
    def update(self, key: str, value: Any):
        """Update a specific state value."""
        self.state[key] = value
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a specific state value."""
        return self.state.get(key, default)
    
    def to_dict(self) -> Dict:
        """Export state as dictionary for memory storage."""
        return {
            "user_id": self.user_id,
            "user_language": self.state.get("user_language"),
            "language_confirmed": self.state.get("language_confirmed", False),
            "current_mode": self.state.get("current_mode", "normal"),
            "conversation_depth": self.state.get("conversation_depth", 0),
            "last_mood": self.state.get("last_mood"),
            "session_start": self.state.get("session_start"),
        }
    
    @classmethod
    def from_dict(cls, data: Dict, user_id: str = "default") -> "StateManager":
        """Create StateManager from stored data (e.g., from memory)."""
        manager = cls(user_id)
        manager.state["user_language"] = data.get("user_language")
        manager.state["language_confirmed"] = data.get("language_confirmed", False)
        manager.state["current_mode"] = data.get("current_mode", "normal")
        manager.state["conversation_depth"] = data.get("conversation_depth", 0)
        manager.state["last_mood"] = data.get("last_mood")
        manager.state["session_start"] = data.get("session_start")
        manager.state["first_interaction"] = False
        return manager
