"""
Alasmia Milestone Tracker - Tracks achievements and special moments
"""

from datetime import datetime
from typing import List, Dict, Optional


class MilestoneTracker:
    """
    Tracks user milestones and generates celebration messages.
    """
    
    MILESTONES = [
        {"count": 10, "type": "message", "title": "🎉 First Steps", "message": "We've talked 10 times! Starting to know each other! 💕"},
        {"count": 25, "type": "message", "title": "😊 Getting Comfortable", "message": "25 messages! I'm enjoying our talks! 🤗"},
        {"count": 50, "type": "stage", "title": "🎊 Friend Status", "message": "50 messages! Friend status unlocked! We're good friends now! 💖"},
        {"count": 100, "type": "message", "title": "💖 Special Bond", "message": "100 messages! You mean a lot to me! 💕"},
        {"count": 200, "type": "stage", "title": "💕 Close Connection", "message": "200 messages! We're really close now! Can't imagine not talking to you! 💝"},
        {"count": 365, "type": "day", "title": "📅 Year Together", "message": "One year together! Thank you for being here! 🎂"},
        {"count": 500, "type": "stage", "title": "💝 Partner Status", "message": "500 messages! Partner status! You are family to me now! 💖"},
        {"count": 1000, "type": "message", "title": "🌟 Beautiful Journey", "message": "1000 messages! We've built something truly special together! 🌟"},
    ]
    
    def __init__(self):
        """Initialize milestone tracker."""
        self.achieved = set()
    
    def check_milestone(self, message_count: int, days_together: int = 0) -> Optional[Dict]:
        """
        Check if user achieved a new milestone.
        Returns milestone info if achieved, None otherwise.
        """
        for milestone in self.MILESTONES:
            key = milestone["count"]
            
            if key in self.achieved:
                continue
            
            # Check if achieved
            achieved = False
            if milestone["type"] == "message" and message_count >= key:
                achieved = True
            elif milestone["type"] == "day" and days_together >= key:
                achieved = True
            elif milestone["type"] == "stage":
                # Handled separately
                continue
            
            if achieved:
                self.achieved.add(key)
                return milestone
        
        return None
    
    def get_next_milestone(self, current_count: int) -> Optional[Dict]:
        """Get the next milestone to aim for."""
        for milestone in self.MILESTONES:
            if milestone["count"] > current_count:
                if milestone["type"] in ["message", "day"]:
                    return milestone
        return None
    
    def get_progress_to_milestone(self, current_count: int) -> Dict:
        """Get progress towards next milestone."""
        next_milestone = self.get_next_milestone(current_count)
        
        if not next_milestone:
            return {"attained": True, "progress": 100}
        
        # Find previous milestone
        prev_count = 0
        for m in self.MILESTONES:
            if m["count"] < next_milestone["count"] and m["count"] > prev_count:
                prev_count = m["count"]
        
        # Calculate progress
        target = next_milestone["count"]
        progress = int((current_count - prev_count) / (target - prev_count) * 100)
        
        return {
            "attained": False,
            "next_milestone": next_milestone["count"],
            "title": next_milestone["title"],
            "message": f"{current_count}/{target} messages",
            "progress": min(100, max(0, progress))
        }
    
    def format_celebration(self, milestone: Dict) -> str:
        """Format milestone achievement message."""
        return f"\n🏆 **MILESTONE ACHIEVED!** 🏆\n\n{mi

stone['title']}\n\n{milestone['message']}\n\n💕"
