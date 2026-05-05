# 💻 CLI User Guide

Command line interface for Alasmia.

## Starting Alasmia

```bash
# Basic start
python main.py

# With CLI chat mode
python -m alasmia.cli.chat

# Start with specific config
python main.py --config custom-config.yaml
```

## Available Commands

### Bot Commands (Telegram)

| Command | Description | Example |
|---------|-------------|---------|
| `/start` | Start conversation | `/start` |
| `/new` | Start fresh conversation | `/new` |
| `/reset` | Reset memory and start over | `/reset` |
| `/memory` | Check memory status | `/memory` |
| `/status` | Bot status and stats | `/status` |
| `/config` | View configuration | `/config` |
| `/model` | Switch LLM model | `/model your_preferred_model` |
| `/help` | Show help | `/help` |

### CLI Commands

```bash
# Chat in terminal
python main.py chat

# Run specific integration
python -m alasmia.integrations.telegram_bot
python -m alasmia.integrations.whatsapp_bot

# Test memory
python -m alasmia.agent.memory --test

# Check system status
python main.py status
```

## Interactive Mode

When running `python main.py` without arguments, you enter interactive mode:

```
Alasmia> Hello! How can I help you today?
You: What do you know about me?
Alasmia: You're Alex from New York. You're a software developer who enjoys building automation scripts. You prefer concise responses and like to experiment with new AI tools...
Alasmia>
```

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+C` | Interrupt current response |
| `Ctrl+D` | Exit |
| `Ctrl+L` | Clear screen |
| `↑/↓` | History navigation |

## Configuration Commands

```bash
# Set value
alasmia config set TELEGRAM_BOT_TOKEN new_token

# Get value
alasmia config get TELEGRAM_BOT_TOKEN

# List all
alasmia config list

# Reset to defaults
alasmia config reset
```

## Debug Mode

```bash
# Verbose logging
python main.py --debug

# Show full tracebacks
python main.py --verbose

# Log to file
python main.py --log-file alasmia.log
```