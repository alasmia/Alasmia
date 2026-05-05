#!/usr/bin/env python3
"""
Alasmia Web UI - FastAPI Application

Web interface for Alasmia using FastAPI.
"""

import sys
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from dotenv import load_dotenv

load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="Alasmia",
    description="Your AI Life Partner"
)

# Initialize Alasmia core
try:
    from alasmia.models.model_loader import ModelLoader
    from alasmia.agent.memory import MemoryManager
    from alasmia.agent.personality import PersonalityEngine
    
    model_loader = ModelLoader()
    memory = MemoryManager()
    personality = PersonalityEngine(memory)
    core_initialized = True
except ImportError as e:
    core_initialized = False
    print(f"Warning: Could not initialize core modules: {e}")


@app.get("/", response_class=HTMLResponse)
async def home():
    """Render home page."""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Alasmia - Your AI Life Partner</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; }
            .chat-container { border: 1px solid #ccc; border-radius: 10px; padding: 20px; }
            .message { margin: 10px 0; padding: 10px; border-radius: 5px; }
            .user { background: #e3f2fd; text-align: right; }
            .bot { background: #f3e5f5; text-align: left; }
            input { width: 70%; padding: 10px; margin-right: 10px; }
            button { padding: 10px 20px; background: #7c4dff; color: white; border: none; border-radius: 5px; }
        </style>
    </head>
    <body>
        <h1>💜 Alasmia</h1>
        <p>Your AI Life Partner</p>
        <div class="chat-container">
            <div id="chat"></div>
            <input type="text" id="message" placeholder="Type a message..." onkeypress="if(event.key==='Enter')send()">
            <button onclick="send()">Send</button>
        </div>
        <script>
            async function send() {
                const input = document.getElementById('message');
                const chat = document.getElementById('chat');
                const msg = input.value;
                if (!msg) return;
                
                chat.innerHTML += `<div class='message user'>You: ${msg}</div>`;
                input.value = '';
                
                const res = await fetch('/chat', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({message: msg})
                });
                const data = await res.json();
                chat.innerHTML += `<div class='message bot'>Alasmia: ${data.response}</div>`;
            }
        </script>
    </body>
    </html>
    """


@app.post("/chat")
async def chat(message: str, user_id: str = "web_user"):
    """Handle chat message."""
    if not core_initialized:
        return {"response": "Alasmia core not initialized. Run 'python main.py setup' first.", "user_id": user_id}
    
    try:
        # Get conversation history
        history = memory.get_conversation(user_id)
        
        # Generate response
        response = model_loader.generate(
            message=message,
            history=history,
            system_prompt=personality.get_system_prompt(user_id)
        )
        
        # Save to memory
        memory.add_message(user_id, "user", message)
        memory.add_message(user_id, "assistant", response)
        
        return {"response": response, "user_id": user_id}
    except Exception as e:
        return {"response": f"Error: {str(e)}", "user_id": user_id}


@app.get("/health")
async def health():
    """Health check endpoint."""
    return JSONResponse({"status": "healthy", "alasmia": "running"})


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run(app, host="0.0.0.0", port=port)