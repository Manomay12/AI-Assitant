# ==================================================
# JARVIS 4.0 — User-Configurable Settings
# ==================================================
# Edit values in this file to customize JARVIS.
# Do NOT put API keys or secrets here.
# ==================================================


# --------------------------------------------------
# CHROME BROWSER
# --------------------------------------------------

# Your Chrome profile directory name.
# To find it: open Chrome → address bar → chrome://version/
# Look at "Profile Path" — use only the last folder name.
# Common values: "Default", "Profile 1", "Profile 2"
CHROME_PROFILE = "Profile 1"


# --------------------------------------------------
# LOCAL AI (OLLAMA)
# --------------------------------------------------

# The Ollama model to use for AI responses and action classification.
OLLAMA_MODEL = "llama3.2"

# The Ollama API endpoint. Change only if you run Ollama on a different port.
OLLAMA_URL = "http://localhost:11434/api/chat"

# How many seconds to wait for Ollama before giving up.
OLLAMA_TIMEOUT = 120


# --------------------------------------------------
# VOICE SETTINGS
# --------------------------------------------------

# Speech rate for TTS (words per minute). 175 is natural speed.
VOICE_RATE = 175

# TTS volume. Range: 0.0 (silent) to 1.0 (full volume).
VOICE_VOLUME = 1.0

# Maximum seconds to wait for a spoken phrase before cutting off.
SPEECH_PHRASE_TIME_LIMIT = 5

# Seconds of silence before considering a phrase complete.
SPEECH_PAUSE_THRESHOLD = 0.8


# --------------------------------------------------
# MEMORY
# --------------------------------------------------

# Path to the long-term memories JSON file.
MEMORY_FILE = "memory/memories.json"


# --------------------------------------------------
# SCREENSHOT
# --------------------------------------------------

# Default filename for screenshots. Can include a path.
SCREENSHOT_FILENAME = "jarvis_screenshot.png"
