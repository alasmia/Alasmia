# 🎭 Emotion Tracking

Alasmia's emotional intelligence system.

## How It Works

Alasmia tracks emotions in real-time:
- 😊 **Input Analysis** - Detects emotion from your messages
- 🎯 **Response Calibration** - Adjusts reply based on your mood
- 💜 **Empathy Engine** - Responds with appropriate empathy
- 🔄 **Continuity** - Remembers emotional patterns

## Emotion Categories

| Emotion | Detection Triggers | Response Style |
|---------|-------------------|----------------|
| Happy | 😊 😂 🎉 positive words | Enthusiastic, celebratory |
| Sad | 😢 😔 sad words | Gentle, comforting |
| Angry | 😠 😤 frustration | Calm, understanding |
| Anxious | 😰 😟 worry | Reassuring, grounding |
| Excited | 🤩 🚀 enthusiasm | Matching energy |
| Tired | 😴 😪 fatigue | Brief, caring |
| Neutral | 😊 | Normal response |

## Emotion Tracking in Action

```
You: I had a really rough day today
Alasmia: 😔 A rough day? I'm sorry to hear that. Want to talk about it, or should I just be here for you?

You: Work was exhausting
Alasmia: 💜 That sounds really draining. Take a breath - you're talking to someone who cares. What happened?
```

## Emotion Memory

Alasmia remembers your emotional patterns:

- What times of day you're usually stressed
- Topics that make you upset
- What helps you feel better
- Your coping preferences

```
You: I always feel anxious before presentations
Alasmia: I remember - presentations make you nervous. But you've done amazing每一次 time! Want me to help you practice?
```

## Mood Timeline

Track your emotional patterns over time:

```bash
# Check mood history
You: /mood
Alasmia: 📊 Your Mood Timeline (last 7 days):
- Monday: Stressed (work deadline)
- Tuesday: Happy (n8n workflow worked!)
- Wednesday: Neutral
- Thursday: Excited (new project idea)
- Friday: Relaxed
```

## Configuration

```yaml
emotions:
  enabled: true
  tracking: true
  empathy_level: high  # low, medium, high
  response_calibration: true
```

## Turn Off Emotion Tracking

If you prefer purely factual interactions:

```yaml
emotions:
  enabled: false
```

Or tell Alasmia directly:
```
You: Don't analyze my emotions, just respond to my words
Alasmia: Got it! I'll respond to the content of your messages without emotional analysis.
```