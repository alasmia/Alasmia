#!/bin/sh
# ─────────────────────────────────────────────────────────────────────────────
# Alasmia Installer — One-command setup
# ─────────────────────────────────────────────────────────────────────────────
# Usage:
#   curl -fsSL https://raw.githubusercontent.com/alasmia/Alasmia/main/install.sh | bash
#   curl -fsSL https://raw.githubusercontent.com/alasmia/Alasmia/main/install.sh | bash -- --minimal
#   curl -fsSL https://raw.githubusercontent.com/alasmia/Alasmia/main/install.sh | bash -- --skip-onboard
#
# POSIX sh — no bash required. Works on Linux, macOS, WSL2, Alpine.
# ─────────────────────────────────────────────────────────────────────────────

set -eu

REPO_URL="https://github.com/alasmia/Alasmia.git"
INSTALL_DIR="${HOME}/.alasmia"
VENV_DIR="${INSTALL_DIR}/venv"
MINIMAL=false
SKIP_ONBOARD=false

# ── Parse args ───────────────────────────────────────────────────────────────
for arg in "$@"; do
  case "$arg" in
    --minimal)    MINIMAL=true ;;
    --skip-onboard) SKIP_ONBOARD=true ;;
  esac
done

# ── Terminal helpers ─────────────────────────────────────────────────────────
if [ -t 1 ]; then
  BOLD='\033[1m'
  GREEN='\033[32m'
  YELLOW='\033[33m'
  RED='\033[31m'
  CYAN='\033[36m'
  RESET='\033[0m'
else
  BOLD='' GREEN='' YELLOW='' RED='' CYAN='' RESET=''
fi

info()  { printf "  ${GREEN}✓${RESET} %s\n" "$*"; }
warn()  { printf "  ${YELLOW}⚠${RESET} %s\n" "$*" >&2; }
die()   { printf "  ${RED}✗${RESET} %s\n" "$*" >&2; exit 1; }
bold()  { printf "${BOLD}%s${RESET}" "$*"; }

# ── Banner ────────────────────────────────────────────────────────────────────
banner() {
  echo ""
  echo "╔═══════════════════════════════════════════════════════════════════════╗"
  echo "║                                                                       ║"
  echo "║   ██████╗  █████╗ ██╗     ██╗████████╗ ██████╗ ██████╗ ██╗   ██╗   ║"
  echo "║  ██╔════╝ ██╔══██╗██║     ██║╚══██╔══╝██╔═══██╗██╔══██╗╚██╗ ██╔╝   ║"
  echo "║  ██║  ███╗███████║██║     ██║   ██║   ██║   ██║██████╔╝ ╚████╔╝    ║"
  echo "║  ██║   ██║██╔══██║██║     ██║   ██║   ██║   ██║██╔══██╗  ╚██╔╝     ║"
  echo "║  ╚██████╔╝██║  ██║███████╗██║   ██║   ╚██████╔╝██║  ██║   ██║      ║"
  echo "║   ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝   ╚═╝      ║"
  echo "║                                                                       ║"
  echo "║                      💜 Your AI Life Partner 💜                       ║"
  echo "║                                                                       ║"
  echo "╚═══════════════════════════════════════════════════════════════════════╝"
  echo ""
}

# ── Check requirements ────────────────────────────────────────────────────────
check_python() {
  if command -v python3 >/dev/null 2>&1; then
    PYTHON_VERSION=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
    PYTHON_MAJOR=$(echo "$PYTHON_VERSION" | cut -d. -f1)
    PYTHON_MINOR=$(echo "$PYTHON_VERSION" | cut -d. -f2)
    if [ "$PYTHON_MAJOR" -gt 3 ] || { [ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -ge 10 ]; }; then
      info "Python $PYTHON_VERSION"
      return 0
    fi
  fi
  die "Python 3.10+ required. Install: https://www.python.org/downloads/"
}

check_pip() {
  if command -v pip3 >/dev/null 2>&1 || command -v pip >/dev/null 2>&1; then
    info "pip found"
  else
    die "pip not found. Install: pip install -U pip"
  fi
}

check_git() {
  if command -v git >/dev/null 2>&1; then
    info "git found"
  else
    die "git not found. Install: sudo apt install git"
  fi
}

# ── Install ───────────────────────────────────────────────────────────────────
install_alasmia() {
  echo "  Downloading Alasmia..."

  if [ -d "$INSTALL_DIR" ]; then
    warn "Existing installation found at $INSTALL_DIR"
    echo "  Updating..."
    cd "$INSTALL_DIR"
    git pull
  else
    echo "  Cloning repository..."
    git clone "$REPO_URL" "$INSTALL_DIR"
    cd "$INSTALL_DIR"
  fi

  # Create venv
  if [ ! -d "$VENV_DIR" ]; then
    info "Creating virtual environment..."
    python3 -m venv "$VENV_DIR"
  fi

  # Install dependencies
  info "Installing dependencies..."
  . "$VENV_DIR/bin/activate"
  pip install --upgrade pip
  pip install -r requirements.txt

  # Create .env
  if [ ! -f "$INSTALL_DIR/.env" ]; then
    cp "$INSTALL_DIR/.env.example" "$INSTALL_DIR/.env"
    info ".env file created"
  fi

  # Create shortcuts
  info "Creating shortcuts..."
  SHORTCUT="${HOME}/.local/bin/alasmia"
  mkdir -p "$(dirname "$SHORTCUT")"
  cat > "$SHORTCUT" << 'SCRIPT'
#!/bin/sh
# Alasmia launcher
ALASMIA_DIR="${HOME}/.alasmia"
. "${ALASMIA_DIR}/venv/bin/activate"
cd "$ALASMIA_DIR"
exec python main.py "$@"
SCRIPT
  chmod +x "$SHORTCUT"

  # Add to PATH hint
  if ! echo "$PATH" | grep -q "${HOME}/.local/bin"; then
    echo ""
    warn "Add ~/.local/bin to your PATH:"
    echo "    echo 'export PATH=\$HOME/.local/bin:\$PATH' >> ~/.bashrc"
    echo "    source ~/.bashrc"
  fi

  echo ""
  info "Installation complete!"
}

# ── Main ──────────────────────────────────────────────────────────────────────
main() {
  banner

  echo "$(bold "Alasmia") — AI Life Partner"
  echo ""
  printf "  %s\n" "$(bold "Checking requirements...")"
  check_python
  check_pip
  check_git

  echo ""
  printf "  %s\n" "$(bold "Installing Alasmia...")"
  install_alasmia

  echo ""
  if [ "$SKIP_ONBOARD" = false ]; then
    printf "  %s\n" "$(bold "Starting setup wizard...")"
    echo ""
    . "$VENV_DIR/bin/activate"
    cd "$INSTALL_DIR"
    python main.py setup
  fi

  echo ""
  echo "╔═══════════════════════════════════════════════════════════════════════╗"
  echo "║                    ✅ Setup Complete! 💜                              ║"
  echo "╠═══════════════════════════════════════════════════════════════════════╣"
  echo "║                                                                       ║"
  echo "║   To start:                                                            ║"
  echo "║     alasmia --platform cli                                             ║"
  echo "║     alasmia --platform telegram                                        ║"
  echo "║                                                                       ║"
  echo "║   Or manually:                                                         ║"
  echo "║     cd ~/.alasmia                                                       ║"
  echo "║     source venv/bin/activate                                           ║"
  echo "║     python main.py --platform cli                                      ║"
  echo "║                                                                       ║"
  echo "╚═══════════════════════════════════════════════════════════════════════╝"
  echo ""
}

main "$@"