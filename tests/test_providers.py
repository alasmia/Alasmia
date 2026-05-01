"""
Tests for Model Providers
"""

import pytest
from alasmia.models.model_loader import ModelLoader


def test_model_loader_initialization():
    """Test model loader initializes."""
    loader = ModelLoader()
    assert loader.current_provider is not None


def test_ollama_provider_default():
    """Test Ollama provider has default model."""
    loader = ModelLoader()
    # Should initialize with default Ollama model
    assert "ollama" in str(type(loader.current_provider).__name__.lower())


def test_invalid_provider_raises():
    """Test invalid provider raises error."""
    loader = ModelLoader()
    
    with pytest.raises(ValueError) as excinfo:
        loader.set_provider("invalid_provider")
    
    assert "Unknown provider" in str(excinfo.value)
