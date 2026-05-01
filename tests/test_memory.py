"""
Tests for Memory Manager
"""

import pytest
import os
import tempfile
from alasmia.agent.memory import MemoryManager


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
