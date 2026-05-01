# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x   | ✅ Currently supported |

## Reporting a Vulnerability

If you discover a security vulnerability within Alasmia, please:

1. **Do NOT** create a public GitHub issue
2. Send details to the maintainers via:
   - GitHub Security Advisories
   - Or contact through the project page

We will respond within 48 hours and work with you to understand and address the issue promptly.

## Security Best Practices

### For Users

1. **Protect your .env file** - Never commit it to version control
2. **API Keys** - Keep your model API keys secure
3. **Telegram Tokens** - Treat bot tokens like passwords
4. **Regular Updates** - Keep Alasmia updated to latest version

### For Developers

1. **Input Validation** - Always validate user input
2. **SQL Injection** - Use parameterized queries (SQLAlchemy)
3. **Command Injection** - Never use user input in shell commands
4. **Secrets** - Use environment variables, never hardcode

## Data Privacy

- All conversation data stored locally
- No data sent to external servers (except AI model provider)
- User can delete all data by removing `./data/` directory
- No analytics or tracking

## Content Safety

Default mode includes content filtering to prevent:
- Harmful content generation
- Personal information leaks
- Malicious links or code

Advanced mode (opt-in) relaxes these restrictions per user preference.

---

**Last Updated:** May 2025
