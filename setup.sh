#!/bin/bash
# Alasmia Setup Script - First time deployment
set -e

echo "╔═══════════════════════════════════════════╗"
echo "║   ALASMIA - AI Companion Setup            ║"
echo "╚═══════════════════════════════════════════╝"

# 1. Install Ollama
echo "📦 Installing Ollama..."
curl -fsSL https://ollama.com/install.sh | sh

# 2. Start Ollama
echo "🚀 Starting Ollama..."
sudo systemctl enable ollama
sudo systemctl start ollama

# 3. Download model (8.6 GB - takes time)
echo "📥 Downloading Qwen 2.5 14B model..."
echo "   This is ~8.6 GB, may take 10-30 minutes depending on internet..."
ollama pull qwen2.5:14b

# 4. Install Python dependencies
echo "📚 Installing Python dependencies..."
pip3 install aiohttp python-telegram-bot pyyaml

# 5. Configure
echo "⚙️  Configuration..."
if [ ! -f config/config.yaml ]; then
    cp config/config.yaml.example config/config.yaml
    echo "   Created config/config.yaml - PLEASE EDIT and add your Telegram bot token!"
fi

echo ""
echo "╔═══════════════════════════════════════════╗"
echo "║   ✅ SETUP COMPLETE!                      ║"
echo "╚═══════════════════════════════════════════╝"
echo ""
echo "Next steps:"
echo "  1. Edit config/config.yaml and add your Telegram bot token"
echo "  2. Run: ./run.sh"
echo ""
echo "Or use systemd:"
echo "  sudo systemctl enable alasmia ollama"
echo "  sudo systemctl start alasmia"
echo ""