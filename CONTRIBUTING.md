# Contributing to Alasmia

Thank you for your interest in contributing to Alasmia! 🎉

## 🤝 Code of Conduct

By participating in this project, you agree to maintain a respectful and inclusive environment for everyone.

## 🐛 Reporting Issues

- **Search first**: Check if the issue already exists
- **Use issue templates**: Fill out the provided issue templates
- **Be detailed**: Include steps to reproduce, expected vs actual behavior
- **Add logs**: If applicable, include relevant log output

## 🔧 Development Setup

```bash
# Clone the repository
git clone https://github.com/alasmia/Alasmia.git
cd Alasmia

# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp .env.example .env
# Edit .env with your configuration

# Run tests
pytest tests/

# Run the application
python main.py
```

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=alasmia tests/

# Run specific test file
pytest tests/test_memory.py -v
```

## 📝 Coding Standards

- Follow PEP 8 style guidelines
- Use type hints for function parameters and return values
- Write docstrings for all public functions and classes
- Keep functions focused and small (under 100 lines preferred)

## 🔄 Pull Request Process

1. **Fork** the repository
2. **Create a feature branch**: `git checkout -b feature/your-feature-name`
3. **Make your changes**: Follow coding standards, add tests
4. **Commit**: Use clear, descriptive commit messages
5. **Push**: `git push origin feature/your-feature-name`
6. **Open PR**: Fill out the PR template completely

### PR Template

```markdown
## Description
[Describe your changes]

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex code
- [ ] Documentation updated
- [ ] Tests added/updated
- [ ] All tests pass
```

## 📋 Code Review Criteria

PRs are reviewed based on:
- ✅ Code quality and readability
- ✅ Test coverage
- ✅ Documentation updates
- ✅ Following project conventions
- ✅ No breaking changes (or clearly documented)

## 🚀 Areas for Contribution

- 📱 Platform integrations (more messaging platforms)
- 🤖 AI provider support (more LLM providers)
- 📖 Documentation improvements
- 🧪 Test coverage expansion
- ⚡ Performance optimizations
- 🔒 Security enhancements

## 📞 Getting Help

- **GitHub Issues**: For bug reports and feature requests
- **Discussions**: For questions and community support

## 🎯 Style Guide

### Python Code
```python
# ✅ Good
def process_message(user_id: str, message: str) -> str:
    """Process a user message and return response."""
    return response

# ❌ Bad
def p(u,m):
    return r
```

### Commit Messages
```
✅ feat: add NVIDIA API support
✅ fix: resolve memory leak in情感 continuity
✅ docs: update README with new provider list

❌ fixed stuff
❌ WIP
❌ asdfgh
```

## 🙏 Thank You!

Every contribution, no matter how small, makes Alasmia better for everyone.

**Made with 💜 by Doctor Kaif**