"""
Alasmia Model Providers

Flexible support for any LLM provider - local or cloud.
"""

import os
import warnings
from abc import ABC, abstractmethod
from typing import List, Dict, Optional, Iterator, Any
from dotenv import load_dotenv

load_dotenv()


class BaseProvider(ABC):
    """Abstract base class for AI model providers."""

    @abstractmethod
    def generate(self, messages: List[Dict[str, str]], context: Dict) -> str:
        """Generate a response."""
        pass

    @abstractmethod
    def generate_stream(self, messages: List[Dict[str, str]], context: Dict) -> Iterator[str]:
        """Generate a streaming response."""
        pass

    @abstractmethod
    def set_model(self, model: str) -> None:
        """Set the model to use."""
        pass


class OpenAIProvider(BaseProvider):
    """
    OpenAI-compatible provider.
    Works with: OpenAI, MiniMax, Groq, xAI, Together AI, DeepSeek, Mistral, Fireworks, Perplexity, and ANY OpenAI-compatible API.
    """

    def __init__(self, model: Optional[str] = None):
        self.model = model or os.getenv("OPENAI_MODEL", "gpt-4")
        self.api_key = os.getenv("OPENAI_API_KEY", "")
        self.base_url = os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")
        self._client = None

    def _get_client(self):
        if self._client is None:
            try:
                from openai import OpenAI
                self._client = OpenAI(
                    api_key=self.api_key,
                    base_url=self.base_url if self.base_url != "https://api.openai.com/v1" else None
                )
            except ImportError:
                raise ImportError("Run: pip install openai")
        return self._client

    def generate(self, messages: List[Dict[str, str]], context: Dict) -> str:
        client = self._get_client()
        if not self.api_key:
            return "Error: OPENAI_API_KEY not set"

        try:
            response = client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=context.get("temperature", 0.7),
                top_p=context.get("top_p", 0.9),
                max_tokens=context.get("max_tokens", 2048),
            )
            return response.choices[0].message.content or ""
        except Exception as e:
            return f"Error: {str(e)}"

    def generate_stream(self, messages: List[Dict[str, str]], context: Dict) -> Iterator[str]:
        client = self._get_client()
        if not self.api_key:
            yield "Error: OPENAI_API_KEY not set"
            return

        try:
            stream = client.chat.completions.create(
                model=self.model,
                messages=messages,
                stream=True,
                temperature=context.get("temperature", 0.7),
                top_p=context.get("top_p", 0.9),
            )
            for chunk in stream:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
        except Exception as e:
            yield f"Error: {str(e)}"

    def set_model(self, model: str) -> None:
        self.model = model


class GroqProvider(OpenAIProvider):
    """Groq API provider - OpenAI compatible."""
    def __init__(self, model: Optional[str] = None):
        os.environ.setdefault("OPENAI_API_BASE", "https://api.groq.com/openai/v1")
        os.environ.setdefault("OPENAI_API_KEY", os.getenv("GROQ_API_KEY", ""))
        super().__init__(model or "llama-3.2-90b-vision")
        self.base_url = "https://api.groq.com/openai/v1"


class MiniMaxProvider(OpenAIProvider):
    """MiniMax API provider - OpenAI compatible with custom endpoint."""
    def __init__(self, model: Optional[str] = None):
        os.environ.setdefault("OPENAI_API_BASE", "https://api.minimax.io/v1")
        os.environ.setdefault("OPENAI_API_KEY", os.getenv("MINIMAX_API_KEY", ""))
        super().__init__(model or "Speech-02-HD")
        self.base_url = "https://api.minimax.io/v1"


class xAIProvider(OpenAIProvider):
    """xAI (Grok) API provider - OpenAI compatible."""
    def __init__(self, model: Optional[str] = None):
        os.environ.setdefault("OPENAI_API_BASE", "https://api.x.ai/v1")
        os.environ.setdefault("OPENAI_API_KEY", os.getenv("XAI_API_KEY", ""))
        super().__init__(model or "grok-2")
        self.base_url = "https://api.x.ai/v1"


class TogetherProvider(OpenAIProvider):
    """Together AI provider - OpenAI compatible."""
    def __init__(self, model: Optional[str] = None):
        os.environ.setdefault("OPENAI_API_BASE", "https://api.together.xyz/v1")
        os.environ.setdefault("OPENAI_API_KEY", os.getenv("TOGETHER_API_KEY", ""))
        super().__init__(model or "meta-llama/Llama-3-70b-chat-hf")
        self.base_url = "https://api.together.xyz/v1"


