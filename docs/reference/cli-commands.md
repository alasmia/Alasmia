# 📋 CLI Commands Reference

Complete list of all Alasmia CLI commands.

## Global Commands

| Command | Description |
|---------|-------------|
| `alasmia --help` | Show help message |
| `alasmia --version` | Show version |
| `alasmia --config FILE` | Use custom config file |

## Core Commands

### `alasmia run`
Start Alasmia.

```bash
alasmia run [OPTIONS]

Options:
  --platform TEXT    Platform to run (telegram, whatsapp, cli)
  --port PORT        Port for web interface
  --host TEXT        Host for web interface
```

### `alasmia chat`
Start interactive CLI chat.

```bash
alasmia chat [OPTIONS]

Options:
  --model TEXT    Model to use
  --stream        Enable streaming responses
```

### `alasmia config`
Manage configuration.

```bash
# Show all config
alasmia config list

# Get specific value
alasmia config get KEY

# Set value
alasmia config set KEY VALUE

# Reset to defaults
alasmia config reset
```

## Platform Commands

### `alasmia telegram`
Telegram bot management.

```bash
# Start Telegram bot
alasmia telegram start

# Stop Telegram bot
alasmia telegram stop

# Check status
alasmia telegram status

# Set webhook
alasmia telegram webhook URL
```

### `alasmia whatsapp`
WhatsApp bot management.

```bash
# Start WhatsApp bot
alasmia whatsapp start

# Link device
alasmia whatsapp link

# Check status
alasmia whatsapp status
```

## Memory Commands

### `alasmia memory`
Memory management.

```bash
# Show memory status
alasmia memory status

# Search memories
alasmia memory search QUERY

# Export memories
alasmia memory export FILE

# Import memories
alasmia memory import FILE

# Clear all memories
alasmia memory clear
```

## Schedule Commands

### `alasmia schedule`
Schedule management.

```bash
# List all schedules
alasmia schedule list

# Add new schedule
alasmia schedule add NAME --time HH:MM --message TEXT

# Remove schedule
alasmia schedule remove NAME

# Pause scheduling
alasmia schedule pause

# Resume scheduling
alasmia schedule resume
```

## Model Commands

### `alasmia model`
Model management.

```bash
# List available models
alasmia model list

# Show current model
alasmia model current

# Switch model
alasmia model use MODEL_NAME

# Test model
alasmia model test MODEL_NAME
```

## Development Commands

### `alasmia dev`
Development utilities.

```bash
# Run tests
alasmia dev test

# Run with debug
alasmia dev debug

# Generate docs
alasmia dev docs

# Format code
alasmia dev format
```

## Admin Commands

### `alasmia admin`
Administrative functions.

```bash
# Check system status
alasmia admin status

# View logs
alasmia admin logs [LINES]

# Restart services
alasmia admin restart

# Update Alasmia
alasmia admin update
```

## Keyboard Shortcuts (Interactive Mode)

| Shortcut | Action |
|----------|--------|
| `Ctrl+C` | Interrupt |
| `Ctrl+D` | Exit |
| `Ctrl+L` | Clear screen |
| `↑/↓` | History |
| `Tab` | Autocomplete |