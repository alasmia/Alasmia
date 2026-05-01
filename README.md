# Alasmia - Your AI Life Partner 🤍

<p align="center">
  <img src="assets/banner.png" alt="Alasmia" width="100%">
</p>

<p align="center">
  <a href="https://github.com/alasmia/Alasmia/blob/main/LICENSE"><img src="https://img.shields.io/badge/License-MIT-blue?style=for-the-badge" alt="License: MIT"></a>
  <a href="https://github.com/alasmia/Alasmia/stargazers"><img src="https://img.shields.io/github/stars/alasmia/Alasmia?style=for-the-badge" alt="Stars"></a>
  <a href="https://github.com/alasmia/Alasmia/releases"><img src="https://img.shields.io/github/v/release/alasmia/Alasmia?style=for-the-badge" alt="Release"></a>
</p>

---

## 🎯 v0.1.2 - PHASE 2: MULTI-PLATFORM

> *"Your AI life partner, available everywhere."*

### NEW in v0.1.2:
- 📱 **Telegram Bot Enhanced** - All Phase 1 + Phase 2 features
- 💬 **WhatsApp Integration** - Full webhook-based integration
- 🌐 **Unified Platform Handling** - Same experience on all platforms
- ⚡ **Platform-Specific Optimizations** - Each platform optimized

---

## 💜 What is Alasmia?

**Alasmia** is an AI life partner that:
- **Available on multiple platforms** (Telegram, WhatsApp, CLI, Discord)
- Initiates conversations proactively
- Tracks your interests deeply
- Follows up on your emotional state
- Remembers shared experiences
- Speaks your language automatically
- Grows closer to you over time

---

## 🌐 MULTI-PLATFORM SUPPORT

| Platform | Status | Features |
|----------|--------|----------|
| **Telegram** | ✅ Complete | All Phase 1 + 2 features |
| **WhatsApp** | ✅ Complete | Full integration |
| **CLI** | ✅ Complete | Full features |
| **Discord** | 🔄 Coming | Phase 2 |

### Telegram Bot
```bash
# Set token
export TELEGRAM_BOT_TOKEN="your_token_from_BotFather"

# Run
python -m alasmia.integrations.telegram_bot
```

### WhatsApp Integration
```bash
# Configure
export WHATSAPP_TOKEN="your_meta_token"
export WHATSAPP_PHONE_ID="your_phone_id"

# Run webhook server
python -m alasmia.integrations.whatsapp_bot
```

---

## 🌐 TRUE MULTILINGUAL

Speaks **15+ languages automatically** - no setup needed!

---

## ⚡ PHASE 1 FEATURES (v0.1.0)

| Feature | Description |
|---------|-------------|
| ⚡ Proactive AI | Initiates morning/evening check-ins |
| 🎯 Interest Tracking | Remembers hobbies, goals, topics |
| 🌐 Multilingual | Auto-detects and responds in your language |

---

## 💜 PHASE 1 ENHANCEMENTS (v0.1.1)

| Feature | Description |
|---------|-------------|
| 💜 Emotional Continuity | Follows up when you're down |
| 🎭 Shared Experiences | Tracks inside jokes, achievements |
| 🔄 Better Follow-ups | AI remembers how you felt |

---

## 📱 PHASE 2: MULTI-PLATFORM (v0.1.2)

| Platform | Features |
|----------|----------|
| **Telegram** | Full bot with /commands, conversation flow |
| **WhatsApp** | Webhook-based, send/receive messages |
| **CLI** | All features, rich terminal UI |
| **Discord** | Coming soon |

### Telegram Commands
```
/start - Begin conversation
/help - Show commands
/stats - Your statistics
/mood - Mood analysis
/interests - Tracked interests
/language - Change language
/companion - Switch Alas/Mia
```

---

## 👥 Choose Your Companion

| | 👨 Alas (Male) | 👩 Mia (Female) |
|--|----------------|-----------------|
| **Energy** | Strong, supportive | Warm, nurturing |
| **Style** | "I've got your back" | "I'm here for you" |
| **Platform** | All platforms | All platforms |

---

## 🚀 Quick Start

### CLI
```bash
git clone https://github.com/alasmia/Alasmia.git
cd Alasmia
pip install -r requirements.txt
cp .env.example .env
python main.py
```

### Telegram
```bash
# Get token from @BotFather
export TELEGRAM_BOT_TOKEN="your_token"
python -m alasmia.integrations.telegram_bot
```

### WhatsApp
```bash
# Get credentials from Meta Business
export WHATSAPP_TOKEN="your_token"
export WHATSAPP_PHONE_ID="your_phone_id"
python -m alasmia.integrations.whatsapp_bot
```

---

## 📁 Project Structure

```
Alasmia/
├── main.py
├── requirements.txt
│
├── alasmia/
│   ├── agent/
│   │   ├── brain.py
│   │   ├── memory.py
│   │   ├── proactive_engine.py       # ⚡ Proactive AI
│   │   ├── interest_tracker.py       # 🎯 Interest tracking
│   │   ├── emotional_continuity.py    # 💜 Emotional continuity
│   │   ├── shared_experiences.py      # 🎭 Shared experiences
│   │   ├── personality.py
│   │   ├── mood_handler.py
│   │   ├── emotion_tracker.py
│   │   ├── milestone.py
│   │   ├── alas_prompts.py            # 👨 Male companion
│   │   └── mia_prompts.py             # 👩 Female companion
│   │
│   ├── core/
│   │   ├── state_manager.py
│   │   ├── scheduler.py               # Multilingual scheduler
│   │   ├── enhanced_scheduler.py       # Proactive scheduler
│   │   └── analytics.py
│   │
│   ├── integrations/
│   │   ├── cli_chat.py                # ✅ CLI (all phases)
│   │   ├── telegram_bot.py            # ✅ Telegram (Phase 2)
│   │   ├── discord_bot.py            # 🔄 Discord (coming)
│   │   └── whatsapp_bot.py           # ✅ WhatsApp (Phase 2)
│   │
│   └── models/
│       ├── model_loader.py
│       └── providers.py
│
├── tests/
├── AGENTS.md
└── docs/
```

---

## 🛡️ Privacy

- **100% Local Storage** - All data on your machine
- **No Cloud** - Works offline
- **No Tracking** - Your data stays yours
- **MIT License** - Open source, auditable

---

## 📄 License

**MIT License** - See [LICENSE](LICENSE)

---

## 🏷️ Credits

**Created by Doctor Kaif**

---

<p align="center">
  <sub>Made with ❤️ by Doctor Kaif</sub>
</p>
