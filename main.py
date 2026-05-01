#!/usr/bin/env python3
"""
Alasmia - Your Emotional AI Companion

Entry point for the CLI application.
"""

import sys
import argparse
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from alasmia.integrations.cli_chat import CLIChat
from alasmia.integrations.telegram_bot import TelegramBot
from alasmia.integrations.discord_bot import DiscordBot
from alasmia.models.model_loader import ModelLoader
from alasmia.agent.memory import MemoryManager
from alasmia.agent.personality import PersonalityEngine
from dotenv import load_dotenv


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Alasmia - Your Emotional AI Companion",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        "--platform",
        choices=["cli", "telegram", "discord"],
        default="cli",
        help="Platform to run Alasmia on (default: cli)"
    )
    
    parser.add_argument(
        "--model",
        help="Model to use (e.g., ollama:qwen2.5:14b, openai:gpt-4)"
    )
    
    parser.add_argument(
        "--advanced-mode",
        action="store_true",
        help="Enable advanced/unfiltered mode"
    )
    
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug logging"
    )
    
    return parser.parse_args()


def main():
    """Main entry point."""
    load_dotenv()
    args = parse_args()
    
    # Initialize core components
    print("🤍 Initializing Alasmia...")
    
    # Load model
    model_loader = ModelLoader()
    if args.model:
        model_loader.set_model(args.model)
    
    # Initialize memory
    memory = MemoryManager()
    
    # Initialize personality engine
    personality = PersonalityEngine(memory)
    
    # Start platform
    print(f"Starting Alasmia on {args.platform}...")
    
    if args.platform == "cli":
        cli = CLIChat(model_loader, memory, personality)
        cli.start()
    
    elif args.platform == "telegram":
        bot = TelegramBot(model_loader, memory, personality)
        bot.start()
    
    elif args.platform == "discord":
        bot = DiscordBot(model_loader, memory, personality)
        bot.start()


if __name__ == "__main__":
    main()
