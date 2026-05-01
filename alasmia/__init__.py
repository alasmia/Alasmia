"""Alasmia - Your Emotional AI Companion."""

__version__ = "0.2.0"
__author__ = "Doctor Kaif"

from alasmia.agent.brain import Brain
from alasmia.agent.memory import MemoryManager
from alasmia.agent.personality import PersonalityEngine
from alasmia.agent.mood_handler import MoodHandler
from alasmia.agent.emotion_tracker import EmotionTracker
from alasmia.agent.milestone import MilestoneTracker
from alasmia.models.model_loader import ModelLoader
from alasmia.core.setup_flow import SetupFlow
from alasmia.core.state_manager import StateManager
from alasmia.core.scheduler import Scheduler
from alasmia.core.analytics import Analytics

__all__ = [
    "Brain",
    "MemoryManager", 
    "PersonalityEngine",
    "MoodHandler",
    "EmotionTracker",
    "MilestoneTracker",
    "ModelLoader",
    "SetupFlow",
    "StateManager",
    "Scheduler",
    "Analytics",
]
