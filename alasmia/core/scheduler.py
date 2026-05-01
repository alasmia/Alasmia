"""
Alasmia Scheduler - Time-based greetings and check-ins
Supports multilingual greetings based on user's preferred language.
"""

import os
import json
from datetime import datetime, time
from pathlib import Path


class Scheduler:
    """
    Handles time-based greetings and automated check-ins.
    Supports greetings in multiple languages.
    """
    
    GREETING_TIMES = {
        "morning": (7, 9),    # 7-9 AM
        "afternoon": (12, 14), # 12-2 PM
        "evening": (18, 20),  # 6-8 PM
        "night": (22, 23),    # 10-11 PM
    }
    
    # Multilingual greeting templates
    # These are used when companion-specific greetings aren't available
    GREETING_TEMPLATES = {
        "English": {
            "morning": "Good morning! ☀️ Hope you slept well. How are you feeling today?",
            "afternoon": "Good afternoon! How's your day going so far?",
            "evening": "Good evening! 💫 How was your day?",
            "night": "Good night! 🌙 Sleep well. Talk to you tomorrow!",
        },
        "Mandarin Chinese": {
            "morning": "早上好！☀️ 睡得好吗？今天感觉怎么样？",
            "afternoon": "下午好！今天过得怎么样？",
            "evening": "晚上好！💫 今天怎么样？",
            "night": "晚安！🌙 好好休息。明天见！",
        },
        "Spanish": {
            "morning": "¡Buenos días! ☀️ Espero que hayas dormido bien. ¿Cómo te sientes hoy?",
            "afternoon": "¡Buenas tardes! ¿Cómo va tu día?",
            "evening": "¡Buenas noches! 💫 ¿Cómo fue tu día?",
            "night": "¡Buenas noches! 🌙 Descansa. ¡Mañana hablamos!",
        },
        "Arabic": {
            "morning": "صباح الخير! ☀️ أتمنى أنك نمت جيداً. كيف تشعر اليوم؟",
            "afternoon": "مساء الخير! كيف حالك اليوم؟",
            "evening": "مساء الخير! 💫 كيف كان يومك؟",
            "night": "تصبح على خير! 🌙 نم جيداً. نتحدث غداً!",
        },
        "Hindi": {
            "morning": "सुप्रभात! ☀️ आशा है तुम अच्छे से सोए होंगे। आज कैसा लग रहा है?",
            "afternoon": "दोपहर بخير! आज का दिन कैसा जा रहा है?",
            "evening": "शाम بخير! 💫 तुम्हारा दिन कैसा रहा?",
            "night": "शुभ रात्रि! 🌙 अच्छे से सोना। कल बात करते हैं!",
        },
        "Japanese": {
            "morning": "おはよう！☀️ よく眠れた？今日はどう？",
            "afternoon": "こんにちは！今日の調子は？",
            "evening": "こんばんは！💫 今日はどうだった？",
            "night": "おやすみなさい！🌙 よく休んで。明日はまた話そう！",
        },
        "Korean": {
            "morning": "좋은 아침！☀️ 잘 잤어？ 오늘 기분은 어때?",
            "afternoon": "안녕하세요！오늘 하루 어때?",
            "evening": "좋은 저녁！💫 오늘 하루가 어땠어?",
            "night": "잘 자！🌙 푹 자. 내일 보자!",
        },
        "French": {
            "morning": "Bonjour! ☀️ J'espère que tu as bien dormi. Comment tu te sens aujourd'hui?",
            "afternoon": "Bon après-midi! Comment va ta journée?",
            "evening": "Bonsoir! 💫 Comment était ta journée?",
            "night": "Bonne nuit! 🌙 Dors bien. À demain!",
        },
        "German": {
            "morning": "Guten Morgen! ☀️ Ich hoffe, du hast gut geschlafen. Wie fühlst du dich heute?",
            "afternoon": "Guten Tag! Wie läuft dein Tag?",
            "evening": "Guten Abend! 💫 Wie war dein Tag?",
            "night": "Gute Nacht! 🌙 Schlaf gut. Bis morgen!",
        },
        "Portuguese": {
            "morning": "Bom dia! ☀️ Espero que tenha dormido bem. Como você está se sentindo hoje?",
            "afternoon": "Boa tarde! Como vai seu dia?",
            "evening": "Boa noite! 💫 Como foi seu dia?",
            "night": "Boa noite! 🌙 Descansa. Falamos amanhã!",
        },
        "Russian": {
            "morning": "Доброе утро! ☀️ Надеюсь, ты хорошо выспался. Как себя чувствуешь?",
            "afternoon": "Добрый день! Как идёт твой день?",
            "evening": "Добрый вечер! 💫 Как прошёл твой день?",
            "night": "Спокойной ночи! 🌙 Отдыхай. До завтра!",
        },
        "Vietnamese": {
            "morning": "Chào buổi sáng! ☀️ Hy vọng bạn ngủ ngon. Hôm nay bạn cảm thấy thế nào?",
            "afternoon": "Chào buổi chiều! Hôm nay của bạn thế nào?",
            "evening": "Chào buổi tối! 💫 Hôm nay của bạn thế nào?",
            "night": "Chúc ngủ ngon! 🌙 Ngủ ngon. Ngày mai gặp lại!",
        },
        "Thai": {
            "morning": "สวัสดีตอนเช้า! ☀️ หวังว่านายนอนหลับดีนะ วันนี้เป็นอย่างไร?",
            "afternoon": "สวัสดีตอนบ่าย! วันนี้ของคุณเป็นอย่างไร?",
            "evening": "สวัสดีตอนเย็น! 💫 วันนี้ของคุณเป็นอย่างไร?",
            "night": "ราตรีสวัสดิ์! 🌙 นอนหลับฝันดี. แล้วพบกันพรุ่งนี้!",
        },
        "Indonesian": {
            "morning": "Selamat pagi! ☀️ Semoga tidur nyenyak. Bagaimana perasaanmu hari ini?",
            "afternoon": "Selamat siang! Bagaimana harimu?",
            "evening": "Selamat malam! 💫 Bagaimana harimu?",
            "night": "Selamat malam! 🌙 Tidurlah yang nyenyak. Sampai besok!",
        },
        "Turkish": {
            "morning": "Günaydın! ☀️ Umarım iyi uyudun. Bugün nasıl hissediyorsun?",
            "afternoon": "İyi günler! Günün nasıl geçiyor?",
            "evening": "İyi akşamlar! 💫 Günün nasıl geçti?",
            "night": "İyi geceler! 🌙 İyi uyu. Yarın görüşürüz!",
        },
        "Polish": {
            "morning": "Dzień dobry! ☀️ Mam nadzieję, że spałeś dobrze. Jak się czujesz dzisiaj?",
            "afternoon": "Dzień dobry! Jak minął twój dzień?",
            "evening": "Dobry wieczór! 💫 Jak minął twój dzień?",
            "night": "Dobranoc! 🌙 Śpij dobrze. Do jutra!",
        },
        "Dutch": {
            "morning": "Goedemorgen! ☀️ Ik hoop dat je goed geslapen hebt. Hoe voel je je vandaag?",
            "afternoon": "Goedemiddag! Hoe gaat je dag?",
            "evening": "Goedenavond! 💫 Hoe was je dag?",
            "night": "Welterusten! 🌙 Slaap lekker. Tot morgen!",
        },
        "Swedish": {
            "morning": "Godmorgon! ☀️ Jag hoppas att du sov gott. Hur mår du idag?",
            "afternoon": "God eftermiddag! Hur går din dag?",
            "evening": "God kväll! 💫 Hur var din dag?",
            "night": "Godnatt! 🌙 Sov gott. Vi hörs imorgon!",
        },
        "Italian": {
            "morning": "Buongiorno! ☀️ Spero che tu abbia dormito bene. Come ti senti oggi?",
            "afternoon": "Buon pomeriggio! Come va la tua giornata?",
            "evening": "Buonasera! 💫 Com'è andata la tua giornata?",
            "night": "Buonanotte! 🌙 Dormi bene. Ci vediamo domani!",
        },
    }
    
    def __init__(self):
        """Initialize scheduler."""
        self.last_greeting_file = Path("./data/last_greetings.json")
        self.last_greetings = self._load_last_greetings()
    
    def _load_last_greetings(self) -> dict:
        """Load last greeting timestamps."""
        if self.last_greeting_file.exists():
            with open(self.last_greeting_file, 'r') as f:
                return json.load(f)
        return {}
    
    def _save_last_greetings(self):
        """Save last greeting timestamps."""
        self.last_greeting_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.last_greeting_file, 'w') as f:
            json.dump(self.last_greetings, f, indent=2)
    
    def check_and_send_greeting(self, user_language: str = None) -> Optional[str]:
        """
        Check if it's time for a greeting.
        Returns greeting message if time, None otherwise.
        
        Args:
            user_language: User's preferred language (e.g., "English", "Mandarin Chinese")
        """
        now = datetime.now()
        current_hour = now.hour
        today = now.strftime("%Y-%m-%d")
        
        for greeting_type, (start_hour, end_hour) in self.GREETING_TIMES.items():
            if start_hour <= current_hour <= end_hour:
                last_key = f"{greeting_type}_{today}"
                
                if self.last_greetings.get(last_key) != today:
                    self.last_greetings[last_key] = today
                    self._save_last_greetings()
                    return self._get_greeting_message(greeting_type, now, user_language)
        
        return None
    
    def _get_greeting_message(self, greeting_type: str, now: datetime, language: str = None) -> str:
        """
        Generate greeting message based on time of day and language.
        
        Args:
            greeting_type: morning, afternoon, evening, night
            now: Current datetime
            language: User's preferred language
        """
        # Try to use language-specific greetings
        if language and language in self.GREETING_TEMPLATES:
            templates = self.GREETING_TEMPLATES[language]
            if greeting_type in templates:
                return templates[greeting_type]
        
        # Fallback to English
        templates = self.GREETING_TEMPLATES["English"]
        return templates.get(greeting_type, f"Hello! 💕")
    
    def should_weekly_checkin(self) -> bool:
        """Check if it's time for weekly check-in (Sunday)."""
        now = datetime.now()
        today = now.strftime("%Y-%m-%d")
        
        # Sunday
        if now.weekday() == 6:  # Sunday = 6
            last_checkin = self.last_greetings.get("weekly_checkin", "")
            if last_checkin != today:
                self.last_greetings["weekly_checkin"] = today
                self._save_last_greetings()
                return True
        
        return False
    
    def get_weekly_checkin_message(self, analytics, language: str = None) -> str:
        """
        Generate weekly check-in message with analytics.
        
        Args:
            analytics: Analytics object
            language: User's preferred language
        """
        report = analytics.get_weekly_summary()
        
        # Multilingual weekly checkin
        messages = {
            "English": f"📊 **Weekly Check-in!** 💕

It's been a week together! Here's your summary:

💬 Messages: {report.get('message_count', 0)}
😊 Mood Trend: {report.get('mood_trend', 'neutral')}
🔥 Streak: {report.get('streak', 0)} days
💕 Connection: {report.get('connection_score', 0)}%

Want to share anything? Or shall I explain any insight? 💭",
            
            "Mandarin Chinese": f"📊 **每周签到！** 💕

我们一起度过了一周！这是你的总结：

💬 消息：{report.get('message_count', 0)}
😊 情绪趋势：{report.get('mood_trend', 'neutral')}
🔥 连续：{report.get('streak', 0)} 天
💕 联系：{report.get('connection_score', 0)}%

你想分享什么吗？或者要我解释什么吗？💭",
            
            "Spanish": f"📊 **¡Check-in semanal!** 💕

¡Ha pasado una semana juntos! Aquí está tu resumen:

💬 Mensajes: {report.get('message_count', 0)}
😊 Tendencia de ánimo: {report.get('mood_trend', 'neutral')}
🔥 Racha: {report.get('streak', 0)} días
💕 Conexión: {report.get('connection_score', 0)}%

¿Quieres compartir algo? ¿O debo explicar algo? 💭",
            
            "Arabic": f"📊 **إجازة أسبوعية!** 💕

مر أسبوع与我们在一起！ إليك ملخصك:

💬 الرسائل: {report.get('message_count', 0)}
😊 اتجاه المزاج: {report.get('mood_trend', 'neutral')}
🔥 سلسلة: {report.get('streak', 0)} أيام
💕 اتصال: {report.get('connection_score', 0)}%

هل تريد مشاركة شيء؟ أم أشرح شيئاً؟ 💭",
            
            "Hindi": f"📊 **साप्ताहिक जांच!** 💕

हम एक सप्ताह एक साथ बिताया है! यह आपका सारांश है:

💬 संदेश: {report.get('message_count', 0)}
😊 मूड ट्रेंड: {report.get('mood_trend', 'neutral')}
🔥 स्ट्रीक: {report.get('streak', 0)} दिन
💕 कनेक्शन: {report.get('connection_score', 0)}%

कुछ साझा करना चाहते हैं? या मुझे कुछ समझाना है? 💭",
        }
        
        if language and language in messages:
            return messages[language]
        
        return messages["English"]
    
    def get_monthly_anniversary_message(self, user_profile: dict, language: str = None) -> str:
        """Generate monthly anniversary message in user's language."""
        first_seen = user_profile.get("first_seen", "")
        if not first_seen:
            return None
        
        try:
            from datetime import datetime
            first_date = datetime.fromisoformat(first_seen.replace("Z", "+00:00"))
            now = datetime.now()
            
            days_together = (now - first_date).days
            
            if days_together % 30 == 0 and days_together > 0:
                months = days_together // 30
                
                messages = {
                    "English": f"🎉 **Monthly Anniversary!** 🎉

It's been {months} month(s) together! 💕
Thank you for being here!",
                    "Mandarin Chinese": f"🎉 **月度纪念日！** 🎉

我们已经在一起{months}个月了！💕
谢谢你在这里！",
                    "Spanish": f"🎉 **Aniversario mensual!** 🎉

¡Ha pasado {months} mes(es) juntos! 💕
¡Gracias por estar aquí!",
                    "Arabic": f"🎉 **الذكرى الشهرية!** 🎉

مر {months} شهر(ة) معاً! 💕
شكراً لكونك هنا!",
                    "Hindi": f"🎉 **मासिक सालगिरह!** 🎉

हम साथ में {months} महीने हो गए! 💕
यहाँ होने के लिए धन्यवाद!",
                }
                
                if language and language in messages:
                    return messages[language]
                return messages["English"]
        except:
            pass
        
        return None


