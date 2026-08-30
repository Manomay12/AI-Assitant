# ==================================================
# JARVIS AI — Constants, Scopes, and Allowlists
# ==================================================

import os
from enum import Enum


class PermissionScope(str, Enum):
    SCREEN_READ = "screen:read"
    SCREEN_CONTROL = "screen:control"
    CAMERA = "camera:access"
    MICROPHONE = "microphone:access"
    APPLICATION_LAUNCH = "app:launch"
    APPLICATION_TERMINATE = "app:terminate"
    BROWSER_CONTROL = "browser:control"
    SYSTEM_CONTROL = "system:control"
    FILE_READ = "file:read"
    FILE_WRITE = "file:write"
    COMMUNICATION_SEND = "comm:send"
    INTERNET_RESEARCH = "internet:research"


class PermissionLevel(str, Enum):
    DENY = "deny"
    ALLOW_ONCE = "allow_once"
    ALLOW_SESSION = "allow_session"
    ALWAYS_ALLOW = "always_allow"


# --------------------------------------------------
# Chrome Paths for Windows & Fallbacks
# --------------------------------------------------
CHROME_POSSIBLE_PATHS = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"),
    r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
]

# --------------------------------------------------
# Application Allowlists & Executables
# --------------------------------------------------
DEFAULT_APPS = {
    "chrome": "chrome.exe",
    "notepad": "notepad.exe",
    "calculator": "calc.exe",
    "paint": "mspaint.exe",
    "cmd": "cmd.exe",
    "powershell": "powershell.exe",
    "explorer": "explorer.exe",
    "code": "code.cmd",
    "vs code": "code.cmd",
    "vscode": "code.cmd",
    "task manager": "taskmgr.exe",
}

# --------------------------------------------------
# Website Allowlists & Aliases
# --------------------------------------------------
DEFAULT_WEBSITES = {
    "youtube": "https://www.youtube.com",
    "google": "https://www.google.com",
    "chatgpt": "https://chatgpt.com",
    "github": "https://github.com",
    "gmail": "https://mail.google.com",
    "instagram": "https://www.instagram.com",
    "spotify": "https://open.spotify.com",
    "netflix": "https://www.netflix.com",
    "linkedin": "https://www.linkedin.com",
    "twitter": "https://x.com",
    "reddit": "https://www.reddit.com",
    "wikipedia": "https://www.wikipedia.org",
}

# --------------------------------------------------
# Voice & Intent Phrasings
# --------------------------------------------------
EXIT_PHRASES = {
    "exit", "quit", "shutdown jarvis", "shut down", "goodbye", "bye", "terminate", "sleep mode"
}

AFFIRMATIVE_PHRASES = {
    "yes", "yeah", "yep", "sure", "proceed", "confirm", "allow", "go ahead", "do it", "haan", "ha"
}

NEGATIVE_PHRASES = {
    "no", "nope", "cancel", "stop", "don't", "dont", "deny", "abort", "nahi", "mat karo"
}

LANGUAGE_NAMES = {
    "en": "English",
    "hi": "Hindi",
    "mr": "Marathi",
    "hinglish": "Hinglish",
}
