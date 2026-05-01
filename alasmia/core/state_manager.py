"""
Alasmia State Manager - Handles user session state and context
"""

import json
from typing import Dict, Optional, Any
from datetime import datetime


class StateManager:
    """
    Manages user session state, current context, and active modes.
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
