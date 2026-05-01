"""
Alasmia Brain - LLM Response Generation

Handles interaction with AI models and response generation.
"""

from typing import List, Dict, Optional
from alasmia.models.model_loader import ModelLoader


class Brain:
    """The thinking core of Alasmia - generates responses using AI models."""
    
    def __init__(self, model_loader: ModelLoader):
        """Initialize the brain with a model loader."""
        self.model_loader = model_loader
        self.context_window = 4096  # Default context window
    
    def think(
        self,
        message: str,
        history: List[Dict[str, str]],
        system_prompt: str,
        context: Optional[Dict] = None
    ) -> str:
        """
        Generate a thoughtful response.
        
        Args:
            message: Current user message
            history: Conversation history [{"role": "user"/"assistant", "content": "..."}]
            system_prompt: Personality and behavior instructions
            context: Additional context (user preferences, etc.)
        
        Returns:
            Generated response string
        """
        # Build full prompt with system, history, and current message
        full_history = [{"role": "system", "content": system_prompt}]
        full_history.extend(history)
        full_history.append({"role": "user", "content": message})
        
        # Generate response
        response = self.model_loader.generate(
            messages=full_history,
            context=context or {}
        )
        
        return response
    
    def think_stream(
        self,
        message: str,
        history: List[Dict[str, str]],
        system_prompt: str,
        context: Optional[Dict] = None
    ):
        """
        Generate streaming response (for real-time output).
        
        Yields response chunks as they're generated.
        """
        full_history = [{"role": "system", "content": system_prompt}]
        full_history.extend(history)
        full_history.append({"role": "user", "content": message})
        
        for chunk in self.model_loader.generate_stream(
            messages=full_history,
            context=context or {}
        ):
            yield chunk
    
    def set_context_window(self, size: int):
        """Set the context window size for long conversations."""
        self.context_window = size
    
    def compress_context(self, history: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """
        Compress conversation history when it exceeds context window.
        
        Keeps recent messages and summarizes older ones.
        """
        if len(history) <= self.context_window:
            return history
        
        # Keep system prompt
        if history and history[0].get("role") == "system":
            system = [history[0]]
            history = history[1:]
        else:
            system = []
        
        # Keep recent messages (half of context window)
        keep_count = self.context_window // 2
        recent = history[-keep_count:]
        
        # Summarize old messages (placeholder - would use LLM to summarize)
        old_messages = history[:-keep_count]
        summary = "Previous conversation involved discussing various topics."
        
        return system + [{"role": "system", "content": f"[Summary: {summary}]"}] + recent
