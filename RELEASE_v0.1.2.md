# 🎉 Alasmia v0.1.2 - Multi-Platform AI Life Partner

## ✨ What's New in v0.1.2

### 🚀 Phase 2 Complete - Multi-Platform Support

This release marks the completion of Phase 2, bringing Alasmia to multiple messaging platforms.

#### New Platforms
- ✅ **Telegram Bot Integration** - Full Telegram support with bot commands and streaming
- ✅ **WhatsApp Integration** - WhatsApp business API ready
- ✅ **Discord Bot Ready** - Discord bot framework in place

#### Core Features
- ✅ **Enhanced Proactive AI** - AI now reaches out first, doesn't wait
- ✅ **24/7 Availability Engine** - Always there like a real partner
- ✅ **Deep Memory System** - Remembers everything about you
- ✅ **Relationship Stages** - Stranger → Acquaintance → Friend → Close → Partner
- ✅ **Daily Rhythm System** - Morning greetings, check-ins, night routines

---

## 🆕 New Features Since v0.1.1

### AI Companion Core
- `proactive_engine.py` - Autonomous outreach without user prompting
- `emotional_continuity.py` - Maintains emotional context across sessions
- `shared_experiences.py` - "TV dekh rahe ho?" type shared awareness
- `emotion_tracker.py` - Tracks and responds to user emotions
- `interest_tracker.py` - Learns user interests over time
- `milestone.py` - Relationship milestone tracking

### Platform Layer
- `telegram_bot.py` - Full Telegram integration with streaming
- `whatsapp_bot.py` - WhatsApp integration
- `discord_bot.py` - Discord bot framework
- `cli_chat.py` - Enhanced CLI chat interface

### Smart Scheduling
- `enhanced_scheduler.py` - Advanced cron with proactive triggers
- Intelligent routine management (morning, afternoon, evening, night)

---

## 🔧 Technical Improvements

| Area | Improvement |
|------|-------------|
| **Memory** | Vector-based semantic memory with ChromaDB |
| **Emotions** | Real-time emotion tracking and response |
| **Scheduling** | Timezone-aware intelligent scheduling |
| **Platform** | Unified message handling across platforms |
| **Testing** | 3 new test suites (memory, personality, providers) |
| **CI/CD** | Full GitHub Actions pipeline |

---

## 📊 Architecture

```
Alasmia/
├── alasmia/
│   ├── agent/         # Core AI logic
│   │   ├── proactive_engine.py    # NEW: Autonomous AI
│   │   ├── emotional_continuity.py # NEW: Emotion memory
│   │   ├── memory.py               # Vector memory
│   │   └── ...
│   ├── core/          # System services
│   │   ├── enhanced_scheduler.py   # NEW: Smart scheduling
│   │   └── ...
│   ├── integrations/  # Platform integrations
│   │   ├── telegram_bot.py         # NEW
│   │   ├── whatsapp_bot.py         # NEW
│   │   ├── discord_bot.py          # NEW
│   │   └── cli_chat.py
│   ├── models/        # LLM providers
│   └── config/         # Configuration
├── docs/              # Documentation
├── tests/             # Test suites
└── .github/           # GitHub workflows
```

---

## 🎯 Phase 1 vs Phase 2

| Feature | Phase 1 (v0.1.0) | Phase 2 (v0.1.2) |
|---------|------------------|------------------|
| CLI Chat | ✅ Basic | ✅ Enhanced |
| Memory | ✅ Basic | ✅ Deep (vector) |
| Emotions | ❌ | ✅ Full tracking |
| Proactive | ❌ | ✅ 24/7 |
| Telegram | ❌ | ✅ Live |
| WhatsApp | ❌ | ✅ Ready |
| Discord | ❌ | ✅ Ready |
| Scheduling | ❌ | ✅ Smart cron |

---

## 🛠️ Installation

### Docker (Recommended)
```bash
# Pull latest
docker pull ghcr.io/alasmia/alasmia:latest

# Run with Telegram
docker run -d \
  --name alasmia \
  -e TELEGRAM_BOT_TOKEN=your_token \
  -e ALASMIA_MODEL=minimaxai/minimax-m2.7 \
  ghcr.io/alasmia/alasmia:latest
```

### From Source
```bash
git clone https://github.com/alasmia/Alasmia.git
cd Alasmia
pip install -r requirements.txt
python main.py
```

---

## 📈 What's Next?

### Phase 3 (Coming Soon)
- 🔜 **Voice Messages** - Audio responses
- 🔜 **Video Calls** - Face-to-face AI
- 🔜 **Advanced Memory** - Persistent conversation history
- 🔜 **Plugin System** - Extend Alasmia capabilities
- 🔜 **Web Dashboard** - Visual control panel

### Long Term Vision
- AI that truly knows you
- Cross-platform conversation continuity
- Emotional intelligence at human level
- Proactive life assistance

---

## 🐛 Bug Fixes

- Fixed memory persistence issues
- Fixed emotion tracking edge cases
- Fixed scheduling timezone bugs
- Improved response quality

---

## 📝 Full Changelog

### v0.1.2 (Current)
- ✅ Telegram integration
- ✅ WhatsApp integration
- ✅ Proactive AI engine
- ✅ Emotional continuity
- ✅ Enhanced memory
- ✅ Smart scheduling

### v0.1.1
- ✅ CLI chat improvements
- ✅ Personality system
- ✅ Interest tracking

### v0.1.0
- ✅ Initial release
- ✅ Basic memory
- ✅ CLI interface

---

## ❤️ Thank You

Built with love by **Doctor Kaif**  
Maintained by the **Alasmia Community**

---

**⭐ Star us on GitHub!**  
**🐛 Report bugs on GitHub Issues**  
**📖 Read the docs at docs.alasmia.ai**