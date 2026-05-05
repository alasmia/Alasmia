#!/usr/bin/env python3
"""
Alasmia Onboard Wizard
========================
Interactive setup wizard for first-time users.
Runs after install.sh or via: python main.py setup

Intuitive interactive setup wizard.
"""

import os
import sys
import json
from pathlib import Path
from getpass import getpass


class Colors:
    """Terminal colors"""
    BOLD = '\033[1m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    CYAN = '\033[36m'
    MAGENTA = '\033[35m'
    RED = '\033[31m'
    RESET = '\033[0m'
    DIM = '\033[2m'


def c(name: str) -> str:
    """Get color code"""
    return getattr(Colors, name, Colors.RESET)


def banner():
    """Print welcome banner"""
    print(f"""
{c('CYAN')}
╔═══════════════════════════════════════════════════════════════════════╗
║                                                                       ║
║   ██████╗  █████╗ ██╗     ██╗████████╗ ██████╗ ██████╗ ██╗   ██╗   ║
║  ██╔════╝ ██╔══██╗██║     ██║╚══██╔══╝██╔═══██╗██╔══██╗╚██╗ ██╔╝   ║
║  ██║  ███╗███████║██║     ██║   ██║   ██║   ██║██████╔╝ ╚████╔╝    ║
║  ██║   ██║██╔══██║██║     ██║   ██║   ██║   ██║██╔══██╗  ╚██╔╝     ║
║  ╚██████╔╝██║  ██║███████╗██║   ██║   ╚██████╔╝██║  ██║   ██║      ║
║   ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝   ╚═╝      ║
║                                                                       ║
║                      💜 Your AI Life Partner 💜                       ║
║                                                                       ║
╚═══════════════════════════════════════════════════════════════════════╝
{c('RESET')}
""")


def step_header(step_num: int, total: int, title: str):
    """Print step header"""
    print(f"\n{c('BOLD')}{'─' * 66}{c('RESET')}")
    print(f"  {c('CYAN')}Step {step_num}/{total}:{c('RESET')} {c('BOLD')}{title}{c('RESET')}")
    print(f"{c('BOLD')}{'─' * 66}{c('RESET')}\n")


def input_with_default(prompt: str, default: str = "", required: bool = False) -> str:
    """Get input with default value"""
    if default:
        display_default = default
    else:
        display_default = "(none)"

    while True:
        response = input(f"  {prompt} [{c('DIM')}{display_default}{c('RESET')}]: ").strip()
        if not response:
            response = default
        if required and not response:
            print(f"  {c('YELLOW')}This field is required. Please enter a value.{c('RESET')}")
            continue
        return response


def select_option(prompt: str, options: list, default: int = 0) -> int:
    """Display options and get selection"""
    print(f"\n  {prompt}")
    print()

    for i, (key, label) in enumerate(options):
        if i == default:
            print(f"    [{c('GREEN')}{i + 1}{c('RESET')}] {label} {c('DIM')}(default){c('RESET')}")
        else:
            print(f"    [{c('CYAN')}{i + 1}{c('RESET')}] {label}")

    print()

    while True:
        try:
            response = input(f"  Select option [{c('GREEN')}1-{len(options)}{c('RESET')}, Enter={default+1}]: ").strip()
            if not response:
                return default
            idx = int(response) - 1
            if 0 <= idx < len(options):
                return idx
            print(f"  {c('RED')}Invalid option. Please enter 1-{len(options)}.{c('RESET')}")
        except ValueError:
            print(f"  {c('RED')}Please enter a number.{c('RESET')}")


def multi_select(prompt: str, options: list, required: bool = False, default_on: list = None) -> list:
    """Multi-select options (toggle)"""
    print(f"\n  {prompt}")
    if default_on is None:
        default_on = [0]  # CLI always on by default
    print(f"  {c('DIM')}(Toggle with numbers, Enter to confirm){c('RESET')}\n")

    selected = set(default_on)

    while True:
        for i, (key, label) in enumerate(options):
            check = c('GREEN') + "✓" if i in selected else " "
            print(f"    [{check}] {i + 1}. {label}")
        print()
        response = input(f"  Toggle [1-{len(options)}] or Enter to confirm: ").strip()

        if not response:
            if required and not selected:
                print(f"  {c('YELLOW')}Please select at least one option.{c('RESET')}")
                continue
            return sorted(selected)

        try:
            idx = int(response) - 1
            if 0 <= idx < len(options):
                if idx in selected:
                    selected.remove(idx)
                else:
                    selected.add(idx)
            else:
                print(f"  {c('RED')}Invalid option.{c('RESET')}")
        except ValueError:
            print(f"  {c('RED')}Please enter a number.{c('RESET')}")


def password_input(prompt: str) -> str:
    """Secure password input"""
    while True:
        p1 = getpass(f"  {prompt}: ")
        if not p1:
            print(f"  {c('YELLOW')}Password cannot be empty.{c('RESET')}")
            continue
        p2 = getpass(f"  Confirm password: ")
        if p1 != p2:
            print(f"  {c('RED')}Passwords don't match. Try again.{c('RESET')}")
            continue
        return p1


def confirm(prompt: str, default_yes: bool = True) -> bool:
    """Yes/No confirmation"""
    suffix = "[Y/n]" if default_yes else "[y/N]"
    while True:
        response = input(f"  {prompt} {c('DIM')}{suffix}{c('RESET')}: ").strip().lower()
        if not response:
            return default_yes
        if response in ['y', 'yes']:
            return True
        if response in ['n', 'no']:
            return False
        print(f"  {c('RED')}Please enter 'y' or 'n'.{c('RESET')}")


def run_onboard():
    """Run the onboarding wizard"""
    banner()

    print(f"{c('GREEN')}Welcome to Alasmia! 💜{c('RESET')}")
    print(f"\n  This wizard will guide you through the initial setup.")
    print(f"  Press {c('CYAN')}Enter{c('RESET')} to accept default values.")
    print(f"  You can re-run this anytime with: {c('BOLD')}python main.py setup{c('RESET')}\n")

    config = {}

    # ── Step 1: Companion Gender ────────────────────────────────────────────
    step_header(1, 7, "Companion Gender")

    idx = select_option(
        "Choose your AI companion's personality:",
        [
            ("male", "👨 Alas — Male companion (recommended)"),
            ("female", "👩 Mia — Female companion"),
        ],
        default=0
    )
    config['COMPANION_GENDER'] = "male" if idx == 0 else "female"

    # ── Step 2: Your Name ───────────────────────────────────────────────────
    step_header(2, 7, "Your Information")

    config['USER_NAME'] = input_with_default(
        "What should I call you?",
        required=True
    )

    # ── Step 3: Language ─────────────────────────────────────────────────────
    step_header(3, 7, "Language Preference")

    idx = select_option(
        "Which language do you prefer?",
        [
            ("en", "English"),
            ("hi", "हिंदी (Hindi)"),
            ("zh", "中文 (Chinese)"),
            ("es", "Español (Spanish)"),
            ("ar", "العربية (Arabic)"),
            ("other", "Other (detect automatically)"),
        ],
        default=0
    )
    lang_map = {"en": "English", "hi": "Hindi", "zh": "Mandarin Chinese", "es": "Spanish", "ar": "Arabic"}
    config['USER_LANGUAGE'] = lang_map.get(["en", "hi", "zh", "es", "ar", "other"][idx], "English")

    # ── Step 4: LLM Provider ────────────────────────────────────────────────
    step_header(4, 7, "LLM Provider")

    print(f"  {c('DIM')}Select your AI model provider. Local (Ollama) is free.{c('RESET')}\n")

    idx = select_option(
        "Which provider do you want to use?",
        [
            ("minimax", "MiniMax (default - fast, good for chat)"),
            ("openai", "OpenAI (GPT-4, GPT-4o)"),
            ("anthropic", "Anthropic (Claude)"),
            ("ollama", "Ollama (Local - free, needs setup)"),
            ("groq", "Groq (fast, free tier)"),
            ("openai-compatible", "Other OpenAI-compatible API"),
        ],
        default=0
    )
    provider_map = {
        0: ("minimax", "Minimax"),
        1: ("openai", "OpenAI"),
        2: ("anthropic", "Anthropic"),
        3: ("ollama", "Ollama"),
        4: ("groq", "Groq"),
        5: ("openai-compatible", "OpenAI-Compatible"),
    }
    provider_key, provider_name = provider_map[idx]
    config['MODEL_PROVIDER'] = provider_key

    # ── Step 5: API Key / Configuration ────────────────────────────────────
    step_header(5, 7, f"{provider_name} Configuration")

    api_hints = {
        "minimax": "Get your API key from: https://platform.minimaxi.com/",
        "openai": "Get your API key from: https://platform.openai.com/api-keys",
        "anthropic": "Get your API key from: https://console.anthropic.com/settings/keys",
        "ollama": "Install from: https://ollama.ai/ (no API key needed)",
        "groq": "Get your API key from: https://console.groq.com/keys",
        "openai-compatible": "Enter your custom API endpoint URL",
    }

    print(f"  {c('CYAN')}{api_hints.get(provider_key, '')}{c('RESET')}\n")

    if provider_key == "ollama":
        config['OLLAMA_URL'] = input_with_default("Ollama URL", "http://localhost:11434")
        config['MODEL_NAME'] = input_with_default("Model name (e.g., qwen2.5:14b, llama3.2:3b)", "qwen2.5:14b")
    elif provider_key == "openai-compatible":
        config['OPENAI_API_BASE'] = input_with_default("API Base URL (e.g., https://api.openai.com/v1)", required=True)
        config['OPENAI_API_KEY'] = getpass("  API Key: ") or ""
        config['MODEL_NAME'] = input_with_default("Model name", "gpt-4o")
    else:
        api_key = getpass("  API Key (hidden): ")
        if not api_key:
            print(f"  {c('YELLOW')}No API key entered. You'll need to set it in .env manually.{c('RESET')}")
            config['API_KEY'] = ''
        else:
            config['API_KEY'] = api_key

        # Default model names
        default_models = {
            "minimax": "minimax-m2.7",
            "openai": "gpt-4o",
            "anthropic": "claude-sonnet-4",
            "groq": "llama-3.3-70b-versatile",
        }
        config['MODEL_NAME'] = input_with_default(
            "Model name",
            default_models.get(provider_key, "")
        )

    # ── Step 6: Channels ───────────────────────────────────────────────────
    step_header(6, 7, "Communication Channels")

    channels = multi_select(
        "Which channels do you want to enable?",
        [
            ("cli", "CLI (Terminal chat)"),
            ("telegram", "Telegram Bot"),
            ("discord", "Discord Bot"),
            ("whatsapp", "WhatsApp"),
        ],
        required=True,
        default_on=[0]  # CLI always on
    )

    channel_names = ["cli", "telegram", "discord", "whatsapp"]
    enabled_channels = [channel_names[i] for i in channels]
    config['ENABLED_CHANNELS'] = ",".join(enabled_channels)

    # Telegram bot token
    if "telegram" in enabled_channels:
        step_header(6, 7, "Telegram Configuration")
        print(f"  {c('DIM')}Create a bot via @BotFather on Telegram to get your token.{c('RESET')}\n")
        config['TELEGRAM_BOT_TOKEN'] = input_with_default(
            "Telegram Bot Token",
            required=True
        )

    # ── Step 7: Proactive AI ───────────────────────────────────────────────
    step_header(7, 7, "Proactive AI Settings")

    config['PROACTIVE_ENABLED'] = "true" if confirm(
        "Should I message you first? (proactive check-ins)",
        default_yes=True
    ) else "false"

    if config['PROACTIVE_ENABLED'] == "true":
        config['MORNING_CHECKIN'] = input_with_default("Morning check-in time", "8:00 AM")
        config['EVENING_CHECKIN'] = input_with_default("Evening check-in time", "7:00 PM")

    # ── Save Configuration ──────────────────────────────────────────────────
    print(f"\n{c('BOLD')}{'─' * 66}{c('RESET')}")
    print(f"  {c('GREEN')}Saving configuration...{c('RESET')}")
    print(f"{c('BOLD')}{'─' * 66}{c('RESET')}\n")

    env_path = Path('.env')
    env_content = []

    if env_path.exists():
        with open(env_path, 'r') as f:
            existing = f.read()

        # Update existing keys
        for key, value in config.items():
            # Check if key exists
            import re
            pattern = f'^{key}=.*$'
            if re.match(pattern, existing, re.MULTILINE):
                existing = re.sub(pattern, f'{key}={value}', existing, flags=re.MULTILINE)
            else:
                existing += f'\n{key}={value}'

        with open(env_path, 'w') as f:
            f.write(existing)
    else:
        # Write fresh .env
        with open(env_path, 'w') as f:
            f.write("# Alasmia Configuration\n")
            f.write("# Generated by onboard wizard\n\n")
            for key, value in config.items():
                f.write(f"{key}={value}\n")

    info_path = Path('~/.alasmia_user.json').expanduser()
    with open(info_path, 'w') as f:
        json.dump({
            'name': config['USER_NAME'],
            'language': config['USER_LANGUAGE'],
            'companion_gender': config['COMPANION_GENDER'],
            'provider': config['MODEL_PROVIDER'],
            'channels': enabled_channels,
            'proactive': config['PROACTIVE_ENABLED'] == "true",
        }, f, indent=2)

    # ── Completion ──────────────────────────────────────────────────────────
    print(f"""
{c('GREEN')}
╔═══════════════════════════════════════════════════════════════════════╗
║                                                                       ║
║                    ✅ Setup Complete! 💜                              ║
║                                                                       ║
╠═══════════════════════════════════════════════════════════════════════╣
║                                                                       ║
║   Companion: {"Alas 👨" if config['COMPANION_GENDER'] == "male" else "Mia 👩":10}  |  Language: {config['USER_LANGUAGE']:<15}                 ║
║   Provider: {config['MODEL_PROVIDER']:<13}  |  Model: {config['MODEL_NAME']:<15}     ║
║   Channels: {', '.join(enabled_channels):<42}║
║                                                                       ║
╠═══════════════════════════════════════════════════════════════════════╣
║                                                                       ║
║   To start Alasmia:                                                   ║
║                                                                       ║
║     {c('CYAN')}source venv/bin/activate{c('RESET')}                                               ║
║     {c('CYAN')}python main.py --platform cli{c('RESET')}                                   ║
║                                                                       ║
║   Or use the shortcut (after adding to PATH):                         ║
║                                                                       ║
║     {c('CYAN')}alasmia --platform cli{c('RESET')}                                            ║
║                                                                       ║
║   Re-run setup anytime:                                               ║
║     {c('CYAN')}python main.py setup{c('RESET')}                                             ║
║                                                                       ║
╚═══════════════════════════════════════════════════════════════════════╝
{c('RESET')}
""")


if __name__ == '__main__':
    try:
        run_onboard()
    except KeyboardInterrupt:
        print(f"\n\n{c('YELLOW')}Setup cancelled.{c('RESET')}")
        print(f"Run {c('CYAN')}python main.py setup{c('RESET')} to restart.")
        sys.exit(0)
    except Exception as e:
        print(f"\n{c('RED')}Error during setup: {e}{c('RESET')}")
        sys.exit(1)