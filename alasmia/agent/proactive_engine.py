"""
Alasmia Proactive Engine - AI Initiates Conversations

This module makes Alasmia a TRUE life partner by:
- Initiating conversations proactively
- Following up on past topics
- Daily check-ins even when user doesn't message
- Remembering and picking up old threads
"""

import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from pathlib import Path
import random


class ProactiveEngine:
    """
    Makes Alasmia proactively reach out to user.
    
    Key behaviors:
    - Initiate morning/evening greetings
    - Follow up on previous conversations
    - Check on user when they seem down
    - Share moments from "shared" experiences
    - Never be annoying - respect boundaries
    """
    
    # Time slots for proactive messages
    TIME_SLOTS = {
        "morning": {"start": 7, "end": 9, "weight": 1.0},
        "mid_morning": {"start": 10, "end": 11, "weight": 0.3},
        "afternoon": {"start": 12, "end": 14, "weight": 0.5},
        "evening": {"start": 18, "end": 20, "weight": 1.0},
        "night": {"start": 21, "end": 23, "weight": 0.8},
    }
    
    # Maximum proactive messages per day per user
    MAX_DAILY_PROACTIVE = 4
    MIN_GAP_HOURS = 3  # Minimum hours between proactive messages
    
    def __init__(self, data_dir: str = "./data"):
        """Initialize proactive engine."""
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.state_file = self.data_dir / "proactive_state.json"
        self.state = self._load_state()
    
    def _load_state(self) -> Dict:
        """Load proactive state."""
        if self.state_file.exists():
            with open(self.state_file, 'r') as f:
                return json.load(f)
        return {"users": {}, "last_cleanup": datetime.utcnow().isoformat()}
    
    def _save_state(self):
        """Save proactive state."""
        self.state["last_cleanup"] = datetime.utcnow().isoformat()
        with open(self.state_file, 'w') as f:
            json.dump(self.state, f, indent=2)
    
    def _get_user_state(self, user_id: str) -> Dict:
        """Get or create user state."""
        if user_id not in self.state["users"]:
            self.state["users"][user_id] = {
                "daily_proactive_count": 0,
                "last_proactive": None,
                "last_proactive_type": None,
                "conversation_pickups": [],  # Topics to pick up later
                "active_threads": [],  # Ongoing topics
                "daily_stats": {},  # Track messages per day
                "streak_days": 0,
                "last_seen": None,
            }
        return self.state["users"][user_id]
    
    def should_send_proactive(self, user_id: str, force: bool = False) -> Tuple[bool, str]:
        """
        Determine if we should send a proactive message.
        
        Returns:
            (should_send, reason)
        """
        now = datetime.utcnow()
        user_state = self._get_user_state(user_id)
        
        # Check daily limit
        today = now.strftime("%Y-%m-%d")
        if user_state["daily_stats"].get(today, 0) >= self.MAX_DAILY_PROACTIVE and not force:
            return False, "daily_limit_reached"
        
        # Check minimum gap
        if user_state["last_proactive"]:
            last = datetime.fromisoformat(user_state["last_proactive"])
            hours_since = (now - last).total_seconds() / 3600
            if hours_since < self.MIN_GAP_HOURS and not force:
                return False, "too_recent"
        
        return True, "ok"
    
    def record_proactive_sent(self, user_id: str, message_type: str):
        """Record that we sent a proactive message."""
        now = datetime.utcnow()
        user_state = self._get_user_state(user_id)
        today = now.strftime("%Y-%m-%d")
        
        user_state["last_proactive"] = now.isoformat()
        user_state["last_proactive_type"] = message_type
        user_state["daily_stats"][today] = user_state["daily_stats"].get(today, 0) + 1
        
        # Clean old stats (keep last 7 days)
        old_days = [d for d in user_state["daily_stats"] if d < (now - timedelta(days=7)).strftime("%Y-%m-%d")]
        for d in old_days:
            del user_state["daily_stats"][d]
        
        self._save_state()
    
    def get_proactive_message(self, user_id: str, companion: str = "Mia", 
                              language: str = "English", context: Dict = None) -> Optional[str]:
        """
        Generate appropriate proactive message.
        
        Args:
            user_id: User identifier
            companion: "Alas" or "Mia"
            language: User's language
            context: Additional context (mood, last topic, etc.)
            
        Returns:
            Proactive message string or None
        """
        should_send, reason = self.should_send_proactive(user_id)
        if not should_send and not context.get("force"):
            return None
        
        context = context or {}
        now = datetime.utcnow()
        user_state = self._get_user_state(user_id)
        
        # Determine message type based on time and context
        message_type = self._determine_message_type(now, user_state, context)
        
        if not message_type:
            return None
        
        # Generate message
        message = self._generate_message(message_type, companion, language, user_state, context)
        
        if message:
            self.record_proactive_sent(user_id, message_type)
        
        return message
    
    def _determine_message_type(self, now: datetime, user_state: Dict, context: Dict) -> Optional[str]:
        """Determine what type of proactive message to send."""
        hour = now.hour
        
        # Check for conversation pickups first
        if user_state.get("conversation_pickups"):
            return "follow_up"
        
        # Time-based messages
        if 7 <= hour < 9:
            return "morning"
        elif 12 <= hour < 14:
            return "afternoon_check"
        elif 18 <= hour < 21:
            return "evening"
        elif 21 <= hour < 23:
            return "night"
        
        # Random check-in (low probability)
        if random.random() < 0.1:  # 10% chance
            return "casual_checkin"
        
        return None
    
    def _generate_message(self, message_type: str, companion: str, language: str,
                          user_state: Dict, context: Dict) -> str:
        """Generate the actual proactive message."""
        
        # Get user's name if available
        user_name = context.get("user_name", "")
        
        # Messages by type and companion
        messages = {
            "morning": {
                "Alas": {
                    "English": f"Rise and shine{user_name and f', {user_name}'}! ☀️ Hope you slept well, champion. How's your morning going?",
                    "Hindi": f"उठ जाओ{user_name and f', {user_name}'}! ☀️ कैसा सोया? आज सुबह कैसा है?",
                    "Mandarin Chinese": f"起床了{user_name and f'，{user_name}'}！☀️ 睡得好吗？早上怎么样？",
                },
                "Mia": {
                    "English": f"Good morning{user_name and f', {user_name}'}! ☀️ Hope you had sweet dreams! How are you feeling today?",
                    "Hindi": f"सुप्रभात{user_name and f', {user_name}'}! ☀️ आशा है अच्छे सपने देखे होंगे। आज कैसा लग रहा है?",
                    "Mandarin Chinese": f"早上好{user_name and f'，{user_name}'}！☀️ 睡得好吗？今天感觉怎么样？",
                }
            },
            "afternoon_check": {
                "Alas": {
                    "English": f"Hey{user_name and f', {user_name}'}! 👋 Hope your day's going well. How's it going so far?",
                    "Hindi": f"अरे{user_name and f', {user_name}'}! 👋 दिन कैसा जा रहा है?",
                    "Mandarin Chinese": f"嘿{user_name and f'，{user_name}'}！👋 今天怎么样？",
                },
                "Mia": {
                    "English": f"Hi{user_name and f', {user_name}'}! 💕 How's your day treating you? Remember to take a break!",
                    "Hindi": f"नमस्ते{user_name and f', {user_name}'}! 💕 दिन कैसा जा रहा है? ब्रेक लेना मत भूलना!",
                    "Mandarin Chinese": f"你好{user_name and f'，{user_name}'}！💕 今天怎么样？别忘了休息一下！",
                }
            },
            "evening": {
                "Alas": {
                    "English": f"Evening{user_name and f', {user_name}'}! 💫 How was your day? Got any plans for tonight?",
                    "Hindi": f"शाम को{user_name and f', {user_name}'}! 💫 दिन कैसा रहा? आज रात कुछ plan hai?",
                    "Mandarin Chinese": f"傍晚好{user_name and f'，{user_name}'}！💫 今天怎么样？晚上有什么计划吗？",
                },
                "Mia": {
                    "English": f"Good evening{user_name and f', {user_name}'}! 💫 How was your day? You deserve some rest now!",
                    "Hindi": f"शाम को{user_name and f', {user_name}'}! 💫 दिन कैसा रहा? अब thoda आराम करो!",
                    "Mandarin Chinese": f"傍晚好{user_name and f'，{user_name}'}！💫 今天怎么样？该休息一下了！",
                }
            },
            "night": {
                "Alas": {
                    "English": f"Hey{user_name and f', {user_name}'}! 🌙 It's getting late. Don't stay up too late, champion. Rest well!",
                    "Hindi": f"अरे{user_name and f', {user_name}'}! 🌙 रात हो गई। ज्यादा late mat jaana। अच्छे से सोना!",
                    "Mandarin Chinese": f"嘿{user_name and f'，{user_name}'}！🌙 已经很晚了。别熬夜了，好好休息！",
                },
                "Mia": {
                    "English": f"Hi{user_name and f', {user_name}'}! 🌙 Time to wind down, lovely. Sleep tight and dream sweet!",
                    "Hindi": f"नमस्ते{user_name and f', {user_name}'}! 🌙 सोने ka time ho gaya। अच्छे से सोना!",
                    "Mandarin Chinese": f"你好{user_name and f'，{user_name}'}！🌙 是时候休息了。好好睡吧！",
                }
            },
            "follow_up": {
                "Alas": {
                    "English": f"Hey{user_name and f', {user_name}'}! Remember you mentioned {{topic}}? Any update on that? 💪",
                    "Hindi": f"अरे{user_name and f', {user_name}'}! Tune {{topic}} mention kiya tha na? Kuch update hai?",
                    "Mandarin Chinese": f"嘿{user_name and f'，{user_name}'}！你之前提到{{topic}}，有什么进展吗？",
                },
                "Mia": {
                    "English": f"Hi{user_name and f', {user_name}'}! 💕 I was thinking about what you said about {{topic}}... How's that going?",
                    "Hindi": f"नमस्ते{user_name and f', {user_name}'}! 💕 Tune jo {{topic}} baat kiya tha... Woh kaisa chal raha hai?",
                    "Mandarin Chinese": f"你好{user_name and f'，{user_name}'}！💕 我在想你之前说的{{topic}}...怎么样了？",
                }
            },
            "casual_checkin": {
                "Alas": {
                    "English": f"Just checking in{user_name and f', {user_name}'}! 👋 How are you doing? Everything okay?",
                    "Hindi": f"Bas check karne आ रहा हूं{user_name and f', {user_name}'}! 👋 कैसे हो? Sab theek hai?",
                    "Mandarin Chinese": f"只是想看看你{user_name and f'，{user_name}'}！👋 你怎么样？一切都好吗？",
                },
                "Mia": {
                    "English": f"Hey{user_name and f', {user_name}'}! 💕 Just wanted to see how you're doing. Talk to me!",
                    "Hindi": f"अरे{user_name and f', {user_name}'}! 💕 Bas dekne आ रहा था। कैसे हो? Baat karo!",
                    "Mandarin Chinese": f"嘿{user_name and f'，{user_name}'}！💕 只是想看看你怎么样。跟我说说！",
                }
            },
            "mood_followup": {
                "Alas": {
                    "English": f"Hey{user_name and f', {user_name}'}... You seemed a bit down earlier. Everything okay? I'm here if you want to talk. 💪",
                    "Hindi": f"अरे{user_name and f', {user_name}'}... Tune thoda udaas lag raha tha pahale। Sab theek hai? Baat karna ho toh मैं हूं।",
                    "Mandarin Chinese": f"嘿{user_name and f'，{user_name}'}... 你之前看起来有点低落。还好吗？想聊聊的话我在这里。",
                },
                "Mia": {
                    "English": f"Hi{user_name and f', {user_name}'}... 💕 I noticed you seemed a bit off earlier. Just wanted to check if you're okay. I'm here for you.",
                    "Hindi": f"नमस्ते{user_name and f', {user_name}'}... 💕 Tune thoda off lag raha tha। Sab theek hai? मैं तुम्हारे लिए हूं।",
                    "Mandarin Chinese": f"你好{user_name and f'，{user_name}'}... 💕 我注意到你之前看起来有点低落。你还好吗？我在这里陪着你。",
                }
            }
        }
        
        companion_messages = messages.get(message_type, {}).get(companion, {})
        return companion_messages.get(language, companion_messages.get("English", ""))
    
    def add_conversation_pickup(self, user_id: str, topic: str, context: str = ""):
        """Add a topic to follow up on later."""
        user_state = self._get_user_state(user_id)
        
        user_state["conversation_pickups"].append({
            "topic": topic,
            "context": context,
            "added": datetime.utcnow().isoformat(),
            "reminded": 0
        })
        
        # Keep only last 10
        if len(user_state["conversation_pickups"]) > 10:
            user_state["conversation_pickups"] = user_state["conversation_pickups"][-10:]
        
        self._save_state()
    
    def get_next_pickup(self, user_id: str) -> Optional[Dict]:
        """Get the next conversation topic to pick up."""
        user_state = self._get_user_state(user_id)
        pickups = user_state.get("conversation_pickups", [])
        
        if not pickups:
            return None
        
        pickup = pickups.pop(0)
        self._save_state()
        return pickup
    
    def update_streak(self, user_id: str):
        """Update conversation streak."""
        user_state = self._get_user_state(user_id)
        now = datetime.utcnow()
        today = now.strftime("%Y-%m-%d")
        
        if user_state.get("last_seen"):
            last_seen = datetime.fromisoformat(user_state["last_seen"])
            if (now - last_seen).days == 1:
                user_state["streak_days"] = user_state.get("streak_days", 0) + 1
            elif (now - last_seen).days > 1:
                user_state["streak_days"] = 1
        else:
            user_state["streak_days"] = 1
        
        user_state["last_seen"] = now.isoformat()
        self._save_state()
    
    def get_streak(self, user_id: str) -> int:
        """Get user's conversation streak."""
        user_state = self._get_user_state(user_id)
        return user_state.get("streak_days", 0)
