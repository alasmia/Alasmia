"""
Alasmia Telegram Bot - v0.1.2

Enhanced Telegram integration with:
- Phase 1 features (Proactive, Interest Tracking, Emotional Continuity)
- Phase 2 features (Multi-platform, Unified handling)
- All multilingual support
"""

import os
import logging
from datetime import datetime
from typing import Dict, Optional

from telegram import Update, ForceReply
from telegram.ext import (
    Application, CommandHandler, MessageHandler, 
    filters, ContextTypes, ConversationHandler
)

# Import Alasmia components
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from alasmia.agent.brain import Brain
from alasmia.agent.memory import MemoryManager
from alasmia.agent.personality import PersonalityEngine
from alasmia.agent.mood_handler import MoodHandler
from alasmia.agent.emotion_tracker import EmotionTracker
from alasmia.agent.milestone import MilestoneTracker
from alasmia.agent.proactive_engine import ProactiveEngine
from alasmia.agent.interest_tracker import InterestTracker
from alasmia.agent.emotional_continuity import EmotionalContinuity
from alasmia.agent.shared_experiences import SharedExperiences
from alasmia.core.state_manager import StateManager
from alasmia.core.scheduler import Scheduler, detect_language
from alasmia.core.enhanced_scheduler import EnhancedScheduler
from alasmia.core.analytics import Analytics
from alasmia.models.model_loader import ModelLoader

