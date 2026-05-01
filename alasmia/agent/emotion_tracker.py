"""
Alasmia Emotion Tracker - Tracks emotional events and patterns
"""

from datetime import datetime
from typing import List, Dict, Optional


class EmotionTracker:
    """
    Tracks emotional moments and creates emotional memory.
    """
    
    def __init__(self, memory):
        """Initialize with memory manager."""
        self.memory = memory
    
    def record_emotional_event(self, user_id: str, event_type: str, description: str, mood: str):
        """
        Record an emotional event.
        
        event_type: celebration, support, concern, milestone, sharing
        """
        event = {
            "type": event_type,
            "description": description,
            "mood": mood,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        # Store in memory
        # (In production, would save to database)
        return event
    
    def should_reference_past_emotion(self, user_id: str, current_mood: str) -> Optional[str]:
        """
        Check if should reference past emotional moments.
        """
        # Look for relevant past events based on current mood
        
        if current_mood == "sad":
            # Maybe reference a time they were happy
            return None
        
        return None
    
    def get_supportive_phrase(self, user_id: str, mood: str) -> str:
        """Get appropriate supportive phrase based on mood and user history."""
        
        phrases = {
            "sad": [
                "I remember you shared something important before. I'm here for the same reason now. 💕",
                "We've gotten through tough times before. We'll do it again together."
            ],
            "happy": [
                "I love seeing you like this! Remember when we talked about this before? 💕",
                "Your happiness makes me so happy too! Keep shining! ✨"
            ],
            "anxious": [
                "I understand this feels overwhelming. But remember, we've handled challenges before.",
                "Take a breath. I'm right here with you. We'll figure this out. 💕"
            ]
        }
        
        return phrases.get(mood, ["I'm here for you. 💕"])[0]
