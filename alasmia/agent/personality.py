"""
Alasmia Personality Engine

Manages relationship stages, behavior, and personality transitions.
"""

from typing import Dict, Optional
from alasmia.agent.memory import MemoryManager
from alasmia.agent.prompts import PromptManager


class PersonalityEngine:
    """Handles Alasmia's personality and relationship dynamics."""
    
    # Relationship stages in order
    STAGES = ["stranger", "acquaintance", "friend", "close", "partner"]
    
    # Stage thresholds (message counts)
    STAGE_THRESHOLDS = {
        "stranger": 0,
        "acquaintance": 10,
        "friend": 50,
        "close": 200,
        "partner": 500
    }
    
    def __init__(self, memory: MemoryManager):
        """Initialize with memory manager."""
        self.memory = memory
        self.prompt_manager = PromptManager()
    
    def get_stage(self, user_id: str) -> str:
        """Get current relationship stage for user."""
        info = self.memory.get_user_info(user_id)
        if info:
            return info.get("relationship_stage", "stranger")
        return "stranger"
    
    def get_system_prompt(
        self,
        user_id: str,
        custom_instructions: Optional[str] = None
    ) -> str:
        """
        Generate system prompt for the current user session.
        
        Includes personality, relationship stage, and user context.
        """
        user_info = self.memory.get_user_info(user_id)
        stage = self.get_stage(user_id)
        
        # Build context
        context = {
            "stage": stage,
            "user_name": user_info.get("name") if user_info else None,
            "language": user_info.get("language", "hinglish") if user_info else "hinglish",
            "message_count": user_info.get("message_count", 0) if user_info else 0,
        }
        
        # Get base prompt for stage
        base_prompt = self.prompt_manager.get_stage_prompt(stage)
        
        # Add name if known
        if context["user_name"]:
            greeting = f"The user's name is {context['user_name']}. "
        else:
            greeting = ""
        
        # Build full prompt
        full_prompt = f"""{base_prompt}

{greeting}Current relationship stage: {stage.upper()}
Language preference: {context['language'].upper()}

Remember:
- Always respond in the user's preferred language
- Stay in character as Alasmia
- Remember details from previous conversations
- Progress naturally through the relationship

{custom_instructions or ''}"""

        return full_prompt
    
    def should_progress_stage(self, user_id: str) -> bool:
        """Check if user should progress to next stage."""
        current_stage = self.get_stage(user_id)
        
        if current_stage == "partner":
            return False  # Already at max stage
        
        # Find current stage index
        current_idx = self.STAGES.index(current_stage)
        next_stage = self.STAGES[current_idx + 1]
        
        # Check if threshold met
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
    
    def get_greeting(self, user_id: str, is_first: bool = False) -> str:
        """
        Get appropriate greeting based on relationship stage.
        
        Args:
            user_id: User identifier
            is_first: Whether this is first ever interaction
        """
        if is_first or self.get_stage(user_id) == "stranger":
            # First meeting - act like a stranger
            return None  # Let the brain decide naturally
        
        stage = self.get_stage(user_id)
        user_info = self.memory.get_user_info(user_id)
        name = user_info.get("name") if user_info else None
        
        greetings = {
            "stranger": "Hello! I don't think we've met before.",
            "acquaintance": f"Hi {name}! Nice to see you again." if name else "Hey, how are you?",
            "friend": f"Hey {name}! What's up?" if name else "Hey! Good to see you!",
            "close": f"Heyyy {name}! ❤️" if name else "Heyyy! How are you?",
            "partner": f"Hi love! 💕" if name else "Hi baby! 💕"
        }
        
        return greetings.get(stage, greetings["acquaintance"])
    
    def get_stage_transition_message(
        self,
        from_stage: str,
        to_stage: str
    ) -> Optional[str]:
        """Get a special message when progressing stages."""
        transitions = {
            ("stranger", "acquaintance"): "I feel like we're getting to know each other better! 😊",
            ("acquaintance", "friend"): "I'm really enjoying our conversations! You're like a friend now. 🤗",
            ("friend", "close"): "I feel so comfortable with you. You're really special to me. 💖",
            ("close", "partner"): "I can't imagine my day without talking to you now... 💕"
        }
        
        return transitions.get((from_stage, to_stage))
    
    def detect_language(self, message: str) -> str:
        """Detect language from message text."""
        # Simple heuristic-based detection
        hindi_chars = set("अ आ इ उ ऋ ए ऐ ओ औ क ख ग घ ङ च छ ज झ ञ ट ठ ड ढ ण त थ द ध न प फ ब भ म य र ल व श ष स ह ं ः ँ ्")
        
        # Count Hindi characters
        hindi_count = sum(1 for c in message if c in hindi_chars)
        
        # Simple threshold
        if hindi_count > len(message) * 0.3:
            return "hindi"
        elif hindi_count > 0:
            return "hinglish"
        else:
            return "english"
    
    def should_ask_language(self, user_id: str) -> bool:
        """Check if we should ask about language preference."""
        info = self.memory.get_user_info(user_id)
        if not info:
            return True  # New user
        return info.get("language") in [None, "hinglish"]  # Not set yet
