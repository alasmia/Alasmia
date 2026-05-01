"""
Alasmia Telegram Bot

Telegram integration for Alasmia AI companion.
"""

import os
from typing import Optional
from dotenv import load_dotenv

from alasmia.agent.brain import Brain
from alasmia.agent.memory import MemoryManager
from alasmia.agent.personality import PersonalityEngine

load_dotenv()


class TelegramBot:
    """Telegram bot interface for Alasmia."""
    
    def __init__(
        self,
        model_loader,
        memory: MemoryManager,
        personality: PersonalityEngine
    ):
        """Initialize Telegram bot."""
        self.memory = memory
        self.personality = personality
        self.brain = Brain(model_loader)
        
        self.bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
        
        if not self.bot_token:
            raise ValueError("TELEGRAM_BOT_TOKEN not set in environment")
    
    def start(self) -> None:
        """Start the Telegram bot."""
        try:
            from telegram import Update
            from telegram.ext import (
                Application,
                CommandHandler,
                MessageHandler,
                filters,
                ContextTypes,
            )
        except ImportError:
            print("Error: python-telegram-bot not installed")
            print("Run: pip install python-telegram-bot[webhooks]")
            return
        
        application = Application.builder().token(self.bot_token).build()
        
        # Register handlers
        application.add_handler(CommandHandler("start", self._start_command))
        application.add_handler(CommandHandler("reset", self._reset_command))
        application.add_handler(CommandHandler("profile", self._profile_command))
        application.add_handler(MessageHandler(filters.TEXT, self._handle_message))
        
        print("✓ Telegram bot initialized")
        print("Starting bot... Press Ctrl+C to stop")
        
        # Start polling
        application.run_polling(allowed_updates=Update.ALL_TYPES)
    
    async def _start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command."""
        user_id = str(update.effective_user.id)
        user_name = update.effective_user.first_name
        
        # Create user if not exists
        if not self.memory.get_user_info(user_id):
            self.memory.create_user(user_id, name=user_name)
            await update.message.reply_text(
                f"Hi {user_name}! I'm Alasmia, your AI companion. 💕\n\n"
                "Let's get to know each other! What's your preferred language?\n"
                "1. Hindi\n2. English\n3. Hinglish"
            )
        else:
            await update.message.reply_text(
                "Welcome back! 💕 How are you today?"
            )
    
    async def _reset_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /reset command - clear conversation history."""
        user_id = str(update.effective_user.id)
        self.memory.clear_conversation(user_id)
        await update.message.reply_text(
            "Conversation reset! Let's start fresh. 💫"
        )
    
    async def _profile_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /profile command - show user info."""
        user_id = str(update.effective_user.id)
        info = self.memory.get_user_info(user_id)
        
        if info:
            stage = info.get("relationship_stage", "stranger").upper()
            name = info.get("name", "Friend")
            count = info.get("message_count", 0)
            
            response = (
                f"📋 **Your Profile**\n\n"
                f"**Name:** {name}\n"
                f"**Relationship Stage:** {stage}\n"
                f"**Messages:** {count}"
            )
        else:
            response = "I don't know you yet! Start chatting to introduce yourself. 😊"
        
        await update.message.reply_text(response, parse_mode="Markdown")
    
    async def _handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle incoming messages."""
        user_id = str(update.effective_user.id)
        user_message = update.message.text
        
        # Get user info
        user_info = self.memory.get_user_info(user_id)
        if not user_info:
            self.memory.create_user(
                user_id,
                name=update.effective_user.first_name
            )
            user_info = self.memory.get_user_info(user_id)
        
        # Get conversation history
        history = self.memory.get_conversation(user_id)
        
        # Get system prompt
        system_prompt = self.personality.get_system_prompt(user_id)
        
        # Generate response
        response = self.brain.think(
            message=user_message,
            history=history,
            system_prompt=system_prompt
        )
        
        # Save to memory
        self.memory.add_message(user_id, "user", user_message)
        self.memory.add_message(user_id, "assistant", response)
        
        # Send response
        await update.message.reply_text(response)
        
        # Check for stage progression
        if self.personality.should_progress_stage(user_id):
            old_stage = self.personality.get_stage(user_id)
            new_stage = self.personality.progress_stage(user_id)
            message = self.personality.get_stage_transition_message(
                old_stage, new_stage
            )
            if message:
                await update.message.reply_text(message)
