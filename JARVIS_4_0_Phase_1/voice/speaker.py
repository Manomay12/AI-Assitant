# ==================================================
# JARVIS 4.0 — Voice Speaker (TTS)
# ==================================================

# pyrefly: ignore [missing-import]
import pyttsx3

from config.settings import VOICE_RATE, VOICE_VOLUME


class Speaker:

    def __init__(self):

        self.engine = pyttsx3.init()
        self.engine.setProperty("rate", VOICE_RATE)
        self.engine.setProperty("volume", VOICE_VOLUME)

    def speak(self, text: str):
        """Speak the given text aloud and print it to the console."""
        print(f"[JARVIS] {text}")
        self.engine.say(text)
        self.engine.runAndWait()