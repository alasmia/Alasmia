"""
Alasmia Interest Tracker - Deep User Interest Memory

Tracks what user cares about: hobbies, preferences, goals, people, topics.
Builds a comprehensive interest profile over time.
"""

import json
from typing import Dict, List, Optional, Any
from datetime import datetime
from pathlib import Path


class InterestTracker:
    """
    Tracks and remembers user interests across conversations.
    
    Interest Categories:
    - hobbies: cricket, anime, cooking, gaming, music, etc.
    - goals: career, fitness, learning, relationships, etc.
    - people: friends, family mentioned by name
    - topics: things user talks about frequently
    - preferences: likes, dislikes, pet peeves
    - events: upcoming events, plans, occasions
    """
    
    INTEREST_CATEGORIES = [
        "hobbies",      # Activities user enjoys
        "goals",        # Things user wants to achieve
        "people",       # Friends, family, people in their life
        "topics",       # Subjects user discusses often
        "preferences",  # Likes and dislikes
        "events",       # Plans, upcoming events, occasions
        "places",       # Places user mentions wanting to visit
        "food",         # Food preferences, restaurants
        "media",        # Movies, shows, books, music
        "work",         # Job, career, work-related
        "health",       # Fitness, wellness, medical
    ]
    
    def __init__(self, data_dir: str = "./data"):
        """Initialize interest tracker."""
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.interest_file = self.data_dir / "interests.json"
        self.interests = self._load_interests()
        
        # Keywords for interest detection
        self.interest_keywords = self._load_interest_keywords()
    
    def _load_interest_keywords(self) -> Dict[str, List[str]]:
        """Load keywords for interest detection."""
        return {
            "hobbies": [
                "cricket", "football", "anime", "gaming", "gym", "workout", "running",
                "cooking", "reading", "painting", "music", "guitar", "piano", "dance",
                "photography", "writing", "gardening", "hiking", "cycling", "swimming",
                "tennis", "badminton", "volleyball", "basketball", "yoga", "meditation",
                "movies", "netflix", "series", "youtube", "streaming", "podcast"
            ],
            "goals": [
                "lose weight", "fit", "healthy", "career", "promotion", "new job",
                "learn", "study", "exam", "course", "certification", "startup",
                "business", "save money", "invest", "buy house", "marriage", "family",
                "learn spanish", "learn japanese", "learn coding", "skill"
            ],
            "food": [
                "pizza", "burger", "sushi", "biryani", "pasta", "noodles", "chinese",
                "italian", "indian food", "thai", "korean", "vegetarian", "vegan",
                "coffee", "tea", "dessert", "ice cream", "cake", "restaurant"
            ],
            "media": [
                "movie", "film", "series", "show", "anime", "drama", "documentary",
                "netflix", "amazon prime", "hotstar", "spotify", "music", "song",
                "podcast", "youtube", "book", "novel", "comic", "manga"
            ],
            "work": [
                "office", "meeting", "project", "deadline", "boss", "colleague",
                "remote", "wfh", "interview", "resume", " LinkedIn", "client"
            ],
            "health": [
                "headache", "cold", "fever", "sleep", "tired", "stress", "anxiety",
                "doctor", "medicine", "hospital", "checkup", "diet", "weight"
            ]
        }
    
    def _load_interests(self) -> Dict:
        """Load interests from file."""
        if self.interest_file.exists():
            with open(self.interest_file, 'r') as f:
                return json.load(f)
        return {}
    
    def _save_interests(self):
        """Save interests to file."""
        with open(self.interest_file, 'w') as f:
            json.dump(self.interests, f, indent=2)
    
    def track_message(self, user_id: str, message: str, mood: str = None):
        """
        Analyze message and extract interests.
        
        Args:
            user_id: User identifier
            message: User's message
            mood: Detected mood
        """
        if user_id not in self.interests:
            self.interests[user_id] = {
                "categories": {cat: [] for cat in self.INTEREST_CATEGORIES},
                "mentions": {},  # Word count for frequency
                "last_updated": datetime.utcnow().isoformat(),
                "total_analyzed": 0
            }
        
        user_interests = self.interests[user_id]
        user_interests["total_analyzed"] += 1
        message_lower = message.lower()
        
        # Detect interests from keywords
        for category, keywords in self.interest_keywords.items():
            for keyword in keywords:
                if keyword.lower() in message_lower:
                    self._add_interest(user_id, category, keyword)
        
        # Extract named entities (simple approach)
        self._extract_names(user_id, message)
        
        # Track mood context
        if mood:
            if "mood_context" not in user_interests:
                user_interests["mood_context"] = []
            user_interests["mood_context"].append({
                "mood": mood,
                "timestamp": datetime.utcnow().isoformat()
            })
            # Keep last 100 mood entries
            if len(user_interests["mood_context"]) > 100:
                user_interests["mood_context"] = user_interests["mood_context"][-100:]
        
        user_interests["last_updated"] = datetime.utcnow().isoformat()
        self._save_interests()
    
    def _add_interest(self, user_id: str, category: str, interest: str):
        """Add interest to user's profile."""
        user_interests = self.interests[user_id]
        
        if category not in user_interests["categories"]:
            user_interests["categories"][category] = []
        
        interests_list = user_interests["categories"][category]
        
        # Check if already exists
        for item in interests_list:
            if item["interest"].lower() == interest.lower():
                item["mentions"] += 1
                item["last_mentioned"] = datetime.utcnow().isoformat()
                return
        
        # Add new interest
        interests_list.append({
            "interest": interest,
            "mentions": 1,
            "first_mentioned": datetime.utcnow().isoformat(),
            "last_mentioned": datetime.utcnow().isoformat()
        })
    
    def _extract_names(self, user_id: str, message: str):
        """
        Extract potential names from message.
        Simple heuristic: capitalized words that might be names.
        """
        words = message.split()
        for word in words:
            # Simple check - proper nouns likely names
            if word and word[0].isupper() and len(word) > 2:
                # Avoid common words
                if word.lower() not in ["i", "im", "am", "the", "this", "that", "what", "how", "when", "where", "why"]:
                    self._add_interest(user_id, "people", word)
    
    def get_interests(self, user_id: str, category: str = None, min_mentions: int = 1) -> Dict:
        """
        Get user's interests.
        
        Args:
            user_id: User identifier
            category: Optional specific category
            min_mentions: Minimum mentions to include
            
        Returns:
            Dict of interests by category
        """
        if user_id not in self.interests:
            return {}
        
        user_interests = self.interests[user_id]
        
        if category:
            items = user_interests["categories"].get(category, [])
            return [i for i in items if i["mentions"] >= min_mentions]
        
        # Return all categories with min mentions
        result = {}
        for cat, items in user_interests["categories"].items():
            filtered = [i for i in items if i["mentions"] >= min_mentions]
            if filtered:
                result[cat] = filtered
        return result
    
    def get_top_interests(self, user_id: str, limit: int = 10) -> List[Dict]:
        """Get user's most mentioned interests across all categories."""
        if user_id not in self.interests:
            return []
        
        all_interests = []
        for cat, items in self.interests[user_id]["categories"].items():
            for item in items:
                all_interests.append({
                    "category": cat,
                    "interest": item["interest"],
                    "mentions": item["mentions"]
                })
        
        # Sort by mentions
        all_interests.sort(key=lambda x: x["mentions"], reverse=True)
        return all_interests[:limit]
    
    def get_conversation_starters(self, user_id: str, language: str = "English") -> List[str]:
        """
        Generate conversation starters based on user's interests.
        
        Returns phrases that naturally continue past conversations.
        """
        interests = self.get_top_interests(user_id, limit=5)
        
        starters_by_lang = {
            "English": [
                "Hey! How's your {interest} going?",
                "Thinking about your {interest} - any updates?",
                "Remember you mentioned {interest}? How's that going?",
                "Did you do any {interest} recently?",
                "What's new with your {interest}?"
            ],
            "Hindi": [
                "Kya haal {interest} ka?",
                "Yaad hai tune {interest} mention kiya tha",
                "{interest} ke baare mai batao",
                "Kya {interest} mai kuch naya hai?",
                "Tumhara {interest} kaisa chal raha hai?"
            ],
            "Mandarin Chinese": [
                "你的{interest}最近怎么样？",
                "你提到过{interest}，有什么更新吗？",
                "最近{interest}有什么进展吗？",
                "你最近有做{interest}吗？"
            ]
        }
        
        starters = starters_by_lang.get(language, starters_by_lang["English"])
        result = []
        
        for i, interest_data in enumerate(interests):
            interest = interest_data["interest"]
            starter = starters[i % len(starters)].format(interest=interest)
            result.append(starter)
        
        # If no interests, use generic starters
        if not result:
            generic = {
                "English": ["How are you doing today?", "What's up?", "How's your day going?"],
                "Hindi": ["Kya haal hai?", "Kya kar rahe ho?", "Din kaisa ja raha hai?"],
                "Mandarin Chinese": ["你好！今天怎么样？", "最近如何？", "有什么新鲜事吗？"]
            }
            result = generic.get(language, generic["English"])
        
        return result
    
    def remember_fact(self, user_id: str, fact: str, category: str = "general"):
        """Manually remember a specific fact about user."""
        if user_id not in self.interests:
            self.interests[user_id] = {
                "categories": {cat: [] for cat in self.INTEREST_CATEGORIES},
                "mentions": {},
                "last_updated": datetime.utcnow().isoformat(),
                "total_analyzed": 0
            }
        
        self._add_interest(user_id, category, fact)
        self._save_interests()
    
    def get_memory_context(self, user_id: str) -> str:
        """Get a string summarizing user's interests for AI context."""
        interests = self.get_interests(user_id, min_mentions=2)
        
        if not interests:
            return ""
        
        context = "USER INTERESTS (from past conversations):\n"
        for category, items in interests.items():
            context += f"- {category}: {', '.join([i['interest'] for i in items])}\n"
        
        return context
