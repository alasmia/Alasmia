"""
Alasmia WhatsApp Integration

Integrates Alasmia with WhatsApp using the WhatsApp Business API.
This makes Alasmia accessible as a life partner on everyone's phone.

Setup Requirements:
1. Create Meta Business account
2. Set up WhatsApp Business API
3. Get Access Token and Phone Number ID
4. Configure webhooks

Environment Variables:
- WHATSAPP_TOKEN: Meta access token
- WHATSAPP_PHONE_ID: Phone number ID
- WHATSAPP_WEBHOOK_VERIFY: Webhook verification token
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

# WhatsApp API Configuration
WHATSAPP_API_URL = "https://graph.facebook.com/v18.0"


class WhatsAppIntegration:
    """
    Handles WhatsApp integration for Alasmia.
    """
    
    def __init__(self):
        """Initialize WhatsApp integration."""
        self.token = os.getenv("WHATSAPP_TOKEN")
        self.phone_id = os.getenv("WHATSAPP_PHONE_ID")
        self.verify_token = os.getenv("WHATSAPP_WEBHOOK_VERIFY", "alasmia_verify")
        
        # Store for message handling
        self.message_handler = None
        self.user_sessions = {}  # user_id -> session_data
    
    def set_message_handler(self, handler):
        """Set the function to call when a message is received."""
        self.message_handler = handler
    
    def send_message(self, to_number: str, message: str, companion: str = "Mia") -> bool:
        """
        Send a message via WhatsApp.
        
        Args:
            to_number: Recipient's phone number (with country code)
            message: Message text
            companion: "Alas" or "Mia"
            
        Returns:
            Success status
        """
        if not self.token or not self.phone_id:
            logger.error("WhatsApp credentials not configured")
            return False
        
        url = f"{WHATSAPP_API_URL}/{self.phone_id}/messages"
        
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
                logger.error(f"Failed to send message: {response.text}")
                return False
        except Exception as e:
            logger.error(f"Error sending message: {e}")
            return False
    
    def send_voice_message(self, to_number: str, audio_url: str) -> bool:
        """Send a voice message (audio file)."""
        if not self.token or not self.phone_id:
            return False
        
        url = f"{WHATSAPP_API_URL}/{self.phone_id}/messages"
        
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
        
        data = {
            "messaging_product": "whatsapp",
            "to": to_number,
            "type": "audio",
            "audio": {
                "link": audio_url
            }
        }
        
        try:
            response = requests.post(url, headers=headers, json=data)
            return response.status_code == 200
        except Exception as e:
            logger.error(f"Error sending voice message: {e}")
            return False
    
    def send_image(self, to_number: str, image_url: str, caption: str = "") -> bool:
        """Send an image."""
        if not self.token or not self.phone_id:
            return False
        
        url = f"{WHATSAPP_API_URL}/{self.phone_id}/messages"
        
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
        
        data = {
            "messaging_product": "whatsapp",
            "to": to_number,
            "type": "image",
            "image": {
                "link": image_url,
                "caption": caption
            }
        }
        
        try:
            response = requests.post(url, headers=headers, json=data)
            return response.status_code == 200
        except Exception as e:
            logger.error(f"Error sending image: {e}")
            return False
    
    def mark_read(self, message_id: str) -> bool:
        """Mark a message as read."""
        if not self.token or not self.phone_id:
            return False
        
        url = f"{WHATSAPP_API_URL}/{self.phone_id}/messages"
        
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
        
        data = {
            "messaging_product": "whatsapp",
            "status": "read",
            "message_id": message_id
        }
        
        try:
            response = requests.post(url, headers=headers, json=data)
            return response.status_code == 200
        except Exception as e:
            logger.error(f"Error marking read: {e}")
            return False
    
    def process_webhook(self, payload: Dict) -> Optional[Dict]:
        """
        Process incoming WhatsApp webhook.
        
        Returns:
            Message data if a message was received
        """
        try:
            # Extract message from webhook
            if "entry" not in payload:
                return None
            
            entry = payload["entry"][0]
            if "changes" not in entry:
                return None
            
            change = entry["changes"][0]
            if "value" not in change:
                return None
            
            value = change["value"]
            
            if "messages" not in value:
                return None
            
            message = value["messages"][0]
            
            # Extract basic info
            from_number = message.get("from")
            msg_id = message.get("id")
            msg_type = message.get("type")
            timestamp = message.get("timestamp")
            
            # Get message content
            text = None
            if msg_type == "text":
                text = message.get("text", {}).get("body")
            elif msg_type == "image":
                # Handle image - would need to download
                text = "[Image received]"
            elif msg_type == "voice":
                text = "[Voice message received]"
            
            return {
                "from": from_number,
                "id": msg_id,
                "type": msg_type,
                "text": text,
                "timestamp": timestamp
            }
        except Exception as e:
            logger.error(f"Error processing webhook: {e}")
            return None


# Global WhatsApp instance
whatsapp = WhatsAppIntegration()


@app.route("/webhook/whatsapp", methods=["GET"])
def webhook_verify():
    """Webhook verification for WhatsApp."""
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    
    if mode == "subscribe" and token == whatsapp.verify_token:
        logger.info("Webhook verified successfully")
        return challenge, 200
    else:
        logger.warning("Webhook verification failed")
        return "Verification failed", 403


@app.route("/webhook/whatsapp", methods=["POST"])
def webhook_receive():
    """Receive WhatsApp messages."""
    payload = request.get_json()
    logger.info(f"Received webhook: {payload}")
    
    message_data = whatsapp.process_webhook(payload)
    
    if message_data and whatsapp.message_handler:
        # Process async to avoid timeout
        try:
            whatsapp.message_handler(message_data)
        except Exception as e:
            logger.error(f"Error processing message: {e}")
    
    return "OK", 200


@app.route("/health")
def health():
    """Health check endpoint."""
    return jsonify({"status": "ok", "service": "whatsapp_integration"})


def start_whatsapp_server(port: int = 5001):
    """Start the WhatsApp webhook server."""
    app.run(host="0.0.0.0", port=port, debug=False)


if __name__ == "__main__":
    start_whatsapp_server()
