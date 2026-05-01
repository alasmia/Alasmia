# Alasmia Setup Guide

## Prerequisites

- Python 3.10 or higher
- pip (Python package manager)
- Ollama (optional, for local AI models)

## Installation Methods

### Method 1: One-Command Install (Recommended)

```bash
curl -fsSL https://raw.githubusercontent.com/alasmia/Alasmia/main/setup.sh | bash
```

This will:
1. Check Python version
2. Create virtual environment
3. Install dependencies
4. Create .env file
5. (Optional) Install Ollama and download model

### Method 2: Manual Install

#### 1. Clone the Repository

```bash
git clone https://github.com/alasmia/Alasmia.git
cd Alasmia
```

#### 2. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate  # Windows
```

#### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

#### 4. Configure Environment

```bash
cp .env.example .env
```

Edit `.env` with your settings:

```bash
# For Ollama (default)
MODEL_PROVIDER=ollama
MODEL_NAME=qwen2.5:14b
OLLAMA_URL=http://localhost:11434

# For OpenAI (alternative)
# MODEL_PROVIDER=openai
# MODEL_NAME=gpt-4
# OPENAI_API_KEY=your_api_key_here

# For Anthropic (alternative)
# MODEL_PROVIDER=anthropic
# MODEL_NAME=claude-3-opus-20240229
# ANTHROPIC_API_KEY=your_api_key_here
```

#### 5. Install Ollama (Optional)

If using Ollama:

```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Pull the default model
ollama pull qwen2.5:14b

# Start Ollama service
ollama serve
```

#### 6. Run Alasmia

```bash
python main.py
```

## Docker Installation

### Using Docker Compose (Recommended)

```bash
# Build and start
docker-compose up -d

# View logs
docker-compose logs -f alasmia

# Stop
docker-compose down
```

### Manual Docker Build

```bash
# Build image
docker build -t alasmia .

# Run container
docker run -it --env-file .env alasmia
```

## Platform-Specific Setup

### Linux

All installation methods work on Linux. For systemd service:

```bash
# Create service file
sudo nano /etc/systemd/system/alasmia.service

# Add content:
[Unit]
Description=Alasmia AI Companion
After=network.target

[Service]
Type=simple
User=your_username
WorkingDirectory=/path/to/Alasmia
ExecStart=/path/to/Alasmia/venv/bin/python main.py --platform cli
Restart=always

[Install]
WantedBy=multi-user.target

# Enable and start
sudo systemctl enable alasmia
sudo systemctl start alasmia
```

### macOS

Same as Linux. For LaunchAgent:

```bash
# Create LaunchAgent
mkdir -p ~/Library/LaunchAgents
nano ~/Library/LaunchAgents/com.alasmia.plist
```

### Windows (WSL2)

```bash
# Install WSL2 if not already installed
wsl --install

# Open WSL and follow Linux installation
```

### Android (Termux)

```bash
# Install Termux from F-Droid
# Update packages
pkg update && pkg upgrade

# Install Python
pkg install python

# Clone and setup
git clone https://github.com/alasmia/Alasmia.git
cd Alasmia
pip install -r requirements.txt
python main.py
```

## First Run

On first run, Alasmia will:

1. Greet you as a stranger
2. Ask for your name
3. Ask for your language preference
4. Save your profile

Build your relationship slowly over time!

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| MODEL_PROVIDER | AI provider (ollama, openai, anthropic) | ollama |
| MODEL_NAME | Model to use | qwen2.5:14b |
| OLLAMA_URL | Ollama server URL | http://localhost:11434 |
| TELEGRAM_BOT_TOKEN | Telegram bot token | - |
| DISCORD_BOT_TOKEN | Discord bot token | - |
| ADVANCED_MODE | Enable unfiltered mode | false |
| DATA_DIR | Data directory | ./data |

### Advanced Mode

To enable adult content and less restrictive conversations:

```bash
ADVANCED_MODE=true
```

**Warning:** This allows mature content. Use responsibly and ensure user consent.

## Troubleshooting

### Ollama Connection Issues

```bash
# Check if Ollama is running
curl http://localhost:11434

# Restart Ollama
pkill ollama
ollama serve
```

### Database Issues

If you encounter database errors:

```bash
# Delete database and start fresh
rm -rf ./data/alasmia.db
python main.py
```

### Import Errors

```bash
# Reinstall all dependencies
pip install --upgrade -r requirements.txt
```

## Updating

```bash
# Pull latest changes
git pull

# Update dependencies
pip install -r requirements.txt --upgrade
```

## Uninstallation

```bash
# Remove virtual environment
rm -rf venv

# Remove data directory (optional)
rm -rf ./data

# Uninstall Ollama (if installed)
rm -rf ~/.ollama
```

---

**Created by Doctor Kaif**
