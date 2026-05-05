# 🤝 Contributing Guide

Thank you for your interest in contributing to Alasmia!

## Ways to Contribute

- 🐛 **Bug Reports** - Report issues on [GitHub](../issues)
- 💡 **Feature Requests** - Suggest new features
- 📝 **Documentation** - Improve docs
- 💻 **Code** - Submit PRs
- 🎨 **Design** - UI/UX improvements
- 📢 **Promotion** - Star, share, blog about Alasmia

## Development Setup

### Prerequisites
- Python 3.10+
- Git
- pip or conda

### Setup

```bash
# 1. Fork the repository on GitHub

# 2. Clone your fork
git clone https://github.com/YOUR_USERNAME/Alasmia.git
cd Alasmia

# 3. Add upstream remote
git remote add upstream https://github.com/alasmia/Alasmia.git

# 4. Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/macOS
# or: venv\Scripts\activate  # Windows

# 5. Install dependencies
pip install -r requirements.txt
pip install -e .  # Editable mode

# 6. Install dev dependencies
pip install pytest pytest-asyncio black flake8 mypy

# 7. Create branch for your feature
git checkout -b feature/amazing-feature
```

## Coding Standards

### Python Style
- Follow PEP 8
- Use type hints where possible
- Write docstrings for public functions

### Code Format
```bash
# Format code
black alasmia/ tests/

# Lint
flake8 alasmia/ tests/

# Type check
mypy alasmia/
```

### Commit Messages
Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: add WhatsApp integration
fix: memory persistence issue
docs: update README
refactor: simplify emotion tracking
test: add memory system tests
```

## Pull Request Process

### Before Submitting

1. **Run tests**: `pytest tests/`
2. **Format code**: `black alasmia/`
3. **Lint code**: `flake8 alasmia/`
4. **Update docs** if needed
5. **Add tests** for new features

### PR Template

Fill out the [PR template](../.github/PULL_REQUEST_TEMPLATE.md):

```markdown
## Summary
Brief description of changes

## Motivation
Why is this needed?

## Testing
How was this tested?

## Checklist
- [ ] Code follows style guidelines
- [ ] Tests added/updated
- [ ] Documentation updated
```

### Review Process

1. Maintainer reviews PR
2. Address feedback
3. Once approved, maintainer merges

## Reporting Bugs

Use [issue templates](../.github/ISSUE_TEMPLATE/bug_report.yml):

1. **Summary** - Clear bug description
2. **Steps to Reproduce** - Numbered steps
3. **Expected vs Actual** - What should happen vs what happened
4. **Environment** - OS, Python version, etc.
5. **Logs** - Relevant error logs

## License

By contributing, you agree your contributions will be licensed under the MIT License.

## Questions?

- 📬 Open an issue
- 💬 Join discussions
- 📖 Read [docs](../README.md)

---

**Thank you for making Alasmia better!** 💜