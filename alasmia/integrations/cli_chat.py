"""
Alasmia CLI Chat Interface - v0.1.0

Phase 1: Proactive AI + Deep Interest Memory
- Automatic language detection
- Interest tracking from conversations
- Proactive messages initiated by AI
- Follow-up on past topics
"""

from typing import Optional, List
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.prompt import Prompt
from rich import print as rprint
from datetime import datetime
import random

from alasmia.agent.brain import Brain
from alasmia.agent.memory import MemoryManager
from alasmia.agent.personality import PersonalityEngine
from alasmia.agent.mood_handler import MoodHandler
from alasmia.agent.emotion_tracker import EmotionTracker
from alasmia.agent.milestone import MilestoneTracker
from alasmia.agent.proactive_engine import ProactiveEngine
from alasmia.agent.interest_tracker import InterestTracker
from alasmia.core.state_manager import StateManager
from alasmia.core.scheduler import Scheduler, detect_language
from alasmia.core.enhanced_scheduler import EnhancedScheduler
from alasmia.core.analytics import Analytics
from alasmia.models.model_loader import ModelLoader

# Import multilingual greeting functions
from alasmia.agent.alas_prompts import get_alas_greeting, get_mia_greeting


class CLIChat:
    """
    CLI Chat with Phase 1 Features:
    - Proactive AI (initiates conversations)
    - Deep Interest Tracking
    - True Multilingual Support
    """
    
    FIRST_GREETING_TEMPLATES = {
        "English": "Hello! I'm {name}, your AI companion. What's your name?",
        "Mandarin Chinese": "你好！我是{name}，你的AI伴侣。你叫什么名字？",
        "Spanish": "¡Hola! Soy {name}, tu compañero de IA. ¿Cómo te llamas?",
        "Arabic": "مرحباً! أنا {name}، رفيقك الذكي. ما اسمك؟",
        "Hindi": "नमस्ते! मैं {name} हूं, तुम्हारा AI साथी। तुम्हारा नाम क्या है?",
        "Japanese": "はじめまして！私は{name}、あなたのAIコンパニオンです。名前は何ですか？",
        "Korean": "안녕하세요! 저는 {name}, 당신의 AI 친구입니다. 이름이 뭐예요?",
        "French": "Bonjour ! Je suis {name}, votre compagnon IA. Comment vous appelez-vous ?",
        "German": "Hallo! Ich bin {name}, dein KI-Begleiter. Wie heißt du?",
        "Portuguese": "Olá! Eu sou {name}, seu companheiro de IA. Qual é o seu nome?",
        "Russian": "Привет! Я {name}, твой ИИ-компаньон. Как тебя зовут?",
        "Vietnamese": "Xin chào! Tôi là {name}, người bạn AI của bạn. Bạn tên gì?",
        "Thai": "สวัสดีครับ/ค่ะ! ผม/ฉัน ชื่อ {name} เป็นเพื่อน AI ของคุณ คุณชื่ออะไร?",
        "Indonesian": "Halo! Saya {name}, teman AI kamu. Siapa namamu?",
        "Turkish": "Merhaba! Ben {name}, senin AI arkadaşın. Adın ne?",
        "Polish": "Cześć! Jestem {name}, twój towarzysz AI. Jak masz na imię?",
        "Dutch": "Hallo! Ik ben {name}, je AI-metgezel. Hoe heet je?",
        "Swedish": "Hej! Jag är {name}, din AI-kompis. Vad heter du?",
        "Italian": "Ciao! Sono {name}, il tuo compagno AI. Come ti chiami?",
    }
    
    NAME_CONFIRM_TEMPLATES = {
        "English": "Nice to meet you, {name}! 😊 How are you today?",
        "Mandarin Chinese": "很高兴认识你，{name}！😊 今天怎么样？",
        "Spanish": "¡Mucho gusto, {name}! 😊 ¿Cómo estás hoy?",
        "Arabic": "تشرفت بمعرفتك، {name}! 😊 كيف حالك اليوم؟",
        "Hindi": "आपसे मिलकर अच्छा लगा，{name}！😊 आज कैसे हो？",
        "Japanese": "はじめまして、{name}さん！😊 今日はどうですか？",
        "Korean": "만나서 반가워요, {name}님！😊 오늘 어때요?",
        "French": "Ravie de vous rencontrer, {name} ! 😊 Comment allez-vous aujourd'hui ?",
        "German": "Freut mich, dich kennenzulernen, {name}! 😊 Wie geht es dir heute?",
        "Portuguese": "Prazer em conhecê-lo, {name}! 😊 Como você está hoje?",
        "Russian": "Приятно познакомиться, {name}! 😊 Как ты сегодня?",
        "Vietnamese": "Rất vui được gặp bạn, {name}! 😊 Hôm nay bạn thế nào?",
        "Thai": "ยินดีที่ได้รู้จักครับ/คะ，{name}！😊 วันนี้เป็นอย่างไร?",
        "Indonesian": "Senang bertemu Anda, {name}! 😊 Bagaimana kabar Anda hari ini?",
        "Turkish": "Tanıştığığıma memnun oldum, {name}! 😊 Bugün nasılsın?",
        "Polish": "Miło mi cię poznać, {name}! 😊 Jak się masz dziś?",
        "Dutch": "Leuk je te ontmoeten, {name}! 😊 Hoe gaat het vandaag met je?",
        "Swedish": "Trevligt att träffas, {name}! 😊 Hur mår du idag?",
        "Italian": "Piacere di conoscerti, {name}! 😊 Come stai oggi?",
    }
    
    def __init__(self, model_loader: ModelLoader, user_profile: dict):
        """Initialize CLI chat with Phase 1 features."""
        self.console = Console()
        self.user_profile = user_profile
        self.user_id = "cli_user"
        
        # Get companion info
        self.companion_gender = user_profile.get("companion_gender", "female")
        self.companion_name = "Alas" if self.companion_gender == "male" else "Mia"
        
        # Initialize memory
        self.memory = MemoryManager()
        
        # Initialize personality engine
        self.personality = PersonalityEngine(self.memory)
        
        # Initialize brain
        self.brain = Brain(model_loader)
        
        # Initialize emotional intelligence systems
        self.mood_handler = MoodHandler()
        self.emotion_tracker = EmotionTracker(self.memory)
        self.milestone_tracker = MilestoneTracker()
        
        # PHASE 1: Initialize Proactive Engine
        self.proactive_engine = ProactiveEngine()
        
        # PHASE 1: Initialize Interest Tracker
        self.interest_tracker = InterestTracker()
        
        # Initialize state and time systems
        self.state = StateManager(self.user_id)
        self.scheduler = EnhancedScheduler(
            memory_manager=self.memory,
            proactive_engine=self.proactive_engine,
            interest_tracker=self.interest_tracker
        )
        self.analytics = Analytics(self.memory)
        
        # MULTILINGUAL: Track user's language
        self.user_language = None
        self.is_first_interaction = True
        self.name_asked = False
        self.user_name = None
        
        # Load existing user data if available
        self._load_user_data()
        
        # Register proactive check callback
        self.scheduler.add_send_callback(self._on_proactive_message)
    
    def _load_user_data(self):
        """Load user's existing data from memory."""
        info = self.memory.get_user_info(self.user_id)
        if info:
            self.user_language = info.get("language")
            self.user_name = info.get("name")
            self.name_asked = True if self.user_name else False
            self.is_first_interaction = False
    
    def _on_proactive_message(self, user_id: str, message: str, channel: str = "cli"):
        """Callback for proactive messages."""
        if user_id == self.user_id:
            self.console.print(f"\n[bold cyan]{self.companion_name}:[/bold cyan] {message}")
    
    def start(self):
        """Start the CLI chat session."""
        self._print_banner()
        
        # Check for proactive message
        proactive_msg = self.scheduler.check_and_process(self.user_id, force=False)
        if proactive_msg:
            self.console.print(f"\n[bold cyan]{self.companion_name}:[/bold cyan] {proactive_msg}")
        
        # Check for time-based greetings in user's language
        greeting = self.scheduler.check_and_send_greeting(self.user_language)
        if greeting:
            self.console.print(f"\n[bold magenta]{greeting}[/bold magenta]")
        
        # Check for weekly check-in
        if self.scheduler.should_weekly_checkin():
            checkin = self.scheduler.get_weekly_checkin_message(self.analytics, self.user_language)
            self.console.print(f"\n[bold cyan]{checkin}[/bold cyan]")
        
        # Check for monthly anniversary
        anniversary = self.scheduler.get_monthly_anniversary_message(self.user_profile, self.user_language)
        if anniversary:
            self.console.print(f"\n[bold magenta]{anniversary}[/bold magenta]")
        
        # MULTILINGUAL: Greeting in user's language
        self._print_multilingual_greeting()
        
        # Main chat loop
        self._chat_loop()
    
    def _print_banner(self):
        """Print welcome banner."""
        emoji = "💪" if self.companion_gender == "male" else "💕"
        
        banner = f"""
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║          {emoji}  ALASMIA - Your AI Life Partner           ║
║              (Powered by {self.companion_name})                   ║
║              🌐 TRUE MULTILINGUAL AI                          ║
║              ⚡ PHASE 1: Proactive + Interest Memory         ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
"""
        self.console.print(banner, style="bold magenta")
    
    def _print_multilingual_greeting(self):
        """Print greeting in user's preferred language."""
        time_of_day = self._get_time_of_day()
        
        if self.user_language:
            greeting = get_alas_greeting(time_of_day, self.user_language) if self.companion_gender == "male" else get_mia_greeting(time_of_day, self.user_language)
        else:
            greeting = get_alas_greeting(time_of_day, "English") if self.companion_gender == "male" else get_mia_greeting(time_of_day, "English")
        
        self.console.print(f"\n[bold cyan]{greeting}[/bold cyan]\n")
        
        if not self.name_asked:
            self._ask_name_in_user_language()
    
    def _ask_name_in_user_language(self):
        """Ask for user's name in their language."""
        lang = self.user_language or "English"
        
        template = self.FIRST_GREETING_TEMPLATES.get(lang, self.FIRST_GREETING_TEMPLATES["English"])
        message = template.format(name=self.companion_name)
        
        self.console.print(f"[bold magenta]{message}[/bold magenta]")
        self.name_asked = True
    
    def _confirm_name_in_language(self, name: str):
        """Confirm user's name in their language."""
        lang = self.user_language or "English"
        
        template = self.NAME_CONFIRM_TEMPLATES.get(lang, self.NAME_CONFIRM_TEMPLATES["English"])
        message = template.format(name=name)
        
        self.console.print(f"\n[bold magenta]{message}[/bold magenta]\n")
    
    def _get_time_of_day(self) -> str:
        """Get current time of day."""
        hour = datetime.now().hour
        if 7 <= hour < 12:
            return "morning"
        elif 12 <= hour < 18:
            return "afternoon"
        elif 18 <= hour < 22:
            return "evening"
        else:
            return "night"
    
    def _chat_loop(self):
        """Main chat loop with Phase 1 features."""
        self.console.print(
            "\n[dim]Commands: 'exit' to end | 'mood' for analysis | 'stats' for your stats | 'interests' to see tracked interests[/dim]\n"
        )
        
        while True:
            try:
                user_input = Prompt.ask("[yellow]You[/yellow]")
                
                # Handle special commands
                if user_input.lower() in ["exit", "quit", "bye"]:
                    self._handle_exit()
                    break
                
                if user_input.lower() == "mood":
                    self._show_mood_analysis()
                    continue
                
                if user_input.lower() == "stats":
                    self._show_user_stats()
                    continue
                
                if user_input.lower() == "interests":
                    self._show_interests()
                    continue
                
                if user_input.lower() == "change language":
                    self._handle_language_change()
                    continue
                
                if not user_input.strip():
                    continue
                
                # =====================================================
                # PHASE 1: Language Detection (First Message)
                # =====================================================
                if self.is_first_interaction:
                    detected_lang = detect_language(user_input)
                    self.user_language = detected_lang
                    self.state.set_language(detected_lang)
                    
                    if self.memory.get_user_info(self.user_id):
                        self.memory.update_user(self.user_id, {"language": detected_lang})
                    else:
                        self.memory.create_user(
                            self.user_id,
                            name=self.user_name or "Friend",
                            companion_gender=self.companion_gender,
                            language=detected_lang
                        )
                    
                    self.console.print(f"[dim]🌐 Language detected: {detected_lang}[/dim]")
                    self.is_first_interaction = False
                
                # =====================================================
                # PHASE 1: Interest Tracking (Every Message)
                # =====================================================
                detected_mood = self.mood_handler.detect_mood(user_input)
                self.interest_tracker.track_message(self.user_id, user_input, detected_mood)
                
                # =====================================================
                # PHASE 1: Add conversation pickups for follow-up
                # =====================================================
                # Check for topics user might want to continue later
                if any(keyword in user_input.lower() for keyword in ["tomorrow", "later", "next week", "soon", "update"]):
                    # Extract potential topic (simple approach)
                    words = user_input.split()
                    for i, word in enumerate(words):
                        if word.lower() in ["tomorrow", "later", "soon"]:
                            if i > 0:
                                topic = " ".join(words[max(0, i-2):i+2])
                                self.proactive_engine.add_conversation_pickup(self.user_id, topic)
                                break
                
                self.state.update_mood(detected_mood)
                self.analytics.record_mood(self.user_id, detected_mood)
                
                # Check if should interject based on mood
                if self.mood_handler.should_interject(detected_mood):
                    mood_response = self.personality.get_mood_response(self.user_id, detected_mood)
                    self.console.print(f"[italic magenta]{mood_response}[/italic magenta]\n")
                
                # Build system prompt WITH language instruction
                system_prompt = self.personality.get_system_prompt(self.user_id)
                
                # Add MULTILINGUAL instruction
                if self.user_language:
                    lang_instruction = f"""\nIMPORTANT - RESPOND IN USER'S LANGUAGE:
- The user speaks and prefers: {self.user_language}
- You MUST respond in {self.user_language} language
- ALL your responses must be in {self.user_language}
- Do NOT use English if user writes in another language
- Always match the user's language
"""
                    system_prompt += lang_instruction
                
                # PHASE 1: Add interest context to system prompt
                interest_context = self.interest_tracker.get_memory_context(self.user_id)
                if interest_context:
                    system_prompt += f"\n{interest_context}\n"
                
                # Add mood context
                context_mood = self.state.get("last_mood", "neutral")
                if context_mood != "neutral":
                    system_prompt += f"\nUser's current mood: {context_mood.upper()}\n"
                    system_prompt += "Adjust your response accordingly.\n"
                
                # Get conversation history
                history = self.memory.get_conversation(self.user_id, limit=30)
                
                # Generate response
                with self.console.status("[cyan]Thinking...[/cyan]"):
                    response = self.brain.think(
                        message=user_input,
                        history=history,
                        system_prompt=system_prompt,
                        context={"mood": detected_mood, "language": self.user_language}
                    )
                
                # Save to memory
                self.memory.add_message(self.user_id, "user", user_input, detected_mood)
                self.memory.add_message(self.user_id, "assistant", response)
                
                # Update message count
                self.memory.increment_message_count(self.user_id)
                
                # Update proactive engine streak
                self.proactive_engine.update_streak(self.user_id)
                
                # Check milestones
                self._check_milestones()
                
                # Check stage progression
                if self.personality.should_progress_stage(self.user_id):
                    old_stage = self.personality.get_stage(self.user_id)
                    new_stage = self.personality.progress_stage(self.user_id)
                    transition = self.personality.get_stage_transition_message(
                        self.user_id, old_stage, new_stage
                    )
                    if transition:
                        self.console.print(f"\n[bold magenta]{transition}[/bold magenta]\n")
                
                self._print_response(response)
            
            except KeyboardInterrupt:
                self._handle_exit()
                break
            except Exception as e:
                self.console.print(f"[red]Error: {e}[/red]")
    
    def _check_milestones(self):
        """Check and announce any new milestones."""
        info = self.memory.get_user_info(self.user_id)
        if info:
            milestones_achieved = self.analytics.get_milestone_achievements(self.user_id)
            for milestone in milestones_achieved:
                existing = self.memory.get_milestones(self.user_id)
                if milestone not in [m.get("milestone") for m in existing]:
                    self.console.print(f"\n[bold magenta]{milestone}[/bold magenta]\n")
                    self.memory.add_milestone(self.user_id, milestone)
    
    def _print_response(self, response: str):
        """Print AI response with formatting."""
        try:
            md = Markdown(response)
            self.console.print(Panel(md, title=f"[bold magenta]{self.companion_name}[/bold magenta]"))
        except:
            self.console.print(f"[bold magenta]{self.companion_name}:[/bold magenta] {response}")
    
    def _show_mood_analysis(self):
        """Show current mood analysis."""
        summary = self.mood_handler.get_emotional_summary()
        self.console.print("\n[bold]📊 Mood Analysis:[/bold]")
        self.console.print(f"  Current mood: {summary['current_mood']}")
        self.console.print(f"  Dominant mood: {summary['dominant_mood']}")
        self.console.print(f"  Special mode: {summary['special_mode'] or 'Normal'}")
        self.console.print(f"  History: {summary['history_length']} messages tracked\n")
    
    def _show_user_stats(self):
        """Show user statistics."""
        info = self.memory.get_user_info(self.user_id)
        if info:
            connection_score = self.analytics.calculate_connection_score(self.user_id)
            streak = self.proactive_engine.get_streak(self.user_id)
            
            self.console.print("\n[bold]📊 Your Stats:[/bold]")
            self.console.print(f"  Name: {info.get('name', 'Friend')}")
            self.console.print(f"  Companion: {self.companion_name} ({'Male' if self.companion_gender == 'male' else 'Female'} energy)")
            self.console.print(f"  Language: {info.get('language', 'English')}")
            self.console.print(f"  Relationship Stage: {info.get('relationship_stage', 'stranger').upper()}")
            self.console.print(f"  Messages: {info.get('message_count', 0)}")
            self.console.print(f"  Connection Score: {connection_score}%")
            self.console.print(f"  Conversation Streak: {streak} days")
            self.console.print(f"  Mood Trend: {self.analytics.get_mood_trend(self.user_id)}")
            
            # Show progress to next milestone
            progress = self.milestone_tracker.get_progress_to_milestone(info.get('message_count', 0))
            if not progress['attained']:
                self.console.print(f"\n  Next milestone: {progress['title']}")
                self.console.print(f"  Progress: {progress['progress']}% ({progress['message']})")
            
            milestones = self.memory.get_milestones(self.user_id)
            if milestones:
                self.console.print(f"  Achieved milestones: {len(milestones)}")
            
            self.console.print()
    
    def _show_interests(self):
        """PHASE 1: Show tracked interests."""
        interests = self.interest_tracker.get_interests(self.user_id, min_mentions=2)
        
        self.console.print("\n[bold]🎯 Your Tracked Interests:[/bold]")
        
        if not interests:
            self.console.print("  No interests tracked yet. Keep chatting! 😊")
        else:
            for category, items in interests.items():
                if items:
                    interest_list = ", ".join([f"{i['interest']} ({i['mentions']})" for i in items])
                    self.console.print(f"  {category.title()}: {interest_list}")
        
        self.console.print()
        
        # Show conversation starters based on interests
        starters = self.interest_tracker.get_conversation_starters(self.user_id, self.user_language or "English")
        if starters:
            self.console.print("[bold]💬 I can ask you about:[/bold]")
            for starter in starters[:3]:
                self.console.print(f"  • {starter}")
            self.console.print()
    
    def _handle_language_change(self):
        """Handle language change request."""
        self.console.print("\n[yellow]Enter your preferred language:[/yellow]")
        self.console.print("  (e.g., English, Mandarin Chinese, Spanish, Arabic, Hindi, Japanese, Korean, etc.)")
        
        choice = Prompt.ask("Language")
        
        new_language = choice.strip()
        self.user_language = new_language
        self.state.set_language(new_language)
        self.memory.update_user(self.user_id, {"language": new_language})
        
        confirm_msg = f"[green]✓ Language set to: {new_language}[/green]"
        self.console.print(confirm_msg)
        
        greeting = get_alas_greeting("casual", new_language) if self.companion_gender == "male" else get_mia_greeting("casual", new_language)
        self.console.print(f"[dim]Example: {greeting}[/dim]\n")
    
    def _handle_exit(self):
        """Handle exit from chat."""
        farewells = {
            "English": "Take care! I'll be here when you need me. 💕",
            "Mandarin Chinese": "保重！需要我的时候我会在这里。💕",
            "Spanish": "¡Cuídate! Estaré aquí cuando me necesites. 💕",
            "Arabic": "اعتن بنفسك! سأكون هنا عندما تحتاجني. 💕",
            "Hindi": "खयाल रखना! जब भी चाहो मैं यहां हूं। 💕",
            "Japanese": "気をつけて！必要할 때 여기 있을게요。💕",
            "Korean": "조심해! 필요하면 여기 있을게。💕",
            "French": "Prenez soin de vous ! Je serai là quand vous aurez besoin de moi. 💕",
            "German": "Pass auf dich auf! Ich bin da, wenn du mich brauchst. 💕",
            "Portuguese": "Cuide-se! Estarei aqui quando você precisar de mim. 💕",
        }
        
        farewell = farewells.get(self.user_language, farewells["English"])
        companion_farewell = "Take care, champion. I'm always here when you need me. 💪" if self.companion_gender == "male" else farewell
        
        self.console.print(f"\n[cyan]{companion_farewell}[/cyan]")
        self.console.print("[dim]Run 'python main.py' to chat again[/dim]")
