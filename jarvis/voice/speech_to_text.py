# ==================================================
# JARVIS AI — Multilingual Speech-To-Text Recognizer
# ==================================================

from __future__ import annotations
import logging
from typing import Any, Optional, Tuple

try:
    import speech_recognition as sr
except ImportError:
    sr = None

logger = logging.getLogger("jarvis.voice.stt")


class SpeechRecognizer:
    """
    Multilingual speech recognizer supporting English, Hindi, Marathi, and Hinglish.
    Attempts primary language detection and falls back intelligently.
    """

    def __init__(self):
        if sr:
            try:
                self.recognizer = sr.Recognizer()
                self.recognizer.dynamic_energy_threshold = True
            except Exception as e:
                logger.warning(f"Could not init SpeechRecognition: {e}")
                self.recognizer = None
        else:
            self.recognizer = None

    def recognize(self, audio_data: Any, primary_lang: str = "en-IN") -> Tuple[str, str]:
        """
        Transcribe audio data into text.
        Returns tuple of (transcribed_text, detected_language).
        """
        if not self.recognizer or not sr:
            return "", ""

        # List of candidate languages for bilingual Indian / Global users
        languages = [primary_lang, "en-US", "hi-IN", "mr-IN"]

        for lang in languages:
            try:
                text = self.recognizer.recognize_google(audio_data, language=lang)
                if text and text.strip():
                    return text.strip(), lang
            except sr.UnknownValueError:
                continue
            except sr.RequestError as e:
                logger.warning(f"Google speech recognition network error on lang {lang}: {e}")
                break
            except Exception as e:
                logger.debug(f"Speech recognition exception on {lang}: {e}")
                continue

        return "", ""


speech_recognizer = SpeechRecognizer()
