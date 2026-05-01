"""
Tests for Model Providers
"""

import pytest
from unittest.mock import patch, MagicMock


def test_model_loader_initialization():
    """Test model loader initializes."""
    with patch.dict('sys.modules', {'ollama': MagicMock()}):
        from alasmia.models.model_loader import ModelLoader
        
        # Mock the environment
        with patch('os.getenv', return_value='ollama'):
            loader = ModelLoader()
            assert loader.current_provider is not None


def test_invalid_provider_raises():
    """Test invalid provider raises error."""
    with patch.dict('sys.modules', {'ollama': MagicMock()}):
        from alasmia.models.model_loader import ModelLoader
        
        with patch('os.getenv', return_value='ollama'):
            loader = ModelLoader()
            
            with pytest.raises(ValueError) as excinfo:
                loader.set_provider("invalid_provider")
            
            assert "Unknown provider" in str(excinfo.value)


def test_ollama_provider_initialization():
    """Test Ollama provider initializes."""
    with patch.dict('sys.modules', {'ollama': MagicMock()}):
        from alasmia.models.providers import OllamaProvider
        
        with patch('os.getenv', return_value='http://localhost:11434'):
            with patch('ollama.list') as mock_list:
                mock_list.return_value = {"models": []}
                provider = OllamaProvider("qwen2.5:14b")
                assert provider.model == "qwen2.5:14b"
