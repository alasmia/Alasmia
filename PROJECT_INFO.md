# Alasmia Project Structure

```
/home/ubuntu/alasmia/
├── README.md                    # Project documentation
├── LICENSE                      # MIT License (or your choice)
├── run.sh                       # Quick start launcher
│
├── config/
│   └── config.yaml              # Configuration file
│
├── alasmia-core/                # Main Python package
│   ├── __main__.py             # Entry point
│   ├── __init__.py
│   ├── core.py                  # Memory, trust, relationship engine
│   ├── telegram_bot.py          # Telegram bot (@Alasmiabot)
│   └── skills.py                # Task automation (email, files, etc)
│
├── models/                      # Ollama models (downloaded)
│   └── qwen2.5:14b             # 100% CPU inference model
│
├── data/                        # Persistent data
│   ├── alasmia.db               # SQLite (users, conversations, milestones)
│   └── vector_db/              # ChromaDB (semantic memory) - future
│
└── skills/                      # Custom skills directory
```

## Quick Start

```bash
cd /home/ubuntu/alasmia
./run.sh
```

## Bot Commands

| Command | Description |
|---------|-------------|
| `/start` | Introduce yourself to Alasmia |
| `/profile` | View your relationship status |
| `/skills` | See available automation skills |
| `/reset` | Start fresh (new stranger) |

## Skill Commands

| Pattern | Skill | Trust Level |
|---------|-------|-------------|
| `calculate 2+2` | Calculator | 0 |
| `search for X` | Web Search | 0 |
| `read /path/to/file` | Read File | 1 |
| `write /path:content` | Write File | 2 |
| `run print('hello')` | Execute Code | 2 |
| `system info` | Server Status | 2 |

## Trust Levels

| Level | Name | Conversations | Capabilities |
|-------|------|--------------|--------------|
| 0 | Stranger | 0-50 | Basic chat |
| 1 | Acquaintance | 50-200 | +File reading |
| 2 | Friend | 200-500 | +Code execution, write files |
| 3 | Close | 500-1000 | +Email access |
| 4 | Partner | 1000+ | Full access |

## Systemd Service

```bash
sudo systemctl enable alasmia
sudo systemctl start alasmia
sudo systemctl status alasmia
```

## Logs

```bash
tail -f /tmp/alasmia.log     # Bot output
tail -f /tmp/ollama.log       # Ollama server
```

## Model Info

- **Name:** Qwen 2.5 14B Instruct
- **Quantization:** Q4_K_M (GGUF)
- **Size:** ~8.6 GB
- **RAM needed:** ~10 GB
- **Inference:** 100% CPU, ~20-30 tok/sec
- **Download:** `sudo ollama pull qwen2.5:14b`