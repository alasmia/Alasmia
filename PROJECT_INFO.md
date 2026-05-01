# Alasmia - INDEPENDENT AI Companion

> ⚠️ **This project is COMPLETELY INDEPENDENT** - No shared dependencies with other systems. Deploy anywhere.

## Independence Guarantee

- ✅ Own Python virtual environment (`.venv`)
- ✅ Own config file (`config/config.yaml`)
- ✅ Own database (`data/alasmia.db`)
- ✅ Own logs (`logs/`)
- ✅ Can run on ANY server - zero dependencies on external systems

## Quick Start (Independent Deployment)

```bash
# 1. Clone
git clone https://github.com/alasmia/Alasmia.git
cd Alasmia

# 2. Setup Python venv (YOUR OWN - not shared)
python3 -m venv .venv
source .venv/bin/activate

# 3. Install dependencies
pip install aiohttp python-telegram-bot pyyaml

# 4. Configure (edit YOUR OWN config)
cp config/config.yaml.example config/config.yaml
nano config/config.yaml  # Add your Telegram bot token

# 5. Install Ollama
curl -fsSL https://ollama.com/install.sh | sh
ollama pull tinyllama:1.1b

# 6. Run
python3 alasmia-core/__main__.py
```

## Systemd Service (Independent)

```bash
# Copy service
sudo cp alasmia.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable alasmia ollama
sudo systemctl start alasmia
```

## Architecture

```
Alasmia/
├── .venv/                 # YOUR OWN Python environment
├── alasmia-core/          # Bot source
├── config/
│   └── config.yaml        # YOUR OWN config
├── data/
│   └── alasmia.db         # YOUR OWN database
├── logs/                  # YOUR OWN logs
├── setup.sh              # Independent setup
└── run.sh                # Launcher
```

## Model Configuration

Default: **TinyLlama 1.1B** - Ultra fast (~1 second response on CPU)

For better quality: `ollama pull qwen2.5:3b` (faster than 14B, still CPU-friendly)

## Speed Benchmark

| Model | Size | CPU Response | RAM |
|-------|------|--------------|-----|
| TinyLlama 1.1B | 637 MB | ~1-2 sec | ~1 GB |
| Qwen2.5 3B | 2 GB | ~5-8 sec | ~4 GB |
| Qwen2.5 14B | 9 GB | ~15-25 sec | ~10 GB |

## License

MIT - Fully independent project.