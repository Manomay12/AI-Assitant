# ==================================================
# JARVIS AI — Wake Word Detection Engine
# ==================================================

import logging
from typing import List
from jarvis.config.settings import settings
from jarvis.voice.listener import listener

logger = logging.getLogger("jarvis.voice.wake_word")


class WakeWordDetector:
    """
    Monitors audio stream for trigger wake phrases:
    'Hey Jarvis', 'Jarvis', 'Ultron', 'Hey Ultron'.
    """

    def __init__(self, wake_words: List[str] = settings.WAKE_WORDS):
        self.wake_words = [w.lower() for w in wake_words]

    def check_wake_word(self, text: str) -> bool:
        """Test if text contains any recognized wake phrase."""
        lower = text.lower()
        return any(w in lower for w in self.wake_words)

    async def wait_for_wake_word(self) -> str:
        """Continuously listens until wake word is detected."""
        print(f"[JARVIS] Standby... Waiting for wake word ({', '.join(self.wake_words)})")
        while True:
            text = await listener.listen_async(phrase_time_limit=4)
            if text and self.check_wake_word(text):
                return text


wake_word_detector = WakeWordDetector()
