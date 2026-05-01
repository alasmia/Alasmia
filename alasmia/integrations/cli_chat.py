"""
Alasmia CLI Chat Interface

Terminal-based chat with complete Alas/Mia integration.
"""

from typing import Optional
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.prompt import Prompt
from rich import print as rprint
from datetime import datetime

from alasmia.agent.brain import Brain
from alasmia.agent.memory import MemoryManager
from alasmia.agent.personality import PersonalityEngine
from alasmia.agent.mood_handler import MoodHandler
from alasmia.agent.emotion_tracker import EmotionTracker
from alasmia.agent.milestone import MilestoneTracker
from alasmia.core.state_manager import StateManager
from alasmia.core.scheduler import Scheduler
from alasmia.core.analytics import Analytics
from alasmia.models.model_loader import ModelLoader


class CLIChat:
    """
    Command-line chat interface with full emotional intelligence.
    Integrates Alas/Mia companion system with mood tracking,
    time-based greetings, and milestone celebrations.
    """
    
    def __init__(self, model_loader: ModelLoader, user_profile: dict):
        """Initialize CLI chat with user profile."""
        self.console = Console()
        self.user_profile = user_profile
        self.user_id = "cli_user"
        
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
        
        # Initialize state and time systems
        self.state = StateManager(self.user_id)
        self.scheduler = Scheduler()
        self.analytics = Analytics(self.memory)
        
        # Track if first interaction
        self.is_first_interaction = True
        
        # Create user if needed
        if not self.memory.get_user_info(self.user_id):
            self.memory.create_user(
                self.user_id,
                name=user_profile.get("name", "Friend"),
                companion_gender=user_profile.get("companion_gender", "female"),
                language=user_profile.get("language", "english")
            )
    
    def start(self):
        """Start the CLI chat session."""
        self._print_banner()
        
        # Check for time-based greetings
        greeting = self.scheduler.check_and_send_greeting()
        if greeting:
            self.console.print(f"\n[bold magenta]{greeting}[/bold magenta]")
        
        # Check for weekly check-in
        if self.scheduler.should_weekly_checkin():
            checkin = self.scheduler.get_weekly_checkin_message(self.analytics)
            self.console.print(f"\n[bold cyan]{checkin}[/bold cyan]")
        
        # Check for monthly anniversary
        anniversary = self.scheduler.get_monthly_anniversary_message(self.user_profile)
        if anniversary:
            self.console.print(f"\n[bold magenta]{anniversary}[/bold magenta]")
        
        # Greeting based on companion type and returning status
        self._print_greeting()
        
        # Main chat loop
        self._chat_loop()
    
    def _print_banner(self):
        """Print welcome banner."""
        companion = self.user_profile.get("companion_gender", "female")
        companion_name = "ALAS" if companion == "male" else "MIA"
        emoji = "💪" if companion == "male" else "💕"
        
        banner = f"""
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║          {emoji}  ALASMIA - Your AI Companion              ║
║              (Powered by {companion_name})                       ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
"""
        self.console.print(banner, style="bold magenta")
    
    def _print_greeting(self):
        """Print appropriate greeting."""
        time_of_day = self._get_time_of_day()
        is_returning = not self.is_first_interaction
        
        greeting = self.personality.get_greeting(
            self.user_id, 
            time_of_day=time_of_day,
            is_returning=is_returning
        )
        
        if greeting:
            self.console.print(f"\n[bold cyan]{greeting}[/bold cyan]\n")
        
        self.is_first_interaction = False
    
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
        """Main chat loop with emotional intelligence."""
        self.console.print(
            "\n[dim]Type 'exit' to end, 'mood' to see mood analysis, 'stats' for your stats[/dim]\n"
        )
        
        while True:
            try:
                # Get user input
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
                
                if user_input.lower() == "change language":
                    self._handle_language_change()
                    continue
                
                if not user_input.strip():
                    continue
                
                # Detect mood
                detected_mood = self.mood_handler.detect_mood(user_input)
                self.state.update_mood(detected_mood)
                
                # Record mood for analytics
                self.analytics.record_mood(self.user_id, detected_mood)
                
                # Check if should interject based on mood
                if self.mood_handler.should_interject(detected_mood):
                    mood_response = self.personality.get_mood_response(self.user_id, detected_mood)
                    self.console.print(f"[italic magenta]{mood_response}[/italic magenta]\n")
                
                # Build system prompt
                system_prompt = self.personality.get_system_prompt(self.user_id)
                
                # Add context about mood
                context_mood = self.state.get("current_mood", "neutral")
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
                        context={"mood": detected_mood}
                    )
                
                # Save to memory
                self.memory.add_message(self.user_id, "user", user_input, detected_mood)
                self.memory.add_message(self.user_id, "assistant", response)
                
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
                
                # Print response
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
                # Check if already recorded
                existing = self.memory.get_milestones(self.user_id)
                if milestone not in [m.get("milestone") for m in existing]:
                    self.console.print(f"\n[bold magenta]{milestone}[/bold magenta]\n")
                    self.memory.add_milestone(self.user_id, milestone)
    
    def _print_response(self, response: str):
        """Print AI response with formatting."""
        try:
            md = Markdown(response)
            companion = self.user_profile.get("companion_gender", "female")
            name = "Alas" if companion == "male" else "Mia"
            self.console.print(Panel(md, title=f"[bold magenta]{name}[/bold magenta]"))
        except:
            companion = self.user_profile.get("companion_gender", "female")
            name = "Alas" if companion == "male" else "Mia"
            self.console.print(f"[bold magenta]{name}:[/bold magenta] {response}")
    
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
            companion = self.user_profile.get("companion_gender", "female")
            connection_score = self.analytics.calculate_connection_score(self.user_id)
            
            self.console.print("\n[bold]📊 Your Stats:[/bold]")
            self.console.print(f"  Name: {info.get('name', 'Friend')}")
            self.console.print(f"  Companion: {'Alas (Male)' if companion == 'male' else 'Mia (Female)'}")
            self.console.print(f"  Relationship Stage: {info.get('relationship_stage', 'stranger').upper()}")
            self.console.print(f"  Messages: {info.get('message_count', 0)}")
            self.console.print(f"  Connection Score: {connection_score}%")
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
    
    def _handle_language_change(self):
        """Handle language change request."""
        self.console.print("\n[yellow]Available languages:[/yellow]")
        self.console.print("  1. English")
        self.console.print("  2. Hindi")
        self.console.print("  3. Hinglish")
        
        choice = Prompt.ask("Enter choice (1-3)", default="1")
        lang_map = {"1": "english", "2": "hindi", "3": "hinglish"}
        language = lang_map.get(choice, "english")
        
        self.memory.update_user(self.user_id, {"language": language})
        self.console.print(f"[green]✓ Language set to: {language.title()}[/green]\n")
    
    def _handle_exit(self):
        """Handle exit from chat."""
        name = self.user_profile.get("name", "friend")
        companion = self.user_profile.get("companion_gender", "female")
        
        farewell = "Take care, champion. I'm always here when you need me. 💪" if companion == "male" else "Take care, lovely! I missed you already. Talk soon! 💕"
        
        self.console.print(f"\n[cyan]{farewell}[/cyan]")
        self.console.print("[dim]Run 'python main.py' to chat again[/dim]")
