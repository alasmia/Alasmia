"""
Tests for Personality Engine
"""

import pytest
from unittest.mock import patch, MagicMock

with patch.dict('sys.modules', {'ollama': MagicMock()}):
    from alasmia.agent.memory import MemoryManager
    from alasmia.agent.personality import PersonalityEngine


@pytest.fixture
def mock_memory():
    """Create mock memory manager."""
    memory = MagicMock()
    memory.get_user_info.return_value = {
        "name": "Test",
        "language": "hinglish",
        "relationship_stage": "stranger",
        "message_count": 5
    }
    return memory


@pytest.fixture
def personality(mock_memory):
    """Create personality engine."""
    with patch.dict('sys.modules', {'ollama': MagicMock()}):
        return PersonalityEngine(mock_memory)


def test_initial_stage_is_stranger(personality):
    """Test that new users start as stranger."""
    stage = personality.get_stage("test_user")
    assert stage == "stranger"


def test_get_system_prompt(personality, mock_memory):
    """Test system prompt generation."""
    prompt = personality.get_system_prompt("test_user")
    assert "STRANGER" in prompt
    assert mock_memory.get_user_info.called


def test_detect_language():
    """Test language detection."""
    with patch.dict('sys.modules', {'ollama': MagicMock()}):
        from alasmia.agent.personality import PersonalityEngine
        
        memory = MagicMock()
        engine = PersonalityEngine(memory)
        
        # Test Hindi detection
        assert engine.detect_language("नमस्ते कैसे हो आप") == "hindi"
        
        # Test English detection
        assert engine.detect_language("Hello how are you") == "english"
        
        # Test Hinglish detection
        assert engine.detect_language("Kya haal hai? I'm fine.") == "hinglish"


def test_should_ask_language():
    """Test language preference check."""
    with patch.dict('sys.modules', {'ollama': MagicMock()}):
        from alasmia.agent.personality import PersonalityEngine
        
        memory = MagicMock()
        engine = PersonalityEngine(memory)
        
        # New user - should ask
        memory.get_user_info.return_value = None
        assert engine.should_ask_language("new_user") == True
        
        # Existing user without language - should ask
        memory.get_user_info.return_value = {"language": None}
        assert engine.should_ask_language("existing_user") == True
        
        # Existing user with language - no need
        memory.get_user_info.return_value = {"language": "hindi"}
        assert engine.should_ask_language("known_user") == False
