# ==================================================
# JARVIS AI — Voice Listener & Speech Activity Manager
# ==================================================

import asyncio
import logging
from typing import Optional

try:
    import speech_recognition as sr
except ImportError:
    sr = None

from jarvis.config.settings import settings
from jarvis.voice.speech_to_text import speech_recognizer

logger = logging.getLogger("jarvis.voice.listener")


class VoiceListener:
    """
    Manages microphone input capture with intelligent pause detection,
    ambient noise calibration, and speech activity detection.
    """

    def __init__(self):
        if sr:
            try:
                self.recognizer = sr.Recognizer()
                self.recognizer.pause_threshold = settings.SPEECH_PAUSE_THRESHOLD
                self.recognizer.energy_threshold = settings.SPEECH_ENERGY_THRESHOLD
                self.recognizer.dynamic_energy_threshold = True
            except Exception:
                self.recognizer = None
            try:
                self.microphone = sr.Microphone()
            except Exception:
                self.microphone = None
        else:
            self.recognizer = None
            self.microphone = None
        self._is_calibrated = False

    def calibrate(self):
        """Calibrate microphone to ambient background noise."""
        if not self.microphone or not self.recognizer:
            return
        try:
            with self.microphone as source:
                print("[JARVIS] Calibrating audio to ambient noise...")
                self.recognizer.adjust_for_ambient_noise(source, duration=0.6)
                self._is_calibrated = True
                print(f"[JARVIS] Audio calibrated. Energy threshold: {self.recognizer.energy_threshold:.1f}")
        except Exception as e:
            logger.warning(f"Microphone calibration unavailable: {e}")

    def listen_phrase(self, phrase_time_limit: Optional[int] = None) -> str:
        """
        Listen for a single spoken utterance synchronously.
        Waits intelligently through natural thinking pauses before finalizing.
        """
        if not self.microphone or not self.recognizer:
            return ""

        if not self._is_calibrated:
            self.calibrate()

        time_limit = phrase_time_limit or settings.SPEECH_PHRASE_TIME_LIMIT

        try:
            with self.microphone as source:
                print("[JARVIS] Listening... (speak naturally)")
                audio = self.recognizer.listen(
                    source,
                    timeout=None,
                    phrase_time_limit=time_limit,
                )

            text, lang = speech_recognizer.recognize(audio)
            if text:
                print(f"[YOU ({lang})] {text}")
                return text
        except Exception as e:
            logger.debug(f"Audio capture timeout or noise: {e}")

        return ""

    async def listen_async(self, phrase_time_limit: Optional[int] = None) -> str:
        """Asynchronous wrapper for audio capture."""
        if not self.microphone or not self.recognizer:
            await asyncio.sleep(1.0)
            return ""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.listen_phrase, phrase_time_limit)


listener = VoiceListener()
