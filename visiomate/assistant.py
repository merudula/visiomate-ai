from datetime import datetime
from .intents import route_intent
from .reminders import ReminderStore, ReminderScheduler, parse_reminder
from .navigation import Navigator
from .sos import send_sos
from .utils import capture_frame

HELP = ("I can describe what is in front of you, read text, recognise currency notes, "
        "guide you to a place, set medicine reminders, and send an emergency alert. "
        "Say help me or S O S in an emergency.")


class Assistant:
    def __init__(self, cfg, voice):
        self.cfg, self.voice = cfg, voice
        self.nav = Navigator(cfg)
        self.store = ReminderStore()
        ReminderScheduler(self.store, voice.speak).start()
        self._detector = self._currency = self._ocr = None  # lazy-loaded

    def _frame(self):
        f = capture_frame(self.cfg.get("camera_index", 0))
        if f is None:
            self.voice.speak("I cannot access the camera.")
        return f

    @staticmethod
    def _strip(text, words):
        for w in words:
            text = text.replace(w, " ")
        return " ".join(text.split())

    def handle(self, text: str) -> bool:
        """Returns False when the user wants to exit."""
        intent = route_intent(text)
        say = self.voice.speak
        if intent == "none":
            return True
        if intent == "exit":
            say("Goodbye. Stay safe.")
            return False
        if intent == "help":
            say(HELP)
        elif intent == "time":
            say("It is " + datetime.now().strftime("%I:%M %p"))
        elif intent == "sos":
            self._sos()
        elif intent == "detect":
            f = self._frame()
            if f is not None:
                if not self._detector:
                    from .vision.object_detection import ObjectDetector
                    c = self.cfg["object_detection"]
                    self._detector = ObjectDetector(c["model"], c["confidence"])
                say(self._detector.describe(f))
        elif intent == "currency":
            f = self._frame()
            if f is not None:
                if not self._currency:
                    from .vision.currency import CurrencyRecognizer
                    c = self.cfg["currency"]
                    self._currency = CurrencyRecognizer(c["model"], c["confidence"])
                say(self._currency.describe(f))
        elif intent == "ocr":
            f = self._frame()
            if f is not None:
                if not self._ocr:
                    from .vision.ocr import TextReader
                    self._ocr = TextReader(self.cfg["ocr"]["lang"])
                say(self._ocr.read(f))
        elif intent == "navigate":
            dest = self._strip(text, ["navigate to", "navigate", "take me to", "directions to",
                                      "route to", "way to", "please"])
            if not dest:
                say("Where do you want to go?")
                dest = self.voice.listen()
            say(self.nav.start(dest) if dest else "I did not hear a place.")
        elif intent == "next_step":
            say(self.nav.next())
        elif intent == "add_reminder":
            parsed = parse_reminder(text)
            if not parsed:
                say("Please tell me the medicine and time, for example: remind me to take tablet at 8 30 p m.")
            else:
                self.store.add(*parsed)
                say(f"Okay. I will remind you to {parsed[0]} at {parsed[1]}.")
        elif intent == "list_reminders":
            rows = self.store.all()
            say("; ".join(f"{l} at {a}" for _, l, a in rows) if rows else "You have no reminders.")
        else:
            say("Sorry, I did not understand. Say help to hear what I can do.")
        return True

    def _sos(self):
        n = self.cfg["sos"].get("countdown_seconds", 5)
        self.voice.speak(f"Sending emergency alert in {n} seconds. Say cancel to stop.")
        heard = self.voice.listen(timeout=n, phrase_limit=n)
        if "cancel" in heard or "stop" in heard:
            self.voice.speak("Emergency alert cancelled.")
            return
        self.voice.speak(send_sos(self.cfg))
