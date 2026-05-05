"""
Alasmia Personality Engine - Relationship stages + Alas/Mia integration
"""

from typing import Dict, Optional
from alasmia.agent.memory import MemoryManager
from alasmia.agent.alas_prompts import get_alas_system_prompt, MASCULINE_ENERGY
from alasmia.agent.mia_prompts import get_mia_system_prompt, FEMININE_ENERGY


class PersonalityEngine:
    """
    Handles Alasmia's personality and relationship dynamics.
    Manages both Alas (male) and Mia (female) companion types.
    """
    
    STAGES = ["stranger", "acquaintance", "friend", "close", "partner"]
    STAGE_THRESHOLDS = {"stranger": 0, "acquaintance": 10, "friend": 50, "close": 200, "partner": 500}
    
    def __init__(self, memory: MemoryManager):
        """Initialize with memory manager."""
        self.memory = memory
    
    def get_companion_type(self, user_id: str) -> str:
        """Get user's chosen companion type."""
        info = self.memory.get_user_info(user_id)
        if info:
            return info.get("companion_gender", "female")  # Default Mia
        return "female"
    
    def get_stage(self, user_id: str) -> str:
        """Get current relationship stage."""
        info = self.memory.get_user_info(user_id)
        if info:
            return info.get("relationship_stage", "stranger")
        return "stranger"
    
    def get_system_prompt(self, user_id: str) -> str:
        """Get appropriate system prompt based on companion and stage."""
        info = self.memory.get_user_info(user_id)
        companion = self.get_companion_type(user_id)
        stage = self.get_stage(user_id)
        user_name = info.get("name") if info else None
        
        if companion == "male":
            return get_alas_system_prompt(stage, user_name)
        else:
            return get_mia_system_prompt(stage, user_name)
    
    def get_greeting(self, user_id: str, time_of_day: str = "casual", is_returning: bool = False) -> str:
        """Get appropriate greeting based on companion type."""
        companion = self.get_companion_type(user_id)
        info = self.memory.get_user_info(user_id)
        name = info.get("name") if info else None
        
        if companion == "male":
            greetings = MASCULINE_ENERGY["greetings"]
            if is_returning:
                return greetings["returning"]
            return greetings.get(time_of_day, greetings["casual"])
        else:
            greetings = FEMININE_ENERGY["greetings"]
            if is_returning:
                return greetings["returning"]
            return greetings.get(time_of_day, greetings["casual"])
    
    def get_mood_response(self, user_id: str, mood: str) -> str:
        """Get companion's response to user's current mood."""
        companion = self.get_companion_type(user_id)
        
        if companion == "male":
            responses = MASCULINE_ENERGY["mood_responses"].get(mood, MASCULINE_ENERGY["mood_responses"]["happy"])
        else:
            responses = FEMININE_ENERGY["mood_responses"].get(mood, FEMININE_ENERGY["mood_responses"]["happy"])
        
        import random
        return random.choice(responses)
    
    def get_comfort_style(self, user_id: str) -> str:
        """Get comfort message in companion's style."""
        companion = self.get_companion_type(user_id)
        if companion == "male":
            return MASCULINE_ENERGY["comfort_style"]
        else:
            return FEMININE_ENERGY["comfort_style"]
    
    def get_celebration_style(self, user_id: str) -> str:
        """Get celebration message in companion's style."""
        companion = self.get_companion_type(user_id)
        if companion == "male":
            return MASCULINE_ENERGY["celebration_style"]
        else:
            return FEMININE_ENERGY["celebration_style"]
    
    def detect_language(self, message: str) -> str:
        """Detect language from message."""
        hindi_chars = set("अ आ इ उ ऋ ए ऐ ओ औ क ख ग घ ङ च छ ज झ ञ ट ठ ड ढ ण त थ द ध न प फ ब भ म य र ल व श ष स ह ं ः ँ ्")
        hindi_count = sum(1 for c in message if c in hindi_chars)
        
        if hindi_count > len(message) * 0.3:
            return "hindi"
        elif hindi_count > 0:
            return "hinglish"
        else:
            return "english"
    
    def should_progress_stage(self, user_id: str) -> bool:
        """Check if user should progress to next stage."""
        current_stage = self.get_stage(user_id)
        if current_stage == "partner":
            return False
        
        current_idx = self.STAGES.index(current_stage)
        next_stage = self.STAGES[current_idx + 1]
        threshold = self.STAGE_THRESHOLDS[next_stage]
        
        info = self.memory.get_user_info(user_id)
        message_count = info.get("message_count", 0) if info else 0
        
        return message_count >= threshold
    
    def progress_stage(self, user_id: str) -> str:
        """Progress user to next relationship stage."""
        current_stage = self.get_stage(user_id)
        if current_stage == "partner":
            return current_stage
        
        current_idx = self.STAGES.index(current_stage)
        next_stage = self.STAGES[current_idx + 1]
        self.memory.update_relationship_stage(user_id, next_stage)
        
        return next_stage
    
    def get_stage_transition_message(self, user_id: str, from_stage: str, to_stage: str) -> Optional[str]:
        """Get message when progressing stages."""
        companion = self.get_companion_type(user_id)
        
        if companion == "male":
            return f"We've been through a lot together. I consider you a true friend now. 💪"
        else:
            return f"Our bond has grown so much! You mean the world to me now. 💕"
