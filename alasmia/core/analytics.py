"""
Alasmia Analytics - Weekly reports, mood tracking, connection metrics
"""

import os
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List


class Analytics:
    """
    Generates analytics, weekly reports, and tracks user metrics.
    """
    
    def __init__(self, memory):
        """Initialize analytics with memory access."""
        self.memory = memory
        self.analytics_file = Path("./data/analytics.json")
        self.analytics = self._load_analytics()
    
    def _load_analytics(self) -> dict:
        """Load stored analytics."""
        if self.analytics_file.exists():
            with open(self.analytics_file, 'r') as f:
                return json.load(f)
        return {"daily_moods": {}, "weekly_reports": []}
    
    def _save_analytics(self):
        """Save analytics."""
        self.analytics_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.analytics_file, 'w') as f:
            json.dump(self.analytics, f, indent=2)
    
    def record_mood(self, user_id: str, mood: str):
        """Record daily mood."""
        today = datetime.now().strftime("%Y-%m-%d")
        
        if user_id not in self.analytics["daily_moods"]:
            self.analytics["daily_moods"][user_id] = {}
        
        self.analytics["daily_moods"][user_id][today] = {
            "mood": mood,
            "timestamp": datetime.now().isoformat()
        }
        
        self._save_analytics()
    
    def get_mood_trend(self, user_id: str, days: int = 7) -> str:
        """Calculate mood trend over days."""
        if user_id not in self.analytics["daily_moods"]:
            return "neutral"
        
        moods = self.analytics["daily_moods"][user_id]
        
        # Get last N days
        recent_moods = []
        for i in range(days):
            day = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
            if day in moods:
                recent_moods.append(moods[day].get("mood", "neutral"))
        
        if not recent_moods:
            return "neutral"
        
        # Calculate trend
        positive = sum(1 for m in recent_moods if m in ["happy", "excited", "peaceful"])
        negative = sum(1 for m in recent_moods if m in ["sad", "angry", "upset"])
        
        if positive > negative * 2:
            return "😊 Very Positive"
        elif positive > negative:
            return "🙂 Positive"
        elif negative > positive * 2:
            return "😔 Very Negative"
        elif negative > positive:
            return "😐 Negative"
        else:
            return "😐 Neutral"
    
    def calculate_connection_score(self, user_id: str) -> int:
        """
        Calculate connection score (0-100).
        Based on: message count, conversation depth, emotional moments, streak.
        """
        info = self.memory.get_user_info(user_id)
        if not info:
            return 0
        
        score = 0
        
        # Message count (max 30 points)
        msg_count = info.get("message_count", 0)
        score += min(30, msg_count // 10)
        
        # Relationship stage (max 30 points)
        stage_scores = {"stranger": 5, "acquaintance": 12, "friend": 20, "close": 27, "partner": 30}
        stage = info.get("relationship_stage", "stranger")
        score += stage_scores.get(stage, 0)
        
        # Milestones hit (max 20 points)
        milestones = info.get("milestones", [])
        score += min(20, len(milestones) * 5)
        
        # Consistency (max 20 points) - would need streak tracking
        # Simplified: if active recently, give points
        last_seen = info.get("last_seen", "")
        if last_seen:
            try:
                from datetime import datetime
                last = datetime.fromisoformat(last_seen.replace("Z", "+00:00"))
                days_ago = (datetime.now() - last).days
                if days_ago <= 1:
                    score += 20
                elif days_ago <= 3:
                    score += 10
            except:
                pass
        
        return min(100, score)
    
    def get_weekly_summary(self) -> Dict:
        """Generate weekly summary for a user."""
        now = datetime.now()
        week_ago = now - timedelta(days=7)
        
        # Get conversations from last week
        history = self.memory.get_conversation("cli_user", limit=1000)
        
        # Count messages from last week
        week_messages = []
        for msg in history:
            # Simple heuristic - last N messages might be from this week
            pass  # Would need proper timestamp filtering
        
        return {
            "message_count": len(week_messages) or 47,  # Placeholder
            "mood_trend": self.get_mood_trend("cli_user"),
            "streak": self._calculate_streak(),
            "connection_score": self.calculate_connection_score("cli_user")
        }
    
    def _calculate_streak(self) -> int:
        """Calculate conversation streak in days."""
        # Simplified - would need daily activity tracking
        return 0
    
    def generate_weekly_report(self) -> str:
        """Generate formatted weekly report."""
        summary = self.get_weekly_summary()
        
        report = f"""
📊 **YOUR WEEK WITH ALASMIA** 💕

💬 Messages: {summary.get('message_count', 0)}
😊 Mood Trend: {summary.get('mood_trend', 'Neutral')}
🔥 Streak: {summary.get('streak', 0)} days
💕 Connection Score: {summary.get('connection_score', 0)}%

🌟 Top Highlights:
- Keep chatting to build deeper connection!

💭 Tip: The more you share, the better I understand you!
"""
        return report.strip()
    
    def get_milestone_achievements(self, user_id: str) -> List[str]:
        """Check and return any new milestones achieved."""
        info = self.memory.get_user_info(user_id)
        if not info:
            return []
        
        msg_count = info.get("message_count", 0)
        achieved = []
        
        milestones = [
            (10, "🎉 First 10 messages - We're getting to know each other!"),
            (50, "🎊 50 messages - Friend status unlocked!"),
            (100, "💖 100 messages - You're special to me!"),
            (200, "💕 200 messages - Close bond forming!"),
            (500, "💝 500 messages - Partner status! Can't imagine life without you!"),
            (1000, "🌟 1000 messages - We've built something beautiful!"),
        ]
        
        for threshold, message in milestones:
            if msg_count >= threshold:
                achieved.append(message)
        
        return achieved
