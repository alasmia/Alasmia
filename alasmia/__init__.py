"""
Alasmia - Your Emotional AI Companion

A girlfriend-style conversational AI agent built for emotional connection.
"""

__version__ = "0.1.0"
__author__ = "Doctor Kaif"

from alasmia.agent.brain import Brain
from alasmia.agent.memory import MemoryManager
from alasmia.agent.personality import PersonalityEngine
from alasmia.models.model_loader import ModelLoader

__all__ = [
    "Brain",
    "MemoryManager",
    "PersonalityEngine",
    "ModelLoader",
]
