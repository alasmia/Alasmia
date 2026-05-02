# ⏰ Scheduling & Automation

Automated routines and proactive outreach.

## Daily Rhythm System

Alasmia follows a daily schedule to feel like a real companion:

| Time | Activity | Example |
|------|----------|---------|
| 🌅 7:00 AM | Morning greeting | "Good morning! Hope you slept well." |
| 🌞 12:00 PM | Afternoon check-in | "How's your day going?" |
| 🌙 6:00 PM | Evening check | "Any plans for tonight?" |
| 🌌 10:00 PM | Night routine | "Goodnight! Early start tomorrow?" |

## Setting Up Schedules

### Via Configuration

```yaml
scheduler:
  enabled: true
  timezone: Asia/Kolkata
  
routines:
  morning:
    enabled: true
    time: "07:00"
    message: "Good morning! How did you sleep?"
  
  afternoon:
    enabled: true
    time: "12:00"
    message: "How's your day going?"
  
  evening:
    enabled: true
    time: "18:00"
    message: "Any exciting plans for tonight?"
  
  night:
    enabled: true
    time: "22:00"
    message: "Goodnight! Rest well 💜"
```

### Via CLI

```bash
# Add a routine
alasmia schedule add "Daily check-in" --time 14:00 --message "How's your afternoon?"

# List all schedules
alasmia schedule list

# Remove a schedule
alasmia schedule remove "Daily check-in"
```

## Proactive Outreach

Alasmia reaches out based on:

1. **Time-based** - Greetings at scheduled times
2. **Event-based** - After X hours of silence
3. **Context-based** - "Saw your n8n is down, need help?"
4. **Emotion-based** - "You seemed stressed yesterday, doing better?"

### Configure Proactivity

```yaml
proactive:
  enabled: true
  max_contacts_per_day: 5
  respect_quiet_hours: true  # 10 PM - 7 AM
  learning: true  # Learns when you respond
```

## Cron Syntax

For advanced users, use cron expressions:

```yaml
schedules:
  weekly_report:
    cron: "0 9 * * 1"  # Every Monday at 9 AM
    message: "Here's your weekly summary..."
  
  backup_reminder:
    cron: "0 20 * * 0"  # Every Sunday 8 PM
    message: "Don't forget your weekly backup!"
```

## Interactive Scheduling

During conversation:

```
You: Remind me to check the server every day at 6 PM
Alasmia: ✅ Added! I'll ping you at 6 PM daily to check your server status.
```

## Disable Scheduling

```bash
# Temporarily disable
alasmia schedule pause

# Disable via config
scheduler:
  enabled: false
```

## Quiet Hours

Set times when Alasmia won't message:

```yaml
quiet_hours:
  enabled: true
  start: "22:00"
  end: "07:00"
  timezone: Asia/Kolkata
```

During quiet hours, Alasmia will still respond immediately if you message first, but won't initiate contact.