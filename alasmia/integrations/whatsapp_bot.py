"""
Alasmia WhatsApp Integration 

Complete WhatsApp integration with:
 (Proactive, Interest, Emotional Continuity)
- Webhook-based message handling
- Multi-language support
- Voice message support (future)

Setup Instructions:
1. Create Meta Business account at business.facebook.com
2. Create WhatsApp Business app
3. Get Phone Number ID and Access Token
4. Set webhook URL to: https://your-domain.com/webhook/whatsapp

Environment Variables:
- WHATSAPP_TOKEN: Meta access token
- WHATSAPP_PHONE_ID: WhatsApp phone number ID
- WHATSAPP_WEBHOOK_VERIFY: Webhook verification token (set your own)
- WHATSAPP_API_VERSION: API version (default: latest)
"""

import os
import json
import logging
from datetime import datetime
from typing import Dict, Optional
from pathlib import Path

from flask import Flask, request, jsonify
import requests

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Configuration
WHATSAPP_API_URL = "https://graph.facebook.com"


class WhatsAppHandler:
    """
    Handles WhatsApp messages with all  + Features.
    """
    
    def __init__(self, token: str = None, phone_id: str = None):
        """Initialize WhatsApp handler."""
        self.token = token or os.getenv("WHATSAPP_TOKEN")
        self.phone_id = phone_id or os.getenv("WHATSAPP_PHONE_ID")
        self.verify_token = os.getenv("WHATSAPP_WEBHOOK_VERIFY", "alasmia_whatsapp_verify")
        self.api_version = os.getenv("WHATSAPP_API_VERSION", "latest")
        
        # Import Alasmia components
        self._init_alasmia()
    
    def _init_alasmia(self):
        """Initialize Alasmia components."""
        try:
            from alasmia.agent.brain import Brain
            from alasmia.agent.memory import MemoryManager
            from alasmia.agent.personality import PersonalityEngine
            from alasmia.agent.mood_handler import MoodHandler
            from alasmia.agent.proactive_engine import ProactiveEngine
            from alasmia.agent.interest_tracker import InterestTracker
            from alasmia.agent.emotional_continuity import EmotionalContinuity
            from alasmia.agent.shared_experiences import SharedExperiences
            from alasmia.core.scheduler import detect_language
            from alasmia.models.model_loader import ModelLoader
            
            self.model_loader = ModelLoader()
            self.memory = MemoryManager()
            self.personality = PersonalityEngine(self.memory)
            self.brain = Brain(self.model_loader)
            self.mood_handler = MoodHandler()
            self.proactive_engine = ProactiveEngine()
            self.interest_tracker = InterestTracker()
            self.emotional_continuity = EmotionalContinuity()
            self.shared_experiences = SharedExperiences()
            self.detect_language = detect_language
            
            self.initialized = True
            logger.info("Alasmia components initialized for WhatsApp")
        except Exception as e:
            logger.error(f"Failed to initialize Alasmia: {e}")
            self.initialized = False
    
    def process_message(self, message_data: Dict) -> Optional[str]:
        """
        Process incoming message and generate response.
        
        Args:
            message_data: Dict with from, text, type, etc.
            
        Returns:
            Response message string
        """
        if not self.initialized:
            return "Sorry, I'm not fully initialized yet. Please try again later."
        
        from_number = message_data.get("from")
        text = message_data.get("text", "")
        msg_type = message_data.get("type", "text")
        
        if msg_type != "text" or not text:
            return "I can only process text messages right now! 😊"
        
        user_id = f"whatsapp_{from_number}"
        
        # Get user info
        user_info = self.memory.get_user_info(user_id)
        language = "English"
        
        # Language detection
        if not user_info:
            language = self.detect_language(text)
            self.memory.create_user(
                user_id,
                name="Friend",
                companion_gender="female",
                language=language
            )
        else:
            language = user_info.get("language", "English")
        
        # Track interests
        detected_mood = self.mood_handler.detect_mood(text)
        self.interest_tracker.track_message(user_id, text, detected_mood)
        
        # Emotional continuity
        self.emotional_continuity.record_mood(user_id, detected_mood, text[:50])
        
        # Build system prompt
        system_prompt = self.personality.get_system_prompt(user_id)
        system_prompt += f"""
IMPORTANT - RESPOND IN USER'S LANGUAGE:
- The user speaks and prefers: {language}
- You MUST respond in {language} language
"""
        
        # Interest context
        interest_context = self.interest_tracker.get_memory_context(user_id)
        if interest_context:
            system_prompt += f"\n{interest_context}\n"
        
        # Mood context
        if detected_mood != "neutral":
            system_prompt += f"\nUser's current mood: {detected_mood.upper()}\n"
        
        # Get history
        history = self.memory.get_conversation(user_id, limit=20)
        
        # Generate response
        response = self.brain.think(
            message=text,
            history=history,
            system_prompt=system_prompt,
            context={"mood": detected_mood, "language": language}
        )
        
        # Save to memory
        self.memory.add_message(user_id, "user", text, detected_mood)
        self.memory.add_message(user_id, "assistant", response)
        self.memory.increment_message_count(user_id)
        
        # Shared experiences
        self.shared_experiences.analyze_and_record(user_id, text, response, detected_mood)
        
        return response
    
    def send_message(self, to_number: str, message: str) -> bool:
        """Send message via WhatsApp API."""
        if not self.token or not self.phone_id:
            logger.error("WhatsApp credentials not configured")
            return False
        
        url = f"{WHATSAPP_API_URL}/{self.api_version}/{self.phone_id}/messages"
        
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
        
        data = {
            "messaging_product": "whatsapp",
            "to": to_number,
            "type": "text",
            "text": {
                "preview_url": False,
                "body": message
            }
        }
        
        try:
            response = requests.post(url, headers=headers, json=data)
            if response.status_code == 200:
                logger.info(f"Message sent to {to_number}")
                return True
            else:
                logger.error(f"Failed to send: {response.text}")
                return False
        except Exception as e:
            logger.error(f"Error sending message: {e}")
            return False
    
    def process_webhook(self, payload: Dict) -> Optional[Dict]:
        """Process webhook payload and extract message."""
        try:
            if "entry" not in payload:
                return None
            
            entry = payload["entry"][0]
            if "changes" not in entry:
                return None
            
            change = entry["changes"][0]
            if "value" not in change:
                return None
            
            value = change["value"]
            
            if "messages" not in value or not value["messages"]:
                return None
            
            message = value["messages"][0]
            
            return {
                "from": message.get("from"),
                "id": message.get("id"),
                "type": message.get("type"),
                "text": message.get("text", {}).get("body") if message.get("type") == "text" else None,
                "timestamp": message.get("timestamp")
            }
        except Exception as e:
            logger.error(f"Error processing webhook: {e}")
            return None


