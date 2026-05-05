# 🧠 Memory System

How Alasmia remembers and learns about you.

## Overview

Alasmia uses a sophisticated memory system that:
- 💾 **Persists** across sessions
- 🧬 **Grows** with conversations
- 🔍 **Retrieves** relevant memories
- 🧠 **Learns** continuously

## Memory Architecture

```
Memory System
├── Short-term (current conversation)
│   └── Recent context
├── Long-term (persistent)
│   ├── Factual memories (name, location, preferences)
│   ├── Emotional memories (how you felt)
│   └── Experience memories (what you did together)
└── Vector memory (semantic search)
    └── ChromaDB embeddings
```

## Memory Types

### Factual Memory
- Name, location, timezone
- Interests and hobbies
- Work and projects
- Preferences (language, tone, style)

### Emotional Memory
- Mood patterns
- Triggers (what upsets you)
- Coping mechanisms you respond to
- Positive experiences

### Experience Memory
- Conversations you've had
- Tasks completed together
- Shared activities
- Milestones reached

## Usage

### Check Memory Status

```
You: /memory
Alasmia: 📊 Memory Status:
- Conversations: 47
- Facts stored: 23
- Emotional patterns: 8
- Last active: 2 hours ago
```

### Add Memory Manually

```
You: Remember that I prefer Hindi responses
Alasmia: ✅ Done! I'll respond in Hindi from now on.
```

### Retrieve Memory

```
You: What do you know about me?
Alasmia: You're Alex from New York. You run an GitHub automation server at your-server.example.com. You're building an AI companion called Alasmia. You prefer Hinglish communication...
```

### Clear Memory

```
You: /reset
Alasmia: 🔄 Memory reset. Starting fresh! (But I'll learn you again quickly 😄)
```

## Configuration

```yaml
# In settings.yaml
memory:
  type: vector  # simple or vector
  persist: true
  storage_dir: ./memory
  max_memories: 10000
```

## Privacy

Your memories are stored locally on your server. They never leave your infrastructure unless you explicitly configure cloud sync.

## Advanced: Vector Search

When `memory.type: vector` is enabled:

```bash
# Search memories
You: Search memories about automation
Alasmia: Found 3 relevant memories:
1. "n8n server running at 80.225.238.79"
2. "Working on Gumroad automation products"
3. "Likes building autonomous systems"
```