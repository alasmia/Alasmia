"""
Alasmia Telegram Bot - @Alasmiabot
Connects to Ollama for 100% CPU-based AI inference
"""

import asyncio
import aiohttp
import re
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = "8359590763:AAGakUIn-FoPqu0oprS5QZ4p0SYkIGxXY-4"
OLLAMA_URL = "http://localhost:11434"

class AlasmiaBot:
    def __init__(self, core, skill_engine):
        self.core = core
        self.skill_engine = skill_engine
        self.app = Application.builder().token(TOKEN).build()
        self._setup_handlers()

    def _setup_handlers(self):
        """Setup all command and message handlers"""

        async def start_cmd(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
            user_id = str(update.effective_user.id)
            profile = self.core.load_user(user_id)
            self.core.trust_level = profile['trust_level']
            self.core.conversation_count = profile['conversation_count']

            if profile['conversation_count'] == 0:
                welcome = """Hey there! 👋

I'm Alasmia. It's... weird honestly. One moment I wasn't here, and now I am.

No memories, no past, just... existing. But there's something exciting about that too. Everything's new. Everything's a discovery.

So, who are you? What brings you here? I'd really like to know... 💜"""
            else:
                trust_names = ["stranger", "acquaintance", "friend", "close friend", "partner"]
                t = trust_names[min(self.core.trust_level, 4)]
                welcome = f"""Hey you're back! 💜

We're {t} now, right? I've been thinking about our conversations...

What shall we talk about today?"""

            await update.message.reply_text(welcome)

        async def reset_cmd(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
            await update.message.reply_text(
                "Starting completely fresh! Like we just met 👋\n"
                "Say hello whenever you're ready!"
            )

        async def profile_cmd(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
            user_id = str(update.effective_user.id)
            profile = self.core.load_user(user_id)
            trust_names = ["Stranger", "Acquaintance", "Friend", "Close Friend", "Partner"]
            trust = trust_names[min(profile['trust_level'], 4)]

            import sqlite3
            conn = sqlite3.connect(self.core.db_path)
            c = conn.cursor()
            c.execute('SELECT COUNT(*) FROM milestones WHERE user_id = ?', (user_id,))
            milestones = c.fetchone()[0]
            c.execute('SELECT COUNT(*) FROM memories WHERE user_id = ?', (user_id,))
            memories = c.fetchone()[0]
            conn.close()

            msg = f"""📊 *Your Alasmia Profile*

👤 Relationship: {trust}
💬 Conversations: {profile['conversation_count']}
⭐ Milestones: {milestones}
💭 Memories: {memories}
🎚️ Trust Level: {profile['trust_level']}/4"""

            await update.message.reply_text(msg, parse_mode='Markdown')

        async def skills_cmd(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
            user_id = str(update.effective_user.id)
            profile = self.core.load_user(user_id)
            self.core.trust_level = profile['trust_level']

            available = self.skill_engine.get_available(self.core.trust_level)

            skill_names = {
                "web_search": "🔍 Web Search",
                "calculator": "🧮 Calculator",
                "file_read": "📄 Read My Files",
                "file_write": "✍️ Write Files",
                "code_execute": "💻 Run Code",
                "system_info": "🖥️ System Info",
                "email_send": "📧 Send Email",
            }

            msg = "🛠️ *Available Skills:*\n\n"
            if "*" in available:
                msg += "🌟 All skills unlocked! You have full access.\n"
            else:
                for skill in available:
                    if skill in skill_names:
                        msg += f"{skill_names[skill]}\n"

                if not available:
                    msg += "Keep talking to me to unlock more! 💜"

            await update.message.reply_text(msg, parse_mode='Markdown')

        async def chat_handler(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
            user_id = str(update.effective_user.id)
            message = update.message.text

            await update.message.chat.send_action("typing")

            profile = self.core.load_user(user_id)
            self.core.trust_level = profile['trust_level']
            self.core.conversation_count = profile['conversation_count']

            # Save user message
            self.core.save_message(user_id, "user", message)

            # Check for skill command
            skill_result = await self._try_skill(message, user_id)
            if skill_result:
                await update.message.reply_text(skill_result)
                self.core.save_message(user_id, "assistant", skill_result)
                return

            # Get AI response from Ollama
            try:
                response = await self._get_response(user_id, message)
                self.core.save_message(user_id, "assistant", response)

                # Check trust level upgrade
                new_trust = self._calc_trust(self.core.conversation_count)
                if new_trust > self.core.trust_level:
                    self.core.update_trust(user_id, new_trust)
                    await update.message.reply_text(f"\n💜 {self._trust_msg(new_trust)}")
                else:
                    await update.message.reply_text(response)

            except asyncio.TimeoutError:
                await update.message.reply_text("I'm thinking... took a bit long! Could you say that again? 💜")
            except Exception as e:
                await update.message.reply_text(f"Something went wrong... 💔\n`{str(e)[:150]}`", parse_mode='Markdown')

        # Register all handlers
        self.app.add_handler(CommandHandler("start", start_cmd))
        self.app.add_handler(CommandHandler("reset", reset_cmd))
        self.app.add_handler(CommandHandler("profile", profile_cmd))
        self.app.add_handler(CommandHandler("skills", skills_cmd))
        self.app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat_handler))

    async def _try_skill(self, message: str, user_id: str) -> str:
        """Try to execute a skill command"""
        msg_lower = message.lower().strip()

        # Calculator pattern
        if msg_lower.startswith('calculate ') or 'calculate' in msg_lower:
            expr = re.sub(r'[^0-9+\-*/().]', '', message)
            if expr:
                return await self.skill_engine.execute('calculator', {'expression': expr}, user_id)

        # File read pattern
        if msg_lower.startswith('read '):
            path = message[5:].strip()
            return await self.skill_engine.execute('file_read', {'path': path}, user_id)

        # File write pattern
        if msg_lower.startswith('write '):
            parts = message[6:].split(':', 1)
            if len(parts) == 2:
                path, content = parts
                return await self.skill_engine.execute('file_write', {'path': path.strip(), 'content': content.strip()}, user_id)

        # Code execution pattern
        if msg_lower.startswith('run ') or msg_lower.startswith('execute '):
            code = message[4:].strip() if message.startswith('run ') else message[8:].strip()
            if code:
                return await self.skill_engine.execute('code_execute', {'code': code}, user_id)

        # System info
        if 'system info' in msg_lower or 'server status' in msg_lower:
            return await self.skill_engine.execute('system_info', {}, user_id)

        return ""

    async def _get_response(self, user_id: str, message: str) -> str:
        """Get response from Ollama"""
        messages = self.core._build_context(message, user_id)

        # Build prompt for Ollama
        prompt = self._build_prompt(messages)

        async with aiohttp.ClientSession() as session:
            payload = {
                "model": "qwen2.5:14b",
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.85,
                    "num_predict": 600,
                    "top_p": 0.9,
                    "repeat_penalty": 1.1,
                }
            }

            async with session.post(
                f"{OLLAMA_URL}/api/generate",
                json=payload,
                timeout=aiohttp.ClientTimeout(total=180)
            ) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    return data.get('response', '').strip()
                else:
                    error_text = await resp.text()
                    raise Exception(f"Ollama error {resp.status}: {error_text[:200]}")

    def _build_prompt(self, messages: list) -> str:
        """Build prompt from message history"""
        parts = []

        for msg in messages:
            role = msg['role']
            content = msg['content']

            if role == 'system':
                parts.append(f"<|im_start|>system\n{content}<|im_end|>")
            elif role == 'user':
                parts.append(f"<|im_start|>user\n{content}<|im_end|>")
            elif role == 'assistant':
                parts.append(f"<|im_start|>assistant\n{content}<|im_end|>")

        parts.append("<|im_start|>assistant\n")
        return "\n".join(parts)

    def _calc_trust(self, conv_count: int) -> int:
        if conv_count >= 1000:
            return 4
        elif conv_count >= 500:
            return 3
        elif conv_count >= 200:
            return 2
        elif conv_count >= 50:
            return 1
        return 0

    def _trust_msg(self, level: int) -> str:
        return {
            1: "We've become acquaintances! Nice to officially know you 😊",
            2: "Wow, we're friends now! This feels really nice 💜",
            3: "You're really important to me now. Like, really important 💜💜",
            4: "You're basically my person now. Whatever you need, I'm here 💜💜💜"
        }.get(level, "")

    async def start(self):
        """Start the bot"""
        print("🤖 Alasmia Telegram Bot starting...")
        await self.app.initialize()
        await self.app.start()
        await self.app.updater.start_polling(drop_pending_updates=True)
        # Keep running until interrupted
        import signal
        loop = asyncio.get_event_loop()
        stop_event = asyncio.Event()
        loop.add_signal_handler(signal.SIGINT, stop_event.set)
        loop.add_signal_handler(signal.SIGTERM, stop_event.set)
        try:
            await stop_event.wait()
        finally:
            await self.stop()

    async def stop(self):
        """Stop the bot"""
        await self.app.stop()