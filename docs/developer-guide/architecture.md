# 🏗️ Architecture Guide

Alasmia's internal architecture.

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      User Interface                          │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────────┐  │
│  │ Telegram│  │ WhatsApp│  │ Discord │  │    CLI      │  │
│  └────┬────┘  └────┬────┘  └────┬────┘  └──────┬──────┘  │
└───────┼────────────┼────────────┼───────────────┼──────────┘
        │            │            │               │
        └────────────┴────────────┴───────────────┘
                            │
                    ┌───────▼───────┐
                    │  Integration  │
                    │     Layer     │
                    └───────┬───────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
┌───────▼───────┐   ┌───────▼───────┐   ┌───────▼───────┐
│    Agent      │   │     Core      │   │    Models    │
│    Layer      │   │    Services   │   │    Layer     │
│               │   │               │   │               │
│ • Proactive   │   │ • Scheduler  │   │ • any OpenAI-compatible API    │
│ • Emotional   │   │ • State Mgr  │   │ • OpenAI     │
│ • Memory      │   │ • Analytics  │   │ • Anthropic  │
│ • Learning    │   │               │   │ • Local LLM │
└───────────────┘   └───────────────┘   └───────────────┘
```

## Directory Structure

```
Alasmia/
├── alasmia/                    # Main package
│   ├── agent/                  # AI core
│   │   ├── brain.py           # Main agent logic
│   │   ├── proactive_engine.py # Proactive AI
│   │   ├── emotional_continuity.py # Emotion handling
│   │   ├── memory.py          # Memory system
│   │   ├── emotion_tracker.py # Emotion detection
│   │   ├── interest_tracker.py # Interest learning
│   │   ├── milestone.py       # Relationship milestones
│   │   ├── mood_handler.py    # Mood management
│   │   ├── personality.py     # Personality system
│   │   ├── learning.py        # Continuous learning
│   │   └── prompts.py         # Prompt templates
│   ├── core/                   # System services
│   │   ├── scheduler.py       # Cron scheduling
│   │   ├── enhanced_scheduler.py # Advanced scheduling
│   │   ├── state_manager.py  # State persistence
│   │   └── analytics.py       # Usage analytics
│   ├── integrations/          # Platform integrations
│   │   ├── telegram_bot.py   # Telegram
│   │   ├── whatsapp_bot.py   # WhatsApp
│   │   ├── discord_bot.py    # Discord
│   │   └── cli_chat.py       # CLI interface
│   ├── models/                 # LLM providers
│   │   ├── model_loader.py    # Dynamic loading
│   │   └── providers.py      # Provider configs
│   └── config/                # Configuration
│       └── settings.yaml      # Settings
├── docs/                       # Documentation
├── tests/                      # Test suites
├── main.py                    # Entry point
└── requirements.txt           # Dependencies
```

## Component Descriptions

### Agent Layer

**brain.py** - Central agent orchestrator
- Routes messages to appropriate handlers
- Manages conversation flow
- Coordinates sub-systems

**proactive_engine.py** - Autonomous outreach
- Decides when to initiate contact
- Generates proactive messages
- Respects quiet hours

**emotional_continuity.py** - Emotional memory
- Tracks emotional patterns
- Maintains emotional context
- Enables empathetic responses

### Core Services

**scheduler.py** - Time-based automation
- Executes scheduled tasks
- Manages daily rhythm

**state_manager.py** - State persistence
- Saves/restores state
- Handles graceful shutdown

### Integrations

Each platform has its own adapter that:
- Converts platform-specific formats to unified format
- Handles authentication
- Manages rate limits

## Data Flow

```
User Message
    │
    ▼
Platform Adapter (telegram_bot.py)
    │
    ▼
Integration Layer (normalize)
    │
    ▼
Agent Layer (brain.py)
    │
    ├──► Memory System (check history)
    │
    ├──► Emotion Tracker (analyze)
    │
    ├──► Proactive Engine (should respond?)
    │
    ├──► Model Layer (generate response)
    │
    └──► Response
    │
    ▼
Platform Adapter (format for platform)
    │
    ▼
Send to User
```

## State Management

Alasmia maintains state across:

1. **Conversation state** - Current session context
2. **Persistent state** - User memories, preferences
3. **System state** - Schedules, configurations

## Extension Points

The architecture supports extension via:

1. **New Platforms** - Add adapter in `integrations/`
2. **New Memory Types** - Extend `memory.py`
3. **New Providers** - Add to `models/providers.py`
4. **Skills System** - Add to `optional-skills/` (planned)