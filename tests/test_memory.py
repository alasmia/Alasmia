"""
Tests for Memory Manager
"""

import pytest
import os
import tempfile
from unittest.mock import patch, MagicMock

# Mock ollama before importing
with patch.dict('sys.modules', {'ollama': MagicMock()}):
    from alasmia.agent.memory import MemoryManager


@pytest.fixture
def temp_db():
    """Create temporary database for testing."""
    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    original = os.environ.get("MEMORY_DB_PATH")
    os.environ["MEMORY_DB_PATH"] = path
    yield path
    if original:
        os.environ["MEMORY_DB_PATH"] = original
    else:
        os.unlink(path)


@pytest.fixture
def memory(temp_db):
    """Create memory manager with temp database."""
    with patch.dict('sys.modules', {'ollama': MagicMock()}):
        return MemoryManager()


def test_create_user(memory):
    """Test user creation."""
    memory.create_user("test_user", name="Test", language="english")
    info = memory.get_user_info("test_user")
    
    assert info is not None
    assert info["name"] == "Test"
    assert info["language"] == "english"
    assert info["relationship_stage"] == "stranger"


def test_add_message(memory):
    """Test adding messages."""
    memory.create_user("test_user")
    memory.add_message("test_user", "user", "Hello")
    memory.add_message("test_user", "assistant", "Hi there!")
    
    history = memory.get_conversation("test_user")
    
    assert len(history) == 2
    assert history[0]["role"] == "user"
    assert history[1]["role"] == "assistant"


def test_relationship_stage_progression(memory):
    """Test automatic stage progression."""
    memory.create_user("test_user")
    
    # Simulate message count progression
    for i in range(15):
        memory.increment_message_count("test_user")
    
    info = memory.get_user_info("test_user")
    
    # Should progress from stranger (0) to acquaintance (10+)
    assert info["relationship_stage"] == "acquaintance"


def test_update_language(memory):
    """Test language update."""
    memory.create_user("test_user", language="hinglish")
    memory.update_user_language("test_user", "hindi")
    
    info = memory.get_user_info("test_user")
    assert info["language"] == "hindi"


def test_clear_conversation(memory):
    """Test clearing conversation history."""
    memory.create_user("test_user")
    memory.add_message("test_user", "user", "Hello")
    memory.add_message("test_user", "assistant", "Hi")
    
    memory.clear_conversation("test_user")
    history = memory.get_conversation("test_user")
    
    assert len(history) == 0


def test_get_or_create_user(memory):
    """Test get or create user."""
    # Create new user
    user = memory.get_or_create_user("new_user")
    assert user is not None
    assert user.user_id == "new_user"
    
    # Get existing user
    user2 = memory.get_or_create_user("new_user")
    assert user2.user_id == "new_user"


def test_personality_prefs(memory):
    """Test saving personality preferences."""
    memory.create_user("test_user")
    prefs = {"tone": "playful", "topic": "tech"}
    memory.save_personality_prefs("test_user", prefs)
    
    info = memory.get_user_info("test_user")
    assert info["personality_prefs"]["tone"] == "playful"
