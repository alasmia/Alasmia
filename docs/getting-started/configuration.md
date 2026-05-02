# ⚙️ Configuration Guide

Configure Alasmia for your needs.

## Environment Variables

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

### Required Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `TELEGRAM_BOT_TOKEN` | Telegram bot token from @BotFather | `123456:ABC-DEF...` |
| `ALASMIA_MODEL` | LLM model to use | `minimaxai/minimax-m2.7` |
| `MINIMAX_API_KEY` | MiniMax API key | `your_api_key` |

### Optional Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `ALASMIA_NAME` | `Alasmia` | Bot name |
| `ALASMIA_PERSONALITY` | `caring` | Initial personality |
| `LOG_LEVEL` | `INFO` | Logging level |
| `MEMORY_DIR` | `./memory` | Memory storage path |
| `SCHEDULER_ENABLED` | `true` | Enable scheduling |
| `TIMEZONE` | `Asia/Kolkata` | Your timezone |

## Configuration File

Alasmia also supports YAML configuration in `alasmia/config/settings.yaml`:

```yaml
# Bot Settings
bot:
  name: Alasmia
  personality: caring
  language: en

# Model Settings
model:
  provider: minimax
  name: minimaxai/minimax-m2.7
  temperature: 0.7
  max_tokens: 2000

# Memory Settings
memory:
  enabled: true
  type: vector  # vector or simple
  persist: true

# Scheduler Settings
scheduler:
  enabled: true
  timezone: Asia/Kolkata

# Platform Settings
platforms:
  telegram:
    enabled: true
    streaming: true
  whatsapp:
    enabled: false
  discord:
    enabled: false
```

## Runtime Configuration

Change settings while Alasmia is running:

```bash
# Via CLI
alasmia config set personality caring
alasmia config set log_level DEBUG

# Check current config
alasmia config show
```

## Secrets Management

Never commit `.env` to git! The `.gitignore` already excludes it.

For production, consider:
- Docker secrets
- Environment injection from CI/CD
- Vault/HashiCorp for enterprise