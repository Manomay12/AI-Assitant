# ==================================================
# JARVIS 4.0 — Voice Listener (Speech Recognition)
# ==================================================

import speech_recognition as sr

from config.settings import SPEECH_PHRASE_TIME_LIMIT, SPEECH_PAUSE_THRESHOLD


class Listener:

    def __init__(self):

        self.recognizer = sr.Recognizer()
        self.recognizer.pause_threshold = SPEECH_PAUSE_THRESHOLD
        self.microphone = sr.Microphone()

    def listen(self) -> str:
        """
        Listen for a single spoken phrase.
        Returns the recognised text in lowercase, or an empty string on failure.
        """
        with self.microphone as source:

            print("[JARVIS] Listening...")

            # Calibrate to ambient noise on the first listen
            self.recognizer.adjust_for_ambient_noise(source, duration=0.3)

            try:

                audio = self.recognizer.listen(
                    source,
                    timeout=None,
                    phrase_time_limit=SPEECH_PHRASE_TIME_LIMIT
                )

            except Exception:
                return ""

        try:

            text = self.recognizer.recognize_google(audio)
            print(f"[YOU] {text}")
            return text.lower()

        except sr.UnknownValueError:
            # Could not understand audio — not an error, just silence/noise
            return ""

        except sr.RequestError as e:
            print(f"[JARVIS LISTENER ERROR] Speech service unavailable: {e}")
            return ""

        except Exception as e:
            print(f"[JARVIS LISTENER ERROR] Unexpected error: {e}")
            return ""

    def wait_for_wake_word(self) -> bool:
        """
        Block until the user says 'Hey Jarvis' or 'Jarvis'.
        Returns True when the wake word is detected.
        """
        print("[JARVIS] Waiting for wake word ('Hey Jarvis' or 'Jarvis')...")

        while True:

            text = self.listen()

            if text and ("hey jarvis" in text or "jarvis" in text):
                print("[JARVIS] Wake word detected.")
                return True