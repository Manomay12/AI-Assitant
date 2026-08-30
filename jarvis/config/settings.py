# ==================================================
# JARVIS AI — Global Configuration & Environment Settings
# ==================================================

import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv

# Load .env file from project root or current working directory
env_path = Path(__file__).resolve().parent.parent / ".env"
if env_path.exists():
    load_dotenv(dotenv_path=env_path)
else:
    load_dotenv()


class Settings:
    # --------------------------------------------------
    # Application & Environment
    # --------------------------------------------------
    APP_NAME: str = "JARVIS AI"
    APP_VERSION: str = "5.0.0"
    DEBUG: bool = os.getenv("JARVIS_DEBUG", "False").lower() in ("true", "1", "yes")
    BASE_DIR: Path = Path(__file__).resolve().parent.parent

    # --------------------------------------------------
    # Server & IPC API
    # --------------------------------------------------
    HOST: str = os.getenv("JARVIS_HOST", "127.0.0.1")
    PORT: int = int(os.getenv("JARVIS_PORT", "8000"))
    WS_HEARTBEAT_INTERVAL: int = 15

    # --------------------------------------------------
    # AI Providers & Model Selection
    # --------------------------------------------------
    AI_PROVIDER: str = os.getenv("JARVIS_AI_PROVIDER", "ollama")  # "ollama", "gemini", "openai"
    
    # Ollama Local AI
    OLLAMA_MODEL: str = os.getenv("OLLAMA_MODEL", "llama3.2")
    OLLAMA_URL: str = os.getenv("OLLAMA_URL", "http://localhost:11434/api/chat")
    OLLAMA_TIMEOUT: int = int(os.getenv("OLLAMA_TIMEOUT", "60"))

    # Gemini API
    GEMINI_API_KEY: Optional[str] = os.getenv("GEMINI_API_KEY", None)
    GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")

    # OpenAI-Compatible API
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY", None)
    OPENAI_BASE_URL: Optional[str] = os.getenv("OPENAI_BASE_URL", None)
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    # NVIDIA Free NIM / Build API (https://build.nvidia.com)
    NVIDIA_API_KEY: Optional[str] = os.getenv("NVIDIA_API_KEY", None)
    NVIDIA_BASE_URL: str = os.getenv("NVIDIA_BASE_URL", "https://integrate.api.nvidia.com/v1")
    NVIDIA_MODEL: str = os.getenv("NVIDIA_MODEL", "meta/llama-3.3-70b-instruct")

    # --------------------------------------------------
    # Voice Settings
    # --------------------------------------------------
    VOICE_ENGINE: str = os.getenv("JARVIS_VOICE_ENGINE", "pyttsx3")  # "pyttsx3", "edge-tts"
    VOICE_RATE: int = int(os.getenv("JARVIS_VOICE_RATE", "175"))
    VOICE_VOLUME: float = float(os.getenv("JARVIS_VOICE_VOLUME", "1.0"))
    VOICE_LANG_DEFAULT: str = os.getenv("JARVIS_DEFAULT_LANG", "en-US")
    SPEECH_PHRASE_TIME_LIMIT: int = int(os.getenv("SPEECH_PHRASE_TIME_LIMIT", "8"))
    SPEECH_PAUSE_THRESHOLD: float = float(os.getenv("SPEECH_PAUSE_THRESHOLD", "1.0"))
    SPEECH_ENERGY_THRESHOLD: int = int(os.getenv("SPEECH_ENERGY_THRESHOLD", "300"))
    WAKE_WORDS: list[str] = ["jarvis", "hey jarvis", "ultron", "hey ultron"]

    # --------------------------------------------------
    # Browser & Automation
    # --------------------------------------------------
    CHROME_PROFILE: str = os.getenv("CHROME_PROFILE", "Default")
    SCREENSHOT_DIR: Path = BASE_DIR / "data" / "screenshots"
    SCREENSHOT_FILENAME: str = "latest_screen.png"

    # --------------------------------------------------
    # Memory & Database Storage
    # --------------------------------------------------
    DATA_DIR: Path = BASE_DIR / "data"
    MEMORY_FILE: Path = DATA_DIR / "memory.json"
    CONVERSATION_FILE: Path = DATA_DIR / "conversation_history.json"
    PREFERENCES_FILE: Path = DATA_DIR / "user_preferences.json"
    PERMISSIONS_FILE: Path = DATA_DIR / "permissions.json"

    def __init__(self):
        # Ensure necessary folders exist
        self.DATA_DIR.mkdir(parents=True, exist_ok=True)
        self.SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)


settings = Settings()