class DeepSeekProvider(OpenAIProvider):
    """DeepSeek API provider - OpenAI compatible."""
    def __init__(self, model: Optional[str] = None):
        os.environ.setdefault("OPENAI_API_BASE", "https://api.deepseek.com/v1")
        os.environ.setdefault("OPENAI_API_KEY", os.getenv("DEEPSEEK_API_KEY", ""))
        super().__init__(model or "deepseek-chat")
        self.base_url = "https://api.deepseek.com/v1"


class MistralProvider(OpenAIProvider):
    """Mistral AI provider - OpenAI compatible."""
    def __init__(self, model: Optional[str] = None):
        os.environ.setdefault("OPENAI_API_BASE", "https://api.mistral.ai/v1")
        os.environ.setdefault("OPENAI_API_KEY", os.getenv("MISTRAL_API_KEY", ""))
        super().__init__(model or "mistral-large-latest")
        self.base_url = "https://api.mistral.ai/v1"


class CohereProvider(OpenAIProvider):
    """Cohere API provider - OpenAI compatible."""
    def __init__(self, model: Optional[str] = None):
        os.environ.setdefault("OPENAI_API_BASE", "https://api.cohere.ai/v1")
        os.environ.setdefault("OPENAI_API_KEY", os.getenv("COHERE_API_KEY", ""))
        super().__init__(model or "command-r-plus")
        self.base_url = "https://api.cohere.ai/v1"


class AzureProvider(OpenAIProvider):
    """Microsoft Azure OpenAI provider."""
    def __init__(self, model: Optional[str] = None):
        os.environ.setdefault("AZURE_OPENAI_API_KEY", os.getenv("AZURE_API_KEY", ""))
        os.environ.setdefault("AZURE_OPENAI_ENDPOINT", os.getenv("AZURE_ENDPOINT", ""))
        super().__init__(model or "gpt-4")
        # Azure uses different auth - will be handled by azureai library if needed


class VertexProvider(OpenAIProvider):
    """Google Cloud Vertex AI provider."""
    def __init__(self, model: Optional[str] = None):
        os.environ.setdefault("VERTEX_PROJECT", os.getenv("GCP_PROJECT", ""))
        os.environ.setdefault("VERTEX_LOCATION", os.getenv("GCP_LOCATION", "us-central1"))
        super().__init__(model or "gemini-1.5-pro")
        # Vertex uses google-auth, not standard OpenAI


class FireworksProvider(OpenAIProvider):
    """Fireworks AI provider - OpenAI compatible."""
    def __init__(self, model: Optional[str] = None):
        os.environ.setdefault("OPENAI_API_BASE", "https://api.fireworks.ai/v1")
        os.environ.setdefault("OPENAI_API_KEY", os.getenv("FIREWORKS_API_KEY", ""))
        super().__init__(model or "accounts/fireworks/models/llama-v3-70b-instruct")
        self.base_url = "https://api.fireworks.ai/v1"


class PerplexityProvider(OpenAIProvider):
    """Perplexity AI provider - OpenAI compatible."""
    def __init__(self, model: Optional[str] = None):
        os.environ.setdefault("OPENAI_API_BASE", "https://api.perplexity.ai")
        os.environ.setdefault("OPENAI_API_KEY", os.getenv("PERPLEXITY_API_KEY", ""))
        super().__init__(model or "sonar")
        self.base_url = "https://api.perplexity.ai"


class OpenRouterProvider(OpenAIProvider):
    """OpenRouter provider - OpenAI compatible."""
    def __init__(self, model: Optional[str] = None):
        os.environ.setdefault("OPENAI_API_BASE", "https://openrouter.ai/api/v1")
        os.environ.setdefault("OPENAI_API_KEY", os.getenv("OPENROUTER_API_KEY", ""))
        super().__init__(model or "anthropic/claude-3-haiku")
        self.base_url = "https://openrouter.ai/api/v1"


class CloudflareProvider(OpenAIProvider):
    """Cloudflare Workers AI provider - OpenAI compatible."""
    def __init__(self, model: Optional[str] = None):
        os.environ.setdefault("OPENAI_API_BASE", "https://api.cloudflare.com/client/v4/ai")
        os.environ.setdefault("OPENAI_API_KEY", os.getenv("CF_API_TOKEN", ""))
        super().__init__(model or "@cf/meta/llama-3-70b-instruct")
        self.base_url = "https://api.cloudflare.com/client/v4/ai"


class NVIDIAProvider(OpenAIProvider):
    """NVIDIA API provider - OpenAI compatible, FREE models available!
    
    Free models include:
    - nvidia/nvidia/nemotron-3-super-120b-a12b (262K context)
    - nvidia/moonshotai/kimi-k2.5 (262K context)
    - nvidia/minimaxai/minimax-m2.5 (196K context)
    - nvidia/z-ai/glm5 (202K context)
    
    Get API key: https://build.nvidia.com/settings/api-keys
    """
    def __init__(self, model: Optional[str] = None):
        os.environ.setdefault("OPENAI_API_BASE", "https://integrate.api.nvidia.com/v1")
        os.environ.setdefault("OPENAI_API_KEY", os.getenv("NVIDIA_API_KEY", ""))
        super().__init__(model or "nvidia/nvidia/nemotron-3-super-120b-a12b")
        self.base_url = "https://integrate.api.nvidia.com/v1"


