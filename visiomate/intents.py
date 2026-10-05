"""Keyword intent router (English + Tamil / Tanglish). Pure python, easy to test."""

INTENTS = [
    ("sos", ["sos", "emergency", "help me", "save me", "kaapathunga", "kapathunga", "udhavi", "உதவி", "காப்பாத்து"]),
    ("list_reminders", ["my reminders", "list reminders", "what reminders", "reminders enna"]),
    ("add_reminder", ["remind", "medicine", "tablet", "pill", "maathirai", "mathirai", "மருந்து", "மாத்திரை"]),
    ("currency", ["currency", "note", "money", "rupee", "cash", "panam", "ruba", "பணம்", "ரூபாய்"]),
    ("ocr", ["read", "text", "ocr", "padi", "padikka", "படி", "எழுத்து"]),
    ("navigate", ["navigate", "take me to", "directions", "route", "way to", "vazhi", "வழி"]),
    ("detect", ["in front", "around me", "detect", "object", "what is this", "munnadi", "ennada irukku", "முன்னாடி"]),
    ("time", ["what time", "what's the time", "time enna", "current time", "நேரம்"]),
    ("next_step", ["next step", "next direction", "adutha", "அடுத்து"]),
    ("help", ["help", "what can you do", "features", "enna panna mudiyum"]),
    ("exit", ["exit", "quit", "stop listening", "goodbye", "bye", "nillu"]),
]


def route_intent(text: str) -> str:
    t = text.lower().strip()
    if not t:
        return "none"
    for name, words in INTENTS:
        if any(w in t for w in words):
            return name
    return "unknown"
