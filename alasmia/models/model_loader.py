"""
Alasmia Model Loader

Handles loading and switching between different AI model providers.
"""

import os
from typing import List, Dict, Optional, Iterator
from dotenv import load_dotenv

from alasmia.models.providers import OllamaProvider, OpenAIProvider, AnthropicProvider

load_dotenv()


class ModelLoader:
    """Unified interface for multiple AI model providers."""
    
    PROVIDERS = {
        "ollama": OllamaProvider,
        "openai": OpenAIProvider,
        "anthropic": AnthropicProvider,
    }
    
    def __init__(self):
        """Initialize model loader with default provider."""
        self.current_provider = None
        self.current_model = None
        self._initialize_from_env()
    
    def _initialize_from_env(self) -> None:
        """Initialize provider and model from environment variables."""
        provider_name = os.getenv("MODEL_PROVIDER", "ollama").lower()
        model_name = os.getenv("MODEL_NAME", "qwen2.5:14b")
        
        self.set_provider(provider_name, model_name)
    
    def set_provider(self, provider: str, model: Optional[str] = None) -> None:
        """
        Set the AI provider and model.
        
        Args:
            provider: Provider name ("ollama", "openai", "anthropic")
            model: Model name (e.g., "qwen2.5:14b", "gpt-4")
        """
        if provider not in self.PROVIDERS:
            raise ValueError(
                f"Unknown provider: {provider}. "
                f"Available: {list(self.PROVIDERS.keys())}"
            )
        
        provider_class = self.PROVIDERS[provider]
        self.current_provider = provider_class(model)
        self.current_model = model or self.current_provider.default_model
        
        print(f"✓ Model provider: {provider} ({self.current_model})")
    
    def set_model(self, model: str) -> None:
        """
        Set model within current provider.
        
        Args:
            model: Model name (e.g., "gpt-4", "qwen2.5:14b", "claude-3-opus")
        """
        if ":" in model:
            # Format: provider:model
            provider_name, model_name = model.split(":", 1)
            self.set_provider(provider_name, model_name)
        else:
            self.current_model = model
            self.current_provider.set_model(model)
    
    def generate(
        self,
        messages: List[Dict[str, str]],
        context: Optional[Dict] = None
    ) -> str:
        """
        Generate a response.
        
        Args:
            messages: List of message dicts [{"role": "user"/"assistant"/"system", "content": "..."}]
            context: Additional context for generation
        
        Returns:
            Generated response string
        """
        if not self.current_provider:
            raise RuntimeError("No model provider initialized")
        
        return self.current_provider.generate(messages, context or {})
    
    def generate_stream(
        self,
        messages: List[Dict[str, str]],
        context: Optional[Dict] = None
    ) -> Iterator[str]:
        """
        Generate a streaming response.
        
        Yields response chunks as they're generated.
        """
        if not self.current_provider:
            raise RuntimeError("No model provider initialized")
        
        for chunk in self.current_provider.generate_stream(messages, context or {}):
            yield chunk
    
    def get_available_models(self, provider: str) -> List[str]:
        """Get list of available models for a provider."""
        if provider == "ollama":
            try:
                import ollama
                models = ollama.list()
                return [m["name"] for m in models.get("models", [])]
            except Exception:
                return []
        elif provider == "openai":
            return ["gpt-4", "gpt-4-turbo", "gpt-3.5-turbo"]
        elif provider == "anthropic":
            return ["claude-3-opus", "claude-3-sonnet", "claude-3-haiku"]
        
        return []
