"""
Alasmia Model Loader

Handles loading and switching between different AI model providers.
Works with Ollama (local), OpenAI, Anthropic, and ANY OpenAI-compatible API.
"""

import os
from typing import List, Dict, Optional, Iterator

from alasmia.models.providers import get_provider, BaseProvider, OllamaProvider, OpenAIProvider, AnthropicProvider

class ModelLoader:
    """
    Unified interface for multiple AI model providers.
    Supports: Ollama, OpenAI, Anthropic, and any OpenAI-compatible API.
    """

    # Keep for backwards compatibility
    PROVIDERS = {
        "ollama": OllamaProvider,
        "openai": OpenAIProvider,
        "anthropic": AnthropicProvider,
    }

    def __init__(self):
        """Initialize model loader with default provider."""
        self.current_provider: Optional[BaseProvider] = None
        self.current_model: Optional[str] = None
        self.current_provider_name: Optional[str] = None
        self._initialize_from_env()

    def _initialize_from_env(self) -> None:
        """Initialize provider and model from environment variables."""
        provider_name = os.getenv("MODEL_PROVIDER", "ollama").lower().strip()

        # Model name from env or defaults based on provider
        model_name = os.getenv("MODEL_NAME", "")
        if not model_name:
            model_name = self._get_default_model(provider_name)

        self.set_provider(provider_name, model_name)

    def _get_default_model(self, provider: str) -> str:
        """Get default model for a provider."""
        defaults = {
            # Direct providers
            "ollama": "llama3.2",
            "openai": "gpt-4",
            "anthropic": "claude-3-opus-20240229",
            
            # OpenAI-compatible providers
            "groq": "llama-3.2-90b-vision",
            "minimax": "Speech-02-HD",
            "xai": "grok-2",
            "together": "meta-llama/Llama-3-70b-chat-hf",
            "deepseek": "deepseek-chat",
            "mistral": "mistral-large-latest",
            "cohere": "command-r-plus",
            "azure": "gpt-4",
            "fireworks": "accounts/fireworks/models/llama-v3-70b-instruct",
            "perplexity": "sonar",
            "openrouter": "anthropic/claude-3-haiku",
            "cloudflare": "@cf/meta/llama-3-70b-instruct",
            
            # Local/GGUF
            "lmstudio": "llama3.2",
            "sglang": "llama3.2",
            "vllm": "llama3.2",
            
            # NVIDIA
            "nvidia": "nvidia/nvidia/nemotron-3-super-120b-a12b",
            "nvidia-nemotron": "nvidia/nvidia/nemotron-3-super-120b-a12b",
            "nvidia-kimi": "nvidia/moonshotai/kimi-k2.5",
            "nvidia-minimax": "nvidia/minimaxai/minimax-m2.5",
            "nvidia-glm5": "nvidia/z-ai/glm5",
            
            # Google
            "google": "gemini-1.5-pro",
            "gemini": "gemini-1.5-pro",
            "vertex": "gemini-1.5-pro",
            
            # AWS
            "bedrock": "anthropic.claude-3-sonnet-20240229-v1:0",
            
            # Chinese providers
            "zhipuai": "glm-4",
            "glm": "glm-4",
            "moonshot": "moonshot-v1-8k",
            "qianfan": "ernie-4.0-8k",
            "stepfun": "step-1v-8k",
            
            # Specialized
            "huggingface": "meta-llama/Llama-3-70b-chat-hf",
        }
        return defaults.get(provider, "gpt-4")

    def set_provider(self, provider: str, model: Optional[str] = None) -> None:
        """
        Set the AI provider and model.

        Supports 56+ providers:
        LOCAL: ollama, lmstudio, sglang, vllm, kllm, tensorzero
        OPENAI-COMPATIBLE: openai, deepseek, mistral, groq, together, fireworks,
                            deepinfra, cerebras, perplexity, openrouter, cloudflare
        ANTHROPIC: anthropic
        GOOGLE: google, gemini, vertex, ai-studio
        XAI: xai, grok
        AWS: bedrock
        AZURE: azure
        CHINESE: minimax, zhipuai, glm, moonshot, qianfan, stepfun, volcengine
        """
        try:
            # Use the flexible get_provider function
            self.current_provider = get_provider(provider)
            self.current_provider_name = provider

            # Set model if provided
            if model:
                self.current_provider.set_model(model)
                self.current_model = model
            else:
                # Get default for this provider
                self.current_model = self._get_default_model(provider)
                self.current_provider.set_model(self.current_model)

            print(f"✓ Model: {self.current_provider_name} ({self.current_model})")
        except Exception as e:
            print(f"✗ Failed to initialize {provider}: {e}")
            # Fall back to Ollama
            self.current_provider = get_provider("ollama")
            self.current_provider_name = "ollama"
            self.current_model = "llama3.2"

    def set_model(self, model: str) -> None:
        """
        Set model within current provider.
        Can use format "provider:model" to switch provider and model.
        """
        if ":" in model and any(p in model for p in ["ollama:", "openai:", "anthropic:"]):
            provider_name, model_name = model.split(":", 1)
            self.set_provider(provider_name, model_name)
        else:
            self.current_model = model
            if self.current_provider:
                self.current_provider.set_model(model)

    def generate(
        self,
        messages: List[Dict[str, str]],
        context: Optional[Dict] = None
    ) -> str:
        """Generate a response."""
        if not self.current_provider:
            return "Error: No model provider initialized"

        return self.current_provider.generate(messages, context or {})

    def generate_stream(
        self,
        messages: List[Dict[str, str]],
        context: Optional[Dict] = None
    ) -> Iterator[str]:
        """Generate a streaming response."""
        if not self.current_provider:
            yield "Error: No model provider initialized"
            return

        yield from self.current_provider.generate_stream(messages, context or {})

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

    @property
    def provider_name(self) -> str:
        """Get current provider name."""
        return self.current_provider_name or "unknown"