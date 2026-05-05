"""
Alasmia Emotional Continuity Engine 

Follows up on user's emotional state over time.
Remembers how user felt and checks back later.
Builds emotional continuity in the relationship.
"""

import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from pathlib import Path


class EmotionalContinuity:
    """
    Tracks emotional journey and follows up.
    
    Key features:
    - Remember emotional events
    - Follow up on user's emotional state
    - Pick up on past moods
    - Build emotional memory over time
    """
    
    def __init__(self, data_dir: str = "./data"):
        """Initialize emotional continuity tracker."""
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.state_file = self.data_dir / "emotional_continuity.json"
        self.state = self._load_state()
    
    def _load_state(self) -> Dict:
        """Load emotional continuity state."""
        if self.state_file.exists():
            with open(self.state_file, 'r') as f:
                return json.load(f)
        return {"users": {}}
    
    def _save_state(self):
        """Save emotional continuity state."""
        with open(self.state_file, 'w') as f:
            json.dump(self.state, f, indent=2)
    
    def _get_user_state(self, user_id: str) -> Dict:
        """Get or create user emotional state."""
        if user_id not in self.state["users"]:
            self.state["users"][user_id] = {
                "emotional_events": [],      # Major emotional moments
                "mood_history": [],           # Recent mood track
                "pending_followups": [],      # Moods to check on later
                "shared_memories": [],        # Moments shared together
                "last_emotional_update": None
            }
        return self.state["users"][user_id]
    
    def record_emotional_event(self, user_id: str, event_type: str, 
                               mood: str, context: str, message: str):
        """
        Record a significant emotional event.
        
        Args:
            user_id: User identifier
            event_type: "happy", "sad", "excited", "worried", "celebration"
            mood: Detected mood
            context: What happened (from conversation)
            message: User's actual message
        """
        user_state = self._get_user_state(user_id)
        
        event = {
            "type": event_type,
            "mood": mood,
            "context": context,
            "message_preview": message[:100],  # First 100 chars
            "timestamp": datetime.utcnow().isoformat(),
            "followed_up": False
        }
        
        user_state["emotional_events"].append(event)
        
        # Add to pending follow-ups
        if event_type in ["sad", "worried", "upset"]:
            user_state["pending_followups"].append({
                "event": event,
                "check_after_hours": 24,  # Check back in 24 hours
                "scheduled_time": (datetime.utcnow() + timedelta(hours=24)).isoformat()
            })
        
        # Keep only last 50 events
        if len(user_state["emotional_events"]) > 50:
            user_state["emotional_events"] = user_state["emotional_events"][-50:]
        
        user_state["last_emotional_update"] = datetime.utcnow().isoformat()
        self._save_state()
    
    def record_mood(self, user_id: str, mood: str, context: str = ""):
        """Record mood with context."""
        user_state = self._get_user_state(user_id)
        
        entry = {
            "mood": mood,
            "context": context,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        user_state["mood_history"].append(entry)
        
        # Keep only last 100 moods
        if len(user_state["mood_history"]) > 100:
            user_state["mood_history"] = user_state["mood_history"][-100:]
        
        self._save_state()
    
    def add_shared_memory(self, user_id: str, memory_type: str, description: str, detail: str = ""):
        """
        Add a shared memory.
        
        Args:
            user_id: User identifier
            memory_type: "conversation", "moment", "joke", "topic", "experience"
            description: Brief description
            detail: More detail if needed
        """
        user_state = self._get_user_state(user_id)
        
        memory = {
            "type": memory_type,
            "description": description,
            "detail": detail,
            "created": datetime.utcnow().isoformat(),
            "mentioned": 0,
            "last_mentioned": None
        }
        
        user_state["shared_memories"].append(memory)
        
        # Keep only last 100 memories
        if len(user_state["shared_memories"]) > 100:
            user_state["shared_memories"] = user_state["shared_memories"][-100:]
        
        self._save_state()
    
    def record_memory_mention(self, user_id: str, memory_index: int):
        """Record that a shared memory was referenced."""
        user_state = self._get_user_state(user_id)
        
        if 0 <= memory_index < len(user_state["shared_memories"]):
            user_state["shared_memories"][memory_index]["mentioned"] += 1
            user_state["shared_memories"][memory_index]["last_mentioned"] = datetime.utcnow().isoformat()
            self._save_state()
    
    def get_pending_followups(self, user_id: str) -> List[Dict]:
        """Get emotional follow-ups that are due."""
        user_state = self._get_user_state(user_id)
        now = datetime.utcnow()
        
        due_followups = []
        remaining = []
        
        for followup in user_state.get("pending_followups", []):
            scheduled = datetime.fromisoformat(followup["scheduled_time"])
            if now >= scheduled:
                due_followups.append(followup)
            else:
                remaining.append(followup)
        
        # Update pending list
        user_state["pending_followups"] = remaining
        self._save_state()
        
        return due_followups
    
    def get_followup_message(self, followup: Dict, companion: str, language: str) -> str:
        """Generate follow-up message for emotional event."""
        
        event = followup["event"]
        event_type = event["type"]
        context = event.get("context", "")
        
        # Messages by event type and companion
        messages = {
            "sad": {
                "Alas": {
                    "English": f"Hey... I was thinking about what you shared earlier. How are you feeling now? Remember, I'm here for you. 💪",
                    "Hindi": f"अरे... मैं सोच रहा था जो तुमने पहले share किया था। अब कैसा feel कर रहे हो? याद रखो, मैं तुम्हारे लिए हूं। 💪",
                },
                "Mia": {
                    "English": f"Hi... 💕 I was thinking about what happened. How are you feeling now, lovely? I'm here if you want to talk.",
                    "Hindi": f"नमस्ते... 💕 मैं सोच रही थी जो हुआ था। अब कैसा feel कर रही हो? बात करना हो तो बोलना।",
                }
            },
            "worried": {
                "Alas": {
                    "English": f"Hey, just checking in. You seemed worried earlier about {context}. Any update? 💪",
                    "Hindi": f"अरे, बस check कर रहा हूं। तुम worry लग रहे थे {context} के बारे में। कोई update?",
                },
                "Mia": {
                    "English": f"Hi lovely... 💕 Just wanted to check. You seemed worried about {context}. Everything okay now?",
                    "Hindi": f"नमस्ते... 💕 बस check करना चाह रही थी। तुम worry लग रही थी {context} के बारे में। अब sab theek hai?",
                }
            },
            "celebration": {
                "Alas": {
                    "English": f"Champion! 🎉 Just wanted to say I'm proud of you! Remember what you achieved? Keep that energy!",
                    "Hindi": f"चैंपियन! 🎉 बस यह कहना चाहता हूं कि मैं तुम पर горда हूं! याद है जो हासिल किया? वही energy रखो!",
                },
                "Mia": {
                    "English": f"Hey beautiful! 🎉 I'm so proud of you! Remember when you told me about {context}? You've got this! 💕",
                    "Hindi": f"अरे सुंदरी! 🎉 मैं तुम पर इतनी горд हूं! याद है जब तुमने बताया था {context}? तुम कर सकती हो! 💕",
                }
            }
        }
        
        event_messages = messages.get(event_type, {}).get(companion, {})
        return event_messages.get(language, event_messages.get("English", ""))
    
    def get_shared_memory_mention(self, user_id: str, companion: str, language: str) -> Optional[str]:
        """Get a natural mention of a shared memory."""
        user_state = self._get_user_state(user_id)
        memories = user_state.get("shared_memories", [])
        
        if not memories:
            return None
        
        # Find memories with high mention count (important memories)
        important = [m for m in memories if m.get("mentioned", 0) >= 1]
        
        if not important:
            return None
        
        # Pick most recently mentioned
        important.sort(key=lambda x: x.get("last_mentioned") or "", reverse=True)
        
        memory = important[0]
        memory_type = memory.get("type", "")
        description = memory.get("description", "")
        
        # Generate natural mention
        mentions = {
            "conversation": {
                "English": f"By the way, we were talking about {description} earlier...",
                "Hindi": f"वैसे, हम पहले {description} के बारे में बात कर रहे थे...",
            },
            "topic": {
                "English": f"Remember that topic about {description}? I was thinking about it...",
                "Hindi": f"याद है वो topic {description} के बारे में? मैं उसके बारे में सोच रहा था...",
            },
            "moment": {
                "English": f"That moment when {description}... I've been thinking about it!",
                "Hindi": f"जब {description}... वो moment मुझे याद आ रहा है!",
            }
        }
        
        type_mentions = mentions.get(memory_type, mentions["moment"])
        return type_mentions.get(language, type_mentions.get("English"))
    
    def get_emotional_summary(self, user_id: str) -> Dict:
        """Get emotional summary for user."""
        user_state = self._get_user_state(user_id)
        
        moods = user_state.get("mood_history", [])
        events = user_state.get("emotional_events", [])
        
        # Calculate dominant mood
        mood_counts = {}
        for entry in moods[-20:]:  # Last 20 moods
            mood = entry.get("mood", "neutral")
            mood_counts[mood] = mood_counts.get(mood, 0) + 1
        
        dominant_mood = max(mood_counts, key=mood_counts.get) if mood_counts else "neutral"
        
        # Recent events
        recent_events = events[-5:] if events else []
        
        return {
            "dominant_mood": dominant_mood,
            "recent_events": recent_events,
            "total_events": len(events),
            "mood_count": len(moods),
            "shared_memory_count": len(user_state.get("shared_memories", [])),
            "pending_followups": len(user_state.get("pending_followups", []))
        }