from alasmia.agent.alas_prompts import get_alas_greeting, get_mia_greeting
from alasmia.agent.mia_prompts import get_mia_greeting

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TelegramBot:
    """
    Enhanced Telegram bot with all Phase 1 + Phase 2 features.
    """
    
    # States for conversation handler
    (ASKING_NAME, CHATTING) = range(2)
    
    def __init__(self, token: str = None, model_loader: ModelLoader = None):
        """Initialize Telegram bot."""
        self.token = token or os.getenv("TELEGRAM_BOT_TOKEN")
        self.model_loader = model_loader or ModelLoader()
        
        # Initialize all Phase 1 components
        self.memory = MemoryManager()
        self.personality = PersonalityEngine(self.memory)
        self.brain = Brain(self.model_loader)
        self.mood_handler = MoodHandler()
        self.emotion_tracker = EmotionTracker(self.memory)
        self.milestone_tracker = MilestoneTracker()
        
        # Phase 1 new components
        self.proactive_engine = ProactiveEngine()
        self.interest_tracker = InterestTracker()
        self.emotional_continuity = EmotionalContinuity()
        self.shared_experiences = SharedExperiences()
        
        self.scheduler = EnhancedScheduler(
            memory_manager=self.memory,
            proactive_engine=self.proactive_engine,
            interest_tracker=self.interest_tracker
        )
        self.analytics = Analytics(self.memory)
        
        # User states
        self.user_states: Dict[int, Dict] = {}
        
        # App for bot
        self.app = None
    
    async def start(self):
        """Start the Telegram bot."""
        if not self.token:
            logger.error("No Telegram token provided!")
            return
        
        self.app = Application.builder().token(self.token).build()
        
        # Add handlers
        self.app.add_handler(CommandHandler("start", self.cmd_start))
        self.app.add_handler(CommandHandler("help", self.cmd_help))
        self.app.add_handler(CommandHandler("stats", self.cmd_stats))
        self.app.add_handler(CommandHandler("mood", self.cmd_mood))
        self.app.add_handler(CommandHandler("interests", self.cmd_interests))
        self.app.add_handler(CommandHandler("language", self.cmd_language))
        self.app.add_handler(CommandHandler("companion", self.cmd_companion))
        
        # Message handler with conversation
        conv_handler = ConversationHandler(
            entry_point=[MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message)],
            states={
                self.ASKING_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_name)],
                self.CHATTING: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_chat)],
            },
            fallbacks=[CommandHandler("cancel", self.cmd_cancel)],
        )
        self.app.add_handler(conv_handler)
        
        # Start polling
        logger.info("Starting Telegram bot...")
        await self.app.run_polling(allowed_updates=Update.ALL_TYPES)
    
    async def cmd_start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command."""
        user_id = str(update.effective_user.id)
        
        # Check if user exists
        user_info = self.memory.get_user_info(user_id)
        
        if user_info:
            # Returning user
            companion = user_info.get("companion_gender", "female")
            companion_name = "Alas" if companion == "male" else "Mia"
            name = user_info.get("name", "friend")
            
            # Store state
            self.user_states[update.effective_user.id] = {
                "companion": companion,
                "name": name,
                "language": user_info.get("language", "English"),
                "user_id": user_id,
            }
            
            greeting = get_alas_greeting("returning", self.user_states[update.effective_user.id]["language"]) if companion == "male" else get_mia_greeting("returning", self.user_states[update.effective_user.id]["language"])
            
            await update.message.reply_text(f"{greeting}\n\nWhat would you like to talk about?")
            return self.CHATTING
        else:
            # New user - need companion selection
            await update.message.reply_text(
                "🤍 *Welcome to Alasmia!*\n\n"
                "I'm your AI life partner. Let's get to know each other!\n\n"
                "First, choose your companion:\n"
                "👨 **Alas** - Male energy (strong, supportive)\n"
                "👩 **Mia** - Female energy (warm, nurturing)\n\n"
                "Just send *Alas* or *Mia* to choose!"
            )
            
            self.user_states[update.effective_user.id] = {
                "user_id": user_id,
                "awaiting_companion": True,
            }
            return self.ASKING_NAME
    
    async def handle_name(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle companion selection and name collection."""
        user_id = str(update.effective_user.id)
        text = update.message.text.strip()
        
        state = self.user_states.get(update.effective_user.id, {})
        
        # Check if choosing companion
        if state.get("awaiting_companion"):
            if text.lower() in ["alas", "mia"]:
                companion = "male" if text.lower() == "alas" else "female"
                state["companion"] = companion
                state["awaiting_companion"] = False
                state["awaiting_name"] = True
                
                companion_name = "Alas" if companion == "male" else "Mia"
                await update.message.reply_text(
                    f"Great! You chose *{companion_name}*! 💕\n\n"
                    f"Now, what's your name? (Or just say *skip* to stay anonymous)"
                )
                return self.ASKING_NAME
            else:
                await update.message.reply_text(
                    "Please choose *Alas* or *Mia*:\n"
                    "👨 **Alas** - Male energy\n"
                    "👩 **Mia** - Female energy"
                )
                return self.ASKING_NAME
        
        # Check if providing name
        if state.get("awaiting_name"):
            name = text if text.lower() != "skip" else "Friend"
            state["name"] = name
            state["awaiting_name"] = False
            
            companion = state.get("companion", "female")
            companion_name = "Alas" if companion == "male" else "Mia"
            
            # Create user in memory
            self.memory.create_user(
                user_id,
                name=name,
                companion_gender=companion,
                language="English"  # Will detect from first message
            )
            
            # Store full state
            self.user_states[update.effective_user.id] = {
                "companion": companion,
                "name": name,
                "language": "English",
                "user_id": user_id,
            }
            
            greeting = get_alas_greeting("casual", "English") if companion == "male" else get_mia_greeting("casual", "English")
            await update.message.reply_text(
                f"*{companion_name}:* {greeting}\n\n"
                f"Nice to meet you, {name}! 😊\n\n"
                f"Feel free to chat with me in any language - I'll understand! 🌐"
            )
            return self.CHATTING
        
        return self.ASKING_NAME
    
    async def handle_chat(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle regular chat messages."""
        user_id = str(update.effective_user.id)
        user_message = update.message.text.strip()
        user_state = self.user_states.get(update.effective_user.id, {})
        
        # Get user's companion info
        companion = user_state.get("companion", "female")
        companion_name = "Alas" if companion == "male" else "Mia"
        language = user_state.get("language", "English")
        
        # Language detection on first message
        if language == "English" and not user_state.get("language_detected"):
            detected_lang = detect_language(user_message)
            user_state["language"] = detected_lang
            user_state["language_detected"] = True
            self.memory.update_user(user_id, {"language": detected_lang})
            
            await update.message.reply_text(f"🌐 Detected language: {detected_lang}")
        
        # Get updated language
        language = user_state.get("language", "English")
        
        # Phase 1: Interest tracking
        detected_mood = self.mood_handler.detect_mood(user_message)
        self.interest_tracker.track_message(user_id, user_message, detected_mood)
        
        # Phase 1: Emotional continuity
        self.emotional_continuity.record_mood(user_id, detected_mood, user_message[:50])
        
        # Build system prompt
        system_prompt = self.personality.get_system_prompt(user_id)
        
        # Add language instruction
        system_prompt += f"""
IMPORTANT - RESPOND IN USER'S LANGUAGE:
- The user speaks and prefers: {language}
- You MUST respond in {language} language
- ALL your responses must be in {language}
"""
        
        # Add interest context
        interest_context = self.interest_tracker.get_memory_context(user_id)
        if interest_context:
            system_prompt += f"\n{interest_context}\n"
        
        # Add mood context
        if detected_mood != "neutral":
            system_prompt += f"\nUser's current mood: {detected_mood.upper()}\n"
        
        # Get conversation history
        history = self.memory.get_conversation(user_id, limit=20)
        
        # Generate response
        response = self.brain.think(
            message=user_message,
            history=history,
            system_prompt=system_prompt,
            context={"mood": detected_mood, "language": language}
        )
        
        # Save to memory
        self.memory.add_message(user_id, "user", user_message, detected_mood)
        self.memory.add_message(user_id, "assistant", response)
        self.memory.increment_message_count(user_id)
        
        # Phase 1: Shared experiences
        self.shared_experiences.analyze_and_record(user_id, user_message, response, detected_mood)
        
        # Proactive engine
        self.proactive_engine.update_streak(user_id)
        
        # Send response
        await update.message.reply_text(response)
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Default message handler."""
        # This catches messages when not in a conversation state
        await self.cmd_start(update, context)
    
    async def cmd_help(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command."""
        await update.message.reply_text(
            "*Alasmia Commands:*\n\n"
            "/start - Restart conversation\n"
            "/help - Show this help\n"
            "/stats - Your statistics\n"
            "/mood - Current mood analysis\n"
            "/interests - Your tracked interests\n"
            "/language - Change language\n"
            "/companion - Switch companion (Alas/Mia)"
        )
    
    async def cmd_stats(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /stats command."""
        user_id = str(update.effective_user.id)
        user_info = self.memory.get_user_info(user_id)
        
        if not user_info:
            await update.message.reply_text("Start with /start first!")
            return
        
        user_state = self.user_states.get(update.effective_user.id, {})
        companion = user_state.get("companion", "female")
        companion_name = "Alas" if companion == "male" else "Mia"
        
        connection_score = self.analytics.calculate_connection_score(user_id)
        streak = self.proactive_engine.get_streak(user_id)
        
        stats = (
            f"*📊 Your Stats:*\n\n"
            f"Name: {user_info.get('name', 'Friend')}\n"
            f"Companion: {companion_name}\n"
            f"Language: {user_state.get('language', 'English')}\n"
            f"Stage: {user_info.get('relationship_stage', 'stranger').upper()}\n"
            f"Messages: {user_info.get('message_count', 0)}\n"
            f"Connection: {connection_score}%\n"
            f"Streak: {streak} days"
        )
        
        await update.message.reply_text(stats)
    
    async def cmd_mood(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /mood command."""
        summary = self.mood_handler.get_emotional_summary()
        
        await update.message.reply_text(
            f"*📊 Mood Analysis:*\n\n"
            f"Current: {summary['current_mood']}\n"
            f"Dominant: {summary['dominant_mood']}\n"
            f"Mode: {summary['special_mode'] or 'Normal'}\n"
            f"History: {summary['history_length']} messages"
        )
    
    async def cmd_interests(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /interests command."""
        user_id = str(update.effective_user.id)
        interests = self.interest_tracker.get_interests(user_id, min_mentions=2)
        
        if not interests:
            await update.message.reply_text("No interests tracked yet. Keep chatting! 😊")
            return
        
        msg = "*🎯 Your Tracked Interests:*\n\n"
        for category, items in interests.items():
            if items:
                interest_list = ", ".join([i['interest'] for i in items])
                msg += f"*{category}:* {interest_list}\n"
        
        await update.message.reply_text(msg)
    
    async def cmd_language(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /language command."""
        await update.message.reply_text(
            "🌐 *Change Language*\n\n"
            "Just tell me your preferred language!\n"
            "For example: 'I prefer Japanese' or 'Use Mandarin Chinese'"
        )
    
    async def cmd_companion(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /companion command."""
        await update.message.reply_text(
            "👥 *Switch Companion*\n\n"
            "To switch companion, type *Alas* or *Mia*"
        )
    
    async def cmd_cancel(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /cancel command."""
        await update.message.reply_text("Cancelled. Use /start to begin again.")
        return ConversationHandler.END


def main():
    """Main entry point."""
    import os
    from dotenv import load_dotenv
    
    load_dotenv()
    
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        print("Error: TELEGRAM_BOT_TOKEN not set in environment!")
        print("Get your token from @BotFather on Telegram")
        return
    
    bot = TelegramBot(token=token)
    
    import asyncio
    asyncio.run(bot.start())


if __name__ == "__main__":
    main()
