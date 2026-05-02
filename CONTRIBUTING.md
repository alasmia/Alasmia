# Contributing to Alasmia

Thank you for your interest in contributing to Alasmia! 🤍

## Quick Links

- **GitHub:** https://github.com/alasmia/Alasmia
- **Vision:** [`VISION.md`](VISION.md)
- **Discord:** https://discord.gg/alasmia
- **Issues:** https://github.com/alasmia/Alasmia/issues

## Project Overview

Alasmia is an AI life partner — a proactive, emotionally intelligent companion that:
- Initiates conversations (not just responds)
- Tracks user interests deeply
- Follows up on emotional states
- Speaks 15+ languages automatically
- Builds relationships over time across multiple platforms

## How to Contribute

### 1. Bug Reports & Small Fixes
Open a PR directly! For small fixes:
- Fix the bug
- Add tests if applicable
- Submit PR with clear description

### 2. New Features / Major Changes
For larger features:
1. **Open an Issue first** — Describe your idea
2. **Discuss in Discord** — Get feedback from maintainers
3. **Wait for approval** — Not all features may be accepted
4. **Then implement** — Follow the code guidelines

### 3. Documentation
- Improve existing docs
- Add examples
- Translate docs to other languages
- Fix typos and clarity issues

### 4. Testing
- Add unit tests for new features
- Improve test coverage
- Test on different platforms

## Development Setup

### Prerequisites
- Python 3.10+
- Git
- pip or poetry

### Local Development

```bash
# Clone the repo
git clone https://github.com/alasmia/Alasmia.git
cd Alasmia

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp .env.example .env

# Run tests
pytest tests/

# Run in development mode
python main.py
```

### Code Style

- Follow PEP 8
- Use type hints where possible
- Write docstrings for functions
- Keep functions focused and small

```python
def greet_user(name: str, language: str = "English") -> str:
    """Generate a greeting in the user's language.
    
    Args:
        name: User's name
        language: User's preferred language (default: English)
        
    Returns:
        Localized greeting string
    """
    greetings = {
        "English": f"Hello, {name}!",
        "Hindi": f"नमस्ते, {name}!",
    }
    return greetings.get(language, greetings["English"])
```

## Pull Request Process

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to your branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request
6. **Wait** for code review

### PR Requirements

- Clear, descriptive title
- Link related issues
- Describe what changed and why
- Add screenshots for UI changes
- Include test coverage

## Project Structure

```
alasmia/
├── agent/           # AI components (brain, memory, personality)
├── core/           # Core systems (scheduler, state, analytics)
├── integrations/   # Platform integrations (Telegram, WhatsApp, CLI)
├── models/         # Model abstraction layer
└── ...
```

When adding features:
- Keep related code together
- Add appropriate module documentation
- Update AGENTS.md if behavior changes

## Testing Guidelines

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest --cov=alasmia tests/

# Run specific test file
pytest tests/test_memory.py

# Run in watch mode
pytest-watch tests/
```

## Code of Conduct

- Be respectful and inclusive
- Accept constructive feedback
- Focus on what's best for the project
- Show empathy towards other contributors

## Questions?

- **Discord:** Ask in #help channel
- **GitHub Issues:** For bugs and feature requests
- **Email:** contact@alasmia.ai

## Contributors

See [README.md](README.md) for the maintainer list.

---

**Thank you for making Alasmia better!** 💜
