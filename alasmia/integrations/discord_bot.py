"""
Alasmia Discord Bot

Discord integration for Alasmia AI companion.
"""

import os
from typing import Optional
from dotenv import load_dotenv

from alasmia.agent.brain import Brain
from alasmia.agent.memory import MemoryManager
from alasmia.agent.personality import PersonalityEngine

load_dotenv()


class DiscordBot:
    """Discord bot interface for Alasmia."""
    
    def __init__(
        self,
        model_loader,
        memory: MemoryManager,
        personality: PersonalityEngine
    ):
        """Initialize Discord bot."""
        self.memory = memory
        self.personality = personality
        self.brain = Brain(model_loader)
        
        self.bot_token = os.getenv("DISCORD_BOT_TOKEN")
        
        if not self.bot_token:
            raise ValueError("DISCORD_BOT_TOKEN not set in environment")
    
    async def start(self) -> None:
        """Start the Discord bot."""
        try:
            import discord
            from discord.ext import commands
        except ImportError:
            print("Error: discord.py not installed")
            print("Run: pip install discord.py")
            return
        
        intents = discord.Intents.default()
        intents.message_content = True
        
        bot = commands.Bot(command_prefix="!", intents=intents)
        
        @bot.event
        async def on_ready():
            print(f"✓ Discord bot logged in as {bot.user}")
        
        @bot.command(name="reset")
        async def reset(ctx):
            """Reset conversation history."""
            user_id = str(ctx.author.id)
            self.memory.clear_conversation(user_id)
            await ctx.send("Conversation reset! Let's start fresh. 💫")
        
        @bot.command(name="profile")
        async def profile(ctx):
            """Show user profile."""
            user_id = str(ctx.author.id)
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
            
            await ctx.send(response)
        
        @bot.event
        async def on_message(message):
            """Handle incoming messages."""
            # Ignore bot messages
            if message.author.bot:
                return
            
            user_id = str(message.author.id)
            user_message = message.content
            
            # Get or create user
            user_info = self.memory.get_user_info(user_id)
            if not user_info:
                self.memory.create_user(
                    user_id,
                    name=message.author.name
                )
            
            # Get history and generate response
            history = self.memory.get_conversation(user_id)
            system_prompt = self.personality.get_system_prompt(user_id)
            
            response = self.brain.think(
                message=user_message,
                history=history,
                system_prompt=system_prompt
            )
            
            # Save to memory
            self.memory.add_message(user_id, "user", user_message)
            self.memory.add_message(user_id, "assistant", response)
            
            # Send response
            await message.channel.send(response)
            
            # Check stage progression
            if self.personality.should_progress_stage(user_id):
                old_stage = self.personality.get_stage(user_id)
                new_stage = self.personality.progress_stage(user_id)
                transition_msg = self.personality.get_stage_transition_message(
                    old_stage, new_stage
                )
                if transition_msg:
                    await message.channel.send(transition_msg)
        
        print("Starting Discord bot...")
        bot.run(self.bot_token)
    
    def start_blocking(self) -> None:
        """Start bot (blocking)."""
        import asyncio
        asyncio.run(self.start())
