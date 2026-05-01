"""
Alasmia Scheduler - Time-based greetings and check-ins
"""

import os
import json
from datetime import datetime, time
from pathlib import Path


class Scheduler:
    """
    Handles time-based greetings and automated check-ins.
    """
    
    GREETING_TIMES = {
        "morning": (7, 9),    # 7-9 AM
        "afternoon": (12, 14), # 12-2 PM
        "evening": (18, 20),  # 6-8 PM
        "night": (22, 23),    # 10-11 PM
    }
    
    def __init__(self):
        """Initialize scheduler."""
        self.last_greeting_file = Path("./data/last_greetings.json")
        self.last_greetings = self._load_last_greetings()
    
    def _load_last_greetings(self) -> dict:
        """Load last greeting timestamps."""
        if self.last_greeting_file.exists():
            with open(self.last_greeting_file, 'r') as f:
                return json.load(f)
        return {}
    
    def _save_last_greetings(self):
        """Save last greeting timestamps."""
        self.last_greeting_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.last_greeting_file, 'w') as f:
            json.dump(self.last_greetings, f, indent=2)
    
    def check_and_send_greeting(self) -> Optional[str]:
        """
        Check if it's time for a greeting.
        Returns greeting message if time, None otherwise.
        """
        now = datetime.now()
        current_hour = now.hour
        today = now.strftime("%Y-%m-%d")
        
        for greeting_type, (start_hour, end_hour) in self.GREETING_TIMES.items():
            if start_hour <= current_hour <= end_hour:
                last_key = f"{greeting_type}_{today}"
                
                if self.last_greetings.get(last_key) != today:
                    self.last_greetings[last_key] = today
                    self._save_last_greetings()
                    return self._get_greeting_message(greeting_type, now)
        
        return None
    
    def _get_greeting_message(self, greeting_type: str, now: datetime) -> str:
        """Generate greeting message based on time of day."""
        messages = {
            "morning": "Good morning! ☀️ Hope you slept well. How are you feeling today?",
            "afternoon": "Good afternoon! How's your day going so far? 💕",
            "evening": "Good evening! 💫 How was your day?",
            "night": "Good night! 🌙 Sleep well. Talk to you tomorrow!",
        }
        
        return messages.get(greeting_type, f"Hello! 💕")
    
    def should_weekly_checkin(self) -> bool:
        """Check if it's time for weekly check-in (Sunday)."""
        now = datetime.now()
        today = now.strftime("%Y-%m-%d")
        
        # Sunday
        if now.weekday() == 6:  # Sunday = 6
            last_checkin = self.last_greetings.get("weekly_checkin", "")
            if last_checkin != today:
                self.last_greetings["weekly_checkin"] = today
                self._save_last_greetings()
                return True
        
        return False
    
    def get_weekly_checkin_message(self, analytics) -> str:
        """Generate weekly check-in message with analytics."""
        report = analytics.get_weekly_summary()
        
        message = f"📊 **Weekly Check-in!** 💕\n\n"
        message += f"It's been a week together! Here's your summary:\n\n"
        message += f"💬 Messages: {report.get('message_count', 0)}\n"
        message += f"😊 Mood Trend: {report.get('mood_trend', 'neutral')}\n"
        message += f"🔥 Streak: {report.get('streak', 0)} days\n"
        message += f"💕 Connection: {report.get('connection_score', 0)}%\n\n"
        message += f"Want to share anything? Or shall I explain any insight? 💭"
        
        return message
    
    def get_monthly_anniversary_message(self, user_profile: dict) -> str:
        """Generate monthly anniversary message."""
        first_seen = user_profile.get("first_seen", "")
        if not first_seen:
            return None
        
        try:
            from datetime import datetime
            first_date = datetime.fromisoformat(first_seen.replace("Z", "+00:00"))
            now = datetime.now()
            
            days_together = (now - first_date).days
            
            if days_together % 30 == 0 and days_together > 0:
                months = days_together // 30
                return f"🎉 **Monthly Anniversary!** 🎉\n\nIt's been {months} month(s) together! 💕\nThank you for being here!"
        except:
            pass
        
        return None
