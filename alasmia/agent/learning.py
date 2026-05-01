"""
Alasmia Learning Engine

Handles feedback processing and self-improvement from interactions.
"""

from typing import Dict, Optional, List
from datetime import datetime


class LearningEngine:
    """
    Manages Alasmia's self-improvement from conversations.
    Uses feedback to adapt responses and preferences.
    """
    
    def __init__(self, memory):
        """Initialize with memory manager."""
        self.memory = memory
        self.feedback_history: List[Dict] = []
    
    def process_feedback(
        self,
        user_id: str,
        message: str,
        response: str,
        feedback: str
    ) -> None:
        """
        Process user feedback on a response.
        
        feedback can be: "good", "bad", "too_long", "too_short", "not_relevant"
        """
        feedback_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "user_id": user_id,
            "user_message": message,
            "assistant_response": response,
            "feedback": feedback
        }
        
        self.feedback_history.append(feedback_entry)
        self._adapt_response_style(user_id, feedback)
    
    def _adapt_response_style(
        self,
        user_id: str,
        feedback: str
    ) -> None:
        """Adjust response style based on feedback."""
        prefs = self.memory.get_preference(user_id, "response_style", {})
        
        if feedback == "too_long":
            prefs["preferred_length"] = "shorter"
        elif feedback == "too_short":
            prefs["preferred_length"] = "longer"
        elif feedback == "good":
            prefs["positive_count"] = prefs.get("positive_count", 0) + 1
        elif feedback == "bad":
            prefs["negative_count"] = prefs.get("negative_count", 0) + 1
        
        self.memory.save_preference(user_id, "response_style", prefs)
    
    def get_improvement_suggestions(self, user_id: str) -> List[str]:
        """Get suggestions for improving based on feedback history."""
        user_feedback = [f for f in self.feedback_history if f["user_id"] == user_id]
        
        if not user_feedback:
            return []
        
        suggestions = []
        too_long = sum(1 for f in user_feedback if f["feedback"] == "too_long")
        too_short = sum(1 for f in user_feedback if f["feedback"] == "too_short")
        
        if too_long > too_short:
            suggestions.append("Keep responses shorter")
        elif too_short > too_long:
            suggestions.append("Provide more detailed responses")
        
        return suggestions
    
    def learn_from_correction(
        self,
        user_id: str,
        original_response: str,
        corrected_response: str
    ) -> None:
        """Learn from explicit corrections by the user."""
        correction_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "user_id": user_id,
            "original": original_response,
            "corrected": corrected_response
        }
        # Store for future reference
        self.feedback_history.append(correction_entry)
