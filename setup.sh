#!/bin/bash
# Alasmia INDEPENDENT Setup Script
# Run on ANY server - no shared dependencies
set -e

echo "╔═══════════════════════════════════════════╗"
echo "║   ALASMIA - INDEPENDENT SETUP             ║"
echo "╚═══════════════════════════════════════════╝"

# 1. Create OWN virtual environment
echo "📦 Creating Python virtual environment..."
python3 -m venv .venv
source .venv/bin/activate

# 2. Install OWN dependencies
echo "📚 Installing dependencies..."
pip install --quiet aiohttp python-telegram-bot pyyaml

# 3. Install Ollama
echo "🚀 Installing Ollama..."
curl -fsSL https://ollama.com/install.sh | sh

# 4. Download fast model
echo "📥 Downloading TinyLlama..."
ollama pull tinyllama:1.1b

# 5. Setup config
if [ ! -f config/config.yaml ]; then
    cp config/config.yaml.example config/config.yaml
    echo "⚠️  PLEASE EDIT config/config.yaml and add your Telegram bot token!"
fi

echo ""
echo "╔═══════════════════════════════════════════╗"
echo "║   ✅ INDEPENDENT SETUP COMPLETE!          ║"
echo "╚═══════════════════════════════════════════╝"
echo ""
echo "To run:"
echo "  source .venv/bin/activate"
echo "  python3 alasmia-core/__main__.py"
