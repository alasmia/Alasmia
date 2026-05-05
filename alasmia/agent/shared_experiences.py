"""
Alasmia Shared Experiences 

Tracks shared experiences between user and AI.
Makes conversations feel more connected and personal.
"""

import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from pathlib import Path
import re


class SharedExperiences:
    """
    Tracks things shared between user and Alasmia.
    
    Types of shared experiences:
    - Jokes shared and laughed about
    - Topics discussed deeply
    - Goals mentioned
    - Places user talked about
    - People user mentioned
    - Movies/books/media discussed
    - Achievements celebrated
    """
    
    EXPERIENCE_TYPES = [
        "joke",
        "deep_topic", 
        "goal",
        "place",
        "person",
        "media",
        "achievement",
        "struggle",
        "learning",
        "plan"
    ]
    
    def __init__(self, data_dir: str = "./data"):
        """Initialize shared experiences tracker."""
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.state_file = self.data_dir / "shared_experiences.json"
        self.state = self._load_state()
    
    def _load_state(self) -> Dict:
        """Load shared experiences state."""
        if self.state_file.exists():
            with open(self.state_file, 'r') as f:
                return json.load(f)
        return {"users": {}}
    
    def _save_state(self):
        """Save shared experiences state."""
        with open(self.state_file, 'w') as f:
            json.dump(self.state, f, indent=2)
    
    def _get_user_state(self, user_id: str) -> Dict:
        """Get or create user experiences state."""
        if user_id not in self.state["users"]:
            self.state["users"][user_id] = {
                "experiences": [],     # All shared experiences
                "inside_jokes": [],    # Jokes only
                "topics": [],          # Deep discussions
                "goals": [],           # User's goals
                "mentioned_people": [], # People user talked about
            }
        return self.state["users"][user_id]
    
    def analyze_and_record(self, user_id: str, user_message: str, ai_response: str, mood: str):
        """
        Analyze conversation and record shared experiences.
        
        Called after every conversation turn.
        """
        user_state = self._get_user_state(user_id)
        user_lower = user_message.lower()
        
        # Detect jokes (simple heuristics)
        if self._is_joke(user_message, ai_response):
            self._add_experience(user_id, "joke", self._extract_joke_topic(user_message))
        
        # Detect deep topics
        deep_keywords = ["think", "believe", "feel", "meaning", "purpose", "life", "future", "dream", "idea"]
        if any(kw in user_lower for kw in deep_keywords) and len(user_message) > 30:
            topic = self._extract_topic(user_message)
            if topic:
                self._add_experience(user_id, "deep_topic", topic)
        
        # Detect goals
        goal_keywords = ["want to", "going to", "plan to", "will", "hope to", "looking forward", "goal", "dream"]
        if any(kw in user_lower for kw in goal_keywords):
            goal = self._extract_goal(user_message)
            if goal:
                self._add_experience(user_id, "goal", goal)
        
        # Detect achievements
        achievement_keywords = ["achieved", "accomplished", "success", "won", "got the", "finished", "completed"]
        if any(kw in user_lower for kw in achievement_keywords):
            achievement = self._extract_achievement(user_message)
            if achievement:
                self._add_experience(user_id, "achievement", achievement)
        
        # Detect places mentioned
        place_keywords = ["visited", "went to", "travel", "trip", "vacation", "holiday", "lived", "living in"]
        if any(kw in user_lower for kw in place_keywords):
            place = self._extract_place(user_message)
            if place:
                self._add_experience(user_id, "place", place)
        
        # Detect people mentioned
        people = self._extract_people(user_message)
        for person in people:
            self._add_experience(user_id, "person", person)
        
        self._save_state()
    
    def _is_joke(self, user_message: str, ai_response: str) -> bool:
        """Simple heuristic to detect if a joke was shared."""
        joke_indicators = [
            "😂", "🤣", "haha", "lmao", "rofl", "that's funny",
            "you crack me up", "so funny", "too funny", "hilarious",
            "pun", "joke", "comedian", "humor", "witty"
        ]
        combined = (user_message + " " + ai_response).lower()
        return any(indicator in combined for indicator in joke_indicators)
    
    def _extract_joke_topic(self, message: str) -> str:
        """Extract the topic/subject of a joke."""
        # Simple extraction - just get a noun phrase
        words = message.split()
        # Remove joke indicators and get content
        clean_words = [w for w in words if not any(ind in w.lower() for ind in ["joke", "funny", "haha", "lol"])]
        if clean_words:
            return " ".join(clean_words[:5])[:50]  # First 5 words, max 50 chars
        return "general humor"
    
    def _extract_topic(self, message: str) -> str:
        """Extract a topic from deep conversation."""
        words = message.split()
        if len(words) > 10:
            return " ".join(words[:7])[:60]  # First 7 words
        return message[:60]
    
    def _extract_goal(self, message: str) -> str:
        """Extract a goal from message."""
        # Look for "want to" phrases
        patterns = [
            r"I want to (.+)",
            r"I'm going to (.+)",
            r"I plan to (.+)",
            r"My goal is (.+)",
            r"I hope to (.+)",
        ]
        for pattern in patterns:
            match = re.search(pattern, message, re.IGNORECASE)
            if match:
                return match.group(1)[:50]
        return message[:50]
    
    def _extract_achievement(self, message: str) -> str:
        """Extract achievement from message."""
        # Look for achievement-related phrases
        patterns = [
            r"I (?:just )?(?:achieved|accomplished|finished|completed|got) (.+)",
            r"I'm (?:so )?proud of (.+)",
            r"Finally (.+)",
        ]
        for pattern in patterns:
            match = re.search(pattern, message, re.IGNORECASE)
            if match:
                return match.group(1)[:50]
        return message[:50]
    
    def _extract_place(self, message: str) -> str:
        """Extract a place from message."""
        words = message.split()
        place_indicators = ["visited", "went", "travel", "trip"]
        for i, word in enumerate(words):
            if any(ind in word.lower() for ind in place_indicators):
                if i + 1 < len(words):
                    return " ".join(words[i+1:i+3])[:30]
        return message[:30]
    
    def _extract_people(self, message: str) -> List[str]:
        """Extract people mentioned in message."""
        # Simple heuristic: capitalized words that might be names
        people = []
        words = message.split()
        for word in words:
            if word and word[0].isupper() and len(word) > 2:
                # Avoid common words
                if word.lower() not in ["i", "im", "am", "the", "this", "that", "what", "how", "when", "where", "why", "because", "want", "will", "just", "really"]:
                    people.append(word)
        return list(set(people))[:3]  # Max 3 people per message
    
    def _add_experience(self, user_id: str, exp_type: str, description: str):
        """Add an experience to user's history."""
        user_state = self._get_user_state(user_id)
        
        # Check if this experience already exists (avoid duplicates)
        for exp in user_state["experiences"]:
            if exp["type"] == exp_type and exp["description"].lower() == description.lower():
                exp["mentions"] += 1
                exp["last_mentioned"] = datetime.utcnow().isoformat()
                return  # Don't add duplicate
        
        experience = {
            "type": exp_type,
            "description": description,
            "created": datetime.utcnow().isoformat(),
            "mentions": 1,
            "last_mentioned": datetime.utcnow().isoformat()
        }
        
        user_state["experiences"].append(experience)
        
        # Keep only last 100 experiences
        if len(user_state["experiences"]) > 100:
            user_state["experiences"] = user_state["experiences"][-100:]
        
        # Track by type
        if exp_type == "joke":
            user_state["inside_jokes"].append(description)
        elif exp_type == "deep_topic":
            user_state["topics"].append(description)
        elif exp_type == "goal":
            user_state["goals"].append(description)
        elif exp_type == "person":
            user_state["mentioned_people"].append(description)
    
    def get_random_mention(self, user_id: str, exp_type: str = None) -> Optional[str]:
        """Get a random experience to naturally mention."""
        user_state = self._get_user_state(user_id)
        experiences = user_state["experiences"]
        
        if not experiences:
            return None
        
        # Filter by type if specified
        if exp_type:
            experiences = [e for e in experiences if e["type"] == exp_type]
        
        if not experiences:
            return None
        
        # Pick randomly from recent ones
        import random
        recent = [e for e in experiences if e.get("mentions", 0) < 3]  # Not over-mentioned
        if not recent:
            recent = experiences
        
        exp = random.choice(recent)
        
        # Generate natural mention
        if exp["type"] == "joke":
            return f"Speaking of {exp['description']}... that was hilarious! 😂"
        elif exp["type"] == "deep_topic":
            return f"You know, I was thinking about what you said about {exp['description']}..."
        elif exp["type"] == "goal":
            return f"Hey! Remember your goal to {exp['description']}? How's that going?"
        elif exp["type"] == "achievement":
            return f"I'm still proud of you for {exp['description']}! 🎉"
        elif exp["type"] == "person":
            return f"How's {exp['description']} doing? You mentioned them before."
        else:
            return f"That reminds me of when you talked about {exp['description']}..."
    
    def get_experience_summary(self, user_id: str) -> Dict:
        """Get summary of shared experiences."""
        user_state = self._get_user_state(user_id)
        experiences = user_state["experiences"]
        
        summary = {
            "total": len(experiences),
            "by_type": {},
            "recent": [],
            "inside_jokes": user_state.get("inside_jokes", []),
            "goals": user_state.get("goals", []),
            "topics": user_state.get("topics", [])
        }
        
        # Count by type
        for exp in experiences:
            exp_type = exp["type"]
            summary["by_type"][exp_type] = summary["by_type"].get(exp_type, 0) + 1
        
        # Recent (last 5)
        summary["recent"] = experiences[-5:]
        
        return summary
