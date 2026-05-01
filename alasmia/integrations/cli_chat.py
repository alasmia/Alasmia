"""
Alasmia CLI Chat Interface

Terminal-based chat interface for Alasmia.
"""

from typing import Optional
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich import print as rprint

from alasmia.agent.brain import Brain
from alasmia.agent.memory import MemoryManager
from alasmia.agent.personality import PersonalityEngine


class CLIChat:
    """Command-line chat interface for Alasmia."""
    
    def __init__(
        self,
        model_loader,
        memory: MemoryManager,
        personality: PersonalityEngine
    ):
        """Initialize CLI chat."""
        self.console = Console()
        self.memory = memory
        self.personality = personality
        self.brain = Brain(model_loader)
        
        self.current_user_id = "cli_user"
        self.is_first_interaction = True
    
    def start(self) -> None:
        """Start the CLI chat session."""
        self._print_banner()
        
        # Check if returning user
        user_info = self.memory.get_user_info(self.current_user_id)
        
        if not user_info:
            self.is_first_interaction = True
            self._handle_first_interaction()
        else:
            self.is_first_interaction = False
            self._print_greeting()
        
        # Main chat loop
        self._chat_loop()
    
    def _print_banner(self) -> None:
        """Print welcome banner."""
        banner = """
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║              🤍  ALASMIA - Your AI Companion                  ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
"""
        self.console.print(banner, style="bold magenta")
    
    def _handle_first_interaction(self) -> None:
        """Handle first interaction - introduce and learn name."""
        self.console.print(
            "
[bold]✨ Hi! I'm Alasmia, your AI companion.[/bold]",
            style="cyan"
        )
        
        # Ask for name
        name = Prompt.ask("\n[yellow]What's your name?[/yellow]")
        
        # Create user and save name
        self.memory.create_user(self.current_user_id, name=name)
        
        self.console.print(
            f"\n[green]Nice to meet you, {name}! 💕[/green]"
        )
        
        # Ask language preference
        self._ask_language_preference()
    
    def _ask_language_preference(self) -> None:
        """Ask user for their language preference."""
        self.console.print(
            "\n[yellow]Kaunsi language prefer karte ho?[/yellow]"
        )
        self.console.print("  1. Hindi")
        self.console.print("  2. English") 
        self.console.print("  3. Hinglish (mix of both)")
        
        choice = Prompt.ask("\n[cyan]Enter choice (1-3)[/cyan]", default="3")
        
        lang_map = {"1": "hindi", "2": "english", "3": "hinglish"}
        language = lang_map.get(choice, "hinglish")
        
        self.memory.update_user_language(self.current_user_id, language)
        self.console.print(f"[green]✓ Language set to: {language.title()}[/green]")
    
    def _print_greeting(self) -> None:
        """Print greeting for returning user."""
        greeting = self.personality.get_greeting(self.current_user_id)
        if greeting:
            self.console.print(f"\n[bold cyan]{greeting}[/bold cyan]")
    
    def _chat_loop(self) -> None:
        """Main chat loop."""
        self.console.print(
            "\n[dim]Type 'exit' or 'quit' to end conversation[/dim]\n"
        )
        
        while True:
            try:
                # Get user input
                user_input = Prompt.ask("[yellow]You[/yellow]")
                
                if user_input.lower() in ["exit", "quit", "bye"]:
                    self._handle_exit()
                    break
                
                if not user_input.strip():
                    continue
                
                # Get conversation history
                history = self.memory.get_conversation(self.current_user_id)
                
                # Get system prompt
                system_prompt = self.personality.get_system_prompt(
                    self.current_user_id
                )
                
                # Generate response
                with self.console.status("[cyan]Alasmia is thinking...[/cyan]"):
                    response = self.brain.think(
                        message=user_input,
                        history=history,
                        system_prompt=system_prompt
                    )
                
                # Save to memory
                self.memory.add_message(
                    self.current_user_id,
                    "user",
                    user_input
                )
                self.memory.add_message(
                    self.current_user_id,
                    "assistant",
                    response
                )
                
                # Print response
                self._print_response(response)
                
                # Check for stage progression
                if self.personality.should_progress_stage(self.current_user_id):
                    old_stage = self.personality.get_stage(self.current_user_id)
                    new_stage = self.personality.progress_stage(self.current_user_id)
                    message = self.personality.get_stage_transition_message(
                        old_stage, new_stage
                    )
                    if message:
                        self.console.print(
                            f"\n[bold magenta]{message}[/bold magenta]\n"
                        )
            
            except KeyboardInterrupt:
                self._handle_exit()
                break
            except Exception as e:
                self.console.print(f"[red]Error: {e}[/red]")
    
    def _print_response(self, response: str) -> None:
        """Print AI response with formatting."""
        # Try to render as markdown for nice formatting
        try:
            md = Markdown(response)
            self.console.print(Panel(md, title="[bold magenta]Alasmia[/bold magenta]"))
        except:
            self.console.print(f"[bold magenta]Alasmia:[/bold magenta] {response}")
    
    def _handle_exit(self) -> None:
        """Handle exit from chat."""
        user_info = self.memory.get_user_info(self.current_user_id)
        name = user_info.get("name", "friend") if user_info else "friend"
        
        self.console.print(
            f"\n[cyan]Take care, {name}! Talk to you soon! 💕[/cyan]"
        )
        self.console.print("[dim]Run 'python main.py' to chat again[/dim]")
