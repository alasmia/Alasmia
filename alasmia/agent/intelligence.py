"""
Alasmia Context Awareness & Predictive Intelligence

This module implements:
- Context awareness across conversations
- Predictive suggestions based on patterns
- Advanced emotional intelligence
- Behavioral prediction
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from pathlib import Path
from collections import defaultdict
import re


class ContextTracker:
    """
    Tracks conversation context across multiple sessions.
    Understands what the user is working on, planning, or dealing with.
    """
    
    def __init__(self, data_dir: str = "./data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.context_file = self.data_dir / "context_tracking.json"
        self.context = self._load_context()
    
    def _load_context(self) -> Dict:
        if self.context_file.exists():
            with open(self.context_file, 'r') as f:
                return json.load(f)
        return {
            "active_projects": {},
            "recent_topics": [],
            "user_routines": {},
            "conversation_themes": [],
            "pending_actions": [],
        }
    
    def _save_context(self):
        with open(self.context_file, 'w') as f:
            json.dump(self.context, f, indent=2)
    
    def update_context(self, user_id: str, message: str, response: str):
        """Update context based on conversation."""
        if user_id not in self.context["active_projects"]:
            self.context["active_projects"][user_id] = {
                "topics": [],
                "last_updated": datetime.utcnow().isoformat(),
                "priority": "normal"
            }
        
        # Extract potential topics/projects from message
        topics = self._extract_topics(message)
        for topic in topics:
            if topic not in self.context["active_projects"][user_id]["topics"]:
                self.context["active_projects"][user_id]["topics"].append(topic)
        
        # Update timestamp
        self.context["active_projects"][user_id]["last_updated"] = datetime.utcnow().isoformat()
        
        # Track conversation theme
        theme = self._identify_theme(message)
        if theme:
            recent = self.context["conversation_themes"]
            if not recent or recent[-1] != theme:
                self.context["conversation_themes"].append(theme)
                # Keep only last 20 themes
                self.context["conversation_themes"] = self.context["conversation_themes"][-20:]
        
        self._save_context()
    
    def _extract_topics(self, text: str) -> List[str]:
        """Extract potential topics/projects from text."""
        topics = []
        
        # Look for work-related keywords
        work_patterns = [
            r"i(?:'m| am) (?:working on|building|creating|doing)\s+(.+?)(?:\.|$)",
            r"my\s+(project|work|task|job|assignment)\s+(?:is|on|about)\s+(.+?)(?:\.|$)",
            r"(?:started|began|launched)\s+(.+?)(?:\.|$)",
        ]
        
        for pattern in work_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            topics.extend(matches)
        
        return topics[:5]  # Limit to 5 topics
    
    def _identify_theme(self, text: str) -> Optional[str]:
        """Identify conversation theme."""
        text_lower = text.lower()
        
        themes = {
            "work": ["work", "job", "office", "boss", "meeting", "project", "deadline", "office"],
            "study": ["exam", "study", "college", "university", "school", "course", "learning", "tutorial"],
            "health": ["health", "doctor", "hospital", "medicine", "sick", "feeling", "pain", "fever"],
            "relationships": ["friend", "family", "girlfriend", "boyfriend", "relationship", "date", "love"],
            "technology": ["code", "programming", "ai", "app", "software", "computer", "developer"],
            "finance": ["money", "bank", "loan", "investment", "stock", "trading", "crypto", "salary"],
            "entertainment": ["movie", "music", "game", "netflix", "youtube", "song", "series"],
        }
        
        for theme, keywords in themes.items():
            if any(kw in text_lower for kw in keywords):
                return theme
        
        return None
    
    def get_active_context(self, user_id: str) -> Dict:
        """Get current active context for user."""
        if user_id in self.context["active_projects"]:
            proj = self.context["active_projects"][user_id]
            last_updated = datetime.fromisoformat(proj["last_updated"])
            # Reset if older than 7 days
            if (datetime.utcnow() - last_updated).days > 7:
                return {"topics": [], "priority": "normal"}
            return proj
        return {"topics": [], "priority": "normal"}
    
    def add_pending_action(self, user_id: str, action: str, due_date: str = None):
        """Add a pending action for follow-up."""
        if "pending_actions" not in self.context:
            self.context["pending_actions"] = []
        
        self.context["pending_actions"].append({
            "user_id": user_id,
            "action": action,
            "added": datetime.utcnow().isoformat(),
            "due_date": due_date,
            "completed": False
        })
        self._save_context()
    
    def get_pending_actions(self, user_id: str) -> List[Dict]:
        """Get pending actions for user."""
        return [
            a for a in self.context.get("pending_actions", [])
            if a["user_id"] == user_id and not a.get("completed", False)
        ]
    
    def complete_action(self, user_id: str, action_text: str):
        """Mark an action as completed."""
        for action in self.context.get("pending_actions", []):
            if action["user_id"] == user_id and action["action"] == action_text:
                action["completed"] = True
                action["completed_at"] = datetime.utcnow().isoformat()
        self._save_context()


class PredictiveEngine:
    """
    Predicts user needs and suggests proactive actions.
    Uses pattern analysis to anticipate what user might need.
    """
    
    def __init__(self, data_dir: str = "./data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.predictions_file = self.data_dir / "predictions.json"
        self.predictions = self._load_predictions()
        self.context_tracker = ContextTracker(data_dir)
    
    def _load_predictions(self) -> Dict:
        if self.predictions_file.exists():
            with open(self.predictions_file, 'r') as f:
                return json.load(f)
        return {
            "user_patterns": {},
            "time_based_predictions": {},
            "context_predictions": {},
        }
    
    def _save_predictions(self):
        with open(self.predictions_file, 'w') as f:
            json.dump(self.predictions, f, indent=2)
    
    def learn_pattern(self, user_id: str, message: str, time: datetime):
        """Learn user patterns from messages."""
        if user_id not in self.predictions["user_patterns"]:
            self.predictions["user_patterns"][user_id] = {
                "message_times": [],
                "message_days": [],
                "common_topics": [],
                "mood_correlations": {},
            }
        
        pattern = self.predictions["user_patterns"][user_id]
        
        # Record time patterns
        pattern["message_times"].append(time.strftime("%H:%M"))
        pattern["message_days"].append(time.strftime("%A"))
        
        # Keep only last 100 entries
        pattern["message_times"] = pattern["message_times"][-100:]
        pattern["message_days"] = pattern["message_days"][-100:]
        
        self._save_predictions()
    
    def predict_next_action(self, user_id: str) -> List[Dict]:
        """Predict what user might do next."""
        predictions = []
        user_context = self.context_tracker.get_active_context(user_id)
        
        # If user has active topics, suggest follow-ups
        if user_context.get("topics"):
            for topic in user_context["topics"][:3]:
                predictions.append({
                    "type": "follow_up",
                    "topic": topic,
                    "message": f"Do you want to continue with '{topic}'?",
                    "priority": "high" if len(user_context["topics"]) <= 2 else "medium"
                })
        
        # Check for pending actions
        pending = self.context_tracker.get_pending_actions(user_id)
        for action in pending[:3]:
            predictions.append({
                "type": "reminder",
                "action": action["action"],
                "message": f"Reminder: {action['action']}",
                "priority": "high"
            })
        
        # Time-based predictions
        now = datetime.utcnow()
        pattern = self.predictions["user_patterns"].get(user_id, {})
        
        # Check if user typically messages at this time
        current_hour = now.strftime("%H:%M")
        times = pattern.get("message_times", [])
        if times and times.count(current_hour) >= 2:
            predictions.append({
                "type": "habit",
                "message": "This is typically when you message me!",
                "priority": "low"
            })
        
        return predictions[:5]
    
    def get_smart_suggestion(self, user_id: str, mood: str = None) -> Optional[str]:
        """Generate a smart suggestion based on context."""
        predictions = self.predict_next_action(user_id)
        
        if not predictions:
            return None
        
        # Prioritize by mood
        if mood:
            if mood in ["sad", "down", "angry"]:
                # Check if there's a pending happy interaction
                for p in predictions:
                    if p.get("type") == "follow_up":
                        return f"I remember you were working on '{p['topic']}' - want to continue?"
        
        # Default: highest priority prediction
        high_priority = [p for p in predictions if p.get("priority") == "high"]
        if high_priority:
            return high_priority[0].get("message")
        
        return predictions[0].get("message")


class EmotionalIntelligence:
    """
    Advanced emotional intelligence with:
    - Emotion cause detection
    - Empathy mapping
    - Emotional trend analysis
    - Crisis detection
    """
    
    def __init__(self, data_dir: str = "./data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.emotions_file = self.data_dir / "emotional_intelligence.json"
        self.emotions = self._load_emotions()
    
    def _load_emotions(self) -> Dict:
        if self.emotions_file.exists():
            with open(self.emotions_file, 'r') as f:
                return json.load(f)
        return {
            "emotion_history": {},
            "emotion_causes": {},
            "empathy_responses": {},
        }
    
    def _save_emotions(self):
        with open(self.emotions_file, 'w') as f:
            json.dump(self.emotions, f, indent=2)
    
    def detect_emotion_cause(self, user_id: str, message: str, mood: str) -> Optional[str]:
        """Detect what might have caused the emotion."""
        message_lower = message.lower()
        causes = []
        
        # Relationship causes
        if any(w in message_lower for w in ["breakup", "fight", "argument", "miss", "lonely"]):
            causes.append("relationships")
        
        # Work/stress causes
        if any(w in message_lower for w in ["压力", "stress", "deadline", "busy", "overwhelmed"]):
            causes.append("work_stress")
        
        # Health causes
        if any(w in message_lower for w in ["tired", "sick", "headache", "pain", "exhausted"]):
            causes.append("health")
        
        # Success causes
        if any(w in message_lower for w in ["achieved", "succeeded", "happy", "excited", "proud"]):
            causes.append("achievement")
        
        return causes[0] if causes else None
    
    def get_empathy_response(self, mood: str, cause: str = None) -> str:
        """Get an empathetic response template."""
        empathy_map = {
            "sad": {
                "default": "I hear you, and I understand this feels difficult. 💙",
                "relationships": "Relationships can be so hard sometimes. I'm here to listen.",
                "work_stress": "Work stress is real. Remember to take care of yourself.",
                "health": "Taking care of your health is the most important thing.",
            },
            "angry": {
                "default": "I can sense you're frustrated. Take a deep breath, I'm here.",
                "relationships": "When it involves people we care about, anger is natural.",
                "work_stress": "Work frustrations are tough. Want to talk about it?",
            },
            "happy": {
                "default": "I love seeing you happy! Tell me more! ✨",
                "achievement": "That's amazing! Congratulations! I'm so proud of you! 🎉",
            },
            "anxious": {
                "default": "I understand anxiety can be overwhelming. Let's take it one step at a time.",
                "work_stress": "Deep breaths. We'll figure this out together.",
            },
        }
        
        mood_responses = empathy_map.get(mood, {})
        if cause and cause in mood_responses:
            return mood_responses[cause]
        return mood_responses.get("default", "I'm here for you.")
    
    def detect_crisis(self, user_id: str, messages: List[str], moods: List[str]) -> bool:
        """Detect if user might be in crisis."""
        if len(messages) < 3:
            return False
        
        # Check for concerning patterns
        concerning_keywords = [
            "suicide", "kill myself", "end it all", "don't want to live",
            "self harm", "hurt myself"
        ]
        
        recent_text = " ".join(messages[-3:]).lower()
        if any(kw in recent_text for kw in concerning_keywords):
            return True
        
        # Check for persistent sadness
        if len(moods) >= 3:
            if all(m in ["sad", "angry", "anxious"] for m in moods[-3:]):
                return True
        
        return False
    
    def record_emotion(self, user_id: str, mood: str, cause: str, intensity: int = 5):
        """Record emotion with cause for future reference."""
        if user_id not in self.emotions["emotion_history"]:
            self.emotions["emotion_history"][user_id] = []
        
        self.emotions["emotion_history"][user_id].append({
            "mood": mood,
            "cause": cause,
            "intensity": intensity,
            "timestamp": datetime.utcnow().isoformat()
        })
        
        # Keep last 50 emotions
        self.emotions["emotion_history"][user_id] = self.emotions["emotion_history"][user_id][-50:]
        self._save_emotions()
    
    def get_emotion_trend(self, user_id: str, days: int = 7) -> Dict:
        """Get emotional trend over specified days."""
        if user_id not in self.emotions["emotion_history"]:
            return {"dominant_mood": "neutral", "trend": "stable", "changes": []}
        
        cutoff = datetime.utcnow() - timedelta(days=days)
        recent = [
            e for e in self.emotions["emotion_history"][user_id]
            if datetime.fromisoformat(e["timestamp"]) > cutoff
        ]
        
        if not recent:
            return {"dominant_mood": "neutral", "trend": "stable", "changes": []}
        
        # Calculate dominant mood
        mood_counts = defaultdict(int)
        for e in recent:
            mood_counts[e["mood"]] += 1
        
        dominant = max(mood_counts, key=mood_counts.get)
        
        return {
            "dominant_mood": dominant,
            "mood_distribution": dict(mood_counts),
            "total_recorded": len(recent),
            "trend": "improving" if mood_counts.get("happy", 0) > len(recent) * 0.5 else "stable"
        }