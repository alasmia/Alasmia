#!/usr/bin/env python3
"""
Alasmia Web UI - FastAPI Application

Web interface for Alasmia using FastAPI.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv

from alasmia.models.model_loader import ModelLoader
from alasmia.agent.memory import MemoryManager
from alasmia.agent.personality import PersonalityEngine

load_dotenv()

# Initialize FastAPI app
app = FastAPI(title="Alasmia", description="Your Emotional AI Companion")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="templates")

# Initialize Alasmia core
model_loader = ModelLoader()
memory = MemoryManager()
personality = PersonalityEngine(memory)


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Render home page."""
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/chat")
async def chat(message: str, user_id: str = "web_user"):
    """Handle chat message."""
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


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy", "alasmia": "running"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
