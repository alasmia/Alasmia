"""
Alasmia Setup Flow

Handles first-time setup and configuration.
"""

import os
from typing import Optional
from dotenv import load_dotenv

load_dotenv()


class SetupFlow:
    """Guides users through initial setup."""

    def __init__(self):
        self.required_vars = [
            "TELEGRAM_BOT_TOKEN",
        ]
        self.optional_vars = [
            "MODEL_PROVIDER",
            "MODEL_NAME",
            "OLLAMA_URL",
            "OPENAI_API_KEY",
            "ANTHROPIC_API_KEY",
        ]

    def check_configuration(self) -> dict:
        """Check if required environment variables are set."""
        missing = []
        configured = []

        for var in self.required_vars:
            if os.getenv(var):
                configured.append(var)
            else:
                missing.append(var)

        return {
            "complete": len(missing) == 0,
            "missing": missing,
            "configured": configured,
        }

    def get_setup_instructions(self) -> str:
        """Return setup instructions."""
        return """
📚 Alasmia Setup Instructions

1. Create a .env file:
   cp .env.example .env

2. Add your Telegram Bot Token:
   - Open Telegram and chat with @BotFather
   - Send /newbot and follow instructions
   - Copy the token to TELEGRAM_BOT_TOKEN

3. (Optional) Configure your LLM provider:
   - Ollama (local): MODEL_PROVIDER=ollama, MODEL_NAME=llama3.2
   - OpenAI: MODEL_PROVIDER=openai, OPENAI_API_KEY=sk-...
   - Anthropic: MODEL_PROVIDER=anthropic, ANTHROPIC_API_KEY=sk-ant-...

4. Run Alasmia:
   python main.py
"""

    def run_interactive_setup(self) -> bool:
        """Run interactive setup (placeholder for future)."""
        print("🔧 Alasmia Interactive Setup")
        print("=" * 40)

        status = self.check_configuration()
        if status["complete"]:
            print("✅ All required variables configured!")
            return True

        print("❌ Missing required variables:")
        for var in status["missing"]:
            print(f"   - {var}")

        print(self.get_setup_instructions())
        return False


def get_setup_flow() -> SetupFlow:
    """Get SetupFlow instance."""
    return SetupFlow()