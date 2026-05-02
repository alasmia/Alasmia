# 📱 Telegram Bot Integration

Connect Alasmia to Telegram.

## Setup

### 1. Create a Telegram Bot

1. Open Telegram and chat with [@BotFather](https://t.me/BotFather)
2. Send `/newbot`
3. Follow prompts (name, username)
4. Copy the **bot token** you'll receive

### 2. Configure Alasmia

Add to your `.env`:

```bash
TELEGRAM_BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz
```

Or in `settings.yaml`:

```yaml
platforms:
  telegram:
    enabled: true
    bot_token: "123456789:ABCdefGHIjklMNOpqrsTUVwxyz"
```

### 3. Start Alasmia

```bash
python -m alasmia.integrations.telegram_bot
```

Or with Docker:

```bash
docker run -d \
  --name alasmia \
  -e TELEGRAM_BOT_TOKEN=your_token \
  ghcr.io/alasmia/alasmia:latest
```

## Bot Commands

| Command | Description |
|---------|-------------|
| `/start` | Start conversation |
| `/new` | New conversation |
| `/reset` | Reset memory |
| `/memory` | Memory status |
| `/status` | System status |
| `/model [name]` | Change model |
| `/help` | Help |

## Features

### Streaming Responses
Messages stream in real-time as Alasmia generates them.

### Voice Messages
Send voice messages - Alasmia will transcribe and respond.

### Inline Commands
Type `@yourbot` in any chat to get quick responses.

## Webhook vs Polling

### Polling (Default)
```yaml
telegram:
  use_webhook: false
  polling_interval: 1
```

### Webhook (Production Recommended)
```yaml
telegram:
  use_webhook: true
  webhook_url: "https://yourdomain.com/telegram"
  webhook_secret: "your_secret"
```

Set webhook:
```bash
# After starting Alasmia with webhook configured
curl -X POST "https://api.telegram.org/bot<TOKEN>/setWebhook" \
  -d "url=https://yourdomain.com/telegram" \
  -d "secret_token=your_secret"
```

## Troubleshooting

| Issue | Solution |
|-------|---------|
| Bot not responding | Verify token is correct |
| 403 Forbidden | Bot was blocked by user |
|Webhook timeout | Use polling instead |
| Duplicate messages | Delete webhook, use polling |

## Group Chats

To use in groups:

1. Add bot to group
2. Send `/start` in group
3. Bot requires explicit @mention to respond (privacy mode)

Configure group behavior:

```yaml
telegram:
  group_mode: mention  # all, mention, admin
  allowed_groups: []  # Empty = all groups allowed
```