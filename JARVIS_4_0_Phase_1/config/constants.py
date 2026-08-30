# ==================================================
# JARVIS 4.0 — Constants & Allowlists
# ==================================================
# This file defines fixed mappings and allowlists.
# These control which apps, websites, and actions
# JARVIS is permitted to execute.
# ==================================================

import os


# --------------------------------------------------
# CHROME EXECUTABLE PATHS
# Searched in order — first match is used.
# --------------------------------------------------

CHROME_POSSIBLE_PATHS = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"),
]


# --------------------------------------------------
# ALLOWED APPLICATIONS
# Only these application names may be launched.
# --------------------------------------------------

ALLOWED_APPS = {
    "chrome",
    "notepad",
    "calculator",
}


# --------------------------------------------------
# ALLOWED WEBSITES
# Maps a short name to a full URL.
# Only these websites may be opened directly.
# --------------------------------------------------

ALLOWED_WEBSITES = {
    "youtube":   "https://www.youtube.com",
    "google":    "https://www.google.com",
    "chatgpt":   "https://chatgpt.com",
    "github":    "https://github.com",
    "gmail":     "https://mail.google.com",
    "instagram": "https://www.instagram.com",
    "spotify":   "https://open.spotify.com",
    "netflix":   "https://www.netflix.com",
    "facebook":  "https://www.facebook.com",
    "linkedin":  "https://www.linkedin.com",
}


# --------------------------------------------------
# WEBSITE COMMAND ALIASES
# Maps voice/text phrases to website short names.
# --------------------------------------------------

WEBSITE_COMMAND_ALIASES = {
    "open youtube":   "youtube",
    "launch youtube": "youtube",

    "open google":    "google",
    "launch google":  "google",

    "open chatgpt":   "chatgpt",
    "launch chatgpt": "chatgpt",

    "open github":    "github",
    "launch github":  "github",

    "open gmail":     "gmail",
    "open email":     "gmail",
}


# --------------------------------------------------
# YOUTUBE COMMAND PREFIXES
# Any command starting with one of these is a YouTube search.
# --------------------------------------------------

YOUTUBE_PREFIXES = [
    "search youtube for ",
    "search youtube ",
    "youtube search for ",
    "youtube search ",
]


# --------------------------------------------------
# GOOGLE SEARCH PREFIXES
# Any command starting with one of these is a Google search.
# --------------------------------------------------

GOOGLE_PREFIXES = [
    "search google for ",
    "search google ",
    "google search for ",
    "google search ",
    "search for ",
    "search ",
]


# --------------------------------------------------
# TAB CONTROL KEYWORDS
# --------------------------------------------------

CLOSE_TAB_PHRASES = {
    "close tab",
    "close this tab",
    "close the tab",
    "close current tab",
    "close browser tab",
}

NEW_TAB_PHRASES = {
    "new tab",
    "open new tab",
    "create new tab",
}

REOPEN_TAB_PHRASES = {
    "reopen tab",
    "restore tab",
    "reopen closed tab",
}

NEXT_TAB_PHRASES = {
    "next tab",
    "switch tab",
    "switch to next tab",
}

PREVIOUS_TAB_PHRASES = {
    "previous tab",
    "previous browser tab",
    "switch to previous tab",
}


# --------------------------------------------------
# WINDOW CONTROL KEYWORDS
# --------------------------------------------------

CLOSE_WINDOW_PHRASES = {
    "close window",
    "close this window",
    "close current window",
}

MINIMIZE_PHRASES = {
    "minimize window",
    "minimize this window",
    "minimize",
}

MAXIMIZE_PHRASES = {
    "maximize window",
    "maximize this window",
    "maximize",
}


# --------------------------------------------------
# CHROME CONTROL KEYWORDS
# --------------------------------------------------

CLOSE_CHROME_PHRASES = {
    "close chrome",
    "exit chrome",
    "quit chrome",
    "close google chrome",
}


# --------------------------------------------------
# CLOSEABLE APPLICATIONS
# Maps the spoken app name to its Windows process name.
# Used by: "close notepad", "close calculator", etc.
# --------------------------------------------------

CLOSEABLE_APPS = {
    "notepad":    "notepad.exe",
    "calculator": "CalculatorApp.exe",  # Windows 10/11 UWP calculator
    "paint":      "mspaint.exe",
    "wordpad":    "wordpad.exe",
    "explorer":   "explorer.exe",
}


# --------------------------------------------------
# SCREENSHOT KEYWORDS
# --------------------------------------------------

SCREENSHOT_PHRASES = {
    "take screenshot",
    "take a screenshot",
    "screenshot",
    "capture screen",
}


# --------------------------------------------------
# EXIT KEYWORDS
# --------------------------------------------------

EXIT_PHRASES = {
    "exit",
    "quit",
    "shutdown jarvis",
    "shut down",
    "goodbye",
    "bye",
}


# --------------------------------------------------
# NATURAL LANGUAGE TRIGGER WORDS
# --------------------------------------------------

WATCH_WORDS = [
    "watch",
    "play",
    "show me",
    "find video",
]

SEARCH_WORDS = [
    "search for",
    "find",
    "look for",
    "look up",
]

NOTE_WORDS = [
    "write notes",
    "take notes",
    "make notes",
    "write something",
    "open notes",
]

NATURAL_LANGUAGE_REMOVE_WORDS = [
    "jarvis",
    "please",
    "can you",
    "could you",
    "i want to",
    "i wanna",
    "hey",
]
