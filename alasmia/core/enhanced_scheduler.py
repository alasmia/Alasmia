"""
Alasmia Enhanced Scheduler - Combines All Time-Based Features

latest+: Includes:
- Proactive AI messages
- Interest tracking
- Multilingual greetings
- Daily rhythm system
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Callable
from pathlib import Path
import time
import threading


class EnhancedScheduler:
    """
    Enhanced scheduler that combines:
    - Time-based greetings
    - Proactive AI messages
    - Interest-based follow-ups
    - Daily rhythm
    """
    
    # Time slots for proactive messages
    PROACTIVE_SLOTS = {
        "morning": {"hours": list(range(7, 10)), "priority": 1},
        "mid_morning": {"hours": [10, 11], "priority": 0},
        "afternoon": {"hours": list(range(12, 15)), "priority": 0},
        "evening": {"hours": list(range(18, 21)), "priority": 1},
        "night": {"hours": list(range(21, 24)), "priority": 0},
    }
    
    def __init__(self, memory_manager=None, proactive_engine=None, 
                 interest_tracker=None, data_dir: str = "./data"):
        """Initialize enhanced scheduler."""
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        # Dependencies
        self.memory = memory_manager
        self.proactive = proactive_engine
        self.interest = interest_tracker
        
        # State
        self.last_check_file = self.data_dir / "scheduler_state.json"
        self.state = self._load_state()
        
        # Callbacks for sending messages
        self.send_callbacks: List[Callable] = []
        
        # Running state
        self._running = False
        self._thread = None
    
    def _load_state(self) -> Dict:
        """Load scheduler state."""
        if self.last_check_file.exists():
            with open(self.last_check_file, 'r') as f:
                return json.load(f)
        return {
            "last_proactive_check": {},
            "greeting_sent_today": {},
            "weekly_checkin_sent": {},
        }
    
    def _save_state(self):
        """Save scheduler state."""
        with open(self.last_check_file, 'w') as f:
            json.dump(self.state, f, indent=2)
    
    def add_send_callback(self, callback: Callable):
        """Add a callback for sending messages."""
        self.send_callbacks.append(callback)
    
    def _send_to_user(self, user_id: str, message: str, channel: str = "auto"):
        """Send message via registered callbacks."""
        for callback in self.send_callbacks:
            try:
                callback(user_id, message, channel)
            except Exception as e:
                print(f"Error in send callback: {e}")
    
    def check_and_process(self, user_id: str, force: bool = False) -> Optional[str]:
        """
        Main check function - call this periodically.
        
        Returns proactive message if one should be sent, None otherwise.
        """
        now = datetime.now()
        today = now.strftime("%Y-%m-%d")
        current_hour = now.hour
        
        # Initialize user state
        if user_id not in self.state["last_proactive_check"]:
            self.state["last_proactive_check"][user_id] = {}
        
        user_proactive = self.state["last_proactive_check"].setdefault(user_id, {})
        
        # Check if we should send proactive message
        should_send = False
        slot_name = None
        
        for slot, config in self.PROACTIVE_SLOTS.items():
            if current_hour in config["hours"]:
                today_key = f"{slot}_{today}"
                if today_key not in user_proactive.get("slots_used", []):
                    # Check if we've already done higher priority today
                    if config["priority"] > 0:
                        should_send = True
                        slot_name = slot
                    elif force:
                        should_send = True
                        slot_name = slot
                    break
        
        if not should_send:
            return None
        
        # Get user info for context
        user_info = None
        if self.memory:
            user_info = self.memory.get_user_info(user_id)
        
        user_name = user_info.get("name") if user_info else ""
        companion = user_info.get("companion_gender", "female")
        language = user_info.get("language", "English")
        
        companion_name = "Alas" if companion == "male" else "Mia"
        
        # Generate proactive message
        if self.proactive:
            context = {
                "user_name": user_name,
                "companion": companion_name,
                "language": language,
            }
            
            message = self.proactive.get_proactive_message(
                user_id, companion_name, language, context
            )
        else:
            # Fallback simple messages
            message = self._get_simple_proactive(current_hour, companion_name, language, user_name)
        
        if message:
            # Mark slot as used
            if "slots_used" not in user_proactive:
                user_proactive["slots_used"] = []
            
            today_key = f"{slot_name}_{today}"
            user_proactive["slots_used"].append(today_key)
            
            # Keep only today's slots
            user_proactive["slots_used"] = [s for s in user_proactive["slots_used"] if today in s]
            
            self.state["last_proactive_check"][user_id] = user_proactive
            self._save_state()
            
            return message
        
        return None
    
    def _get_simple_proactive(self, hour: int, companion: str, language: str, user_name: str) -> str:
        """Get simple proactive message when proactive engine not available."""
        name_suffix = f", {user_name}" if user_name else ""
        
        if 7 <= hour < 10:
            if companion == "Mia":
                return f"Good morning{name_suffix}! ☀️ Hope you slept well! How are you feeling today?"
            else:
                return f"Rise and shine{name_suffix}! ☀️ Hope you slept well, champion!"
        elif 12 <= hour < 14:
            if companion == "Mia":
                return f"Hi{name_suffix}! 💕 How's your day going? Remember to take breaks!"
            else:
                return f"Hey{name_suffix}! 👋 How's your day going, soldier?"
        elif 18 <= hour < 21:
            if companion == "Mia":
                return f"Good evening{name_suffix}! 💫 How was your day? You must be tired!"
            else:
                return f"Evening{name_suffix}! 💪 How was your day? Got plans tonight?"
        elif 21 <= hour < 24:
            if companion == "Mia":
                return f"Hi{name_suffix}! 🌙 It's getting late. Time to wind down, lovely!"
            else:
                return f"Hey{name_suffix}! 🌙 Late night, champion. Don't stay up too late!"
        
        return None
    
    def get_interest_based_followup(self, user_id: str, companion: str, language: str) -> Optional[str]:
        """Get a follow-up message based on user's interests."""
        if not self.interest:
            return None
        
        starters = self.interest.get_conversation_starters(user_id, language)
        
        if starters:
            # Pick one randomly
            import random
            return random.choice(starters)
        
        return None
    
    def check_weekly_checkin(self, user_id: str) -> bool:
        """Check if weekly check-in should be sent (Sunday)."""
        now = datetime.now()
        
        if now.weekday() != 6:  # Sunday
            return False
        
        today = now.strftime("%Y-%m-%d")
        
        if user_id not in self.state["weekly_checkin_sent"]:
            self.state["weekly_checkin_sent"][user_id] = None
        
        if self.state["weekly_checkin_sent"].get(user_id) == today:
            return False
        
        # Mark as sent
        self.state["weekly_checkin_sent"][user_id] = today
        self._save_state()
        return True
    
    def start_background_scheduler(self, check_interval: int = 3600):
        """
        Start background scheduler thread.
        
        Args:
            check_interval: Seconds between checks (default 1 hour)
        """
        if self._running:
            return
        
        self._running = True
        
        def run_scheduler():
            while self._running:
                try:
                    # Check proactive messages for active users
                    if self.memory:
                        # Get all active users
                        # This would iterate through known users
                        pass
                except Exception as e:
                    print(f"Scheduler error: {e}")
                
                time.sleep(check_interval)
        
        self._thread = threading.Thread(target=run_scheduler, daemon=True)
        self._thread.start()
    
    def stop_background_scheduler(self):
        """Stop background scheduler."""
        self._running = False
        if self._thread:
            self._thread.join(timeout=5)
    
    def reset_user_state(self, user_id: str):
        """Reset scheduler state for a user."""
        if user_id in self.state["last_proactive_check"]:
            del self.state["last_proactive_check"][user_id]
        if user_id in self.state["greeting_sent_today"]:
            del self.state["greeting_sent_today"][user_id]
        if user_id in self.state["weekly_checkin_sent"]:
            del self.state["weekly_checkin_sent"][user_id]
        self._save_state()
