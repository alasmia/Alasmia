# 🧪 Testing Guide

How to test Alasmia.

## Test Structure

```
tests/
├── __init__.py
├── test_memory.py       # Memory system tests
├── test_personality.py  # Personality tests
├── test_providers.py    # Model provider tests
├── test_emotions.py     # Emotion tracking tests
└── test_scheduler.py    # Scheduling tests
```

## Running Tests

### All Tests
```bash
pytest tests/
```

### Specific Test File
```bash
pytest tests/test_memory.py
```

### Specific Test
```bash
pytest tests/test_memory.py::test_memory_persist
```

### With Coverage
```bash
pytest --cov=alasmia --cov-report=html tests/
```

## Writing Tests

### Basic Test
```python
# tests/test_example.py
import pytest
from alasmia.agent.memory import Memory

def test_memory_basic():
    """Test basic memory operations."""
    m = Memory()
    m.add("Hello")
    assert m.get() == ["Hello"]
```

### Async Test
```python
# tests/test_async.py
import pytest
import asyncio
from alasmia.agent.brain import Brain

@pytest.mark.asyncio
async def test_brain_response():
    """Test brain generates response."""
    brain = Brain()
    response = await brain.think("Hello")
    assert len(response) > 0
```

### Parametrized Test
```python
# tests/test_models.py
import pytest

@pytest.mark.parametrize("model", [
    "minimaxai/minimax-m2.7",
    "openai/gpt-4",
    "anthropic/claude-3"
])
def test_model_loader(model):
    """Test loading various models."""
    from alasmia.models.model_loader import ModelLoader
    loader = ModelLoader()
    assert loader.load(model) is not None
```

## Test Fixtures

```python
# conftest.py
import pytest
from alasmia.agent.memory import Memory

@pytest.fixture
def memory():
    """Fresh memory instance for each test."""
    return Memory()

@pytest.fixture
def sample_user():
    """Sample user data."""
    return {
        "name": "Test User",
        "timezone": "Asia/Kolkata"
    }
```

## Mocking

```python
from unittest.mock import Mock, patch

def test_with_mock():
    """Test with mocked external service."""
    with patch('alasmia.models.providers.requests.get') as mock:
        mock.return_value = Mock(json=lambda: {"result": "ok"})
        # Test code that calls external API
```

## CI/CD

Tests run automatically on:
- Every PR
- Push to main branch
- Scheduled daily run

Check [CI workflow](../.github/workflows/ci.yml).

## Coverage Requirements

| Component | Minimum Coverage |
|-----------|-----------------|
| agent/ | 80% |
| core/ | 70% |
| integrations/ | 60% |

## Test Database

For tests needing database:

```python
import tempfile
import os

def test_with_temp_db():
    """Test with temporary database."""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = os.path.join(tmpdir, "test.db")
        # Test code using temporary database
```

## Debugging Failed Tests

```bash
# Run with verbose output
pytest -v tests/

# Stop on first failure
pytest -x tests/

# Show local variables on failure
pytest -l tests/

# Drop into debugger on failure
pytest --pdb tests/
```

## Performance Tests

```python
import time

def test_response_time():
    """Test response time is acceptable."""
    start = time.time()
    # Run operation
    duration = time.time() - start
    assert duration < 1.0, f"Took {duration}s, expected < 1s"
```