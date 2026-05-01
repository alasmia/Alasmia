#!/bin/bash
# =============================================================================
# Alasmia One-Command Install Script
# =============================================================================
# Usage: curl -fsSL https://raw.githubusercontent.com/alasmia/Alasmia/main/setup.sh | bash
#
# This script installs Alasmia on Linux, macOS, or WSL2

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}"
echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║          Alasmia - Your Emotional AI Companion                ║"
echo "║                  Installing... ⏳                            ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Check if Python 3.10+ is installed
check_python() {
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
        if [ "$(echo "$PYTHON_VERSION >= 3.10" | bc)" = "1" ]; then
            echo -e "${GREEN}✓${NC} Python $PYTHON_VERSION found"
            return 0
        fi
    fi
    echo -e "${RED}✗${NC} Python 3.10+ is required but not found"
    echo "Please install Python 3.10 or higher"
    exit 1
}

# Check if pip is available
check_pip() {
    if command -v pip3 &> /dev/null || command -v pip &> /dev/null; then
        echo -e "${GREEN}✓${NC} pip found"
        return 0
    fi
    echo -e "${RED}✗${NC} pip not found"
    exit 1
}

# Create virtual environment
create_venv() {
    echo -e "${YELLOW}→${NC} Creating virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
    echo -e "${GREEN}✓${NC} Virtual environment created"
}

# Install dependencies
install_deps() {
    echo -e "${YELLOW}→${NC} Installing dependencies..."
    pip install --upgrade pip
    pip install -r requirements.txt
    echo -e "${GREEN}✓${NC} Dependencies installed"
}

# Create .env file
create_env() {
    if [ ! -f .env ]; then
        echo -e "${YELLOW}→${NC} Creating .env file..."
        cp .env.example .env
        echo -e "${GREEN}✓${NC} .env file created (please edit with your settings)"
    else
        echo -e "${YELLOW}→${NC} .env file already exists, skipping..."
    fi
}

# Download Ollama (optional)
install_ollama() {
    if ! command -v ollama &> /dev/null; then
        echo -e "${YELLOW}→${NC} Ollama not found. Installing Ollama..."
        curl -fsSL https://ollama.ai/install.sh | sh
        echo -e "${GREEN}✓${NC} Ollama installed"
        echo -e "${YELLOW}→${NC} Pulling default model (qwen2.5:14b)..."
        ollama pull qwen2.5:14b
        echo -e "${GREEN}✓${NC} Model pulled"
    else
        echo -e "${GREEN}✓${NC} Ollama already installed"
    fi
}

# Main installation
main() {
    echo -e "\n${BLUE}Checking requirements...${NC}"
    check_python
    check_pip
    
    echo -e "\n${BLUE}Setting up Alasmia...${NC}"
    create_venv
    install_deps
    create_env
    
    # Ask about Ollama
    read -p "Do you want to install Ollama and download the default model? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        install_ollama
    fi
    
    echo -e "\n${GREEN}"
    echo "╔═══════════════════════════════════════════════════════════════╗"
    echo "║              Alasmia Installation Complete! 🎉               ║"
    echo "╚═══════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
    echo "Next steps:"
    echo "  1. Edit .env file with your settings"
    echo "  2. Run: source venv/bin/activate"
    echo "  3. Run: python main.py"
    echo ""
    echo "For more info: https://github.com/alasmia/Alasmia"
}

main "$@"
