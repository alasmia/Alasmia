# 📦 Installation Guide

Complete installation instructions for all platforms.

## System Requirements

| Requirement | Minimum | Recommended |
|-------------|---------|-------------|
| Python | 3.10+ | 3.11+ |
| RAM | 2 GB | 4 GB+ |
| Storage | 500 MB | 1 GB+ |
| Internet | Stable | High-speed |

## Linux/macOS

### Using pip

```bash
# Create virtual environment
python3 -m venv alasmia-env
source alasmia-env/bin/activate

# Install
pip install alasmia-ai

# Or install from source
git clone https://github.com/alasmia/Alasmia.git
cd Alasmia
pip install -e .
```

### Using Docker

```bash
# Pull latest image
docker pull ghcr.io/alasmia/alasmia:latest

# Create data directory
mkdir -p ~/alasmia-data

# Run container
docker run -d \
  --name alasmia \
  --restart unless-stopped \
  -p 8000:8000 \
  -e TELEGRAM_BOT_TOKEN=your_token \
  -e ALASMIA_MODEL=your_preferred_model \
  -v ~/alasmia-data:/data \
  ghcr.io/alasmia/alasmia:latest
```

## Windows (WSL2)

```bash
# Install WSL2 first
wsl --install

# Open WSL and follow Linux instructions
wsl
```

## Android (Termux)

```bash
# Install Termux from F-Droid

# Update packages
pkg update && pkg upgrade

# Install Python
pkg install python

# Clone and install
git clone https://github.com/alasmia/Alasmia.git
cd Alasmia
pip install -r requirements.txt
```

## Raspberry Pi

```bash
# ARM64
pip install alasmia-ai

# Or from source
git clone https://github.com/alasmia/Alasmia.git
cd Alasmia
pip install -r requirements.txt
```

## Verification

```bash
# Check installation
python -c "import alasmia; print('Alasmia installed!')"

# Or use CLI
alasmia --help
```

## Uninstall

```bash
# pip
pip uninstall alasmia-ai

# Docker
docker stop alasmia && docker rm alasmia
docker rmi ghcr.io/alasmia/alasmia:latest
```