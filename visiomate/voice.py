"""Speech in / speech out."""
import threading


class Voice:
    def __init__(self, language="en-IN", rate=165, text_mode=False):
        self.language = language
        self.text_mode = text_mode          # keyboard fallback for testing
        self._lock = threading.Lock()
        if not text_mode:
            import pyttsx3
            import speech_recognition as sr
            self._sr = sr
            self.engine = pyttsx3.init()
            self.engine.setProperty("rate", rate)
            self.recognizer = sr.Recognizer()

    def speak(self, text: str):
        print(f"[VisioMate] {text}")
        if self.text_mode:
            return
        with self._lock:
            self.engine.say(text)
            self.engine.runAndWait()

    def listen(self, timeout=6, phrase_limit=8) -> str:
        if self.text_mode:
            return input("You: ").strip().lower()
        sr = self._sr
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source, 0.4)
            try:
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_limit)
            except sr.WaitTimeoutError:
                return ""
        try:
            return self.recognizer.recognize_google(audio, language=self.language).lower()
        except (sr.UnknownValueError, sr.RequestError):
            return ""