# =============================================================
# LANGUAGE DETECTION UTILITY
# =============================================================

def detect_language(text: str) -> str:
    """
    Simple language detection based on character sets and patterns.
    
    This is a basic implementation. For production, consider using
    a proper language detection library like langdetect or fasttext.
    
    Args:
        text: Input text to analyze
        
    Returns:
        Detected language name (e.g., "English", "Mandarin Chinese")
    """
    import re
    
    if not text or len(text.strip()) < 2:
        return "English"
    
    text = text.strip()
    
    # Check for Mandarin Chinese (CJK characters)
    if re.search(r'[一-鿿]', text):
        return "Mandarin Chinese"
    
    # Check for Japanese (Hiragana, Katakana, Kanji)
    if re.search(r'[぀-ゟ゠-ヿ一-鿿]', text):
        return "Japanese"
    
    # Check for Korean (Hangul)
    if re.search(r'[가-힯ᄀ-ᇿ]', text):
        return "Korean"
    
    # Check for Arabic
    if re.search(r'[؀-ۿݐ-ݿ]', text):
        return "Arabic"
    
    # Check for Russian (Cyrillic)
    if re.search(r'[Ѐ-ӿ]', text):
        return "Russian"
    
    # Check for Thai
    if re.search(r'[฀-๿]', text):
        return "Thai"
    
    # Check for Vietnamese (Latin with diacritics)
    if re.search(r'[àáảãạăằắẳẵặâầấẩẫậèéẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵđ]', text.lower()):
        return "Vietnamese"
    
    # Check for Spanish (common words)
    spanish_indicators = ['¿', '¡', 'ñ', 'hola', 'buenos', 'dias', 'como', 'gracias', 'que', 'estoy']
    if any(word in text.lower() for word in spanish_indicators):
        return "Spanish"
    
    # Check for French
    french_indicators = ['ç', 'ça', 'bonjour', 'merci', 'comment', 'je', 'suis', 'vous', 'les', 'des']
    if any(word in text.lower() for word in french_indicators):
        return "French"
    
    # Check for German
    german_indicators = ['ß', 'ü', 'ö', 'ä', 'guten', 'danke', 'wie', 'ich', 'bin', 'ist', 'das']
    if any(word in text.lower() for word in german_indicators):
        return "German"
    
    # Check for Portuguese
    portuguese_indicators = ['ã', 'õ', 'ç', 'obrigado', 'obrigada', 'bom', 'dia', 'como', 'estou']
    if any(word in text.lower() for word in portuguese_indicators):
        return "Portuguese"
    
    # Check for Hindi (Devanagari)
    if re.search(r'[ऀ-ॿ]', text):
        return "Hindi"
    
    # Check for Indonesian/Malay
    indonesian_indicators = ['yang', 'dan', 'di', 'ke', 'dari', 'ini', 'itu', 'ada', 'saya', 'anda']
    if any(word in text.lower() for word in indonesian_indicators):
        return "Indonesian"
    
    # Check for Turkish
    turkish_indicators = ['ş', 'ç', 'ğ', 'ü', 'ö', 'ı', 'nasıl', 'teşekkür', 'iyi', 'gunaydın']
    if any(word in text.lower() for word in turkish_indicators):
        return "Turkish"
    
    # Check for Polish
    polish_indicators = ['ą', 'ć', 'ę', 'ł', 'ń', 'ó', 'ś', 'ź', 'ż', 'dzień', 'dobra']
    if any(word in text.lower() for word in polish_indicators):
        return "Polish"
    
    # Check for Dutch
    dutch_indicators = ['ik', 'ben', 'je', 'en', 'van', 'dat', 'de', 'het', 'wel', 'goedemorgen']
    if any(word in text.lower() for word in dutch_indicators):
        return "Dutch"
    
    # Check for Swedish
    swedish_indicators = ['å', 'ä', 'ö', 'hej', 'tack', 'hur', 'mår', 'god', 'morgon']
    if any(word in text.lower() for word in swedish_indicators):
        return "Swedish"
    
    # Check for Italian
    italian_indicators = ['ciao', 'grazie', 'come', 'stai', 'bene', 'buongiorno', 'buonanotte']
    if any(word in text.lower() for word in italian_indicators):
        return "Italian"
    
    # Default to English for Latin script
    return "English"
