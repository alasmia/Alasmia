# 🔧 Environment Variables Reference

All environment variables supported by Alasmia.

## Quick Reference

```bash
# Copy example file
cp .env.example .env
```

## Required Variables

### `TELEGRAM_BOT_TOKEN`
Telegram bot token from @BotFather.

```bash
TELEGRAM_BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz
```

**Required for:** Telegram integration

---

### `ALASMIA_MODEL`
The LLM model to use.

```bash
ALASMIA_MODEL=minimaxai/minimax-m2.7
```

**Supported models:**
- `minimaxai/minimax-m2.7` (default, recommended)
- `openai/gpt-4`
- `anthropic/claude-3-opus`
- `anthropic/claude-3-sonnet`
- `openai/gpt-3.5-turbo`

**Required for:** Core functionality

---

## API Keys

### `MINIMAX_API_KEY`
MiniMax API key for MiniMax models.

```bash
MINIMAX_API_KEY=your_minimax_key_here
```

### `OPENAI_API_KEY`
OpenAI API key for GPT models.

```bash
OPENAI_API_KEY=sk-your-openai-key
```

### `ANTHROPIC_API_KEY`
Anthropic API key for Claude models.

```bash
ANTHROPIC_API_KEY=sk-ant-your-key
```

---

## Bot Configuration

### `ALASMIA_NAME`
Bot's display name.

```bash
ALASMIA_NAME=Alasmia
```

**Default:** `Alasmia`

---

### `ALASMIA_PERSONALITY`
Initial personality setting.

```bash
ALASMIA_PERSONALITY=caring
```

**Options:** `caring`, `playful`, `professional`, `friendly`

**Default:** `caring`

---

### `ALASMIA_LANGUAGE`
Primary language.

```bash
ALASMIA_LANGUAGE=en
```

**Options:** `en`, `hi`, `mixed`

**Default:** `en`

---

## System Configuration

### `LOG_LEVEL`
Logging verbosity.

```bash
LOG_LEVEL=INFO
```

**Options:** `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`

**Default:** `INFO`

---

### `MEMORY_DIR`
Directory for memory storage.

```bash
MEMORY_DIR=./memory
```

**Default:** `./memory`

---

### `TIMEZONE`
Your timezone for scheduling.

```bash
TIMEZONE=Asia/Kolkata
```

**Default:** `UTC`

---

### `PORT`
Web interface port.

```bash
PORT=8000
```

**Default:** `8000`

---

## Feature Flags

### `SCHEDULER_ENABLED`
Enable scheduled tasks.

```bash
SCHEDULER_ENABLED=true
```

**Options:** `true`, `false`

**Default:** `true`

---

### `PROACTIVE_ENABLED`
Enable proactive outreach.

```bash
PROACTIVE_ENABLED=true
```

**Options:** `true`, `false`

**Default:** `true`

---

### `VOICE_ENABLED`
Enable voice message processing.

```bash
VOICE_ENABLED=false
```

**Options:** `true`, `false`

**Default:** `false`

---

## Database

### `DATABASE_URL`
Database connection string (future feature).

```bash
DATABASE_URL=sqlite:///./alasmia.db
```

**Default:** SQLite in memory

---

## Advanced

### `MAX_TOKENS`
Maximum response length.

```bash
MAX_TOKENS=2000
```

**Default:** `2000`

---

### `TEMPERATURE`
Response creativity (0-1).

```bash
TEMPERATURE=0.7
```

**Range:** `0.0` to `1.0`

**Default:** `0.7`

---

### `STREAMING`
Enable streaming responses.

```bash
STREAMING=true
```

**Options:** `true`, `false`

**Default:** `true`

---

## Production

### `SECRET_KEY`
Secret key for production deployments.

```bash
SECRET_KEY=your-super-secret-key-here
```

**Required for:** Production deployment

---

### `ALLOWED_HOSTS`
Allowed HTTP hosts (comma-separated).

```bash
ALLOWED_HOSTS=example.com,www.example.com
```

**Default:** `localhost,127.0.0.1`

---

## Complete Example

```bash
# Core
TELEGRAM_BOT_TOKEN=123456:ABCDEF
ALASMIA_MODEL=minimaxai/minimax-m2.7
MINIMAX_API_KEY=your_key

# Bot
ALASMIA_NAME=Alasmia
ALASMIA_PERSONALITY=caring
ALASMIA_LANGUAGE=mixed

# System
LOG_LEVEL=INFO
MEMORY_DIR=./memory
TIMEZONE=Asia/Kolkata
PORT=8000

# Features
SCHEDULER_ENABLED=true
PROACTIVE_ENABLED=true

# Production
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=yourdomain.com
```