# Contributing to Alasmia

Thank you for your interest in contributing to Alasmia! 🎉

## Code of Conduct

By participating in this project, you agree to maintain a respectful and inclusive environment for everyone.

## How to Contribute

### 1. Fork the Repository

Click the "Fork" button on the GitHub repository page to create your own copy.

### 2. Clone Your Fork

```bash
git clone https://github.com/YOUR_USERNAME/Alasmia.git
cd Alasmia
```

### 3. Create a Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

### 4. Set Up Development Environment

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt  # If available

# Copy environment
cp .env.example .env
```

### 5. Make Your Changes

- Write clean, readable code
- Follow the existing code style (PEP 8)
- Add comments for complex logic
- Include type hints where appropriate

### 6. Test Your Changes

```bash
# Run tests
pytest

# Run specific test
pytest tests/test_your_module.py

# Lint your code
ruff check .
```

### 7. Commit Your Changes

```bash
git add .
git commit -m "Add: your feature description"
```

### 8. Push and Create Pull Request

```bash
git push origin feature/your-feature-name
```

Then create a Pull Request on GitHub.

## Pull Request Guidelines

- **Clear title:** Summarize your changes
- **Description:** Explain what and why
- **Linked issues:** Reference any related issues
- **Screenshots:** For UI changes, include before/after

## Development Setup

### Prerequisites
- Python 3.10+
- Ollama (for local LLM)
- Git

### Recommended IDE Setup
- VS Code with Python extension
- PyCharm Professional

## Reporting Issues

When reporting issues, please include:
- Your operating system
- Python version
- Steps to reproduce
- Expected vs actual behavior
- Error messages/logs

## Questions?

Feel free to open an issue for any questions!

---

**Created by Doctor Kaif**
