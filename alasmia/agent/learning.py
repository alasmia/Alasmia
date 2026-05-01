"""
Alasmia Learning Engine

Handles feedback processing and self-improvement from interactions.
"""

from typing import Dict, Optional, List
from datetime import datetime
import json


class LearningEngine:
    """Manages Alasmia's self-improvement from conversations."""
    
    def __init__(self, memory: MemoryManager):
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
        
        # Adjust behavior based on feedback
        self._adapt_response_style(user_id, feedback)
    
    def _adapt_response_style(
        self,
        user_id: str,
        feedback: str
    ) -> None:
        """Adjust response style based on feedback."""
        user_info = self.memory.get_user_info(user_id)
        prefs = user_info.get("personality_prefs", {}) if user_info else {}
        
        if feedback == "too_long":
            prefs["preferred_response_length"] = "shorter"
        elif feedback == "too_short":
            prefs["preferred_response_length"] = "longer"
        elif feedback == "good":
            # Track what worked
            prefs["positive_interactions"] = prefs.get("positive_interactions", 0) + 1
        elif feedback == "bad":
            prefs["negative_interactions"] = prefs.get("negative_interactions", 0) + 1
        
        self.memory.save_personality_prefs(user_id, prefs)
    
    def get_improvement_suggestions(self, user_id: str) -> List[str]:
        """Get suggestions for improving based on feedback history."""
        user_feedback = [f for f in self.feedback_history if f["user_id"] == user_id]
        
        if not user_feedback:
            return []
        
        suggestions = []
        
        # Analyze feedback patterns
        too_long = sum(1 for f in user_feedback if f["feedback"] == "too_long")
        too_short = sum(1 for f in user_feedback if f["feedback"] == "too_short")
        bad = sum(1 for f in user_feedback if f["feedback"] == "bad")
        
        if too_long > too_short:
            suggestions.append("Keep responses shorter")
        elif too_short > too_long:
            suggestions.append("Provide more detailed responses")
        
        if bad > len(user_feedback) * 0.3:
            suggestions.append("Focus more on empathy and understanding")
        
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
        # In a more advanced system, this could fine-tune the model
        self._store_correction(correction_entry)
    
    def _store_correction(self, correction: Dict) -> None:
        """Store correction for learning."""
        # Placeholder for correction storage
        # Could be used for RLHF or prompt adjustment
        pass
    
    def get_user_preferences(self, user_id: str) -> Dict:
        """Get learned user preferences."""
        info = self.memory.get_user_info(user_id)
        if info:
            return info.get("personality_prefs", {})
        return {}
