# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | ✅ Latest stable |

## Reporting a Vulnerability

If you discover a security vulnerability within Alasmia, please report it responsibly:

1. **Do NOT** create a public GitHub issue
2. Email directly: [security@alasmia.dev](mailto:security@alasmia.dev)
3. Include details about the vulnerability
4. Allow time for a fix before public disclosure

We aim to respond within 48 hours and provide a fix as quickly as possible.

## Security Best Practices

### Environment Variables

NEVER commit `.env` files or any file containing:
- API keys
- Bot tokens
- Database passwords
- Session secrets
- Personal information

The `.gitignore` excludes `.env` by default. Keep it that way.

### Bot Tokens

Telegram, Discord, and other bot tokens are sensitive. Store them:
- In `.env` file (not committed)
- In environment variables on production servers
- Never in code or configuration files

### Production Deployment

When deploying Alasmia:

```bash
# Use environment variables
export TELEGRAM_BOT_TOKEN="your-token"
export OPENAI_API_KEY="your-key"

# Or use a secrets manager
python main.py --platform telegram
```

### Rate Limiting

Configure rate limits in `.env`:
```
RATE_LIMIT=60  # requests per minute, 0 = unlimited
```

### Data Privacy

Alasmia stores:
- Conversation history (local SQLite)
- User preferences and interests
- Emotional patterns and moods

All data stays on YOUR machine. We do not collect or transmit personal data externally.

## Known Security Considerations

### CLI Mode

The CLI interface runs locally. No network exposure by default.

### Telegram/Discord Bots

When exposing a bot via webhooks:
- Use HTTPS endpoints only
- Validate webhook signatures
- Implement rate limiting
- Monitor for abuse

### Memory Database

The SQLite database contains personal information:
- Protect file permissions: `chmod 600 memory.db`
- Backup regularly
- Don't share the database file

## Security Updates

Security updates are released as patch versions. Always use the latest stable release.