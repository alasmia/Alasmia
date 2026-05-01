# Alasmia Architecture

## System Overview

Alasmia is a modular emotional AI companion built with Python. It uses a layered architecture to separate concerns and enable easy extensibility.

## Architecture Layers

```
┌─────────────────────────────────────────────────────────────┐
│                     USER INTERFACES                         │
│    ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  │
│    │ CLI Chat │  │ Telegram │  │ Discord  │  │  Web UI  │  │
│    └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘  │
└─────────┼─────────────┼─────────────┼─────────────┼─────────┘
          │             │             │             │
          └─────────────┴──────┬──────┴─────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────┐
│                     INTEGRATION LAYER                        │
│    ┌──────────────────────────────────────────────────┐     │
│    │              Integration Router                    │     │
│    │    (Routes messages to correct platform)         │     │
│    └──────────────────────────────────────────────────┘     │
└──────────────────────────────┬──────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────┐
│                      AGENT LAYER                             │
│  ┌─────────────────────────────────────────────────────┐     │
│  │                      BRAIN                          │     │
│  │        LLM interaction & response generation        │     │
│  └─────────────────────────────────────────────────────┘     │
│                                                              │
│  ┌───────────┐  ┌────────────┐  ┌───────────┐  ┌────────┐  │
│  │ PERSONA-  │  │   LEARN-   │  │  PROMPTS  │  │ BRAIN  │  │
│  │   LITY    │  │    ING     │  │           │  │        │  │
│  │           │  │            │  │           │  │        │  │
│  │ Stages:   │  │ Feedback   │  │ System    │  │ Memory │  │
│  │ Stranger  │  │ Processing │  │ Prompts   │  │ Access │  │
│  │ Acquaint  │  │            │  │ Stage-     │  │        │  │
│  │ Friend    │  │ Correction │  │ specific  │  │ Context│  │
│  │ Close     │  │ Learning   │  │ prompts   │  │ Window │  │
│  │ Partner   │  │            │  │           │  │        │  │
│  └─────┬─────┘  └─────┬──────┘  └───────────┘  └────────┘  │
└────────┼──────────────┼─────────────────────────────────────┘
         │              │
┌────────▼──────────────▼─────────────────────────────────────┐
│                    MEMORY LAYER                             │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐   │
│  │                    MEMORY MANAGER                     │   │
│  │                                                      │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐   │   │
│  │  │ Short-Term  │  │  Long-Term  │  │   Vector    │   │   │
│  │  │   (Dict)    │  │  (SQLite)   │  │  (ChromaDB) │   │   │
│  │  │             │  │             │  │             │   │   │
│  │  │ - Current   │  │ - User      │  │ - Semantic  │   │   │
│  │  │   session   │  │   profiles  │  │   search    │   │   │
│  │  │ - Context   │  │ - History   │  │ - Similarity│   │   │
│  │  │ - Temp      │  │ - Prefs     │  │   lookup    │   │   │
│  │  └─────────────┘  └─────────────┘  └─────────────┘   │   │
│  └──────────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────┐
│                     MODEL LAYER                             │
│                                                              │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐            │
│  │  OLLAMA    │  │  OPENAI    │  │ ANTHROPIC  │            │
│  │  Provider  │  │  Provider  │  │  Provider  │            │
│  └────────────┘  └────────────┘  └────────────┘            │
│                                                              │
│  ┌────────────────────────────────────────────────────┐     │
│  │                  MODEL LOADER                       │     │
│  │         Unified interface for all providers         │     │
│  └────────────────────────────────────────────────────┘     │
└──────────────────────────────────────────────────────────────┘
```

## Module Details

### 1. Agent Modules

#### Brain (`brain.py`)
- Handles LLM interaction
- Manages context window
- Compresses history when needed
- Generates responses

#### Personality (`personality.py`)
- Manages relationship stages
- Generates stage-appropriate prompts
- Tracks stage progression
- Language detection

#### Memory (`memory.py`)
- SQLite for user profiles and history
- In-memory cache for short-term
- User preference storage
- Message history management

#### Prompts (`prompts.py`)
- Stage-specific system prompts
- Language selection prompts
- Welcome messages
- Behavioral guidelines

#### Learning (`learning.py`)
- Feedback processing
- Correction learning
- Preference adaptation
- Response style adjustment

### 2. Integration Modules

#### CLI Chat (`cli_chat.py`)
- Rich terminal UI
- First-time user onboarding
- Conversation loop
- Exit handling

#### Telegram Bot (`telegram_bot.py`)
- Telegram API integration
- Command handlers (/start, /reset, /profile)
- Message processing
- Stage progression notifications

#### Discord Bot (`discord_bot.py`)
- Discord.py integration
- Slash commands
- Message events
- Embed responses

### 3. Model Layer

#### Model Loader (`model_loader.py`)
- Provider abstraction
- Model switching
- Unified generate() interface
- Streaming support

#### Providers (`providers.py`)
- Ollama: Local models
- OpenAI: GPT models
- Anthropic: Claude models

## Data Flow

### Message Processing

```
User Message
    ↓
[Integration Layer] - Identify platform, extract user/message
    ↓
[Memory Layer] - Load user context, preferences
    ↓
[Personality] - Get stage, generate system prompt
    ↓
[Brain] - Build prompt, call LLM
    ↓
[Model Layer] - Route to correct provider, generate
    ↓
[Brain] - Format response
    ↓
[Memory] - Save message to history
    ↓
[Integration] - Send response to user
```

### Response Generation

```
1. Receive user message
2. Load conversation history
3. Load user profile/preferences
4. Get relationship stage
5. Generate system prompt
6. Combine: system + history + current message
7. Send to LLM
8. Stream or receive full response
9. Save to memory
10. Return response
```

## Database Schema

### Users Table
```sql
CREATE TABLE user_preferences (
    id INTEGER PRIMARY KEY,
    user_id TEXT UNIQUE,
    name TEXT,
    language TEXT DEFAULT 'hinglish',
    relationship_stage TEXT DEFAULT 'stranger',
    message_count INTEGER DEFAULT 0,
    first_seen TIMESTAMP,
    last_seen TIMESTAMP,
    personality_prefs TEXT
);
```

### Conversations Table
```sql
CREATE TABLE conversations (
    id INTEGER PRIMARY KEY,
    user_id TEXT,
    role TEXT,  -- 'user' or 'assistant'
    content TEXT,
    timestamp TIMESTAMP,
    language TEXT DEFAULT 'hinglish'
);
```

## Configuration

### Environment Variables
- `.env` for user config
- `config/settings.yaml` for defaults
- Command-line for runtime overrides

### Priority Order
1. Environment variables (highest)
2. Command-line arguments
3. .env file
4. settings.yaml (lowest)

## Extension Points

### Adding New Platform
1. Create module in `integrations/`
2. Implement message receive/send interface
3. Register in main.py argument parser

### Adding New Model Provider
1. Create provider class in `providers.py`
2. Implement `generate()` and `generate_stream()`
3. Add to `ModelLoader.PROVIDERS` dict

### Adding New Personality Stage
1. Add stage to `PersonalityEngine.STAGES`
2. Add threshold to `STAGE_THRESHOLDS`
3. Create prompt in `PromptManager._stage_prompt()`

---

**Created by Doctor Kaif**
