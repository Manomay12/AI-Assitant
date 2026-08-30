# ==================================================
# JARVIS AI — High-Reliability Voice Speaker (TTS)
# ==================================================

import asyncio
import logging
import os
import subprocess
import threading
from typing import Optional

try:
    # pyrefly: ignore [missing-import]
    import pyttsx3
except ImportError:
    pyttsx3 = None

from jarvis.config.settings import settings

logger = logging.getLogger("jarvis.voice.tts")


class TextToSpeech:
    """
    Multi-tier Text-To-Speech synthesizer.
    Primary: pyttsx3 (SAPI5 on Windows).
    Secondary Fallback: Native Windows PowerShell SpeechSynthesizer (Zero-dependency).
    """

    def __init__(self):
        self._lock = threading.Lock()
        self.engine = None
        self._init_pyttsx3()

    def _init_pyttsx3(self):
        if not pyttsx3:
            return
        try:
            self.engine = pyttsx3.init("sapi5" if os.name == "nt" else None)
            self.engine.setProperty("rate", settings.VOICE_RATE)
            self.engine.setProperty("volume", settings.VOICE_VOLUME)
            # Select David or Mark (male AI voice) if available
            voices = self.engine.getProperty("voices")
            for v in voices:
                if "david" in v.name.lower() or "jarvis" in v.name.lower() or "zira" in v.name.lower():
                    self.engine.setProperty("voice", v.id)
                    break
        except Exception as e:
            logger.warning(f"pyttsx3 init notice (fallback enabled): {e}")
            self.engine = None

    def speak(self, text: str):
        """Speak the given text aloud with guaranteed audio output on Windows."""
        clean_text = text.replace("*", "").replace("#", "").replace('"', "'").replace("\n", " ").strip()
        if not clean_text:
            return

        print(f"\n[JARVIS SPEAKING] {clean_text}\n")

        # 1. Try pyttsx3 first
        if pyttsx3 and self.engine:
            with self._lock:
                try:
                    self.engine.say(clean_text)
                    self.engine.runAndWait()
                    return
                except Exception as e:
                    logger.debug(f"pyttsx3 runtime issue, falling back to Windows SAPI: {e}")
                    self._init_pyttsx3()

        # 2. Windows Native SAPI5 SpeechSynthesizer Fallback (Runs on 100% of Windows systems)
        if os.name == "nt":
            try:
                # Escape single quotes for PowerShell
                ps_text = clean_text.replace("'", "''")
                cmd = [
                    "powershell",
                    "-NoProfile",
                    "-NonInteractive",
                    "-Command",
                    f"Add-Type -AssemblyName System.Speech; $synth = New-Object System.Speech.Synthesis.SpeechSynthesizer; $synth.Rate = 1; $synth.Speak('{ps_text}')",
                ]
                subprocess.run(cmd, capture_output=True, creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
                return
            except Exception as e:
                logger.error(f"PowerShell speech fallback error: {e}")

    async def speak_async(self, text: str):
        """Asynchronously trigger speech without blocking event loops."""
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, self.speak, text)


speaker = TextToSpeech()