class OllamaProvider(BaseProvider):
    """Ollama local model provider."""

    def __init__(self, model: Optional[str] = None):
        import ollama
        self.ollama = ollama
        self.model = model or os.getenv("OLLAMA_MODEL", "llama3.2")
        self.url = os.getenv("OLLAMA_URL", "http://localhost:11434")
        self._connected = self._check_connection()

    def _check_connection(self) -> bool:
        try:
            self.ollama.list()
            return True
        except Exception:
            return False

    def generate(self, messages: List[Dict[str, str]], context: Dict) -> str:
        ollama_messages = self._convert_messages(messages)
        response = self.ollama.chat(
            model=self.model,
            messages=ollama_messages,
            options={
                "temperature": context.get("temperature", 0.7),
                "top_p": context.get("top_p", 0.9),
                "num_predict": context.get("max_tokens", 2048),
            }
        )
        return response["message"]["content"]

    def generate_stream(self, messages: List[Dict[str, str]], context: Dict) -> Iterator[str]:
        ollama_messages = self._convert_messages(messages)
        stream = self.ollama.chat(
            model=self.model,
            messages=ollama_messages,
            stream=True,
            options={
                "temperature": context.get("temperature", 0.7),
                "top_p": context.get("top_p", 0.9),
            }
        )
        for chunk in stream:
            if chunk["message"]["content"]:
                yield chunk["message"]["content"]

    def set_model(self, model: str) -> None:
        self.model = model

    def _convert_messages(self, messages: List[Dict[str, str]]) -> List[Dict[str, str]]:
        converted = []
        for msg in messages:
            role = msg.get("role", "user")
            if role == "system":
                converted.append({"role": "assistant", "content": f"[System]: {msg['content']}"})
            else:
                converted.append({"role": role, "content": msg["content"]})
        return converted


class AnthropicProvider(BaseProvider):
    """Anthropic Claude API provider."""

    def __init__(self, model: Optional[str] = None):
        self.model = model or os.getenv("ANTHROPIC_MODEL", "claude-3-opus-20240229")
        self.api_key = os.getenv("ANTHROPIC_API_KEY", "")

    def generate(self, messages: List[Dict[str, str]], context: Dict) -> str:
        try:
            from anthropic import Anthropic
        except ImportError:
            return "Error: Run 'pip install anthropic'"

        if not self.api_key:
            return "Error: ANTHROPIC_API_KEY not set"

        client = Anthropic(api_key=self.api_key)

        system = ""
        filtered_messages = []
        for msg in messages:
            if msg.get("role") == "system":
                system = msg["content"]
            else:
                filtered_messages.append(msg)

        response = client.messages.create(
            model=self.model,
            max_tokens=context.get("max_tokens", 1024),
            system=system,
            messages=filtered_messages,
            temperature=context.get("temperature", 0.7),
        )
        return response.content[0].text

    def generate_stream(self, messages: List[Dict[str, str]], context: Dict) -> Iterator[str]:
        try:
            from anthropic import Anthropic
        except ImportError:
            yield "Error: Run 'pip install anthropic'"
            return

        if not self.api_key:
            yield "Error: ANTHROPIC_API_KEY not set"
            return

        client = Anthropic(api_key=self.api_key)

        system = ""
        filtered_messages = []
        for msg in messages:
            if msg.get("role") == "system":
                system = msg["content"]
            else:
                filtered_messages.append(msg)

        with client.messages.stream(
            model=self.model,
            max_tokens=context.get("max_tokens", 1024),
            system=system,
            messages=filtered_messages,
            temperature=context.get("temperature", 0.7),
        ) as stream:
            for text in stream.text_stream:
                yield text

    def set_model(self, model: str) -> None:
        self.model = model


class AWSBedrockProvider(BaseProvider):
    """AWS Bedrock provider for Llama, Claude, etc."""
    
    def __init__(self, model: Optional[str] = None):
        self.model = model or os.getenv("BEDROCK_MODEL", "anthropic.claude-3-sonnet-20240229-v1:0")
        self._client = None
    
    def _get_client(self):
        if self._client is None:
            try:
                import boto3
                self._client = boto3.client("bedrock-runtime")
            except ImportError:
                raise ImportError("Run: pip install boto3")
        return self._client
    
    def generate(self, messages: List[Dict[str, str]], context: Dict) -> str:
        # Simplified - full implementation would handle Claude messages format
        return "AWS Bedrock provider - configure AWS credentials for full support"
    
    def generate_stream(self, messages: List[Dict[str, str]], context: Dict) -> Iterator[str]:
        yield "AWS Bedrock provider - configure AWS credentials for full support"
    
    def set_model(self, model: str) -> None:
        self.model = model


