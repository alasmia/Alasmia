# Changelog

All notable changes to Alasmia will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [Unreleased]

### Added
- (Nothing yet)

### Changed
- (Nothing yet)

### Fixed
- (Nothing yet)

---

## [0.1.2] - Phase 2: Multi-Platform

### Added
- **Telegram Bot** — Full-featured Telegram bot with all Phase 1 + 2 features
  - Conversation flow (companion selection → name → chat)
  - All /commands working (/start, /help, /stats, /mood, /interests, /language, /companion)
  - Interest tracking
  - Emotional continuity
  - Shared experiences
  - Proactive engine

- **WhatsApp Integration** — Complete webhook-based integration
  - Send/receive messages
  - All Alasmia features available
  - Setup guide at /setup endpoint

### Changed
- Enhanced CLI with all Phase 1 + 2 features
- Improved multilingual greeting system
- Better platform-specific optimizations

### Fixed
- Language detection issues
- Interest tracking bugs
- Emotional continuity timing

---

## [0.1.1] - Phase 1 Enhancement

### Added
- **Emotional Continuity Engine** — Follows up on user's emotional state
  - Records emotional events (sad, happy, worried, celebration)
  - Schedules follow-ups (24h check-in when user was down)
  - Mood history tracking
  - Shared memory mentions

- **Shared Experiences Tracker** — Builds shared history
  - Tracks inside jokes and humor
  - Records deep conversation topics
  - Remembers user's goals
  - Tracks achievements mentioned
  - Records people user talks about
  - Generates natural mentions of past experiences

### Changed
- Enhanced CLI with emotional continuity integration
- System prompt includes emotional context
- Mood tracking integrated with continuity engine

### Fixed
- Memory leak in interest tracker
- Proactive message timing issues

---

## [0.1.0] - Phase 1: Proactive AI

### Added
- **Proactive Engine** — AI initiates conversations
  - Morning check-in (7-9 AM)
  - Afternoon check (12-2 PM)
  - Evening check (6-9 PM)
  - Night check (21-23 PM)
  - Follow-up on past conversations
  - Conversation pickups for later
  - Streak tracking

- **Interest Tracker** — Deep user interest memory
  - Tracks hobbies, goals, people, topics, preferences
  - 11 interest categories
  - Generates conversation starters from interests
  - Context passed to AI for personalized responses

- **Enhanced Scheduler** — Combined time-based system
  - Proactive messaging slots
  - Interest-based follow-ups
  - Weekly check-in support
  - Background scheduler thread

- **True Multilingual System** (v0.3.0 merged)
  - 15+ languages supported
  - Automatic language detection
  - All greetings in user's language
  - Memory persists language preference

### Changed
- Complete rewrite of CLI chat interface
- Enhanced memory system with user tracking
- Improved relationship stage progression

---

## [0.0.1] - Initial Release

### Added
- Basic CLI interface
- Companion selection (Alas/Mia)
- Basic mood detection
- Simple memory system
- English/Hindi language support

---

## Versioning

Alasmia uses [Semantic Versioning](https://semver.org/):
- **MAJOR** version: Breaking changes
- **MINOR** version: New features (Phase 1, Phase 2, etc.)
- **PATCH** version: Bug fixes and improvements

### Version Phases

| Phase | Focus | Versions |
|-------|-------|----------|
| **Phase 1** | Core AI Features | 0.1.0 - 0.1.x |
| **Phase 2** | Multi-Platform | 0.2.x |
| **Phase 3** | Voice & Media | 0.3.x |
| **Phase 4** | Advanced Features | 0.4.x |

---

## Migration Guides

### Upgrading to 0.1.x

If you're upgrading from 0.0.x:
1. Backup your data directory (`./data`)
2. Pull latest changes
3. Run `pip install -r requirements.txt`
4. Restart the application

### Downgrading

Not recommended. Some data structures may not be backwards compatible.

---

## Older Releases

For older releases, see [GitHub Releases](https://github.com/alasmia/Alasmia/releases).
