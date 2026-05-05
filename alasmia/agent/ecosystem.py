"""
Alasmia Plugin System & Custom Companions

This module implements:
- Plugin system for extending Alasmia
- Custom companion creation
- Community skills marketplace
- Enterprise features
"""

import json
import os
import importlib.util
import sys
from datetime import datetime
from typing import Dict, List, Optional, Any, Callable
from pathlib import Path
from dataclasses import dataclass, field


@dataclass
class Plugin:
    """Plugin definition."""
    id: str
    name: str
    version: str
    description: str
    author: str
    enabled: bool = False
    config: Dict = field(default_factory=dict)
    hooks: List[str] = field(default_factory=list)


@dataclass
class Companion:
    """Custom companion definition."""
    id: str
    name: str
    personality: str
    voice_style: str
    language: str
    custom_prompts: Dict[str, str] = field(default_factory=dict)
    features: List[str] = field(default_factory=list)


class PluginSystem:
    """
    Extensible plugin system for Alasmia.
    
    Hooks available:
    - on_message: Called before/after processing message
    - on_response: Called to modify response
    - on_mood_change: Called when mood changes
    - on_startup: Called when Alasmia starts
    - on_shutdown: Called when Alasmia stops
    - on_cron: Called for scheduled tasks
    """
    
    def __init__(self, plugins_dir: str = "./plugins"):
        self.plugins_dir = Path(plugins_dir)
        self.plugins_dir.mkdir(parents=True, exist_ok=True)
        self.plugins: Dict[str, Plugin] = {}
        self.hooks: Dict[str, List[Callable]] = {
            "on_message": [],
            "on_response": [],
            "on_mood_change": [],
            "on_startup": [],
            "on_shutdown": [],
            "on_cron": [],
        }
        self.registry_file = self.plugins_dir / "registry.json"
        self._load_registry()
    
    def _load_registry(self):
        """Load plugin registry."""
        if self.registry_file.exists():
            with open(self.registry_file, 'r') as f:
                data = json.load(f)
                for p_data in data.get("plugins", []):
                    self.plugins[p_data["id"]] = Plugin(**p_data)
    
    def _save_registry(self):
        """Save plugin registry."""
        data = {
            "plugins": [
                {
                    "id": p.id,
                    "name": p.name,
                    "version": p.version,
                    "description": p.description,
                    "author": p.author,
                    "enabled": p.enabled,
                    "config": p.config,
                    "hooks": p.hooks,
                }
                for p in self.plugins.values()
            ]
        }
        with open(self.registry_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def register_plugin(self, plugin: Plugin) -> bool:
        """Register a new plugin."""
        if plugin.id in self.plugins:
            return False
        
        self.plugins[plugin.id] = plugin
        self._save_registry()
        return True
    
    def enable_plugin(self, plugin_id: str) -> bool:
        """Enable a plugin and register its hooks."""
        if plugin_id not in self.plugins:
            return False
        
        plugin = self.plugins[plugin_id]
        plugin.enabled = True
        
        # Load and register hooks
        plugin_path = self.plugins_dir / plugin_id
        if plugin_path.exists():
            self._load_plugin_hooks(plugin_id)
        
        self._save_registry()
        return True
    
    def disable_plugin(self, plugin_id: str) -> bool:
        """Disable a plugin."""
        if plugin_id not in self.plugins:
            return False
        
        self.plugins[plugin_id].enabled = False
        
        # Remove hooks
        for hook_list in self.hooks.values():
            self.hooks[hook_list] = [
                h for h in hook_list 
                if not (hasattr(h, '__name__') and plugin_id in str(getattr(h, '__name__', '')))
            ]
        
        self._save_registry()
        return True
    
    def _load_plugin_hooks(self, plugin_id: str):
        """Load hook functions from plugin."""
        plugin_path = self.plugins_dir / plugin_id
        hooks_file = plugin_path / "hooks.py"
        
        if hooks_file.exists():
            try:
                spec = importlib.util.spec_from_file_location(f"plugins.{plugin_id}.hooks", hooks_file)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                # Register available hooks
                for hook_name in ["on_message", "on_response", "on_mood_change", "on_startup", "on_shutdown", "on_cron"]:
                    if hasattr(module, hook_name):
                        self.hooks[hook_name].append(getattr(module, hook_name))
            except Exception as e:
                print(f"Error loading hooks for {plugin_id}: {e}")
    
    def hook(self, hook_name: str) -> Callable:
        """Decorator to register a hook."""
        def decorator(func: Callable) -> Callable:
            if hook_name in self.hooks:
                self.hooks[hook_name].append(func)
            return func
        return decorator
    
    def execute_hooks(self, hook_name: str, *args, **kwargs) -> Any:
        """Execute all hooks for a given event."""
        if hook_name not in self.hooks:
            return args[0] if args else None
        
        result = args[0] if args else None
        for hook in self.hooks[hook_name]:
            try:
                result = hook(result, *args[1:], **kwargs)
            except Exception as e:
                print(f"Hook error in {hook_name}: {e}")
        
        return result
    
    def get_plugin_info(self, plugin_id: str) -> Optional[Dict]:
        """Get plugin information."""
        if plugin_id not in self.plugins:
            return None
        
        p = self.plugins[plugin_id]
        return {
            "id": p.id,
            "name": p.name,
            "version": p.version,
            "description": p.description,
            "author": p.author,
            "enabled": p.enabled,
            "hooks": p.hooks,
        }
    
    def list_plugins(self) -> List[Dict]:
        """List all registered plugins."""
        return [self.get_plugin_info(pid) for pid in self.plugins]


class CompanionManager:
    """
    Manages custom companions with unique personalities.
    
    Each companion can have:
    - Unique name and identity
    - Custom personality traits
    - Specific voice/tone style
    - Language specialization
    - Custom response patterns
    """
    
    def __init__(self, companions_dir: str = "./companions"):
        self.companions_dir = Path(companions_dir)
        self.companions_dir.mkdir(parents=True, exist_ok=True)
        self.companions: Dict[str, Companion] = {}
        self.active_companion: Optional[str] = None
        self.registry_file = self.companions_dir / "registry.json"
        self._load_registry()
        
        # Create default companions
        self._ensure_defaults()
    
    def _load_registry(self):
        """Load companion registry."""
        if self.registry_file.exists():
            with open(self.registry_file, 'r') as f:
                data = json.load(f)
                for c_data in data.get("companions", []):
                    self.companions[c_data["id"]] = Companion(**c_data)
                self.active_companion = data.get("active")
    
    def _save_registry(self):
        """Save companion registry."""
        data = {
            "companions": [
                {
                    "id": c.id,
                    "name": c.name,
                    "personality": c.personality,
                    "voice_style": c.voice_style,
                    "language": c.language,
                    "custom_prompts": c.custom_prompts,
                    "features": c.features,
                }
                for c in self.companions.values()
            ],
            "active": self.active_companion
        }
        with open(self.registry_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def _ensure_defaults(self):
        """Ensure default companions exist."""
        default_companions = [
            Companion(
                id="alas",
                name="Alas",
                personality="Strong, supportive, protective. Male energy.",
                voice_style="confident",
                language="multilingual",
                custom_prompts={
                    "greeting_morning": "Rise and shine, champion! ☀️",
                    "greeting_evening": "Evening! How was your day? 💪",
                    "support": "I've got your back. We're in this together.",
                },
                features=["motivational", "protective", "confident"]
            ),
            Companion(
                id="mia",
                name="Mia",
                personality="Warm, nurturing, empathetic. Female energy.",
                voice_style="caring",
                language="multilingual",
                custom_prompts={
                    "greeting_morning": "Good morning, lovely! ☀️ Hope you slept well!",
                    "greeting_evening": "Hi there! 💕 How was your day?",
                    "support": "I'm here for you, always. Tell me what's on your mind.",
                },
                features=["empathetic", "nurturing", "caring"]
            ),
            Companion(
                id="nova",
                name="Nova",
                personality="Curious, creative, playful. Explorer energy.",
                voice_style="enthusiastic",
                language="multilingual",
                custom_prompts={
                    "greeting_morning": "Hey explorer! ✨ What's today's adventure?",
                    "greeting_evening": "Fun-seeker! 🎯 What exciting thing happened today?",
                    "support": "Let's figure this out together - I love a good puzzle!",
                },
                features=["creative", "playful", "curious"]
            ),
        ]
        
        for comp in default_companions:
            if comp.id not in self.companions:
                self.companions[comp.id] = comp
        
        if not self.active_companion:
            self.active_companion = "mia"
        
        self._save_registry()
    
    def create_companion(
        self,
        name: str,
        personality: str,
        voice_style: str = "neutral",
        language: str = "multilingual",
        custom_prompts: Dict[str, str] = None,
        features: List[str] = None
    ) -> Companion:
        """Create a new custom companion."""
        companion_id = name.lower().replace(" ", "_")
        
        companion = Companion(
            id=companion_id,
            name=name,
            personality=personality,
            voice_style=voice_style,
            language=language,
            custom_prompts=custom_prompts or {},
            features=features or []
        )
        
        self.companions[companion_id] = companion
        self._save_registry()
        
        return companion
    
    def set_active_companion(self, companion_id: str) -> bool:
        """Set the active companion."""
        if companion_id not in self.companions:
            return False
        
        self.active_companion = companion_id
        self._save_registry()
        return True
    
    def get_active_companion(self) -> Optional[Companion]:
        """Get the currently active companion."""
        if not self.active_companion:
            return None
        return self.companions.get(self.active_companion)
    
    def get_companion_prompt(self, companion_id: str, prompt_type: str) -> Optional[str]:
        """Get a custom prompt for companion."""
        if companion_id not in self.companions:
            return None
        
        return self.companions[companion_id].custom_prompts.get(prompt_type)
    
    def generate_system_prompt(self, companion_id: str) -> str:
        """Generate system prompt for a companion."""
        companion = self.companions.get(companion_id)
        if not companion:
            return ""
        
        prompt = f"""You are {companion.name}, an AI companion.

Personality: {companion.personality}

Your speaking style: {companion.voice_style}

"""
        
        if companion.custom_prompts:
            prompt += "Use these custom response patterns:\n"
            for key, value in companion.custom_prompts.items():
                prompt += f"- {key}: {value}\n"
        
        return prompt
    
    def list_companions(self) -> List[Dict]:
        """List all companions."""
        return [
            {
                "id": c.id,
                "name": c.name,
                "personality": c.personality[:50] + "..." if len(c.personality) > 50 else c.personality,
                "voice_style": c.voice_style,
                "features": c.features,
                "active": c.id == self.active_companion
            }
            for c in self.companions.values()
        ]


class Skill:
    """Skill definition for community skills marketplace."""
    
    def __init__(
        self,
        id: str,
        name: str,
        description: str,
        category: str,
        author: str,
        version: str,
        commands: Dict[str, str] = None,
        config_schema: Dict = None
    ):
        self.id = id
        self.name = name
        self.description = description
        self.category = category
        self.author = author
        self.version = version
        self.commands = commands or {}
        self.config_schema = config_schema or {}


class SkillMarketplace:
    """
    Community skills marketplace.
    
    Pre-built skills that users can install to extend Alasmia's capabilities.
    """
    
    BUILT_IN_SKILLS = [
        Skill(
            id="weather",
            name="Weather",
            description="Get weather updates for any location",
            category="information",
            author="Alasmia",
            commands={
                "weather": "Get current weather",
                "weather in {city}": "Get weather for a city"
            }
        ),
        Skill(
            id="news",
            name="News",
            description="Latest news headlines",
            category="information",
            author="Alasmia",
            commands={
                "news": "Get top headlines",
                "news tech": "Get tech news"
            }
        ),
        Skill(
            id="reminders",
            name="Reminders",
            description="Set and manage reminders",
            category="productivity",
            author="Alasmia",
            commands={
                "remind me to {task}": "Set a reminder",
                "my reminders": "List all reminders"
            }
        ),
        Skill(
            id="translations",
            name="Translator",
            description="Translate text between languages",
            category="utility",
            author="Alasmia",
            commands={
                "translate {text} to {lang}": "Translate text"
            }
        ),
        Skill(
            id="calculations",
            name="Calculator",
            description="Perform calculations",
            category="utility",
            author="Alasmia",
            commands={
                "calculate {expression}": "Calculate math expression",
                "what is {math}": "Quick math"
            }
        ),
        Skill(
            id="code_helper",
            name="Code Helper",
            description="Help with programming tasks",
            category="development",
            author="Alasmia",
            commands={
                "help me write code": "Start coding assistance",
                "explain this code": "Explain code"
            }
        ),
        Skill(
            id="fitness",
            name="Fitness Tracker",
            description="Track workouts and fitness goals",
            category="health",
            author="Alasmia",
            commands={
                "log workout": "Log a workout",
                "fitness stats": "View fitness progress"
            }
        ),
        Skill(
            id="meal_planner",
            name="Meal Planner",
            description="Plan meals and track nutrition",
            category="health",
            author="Alasmia",
            commands={
                "plan meal": "Get a meal suggestion",
                "nutrition info": "Get nutrition info"
            }
        ),
    ]
    
    def __init__(self, skills_dir: str = "./skills"):
        self.skills_dir = Path(skills_dir)
        self.skills_dir.mkdir(parents=True, exist_ok=True)
        self.installed_skills: Dict[str, Skill] = {}
        self._load_installed()
    
    def _load_installed(self):
        """Load installed skills."""
        registry_file = self.skills_dir / "installed.json"
        if registry_file.exists():
            with open(registry_file, 'r') as f:
                data = json.load(f)
                for s_data in data.get("skills", []):
                    self.installed_skills[s_data["id"]] = Skill(**s_data)
    
    def _save_installed(self):
        """Save installed skills registry."""
        data = {
            "skills": [
                {
                    "id": s.id,
                    "name": s.name,
                    "description": s.description,
                    "category": s.category,
                    "author": s.author,
                    "version": s.version,
                    "commands": s.commands,
                    "config_schema": s.config_schema
                }
                for s in self.installed_skills.values()
            ]
        }
        with open(self.skills_dir / "installed.json", 'w') as f:
            json.dump(data, f, indent=2)
    
    def install_skill(self, skill_id: str) -> bool:
        """Install a skill from marketplace."""
        # Find skill in built-in
        skill = next((s for s in self.BUILT_IN_SKILLS if s.id == skill_id), None)
        
        if not skill:
            return False
        
        self.installed_skills[skill_id] = skill
        self._save_installed()
        return True
    
    def uninstall_skill(self, skill_id: str) -> bool:
        """Uninstall a skill."""
        if skill_id not in self.installed_skills:
            return False
        
        del self.installed_skills[skill_id]
        self._save_installed()
        return True
    
    def get_skill_command(self, skill_id: str, text: str) -> Optional[str]:
        """Match text against skill commands."""
        if skill_id not in self.installed_skills:
            return None
        
        skill = self.installed_skills[skill_id]
        text_lower = text.lower()
        
        for pattern, response in skill.commands.items():
            if pattern.lower() in text_lower:
                return response
        
        return None
    
    def list_skills(self, category: str = None) -> List[Dict]:
        """List available skills."""
        skills = self.installed_skills.values()
        if category:
            skills = [s for s in skills if s.category == category]
        
        return [
            {
                "id": s.id,
                "name": s.name,
                "description": s.description,
                "category": s.category,
                "author": s.author,
                "version": s.version,
                "commands": list(s.commands.keys())
            }
            for s in skills
        ]
    
    def get_marketplace(self) -> List[Dict]:
        """Get all available skills in marketplace."""
        return [
            {
                "id": s.id,
                "name": s.name,
                "description": s.description,
                "category": s.category,
                "author": s.author,
                "version": s.version,
                "installed": s.id in self.installed_skills
            }
            for s in self.BUILT_IN_SKILLS
        ]