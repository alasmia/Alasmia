# Security Policy

If you believe you've found a security issue in Alasmia, please report it privately.

## Reporting a Security Issue

**Please do NOT open a public issue for security vulnerabilities.**

### How to Report

1. **Email:** security@alasmia.ai
2. **GitHub Security Advisories:** [Report here](https://github.com/alasmia/Alasmia/security/advisories/new)

Include in your report:
- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Any suggested fixes (optional)

### Response Timeline

- **Initial Response:** 24-48 hours
- **Assessment:** 3-5 days
- **Fix Timeline:** Varies by severity

## Security Model

### Trust Boundaries

Alasmia connects to real messaging platforms (Telegram, WhatsApp, etc.). Key trust boundaries:

1. **Platform APIs** — Third-party services with their own security
2. **Local Storage** — Data stored on user's machine
3. **AI Model** — External LLM provider

### Data Privacy

- **100% Local Storage** — All user data stays on the user's machine
- **No Cloud** — Works fully offline
- **No Telemetry** — Zero tracking or data collection
- **No Analytics** — No usage data sent anywhere

### What We Don't Track

- Message content
- User identity
- Conversation history
- Behavioral patterns
- Device information

## Platform-Specific Security

### Telegram Bot

- Uses official Bot API
- Stores tokens securely in environment variables
- User data isolated per user ID

### WhatsApp Integration

- Webhook-based (no persistent connection)
- Token-based authentication with Meta
- No message storage on external servers

### CLI

- All data stored locally in `./data` directory
- No network exposure by default
- User controls all data

## Best Practices for Users

1. **Protect Your Tokens**
   - Never commit `.env` files
   - Use environment variables
   - Rotate tokens periodically

2. **Verify Identities**
   - Confirm who you're talking to
   - Don't share sensitive information
   - Be cautious of impersonators

3. **Keep Software Updated**
   - Pull latest security patches
   - Use latest version of Alasmia

4. **Secure Your Storage**
   - Protect your `./data` directory
   - Use appropriate file permissions

## Security Updates

Critical security updates are released immediately.
Regular updates are released with each version.

Subscribe to:
- **GitHub Releases** — [Get notified](https://github.com/alasmia/Alasmia/releases)
- **Discord** — Security announcements channel

## Known Limitations

Alasmia is:
- NOT designed for HIPAA/medical data
- NOT designed for financial data
- NOT designed for legal documents
- NOT a replacement for professional services

Use appropriate tools for sensitive information.

## Security Researchers

Thank you for helping keep Alasmia secure!

For additional questions: security@alasmia.ai
