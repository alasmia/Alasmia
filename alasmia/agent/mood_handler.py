"""
Alasmia Mood Handler - Detects user mood and triggers appropriate responses
"""

import re
from typing import Dict, Optional


class MoodHandler:
    """
    Detects user mood from messages and triggers appropriate companion responses.
    """
    
    MOOD_INDICATORS = {
        "happy": ["happy", "joy", "excited", "great", "wonderful", "amazing", "good", " 😊", " ❤️", " 😄", " 💕", " 🎉", "yay", "woo"],
        "excited": ["excited", "can't wait", "omg", "wow", "omg!", "wow!", "amazing!", "incredible", " 🙌", " 🚀"],
        "sad": ["sad", "upset", "down", "depressed", "unhappy", "crying", "tears", " 😢", " 😞", " 💔", "😿", "numb", "lost"],
        "angry": ["angry", "mad", "furious", "annoyed", "frustrated", " 😠", " 😤", " 😡", "hate", "stupid"],
        "tired": ["tired", "exhausted", "drained", "fatigued", "sleepy", " 😴", " 💤", " 😫", " 😩", "need rest"],
        "confused": ["confused", "puzzled", "don't understand", "unclear", " 🤔", "what?", "huh?"],
        "anxious": ["anxious", "worried", "nervous", "scared", "stress", " 😅", " 😰", " 😬"],
        "grateful": ["grateful", "thankful", "appreciate", "thanks", " 🙏", "blessed"],
        "proud": ["proud", "accomplished", "achieved", " 😊", " 🙌"]
    }
    
    def __init__(self):
        """Initialize mood handler."""
        self.current_mood = "neutral"
        self.mood_history = []
    
    def detect_mood(self, message: str) -> str:
        """
        Detect mood from user message.
        Returns: happy, excited, sad, angry, tired, confused, anxious, grateful, proud, neutral
        """
        message_lower = message.lower().strip()
        
        # Score each mood
        mood_scores = {}
        for mood, indicators in self.MOOD_INDICATORS.items():
            score = sum(1 for indicator in indicators if indicator.lower() in message_lower)
            if score > 0:
                mood_scores[mood] = score
        
        # Find best match
        if mood_scores:
            detected_mood = max(mood_scores, key=mood_scores.get)
            self.current_mood = detected_mood
            self.mood_history.append({"mood": detected_mood, "message": message_lower[:50]})
            
            # Keep last 20 moods
            if len(self.mood_history) > 20:
                self.mood_history.pop(0)
            
            return detected_mood
        
        return "neutral"
    
    def get_dominant_mood(self, last_n: int = 5) -> str:
        """Get dominant mood from recent messages."""
        recent = self.mood_history[-last_n:] if self.mood_history else []
        if not recent:
            return "neutral"
        
        mood_counts = {}
        for entry in recent:
            mood = entry["mood"]
            mood_counts[mood] = mood_counts.get(mood, 0) + 1
        
        return max(mood_counts, key=mood_counts.get) if mood_counts else "neutral"
    
    def get_special_mode(self, mood: str) -> Optional[str]:
        """
        Determine if mood warrants special mode.
        Returns: comfort, celebration, quiet, deep, playful, or None
        """
        special_moods = {
            "sad": "comfort",
            "angry": "comfort",
            "anxious": "comfort",
            "happy": "celebration",
            "excited": "celebration",
            "grateful": "celebration",
            "proud": "celebration",
            "tired": "quiet",
            "confused": "deep"
        }
        
        return special_moods.get(mood)
    
    def analyze_conversation_depth(self, message: str) -> int:
        """
        Analyze how deep/progressive a message is.
        Returns 0-10 scale.
        """
        depth = 5  # Start neutral
        
        # Shallow indicators (-1 to -2)
        shallow_words = ["hi", "hello", "hey", "okay", "ok", "yeah", "yes", "no", "thanks"]
        if any(word in message.lower() for word in shallow_words):
            depth -= 1
        
        # Deep indicators (+1 to +3)
        deep_words = [
            "feel", "feeling", "thoughts", "think", "believe", "dream",
            "future", "hope", "fear", "love", "care", "important",
            "understand", "meaning", "life", "relationship", "personal"
        ]
        depth_bonus = sum(1 for word in deep_words if word in message.lower())
        depth += min(3, depth_bonus)
        
        # Question depth
        if "why" in message.lower():
            depth += 1
        if "how" in message.lower():
            depth += 1
        
        return max(0, min(10, depth))
    
    def should_interject(self, mood: str) -> bool:
        """
        Determine if companion should proactively interject.
        For comfort or celebration modes.
        """
        return mood in ["sad", "angry", "anxious", "excited", "grateful", "proud"]
    
    def get_emotional_summary(self) -> Dict:
        """Get summary of emotional state."""
        return {
            "current_mood": self.current_mood,
            "dominant_mood": self.get_dominant_mood(),
            "history_length": len(self.mood_history),
            "needs_interject": self.should_interject(self.current_mood),
            "special_mode": self.get_special_mode(self.current_mood)
        }
