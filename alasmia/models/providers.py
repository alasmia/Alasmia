"""
Alasmia Model Providers

Implements support for different AI model providers.
"""

import os
from abc import ABC, abstractmethod
from typing import List, Dict, Optional, Iterator
import ollama
from dotenv import load_dotenv

load_dotenv()


class BaseProvider(ABC):
    """Abstract base class for AI model providers."""
    
    default_model: str = ""
    
    @abstractmethod
    def generate(
        self,
        messages: List[Dict[str, str]],
        context: Dict
    ) -> str:
        """Generate a response."""
        pass
    
    @abstractmethod
    def generate_stream(
        self,
        messages: List[Dict[str, str]],
        context: Dict
    ) -> Iterator[str]:
        """Generate a streaming response."""
        pass
    
    @abstractmethod
    def set_model(self, model: str) -> None:
        """Set the model to use."""
        pass


class OllamaProvider(BaseProvider):
    """Ollama local model provider."""
    
    default_model = "qwen2.5:14b"
    
    def __init__(self, model: Optional[str] = None):
        """Initialize Ollama provider."""
        self.model = model or self.default_model
        self.url = os.getenv("OLLAMA_URL", "http://localhost:11434")
        
        # Verify connection
        try:
            ollama.list()
            print(f"✓ Ollama connected ({self.url})")
        except Exception as e:
            print(f"⚠ Ollama not connected: {e}")
    
    def generate(
        self,
        messages: List[Dict[str, str]],
        context: Dict
    ) -> str:
        """Generate response using Ollama."""
        # Convert messages to Ollama format
        ollama_messages = self._convert_messages(messages)
        
        response = ollama.chat(
            model=self.model,
            messages=ollama_messages,
            options={
                "temperature": context.get("temperature", 0.8),
                "top_p": context.get("top_p", 0.9),
            }
        )
        
        return response["message"]["content"]
    
    def generate_stream(
        self,
        messages: List[Dict[str, str]],
        context: Dict
    ) -> Iterator[str]:
        """Generate streaming response using Ollama."""
        ollama_messages = self._convert_messages(messages)
        
        stream = ollama.chat(
            model=self.model,
            messages=ollama_messages,
            stream=True,
            options={
                "temperature": context.get("temperature", 0.8),
                "top_p": context.get("top_p", 0.9),
            }
        )
        
        for chunk in stream:
            if chunk["message"]["content"]:
                yield chunk["message"]["content"]
    
    def set_model(self, model: str) -> None:
        """Set Ollama model."""
        self.model = model
    
    def _convert_messages(
        self,
        messages: List[Dict[str, str]]
    ) -> List[Dict[str, str]]:
        """Convert messages to Ollama format."""
        converted = []
        for msg in messages:
            role = msg.get("role", "user")
            # Ollama uses "user" and "assistant" only for roles
            if role == "system":
                # System messages become assistant with system prompt
                converted.append({
                    "role": "assistant",
                    "content": f"[System]: {msg['content']}"
                })
            else:
                converted.append({"role": role, "content": msg["content"]})
        return converted


class OpenAIProvider(BaseProvider):
    """OpenAI API provider."""
    
    default_model = "gpt-4"
    
    def __init__(self, model: Optional[str] = None):
        """Initialize OpenAI provider."""
        self.model = model or self.default_model
        self.api_key = os.getenv("OPENAI_API_KEY", "")
        
        if not self.api_key:
            print("⚠ OpenAI API key not set")
    
    def generate(
        self,
        messages: List[Dict[str, str]],
        context: Dict
    ) -> str:
        """Generate response using OpenAI."""
        try:
            from openai import OpenAI
        except ImportError:
            return "OpenAI package not installed. Run: pip install openai"
        
        if not self.api_key:
            return "Error: OPENAI_API_KEY not set in environment"
        
        client = OpenAI(api_key=self.api_key)
        
        response = client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=context.get("temperature", 0.8),
            top_p=context.get("top_p", 0.9),
        )
        
        return response.choices[0].message.content
    
    def generate_stream(
        self,
        messages: List[Dict[str, str]],
        context: Dict
    ) -> Iterator[str]:
        """Generate streaming response using OpenAI."""
        try:
            from openai import OpenAI
        except ImportError:
            yield "OpenAI package not installed."
            return
        
        if not self.api_key:
            yield "Error: OPENAI_API_KEY not set"
            return
        
        client = OpenAI(api_key=self.api_key)
        
        stream = client.chat.completions.create(
            model=self.model,
            messages=messages,
            stream=True,
            temperature=context.get("temperature", 0.8),
            top_p=context.get("top_p", 0.9),
        )
        
        for chunk in stream:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content
    
    def set_model(self, model: str) -> None:
        """Set OpenAI model."""
        self.model = model


class AnthropicProvider(BaseProvider):
    """Anthropic Claude API provider."""
    
    default_model = "claude-3-opus-20240229"
    
    def __init__(self, model: Optional[str] = None):
        """Initialize Anthropic provider."""
        self.model = model or self.default_model
        self.api_key = os.getenv("ANTHROPIC_API_KEY", "")
        
        if not self.api_key:
            print("⚠ Anthropic API key not set")
    
    def generate(
        self,
        messages: List[Dict[str, str]],
        context: Dict
    ) -> str:
        """Generate response using Anthropic."""
        try:
            from anthropic import Anthropic
        except ImportError:
            return "Anthropic package not installed. Run: pip install anthropic"
        
        if not self.api_key:
            return "Error: ANTHROPIC_API_KEY not set in environment"
        
        client = Anthropic(api_key=self.api_key)
        
        # Extract system message if present
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
            temperature=context.get("temperature", 0.8),
        )
        
        return response.content[0].text
    
    def generate_stream(
        self,
        messages: List[Dict[str, str]],
        context: Dict
    ) -> Iterator[str]:
        """Generate streaming response using Anthropic."""
        try:
            from anthropic import Anthropic
        except ImportError:
            yield "Anthropic package not installed."
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
            temperature=context.get("temperature", 0.8),
        ) as stream:
            for text in stream.text_stream:
                yield text
    
    def set_model(self, model: str) -> None:
        """Set Anthropic model."""
        self.model = model