# Global handler
whatsapp_handler = None


def get_handler() -> WhatsAppHandler:
    """Get or create WhatsApp handler."""
    global whatsapp_handler
    if whatsapp_handler is None:
        whatsapp_handler = WhatsAppHandler()
    return whatsapp_handler


@app.route("/webhook/whatsapp", methods=["GET"])
def webhook_verify():
    """Webhook verification endpoint."""
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    
    handler = get_handler()
    
    if mode == "subscribe" and token == handler.verify_token:
        logger.info("WhatsApp webhook verified")
        return challenge, 200
    else:
        logger.warning("Webhook verification failed")
        return "Verification failed", 403


@app.route("/webhook/whatsapp", methods=["POST"])
def webhook_receive():
    """Receive and process WhatsApp messages."""
    payload = request.get_json()
    logger.info(f"Received WhatsApp webhook: {payload}")
    
    handler = get_handler()
    
    if not handler.initialized:
        logger.error("Handler not initialized")
        return "OK", 200  # Return 200 to acknowledge receipt
    
    message_data = handler.process_webhook(payload)
    
    if message_data and message_data.get("text"):
        try:
            response = handler.process_message(message_data)
            if response:
                handler.send_message(message_data["from"], response)
        except Exception as e:
            logger.error(f"Error processing message: {e}")
    
    return "OK", 200


@app.route("/health")
def health():
    """Health check endpoint."""
    handler = get_handler()
    return jsonify({
        "status": "ok",
        "service": "whatsapp_integration",
        "initialized": handler.initialized if handler else False
    })


@app.route("/setup")
def setup_guide():
    """Show WhatsApp setup guide."""
    guide = """
    # WhatsApp Integration Setup
    
    ## Step 1: Create Meta Business Account
    1. Go to https://business.facebook.com
    2. Create a business account
    
    ## Step 2: Create WhatsApp Business App
    1. Go to https://developers.facebook.com
    2. Create new app -> WhatsApp Business
    3. Follow setup wizard
    
    ## Step 3: Get Credentials
    1. Note your Phone Number ID
    2. Generate a permanent access token
    
    ## Step 4: Configure Environment
    ```bash
    export WHATSAPP_TOKEN="your_access_token"
    export WHATSAPP_PHONE_ID="your_phone_number_id"
    export WHATSAPP_WEBHOOK_VERIFY="your_secret_verify_token"
    ```
    
    ## Step 5: Set Webhook
    1. Go to WhatsApp Business API settings
    2. Set webhook URL: `https://your-domain.com/webhook/whatsapp`
    3. Verify webhook with the token above
    
    ## Step 6: Test
    Send a message to your WhatsApp Business number!
    """
    return guide, 200, {"Content-Type": "text/markdown"}


def start_server(port: int = 5001):
    """Start the WhatsApp webhook server."""
    app.run(host="0.0.0.0", port=port, debug=False)


if __name__ == "__main__":
    start_server()
