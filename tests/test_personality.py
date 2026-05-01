"""
Tests for Personality Engine
"""

import pytest
from alasmia.agent.personality import PersonalityEngine
from alasmia.agent.memory import MemoryManager
import os
import tempfile


@pytest.fixture
def temp_db():
    """Create temporary database for testing."""
    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    os.environ["MEMORY_DB_PATH"] = path
    yield path
    os.unlink(path)


@pytest.fixture
def memory(temp_db):
    """Create memory manager with temp database."""
    return MemoryManager()


@pytest.fixture
def personality(memory):
    """Create personality engine."""
    return PersonalityEngine(memory)


def test_initial_stage_is_stranger(personality, memory):
    """Test that new users start as stranger."""
    memory.create_user("test_user")
    stage = personality.get_stage("test_user")
    assert stage == "stranger"


def test_stage_progression(personality, memory):
    """Test stage progression."""
    memory.create_user("test_user")
    
    # Progress through stages
    memory.update_relationship_stage("test_user", "acquaintance")
    assert personality.get_stage("test_user") == "acquaintance"
    
    memory.update_relationship_stage("test_user", "friend")
    assert personality.get_stage("test_user") == "friend"


def test_language_detection():
    """Test language detection."""
    from alasmia.agent.personality import PersonalityEngine
    
    # Create mock memory
    memory = type('MockMemory', (), {})()
    engine = PersonalityEngine(memory)
    
    # Test Hindi detection
    assert engine.detect_language("नमस्ते कैसे हो आप") == "hindi"
    
    # Test English detection
    assert engine.detect_language("Hello how are you") == "english"
    
    # Test Hinglish detection
    assert engine.detect_language("Kya haal hai? I'm fine.") == "hinglish"