class HuggingFaceProvider(BaseProvider):
    """Hugging Face Inference API provider."""
    
    def __init__(self, model: Optional[str] = None):
        self.api_key = os.getenv("HUGGINGFACE_API_KEY", "")
        self.model = model or os.getenv("HUGGINGFACE_MODEL", "meta-llama/Llama-3-70b-chat-hf")
        self.url = f"https://api-inference.huggingface.co/models/{self.model}"
    
    def generate(self, messages: List[Dict[str, str]], context: Dict) -> str:
        if not self.api_key:
            return "Error: HUGGINGFACE_API_KEY not set"
        
        headers = {"Authorization": f"Bearer {self.api_key}"}
        payload = {
            "inputs": messages[-1]["content"] if messages else "",
            "parameters": {"max_new_tokens": context.get("max_tokens", 2048)}
        }
        
        try:
            import requests
            response = requests.post(self.url, json=payload, headers=headers, timeout=60)
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, list) and len(result) > 0:
                    return result[0].get("generated_text", "")
                return str(result)
            return f"Error: {response.status_code}"
        except Exception as e:
            return f"Error: {str(e)}"
    
    def generate_stream(self, messages: List[Dict[str, str]], context: Dict) -> Iterator[str]:
        yield from self.generate(messages, context)
    
    def set_model(self, model: str) -> None:
        self.model = model
        self.url = f"https://api-inference.huggingface.co/models/{model}"


class ReplicateProvider(BaseProvider):
    """Replicate provider for running open models."""
    
    def __init__(self, model: Optional[str] = None):
        self.api_key = os.getenv("REPLICATE_API_KEY", "")
        self.model = model or os.getenv("REPLICATE_MODEL", "meta/llama-3-70b-instruct")
    
    def generate(self, messages: List[Dict[str, str]], context: Dict) -> str:
        if not self.api_key:
            return "Error: REPLICATE_API_KEY not set"
        
        try:
            import replicate
            # Simplified - full implementation needs prediction API
            return f"Replicate provider configured for {self.model} - run predictions via replicate client"
        except ImportError:
            return "Error: Run 'pip install replicate'"
    
    def generate_stream(self, messages: List[Dict[str, str]], context: Dict) -> Iterator[str]:
        yield from self.generate(messages, context)
    
    def set_model(self, model: str) -> None:
        self.model = model


def get_provider(name: Optional[str] = None) -> BaseProvider:
    """
    Get provider instance by name or from environment.
    
    Supported providers:
    - openai: OpenAI GPT models
    - anthropic: Anthropic Claude
    - ollama: Local models
    - groq: Groq (free fast)
    - minimax: MiniMax
    - deepseek: DeepSeek
    - mistral: Mistral AI
    - nvidia: NVIDIA (free models)
    - And 50+ OpenAI-compatible providers
    """
    name = (name or os.getenv("MODEL_PROVIDER", "ollama")).lower().strip()

    # Direct providers with custom implementations
    if name == "ollama":
        return OllamaProvider()
    elif name == "anthropic":
        return AnthropicProvider()
    elif name == "openai":
        return OpenAIProvider()
    
    # OpenAI-compatible cloud providers
    elif name in ["groq", "groq"]:
        return GroqProvider()
    elif name in ["minimax", "minimax-tts"]:
        return MiniMaxProvider()
    elif name in ["xai", "grok"]:
        return xAIProvider()
    elif name in ["together", "togetherai"]:
        return TogetherProvider()
    elif name in ["deepseek"]:
        return DeepSeekProvider()
    elif name in ["mistral", "mistral-ai"]:
        return MistralProvider()
    elif name in ["cohere"]:
        return CohereProvider()
    elif name in ["azure"]:
        return AzureProvider()
    elif name in ["vertex", "google"]:
        return VertexProvider()
    elif name in ["fireworks", "fireworks-ai"]:
        return FireworksProvider()
    elif name in ["perplexity"]:
        return PerplexityProvider()
    elif name in ["openrouter"]:
        return OpenRouterProvider()
    elif name in ["cloudflare", "cf"]:
        return CloudflareProvider()
    elif name in ["nvidia", "nv"]:
        return NVIDIAProvider()
    elif name in ["bedrock", "aws"]:
        return AWSBedrockProvider()
    elif name in ["huggingface", "hf"]:
        return HuggingFaceProvider()
    elif name in ["replicate"]:
        return ReplicateProvider()
    
    # Default to OpenAI provider (generic OpenAI-compatible)
    return OpenAIProvider()