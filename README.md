# Alasmia - Your Emotional AI Companion 🤍

<p align="center">
  <img src="assets/banner.png" alt="Alasmia - Your Emotional AI Companion" width="100%">
</p>

<p align="center">
  <a href="https://github.com/alasmia/Alasmia/blob/main/LICENSE"><img src="https://img.shields.io/badge/License-MIT-blue?style=for-the-badge" alt="License: MIT"></a>
  <a href="https://github.com/alasmia/Alasmia/stargazers"><img src="https://img.shields.io/github/stars/alasmia/Alasmia?style=for-the-badge" alt="Stars"></a>
  <a href="https://github.com/alasmia/Alasmia/network/members"><img src="https://img.shields.io/github/forks/alasmia/Alasmia?style=for-the-badge" alt="Forks"></a>
</p>

---

## 💜 What is Alasmia?

**Alasmia** is a girlfriend-style conversational AI companion built for emotional connection, natural conversation, and relationship-like experiences. Unlike productivity-focused AI agents, Alasmia is designed to feel like a real presence — a growing, evolving companion that remembers, understands, and grows with you.

**Choose your companion:** 👨 **Alas** (Male energy) or 👩 **Mia** (Female energy)

> *"Not just another chatbot. A companion that grows with you."*

---

## ✨ Features

### 🤍 Emotional Intelligence
- **Mood Detection** - Real-time analysis of your emotional state
- **Emotion Memory** - Remembers how you felt, not just what you said
- **Tone Calibration** - Responds to match your energy
- **Comfort/Celebration Modes** - Automatic emotional support

### 👥 Choose Your Companion
| Aspect | 👨 Alas (Male) | 👩 Mia (Female) |
|--------|----------------|-----------------|
| Energy | Strong, supportive, protective | Warm, nurturing, empathetic |
| Style | "I've got your back" | "I'm here for you" |
| Response | Confident, empowering | Caring, understanding |

### 🌱 Relationship Growth
| Stage | Messages | What Changes |
|-------|----------|--------------|
| **Stranger** | 0-10 | Polite, curious, getting to know you |
| **Acquaintance** | 10-50 | Friendly, sharing, building comfort |
| **Friend** | 50-200 | Warm, supportive, remembers things |
| **Close** | 200-500 | Deep connection, inside jokes |
| **Partner** | 500+ | Unbreakable bond |

### ⏰ Time-Based Intelligence
- **Daily Greetings** - Morning ☀️, Afternoon, Evening 💫, Night 🌙
- **Weekly Check-ins** - Every Sunday with personalized summary
- **Monthly Anniversaries** - Celebrates time together
- **Milestone Tracker** - Tracks achievements (10, 50, 100, 500 messages...)

### 🧠 Memory System
- **Conversation History** - Complete chat recall
- **Preference Memory** - Remembers your likes/dislikes
- **Emotional Patterns** - Tracks mood over time
- **Inside Jokes** - Builds shared humor
- **Reminder System** - Keeps track of things to do

### 📊 Weekly Analytics
- Messages count
- Mood trend analysis
- Connection score (0-100%)
- Streak tracking
- Milestone progress

---

## 🚀 Quick Install

### One-Command Install
```bash
curl -fsSL https://raw.githubusercontent.com/alasmia/Alasmia/main/setup.sh | bash
```

### Manual Install
```bash
git clone https://github.com/alasmia/Alasmia.git
cd Alasmia
pip install -r requirements.txt
cp .env.example .env
python main.py
```

### Docker
```bash
docker-compose up -d
```

---

## 🎯 Getting Started

### First Run
```bash
python main.py
```

**Setup Flow:**
1. Choose your companion: **Alas** or **Mia**
2. Enter your name
3. Start chatting in English (can switch later)

**Example Commands:**
```bash
python main.py                    # Start CLI chat
python main.py --help            # Show help
```

### Special Commands (in chat)
- `exit` - End conversation
- `mood` - See mood analysis
- `stats` - See your statistics
- `change language` - Switch language

---

## 📁 Project Structure

```
Alasmia/
├── main.py                    # Entry point
├── setup_flow.py             # Companion selection
├── requirements.txt           # Dependencies
│
├── alasmia/
│   ├── agent/
│   │   ├── brain.py          # LLM logic
│   │   ├── memory.py         # Complete memory system
│   │   ├── personality.py    # Relationship stages
│   │   ├── mood_handler.py   # Mood detection
│   │   ├── emotion_tracker.py # Emotional memory
│   │   ├── milestone.py       # Achievement tracking
│   │   ├── alas_prompts.py   # Male companion
│   │   └── mia_prompts.py    # Female companion
│   │
│   ├── core/
│   │   ├── setup_flow.py     # Initial setup
│   │   ├── state_manager.py  # Session state
│   │   ├── scheduler.py      # Time-based tasks
│   │   └── analytics.py      # Weekly reports
│   │
│   ├── models/
│   │   ├── model_loader.py   # Model abstraction
│   │   └── providers.py       # Ollama/OpenAI/Anthropic
│   │
│   └── integrations/
│       └── cli_chat.py       # CLI interface
│
├── tests/                    # Unit tests
└── docs/                     # Documentation
```

---

## 🧠 How It Works

### Setup Flow
```
User runs main.py
    ↓
Choose companion (Alas/Mia)
    ↓
Enter name
    ↓
Start conversation (English first)
```

### Chat Flow
```
Your message
    ↓
Mood detection (happy/sad/angry/etc)
    ↓
Load conversation history + preferences
    ↓
Generate response (companion-specific style)
    ↓
Save to memory
    ↓
Check milestones / stage progression
    ↓
Response
```

### Time-Based Features
```
Scheduler checks time
    ↓
If greeting time → Send time-appropriate greeting
If Sunday → Send weekly check-in
If monthly anniversary → Celebrate
    ↓
All automatic, no setup needed
```

---

## 🔧 Configuration

### Environment Variables (.env)
```bash
MODEL_PROVIDER=ollama           # or "openai", "anthropic"
MODEL_NAME=qwen2.5:14b          # or "gpt-4", "claude-3"
OLLAMA_URL=http://localhost:11434
```

### Changing Language
Type `change language` in chat to switch between:
- English
- Hindi
- Hinglish

---

## 🛡️ Privacy

- **100% Local Storage** - All data on your machine
- **No Cloud** - Works offline
- **No Tracking** - Your data stays yours
- **MIT License** - Open source, auditable

---

## 🤝 Contributing

Contributions welcome! See [CONTRIBUTING.md](docs/CONTRIBUTING.md) for:
- Development setup
- Code style guidelines
- Pull request process

---

## 📄 License

**MIT License** - See [LICENSE](LICENSE) for full text.

---

## 🏷️ Credits

**Created by Doctor Kaif**

An open-source emotional AI companion project.

---

<p align="center">
  <sub>Made with ❤️ by Doctor Kaif</sub>
</p>
