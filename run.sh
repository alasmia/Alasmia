#!/bin/bash
# Alasmia Launcher - Start Ollama + Telegram Bot
# 100% CPU-based AI Companion

set -e

echo "═══════════════════════════════════════════"
echo "     🤖 ALASMIA - AI Companion"
echo "     100% CPU • No GPU Required"
echo "═══════════════════════════════════════════"

# Start Ollama if not running
if ! curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "🚀 Starting Ollama server..."
    sudo OLLAMA_HOST=0.0.0.0 nohup ollama serve > /tmp/ollama.log 2>&1 &
    sleep 3
    
    # Verify
    for i in {1..5}; do
        if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
            echo "✅ Ollama started"
            break
        fi
        sleep 1
    done
fi

# Check Ollama is running
if ! curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "❌ Ollama failed to start"
    exit 1
fi

# Check model
MODELS=$(curl -s http://localhost:11434/api/tags | python3 -c "import sys,json; d=json.load(sys.stdin); print([m['name'] for m in d.get('models',[])])" 2>/dev/null)

if [[ "$MODELS" == *"qwen2.5:14b"* ]]; then
    echo "✅ Qwen 2.5 14B ready"
else
    echo "⚠️  Qwen 2.5 14B not downloaded"
    echo "   Run: sudo ollama pull qwen2.5:14b"
    exit 1
fi

# Start Alasmia
cd /home/ubuntu/alasmia/alasmia-core

echo "🤖 Starting Alasmia Telegram bot..."
echo ""
echo "═══════════════════════════════════════════"
echo "     ✅ ALASMIA is LIVE!"
echo "═══════════════════════════════════════════"
echo "   Telegram: @Alasmiabot"
echo ""

python3 __main__.py