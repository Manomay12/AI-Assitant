# ==================================================
# JARVIS 4.0 — Brain (Command Router + AI)
# ==================================================

import requests
from datetime import datetime

from config.settings import OLLAMA_MODEL, OLLAMA_URL, OLLAMA_TIMEOUT
from config.constants import (
    ALLOWED_APPS,
    ALLOWED_WEBSITES,
    WEBSITE_COMMAND_ALIASES,
    YOUTUBE_PREFIXES,
    GOOGLE_PREFIXES,
    CLOSE_TAB_PHRASES,
    NEW_TAB_PHRASES,
    REOPEN_TAB_PHRASES,
    NEXT_TAB_PHRASES,
    PREVIOUS_TAB_PHRASES,
    CLOSE_WINDOW_PHRASES,
    MINIMIZE_PHRASES,
    MAXIMIZE_PHRASES,
    CLOSE_CHROME_PHRASES,
    CLOSEABLE_APPS,
    SCREENSHOT_PHRASES,
    EXIT_PHRASES,
    WATCH_WORDS,
    SEARCH_WORDS,
    NOTE_WORDS,
    NATURAL_LANGUAGE_REMOVE_WORDS,
)


class JarvisBrain:

    def __init__(self, memory, computer):

        self.memory = memory
        self.computer = computer

        self.model = OLLAMA_MODEL
        self.url = OLLAMA_URL
        self.timeout = OLLAMA_TIMEOUT

    # ==================================================
    # MAIN COMMAND HANDLER
    # ==================================================

    def handle(self, text: str) -> str:
        """
        Route the user's command through each handler in priority order.
        Returns the response string to be spoken/displayed.
        """

        command = text.strip()
        lower = command.lower()

        # 1. Help
        if lower == "help":
            return self._help_text()

        # 2. Memory commands
        result = self._handle_memory(command, lower)
        if result is not None:
            return result

        # 3. Open applications (keyword)
        result = self._handle_open_app(lower)
        if result is not None:
            return result

        # 4. Tab controls (keyword)
        result = self._handle_tab_controls(lower)
        if result is not None:
            return result

        # 5. Window controls (keyword)
        result = self._handle_window_controls(lower)
        if result is not None:
            return result

        # 6. Close app or website by name (e.g. "close YouTube", "close Notepad")
        result = self._handle_close_command(lower)
        if result is not None:
            return result

        # 7. Close Chrome (keyword)
        if lower in CLOSE_CHROME_PHRASES:
            return self.computer.close_chrome()

        # 8. Screenshot (keyword)
        if lower in SCREENSHOT_PHRASES:
            return self.computer.screenshot()

        # 9. Open websites (keyword alias)
        if lower in WEBSITE_COMMAND_ALIASES:
            return self.computer.open_website(WEBSITE_COMMAND_ALIASES[lower])

        # 10. YouTube search (keyword prefix)
        result = self._handle_youtube_prefix(command, lower)
        if result is not None:
            return result

        # 11. Google search (keyword prefix)
        result = self._handle_google_prefix(command, lower)
        if result is not None:
            return result

        # 12. Time
        if lower == "time" or "what time is it" in lower:
            return datetime.now().strftime("The local time is %I:%M %p.")

        # 13. Exit
        if lower in EXIT_PHRASES:
            return "Shutting down. Goodbye."

        # 14. Natural language commands (watch/play → YouTube, find → Google)
        result = self._handle_natural_command(command, lower)
        if result is not None:
            return result

        # 15. AI action classifier (OPEN_APP, OPEN_WEBSITE, GOOGLE_SEARCH, etc.)
        action = self._decide_action(command)
        result = self._execute_action(action)
        if result is not None:
            return result

        # 16. Fallback: general AI conversation
        return self._ask_local_ai(command)

    # ==================================================
    # HELP TEXT
    # ==================================================

    def _help_text(self) -> str:

        return (
            "Here are some things I can do:\n\n"

            "Computer:\n"
            "  Open Chrome / Notepad / Calculator\n"
            "  Close tab / New tab / Next tab / Previous tab / Reopen tab\n"
            "  Close window / Minimize window / Maximize window\n"
            "  Close Chrome\n"
            "  Take screenshot\n\n"

            "Web:\n"
            "  Open YouTube / Google / Gmail / ChatGPT / GitHub\n"
            "  Search Google for <topic>\n"
            "  Search YouTube for <topic>\n\n"

            "Memory:\n"
            "  Remember <something>\n"
            "  Memories\n\n"

            "Other:\n"
            "  Time\n"
            "  Help\n"
            "  Exit"
        )

    # ==================================================
    # MEMORY COMMANDS
    # ==================================================

    def _handle_memory(self, command: str, lower: str):

        if lower.startswith("remember "):

            value = command[9:].strip()

            if not value:
                return "What should I remember?"

            self.memory.add(value)
            return "Memory saved."

        if lower in {"memories", "show memories", "list memories"}:

            items = self.memory.all()

            if not items:
                return "I don't have any saved memories yet."

            return "\n".join(
                f"{i + 1}. {item}"
                for i, item in enumerate(items)
            )

        return None

    # ==================================================
    # OPEN APPLICATION (KEYWORD)
    # ==================================================

    def _handle_open_app(self, lower: str):

        app_aliases = {
            "open chrome":        "chrome",
            "launch chrome":      "chrome",
            "start chrome":       "chrome",
            "open google chrome": "chrome",

            "open notepad":    "notepad",
            "launch notepad":  "notepad",
            "start notepad":   "notepad",

            "open calculator":   "calculator",
            "launch calculator": "calculator",
            "start calculator":  "calculator",
        }

        if lower in app_aliases:
            return self.computer.open_app(app_aliases[lower])

        return None

    # ==================================================
    # TAB CONTROLS (KEYWORD)
    # ==================================================

    def _handle_tab_controls(self, lower: str):

        if lower in CLOSE_TAB_PHRASES:
            return self.computer.close_tab()

        if lower in NEW_TAB_PHRASES:
            return self.computer.new_tab()

        if lower in REOPEN_TAB_PHRASES:
            return self.computer.reopen_tab()

        if lower in NEXT_TAB_PHRASES:
            return self.computer.next_tab()

        if lower in PREVIOUS_TAB_PHRASES:
            return self.computer.previous_tab()

        return None

    # ==========================================
    # WINDOW CONTROLS (KEYWORD)
    # ==========================================

    def _handle_window_controls(self, lower: str):

        if lower in CLOSE_WINDOW_PHRASES:
            return self.computer.close_window()

        if lower in MINIMIZE_PHRASES:
            return self.computer.minimize_window()

        if lower in MAXIMIZE_PHRASES:
            return self.computer.maximize_window()

        return None

    # ==================================================
    # CLOSE COMMAND (WEBSITE OR APPLICATION BY NAME)
    # ==================================================

    def _handle_close_command(self, lower: str):

        # Direct app close (e.g. "close notepad", "quit calculator")
        for app_name, proc_name in CLOSEABLE_APPS.items():
            if lower in {f"close {app_name}", f"exit {app_name}", f"quit {app_name}", f"kill {app_name}"}:
                return self.computer.close_app_process(proc_name, app_name.capitalize())

        # Direct website close (e.g. "close youtube", "close google")
        for site in ALLOWED_WEBSITES:
            if lower in {f"close {site}", f"exit {site}", f"quit {site}"}:
                self.computer.activate_chrome()
                return self.computer.close_tab()

        # Catch variations like "please close youtube" or "close the youtube tab"
        if any(w in lower for w in ["close", "exit", "quit", "shut"]):
            for site in ALLOWED_WEBSITES:
                if site in lower:
                    self.computer.activate_chrome()
                    return self.computer.close_tab()

            for app_name, proc_name in CLOSEABLE_APPS.items():
                if app_name in lower:
                    return self.computer.close_app_process(proc_name, app_name.capitalize())

        return None

    # ==================================================
    # YOUTUBE PREFIX SEARCH
    # ==================================================

    def _handle_youtube_prefix(self, command: str, lower: str):

        for prefix in YOUTUBE_PREFIXES:

            if lower.startswith(prefix):
                query = command[len(prefix):].strip()

                if query:
                    return self.computer.youtube_search(query)

                return "What should I search for on YouTube?"

        return None

    # ==================================================
    # GOOGLE PREFIX SEARCH
    # ==================================================

    def _handle_google_prefix(self, command: str, lower: str):

        for prefix in GOOGLE_PREFIXES:

            if lower.startswith(prefix):
                query = command[len(prefix):].strip()

                if query:
                    return self.computer.google_search(query)

                return "What should I search for?"

        return None

    # ==================================================
    # NATURAL LANGUAGE COMMAND DETECTION
    # ==================================================

    def _handle_natural_command(self, command: str, lower: str):

        # Watch / Play → YouTube search
        for word in WATCH_WORDS:

            if word in lower:

                query = lower
                remove = NATURAL_LANGUAGE_REMOVE_WORDS + [
                    "watch", "play", "show me", "find video",
                    "on youtube", "youtube",
                ]

                for item in remove:
                    query = query.replace(item, "")

                query = query.strip()

                if query:
                    return self.computer.youtube_search(query)

        # Find / Search → Google search
        for word in SEARCH_WORDS:

            if word in lower:

                query = lower
                remove = NATURAL_LANGUAGE_REMOVE_WORDS + [
                    "search for", "search", "find",
                    "look for", "look up", "google",
                ]

                for item in remove:
                    query = query.replace(item, "")

                query = query.strip()

                if query:
                    return self.computer.google_search(query)

        # Notes → Notepad
        for word in NOTE_WORDS:
            if word in lower:
                return self.computer.open_app("notepad")

        return None

    # ==================================================
    # AI ACTION CLASSIFIER
    # ==================================================

    def _decide_action(self, command: str) -> str:
        """
        Ask the local AI to classify what kind of action the command is.
        Returns a structured action string like 'OPEN_APP: chrome'.
        """

        # Build the list of allowed sites for the prompt
        site_list = "\n".join(
            f"OPEN_WEBSITE: {name}"
            for name in ALLOWED_WEBSITES
        )

        # Build the list of allowed apps for the prompt
        app_list = "\n".join(
            f"OPEN_APP: {name}"
            for name in ALLOWED_APPS
        )

        prompt = f"""You are the action controller for JARVIS.

Analyze the user's command and choose ONLY ONE of these formats:

{app_list}

{site_list}

CLOSE_APP: notepad
CLOSE_APP: calculator
CLOSE_WEBSITE: <website>
CLOSE_TAB
CLOSE_WINDOW
CLOSE_CHROME

GOOGLE_SEARCH: <query>

YOUTUBE_SEARCH: <query>

CHAT

Examples:

User: I want to listen to relaxing music
Answer: YOUTUBE_SEARCH: relaxing music

User: Close youtube please
Answer: CLOSE_WEBSITE: youtube

User: Close notepad
Answer: CLOSE_APP: notepad

User: Close this tab
Answer: CLOSE_TAB

User: Close this window
Answer: CLOSE_WINDOW

User: Show me beginner Arduino tutorials
Answer: YOUTUBE_SEARCH: beginner Arduino tutorials

User: I need to check my emails
Answer: OPEN_WEBSITE: gmail

User: Find some robotics projects
Answer: GOOGLE_SEARCH: robotics projects

User: I need somewhere to write my notes
Answer: OPEN_APP: notepad

User: What is artificial intelligence?
Answer: CHAT

IMPORTANT:
Return ONLY one line.
Do not explain anything.
Do not add extra text.

User command:
{command}
"""

        try:

            response = requests.post(

                self.url,

                json={
                    "model": self.model,
                    "messages": [
                        {
                            "role": "system",
                            "content": (
                                "You are a strict action classifier. "
                                "Return only one valid action."
                            )
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    "stream": False,
                    "options": {
                        "temperature": 0
                    }
                },

                timeout=self.timeout
            )

            response.raise_for_status()

            data = response.json()
            action = data["message"]["content"].strip()

            # Safety: keep only the first line
            action = action.splitlines()[0].strip()

            print(f"[JARVIS ACTION] {action}")

            return action

        except Exception as e:

            print(f"[JARVIS ACTION ERROR] {e}")
            return "CHAT"

    # ==================================================
    # EXECUTE AI ACTION
    # ==================================================

    def _execute_action(self, action: str):
        """
        Execute a structured action string.
        Returns the result string, or None if the action is CHAT.
        """

        action = action.strip()

        # OPEN_APP
        if action.startswith("OPEN_APP:"):

            app = action.split(":", 1)[1].strip().lower()

            if app in ALLOWED_APPS:
                return self.computer.open_app(app)

            return None

        # CLOSE_APP
        if action.startswith("CLOSE_APP:"):

            app = action.split(":", 1)[1].strip().lower()

            if app in CLOSEABLE_APPS:
                return self.computer.close_app_process(CLOSEABLE_APPS[app], app.capitalize())

            return None

        # OPEN_WEBSITE
        if action.startswith("OPEN_WEBSITE:"):

            website = action.split(":", 1)[1].strip().lower()

            if website in ALLOWED_WEBSITES:
                return self.computer.open_website(website)

            return None

        # CLOSE_WEBSITE
        if action.startswith("CLOSE_WEBSITE:"):

            self.computer.activate_chrome()
            return self.computer.close_tab()

        # CLOSE_TAB
        if action == "CLOSE_TAB":
            self.computer.activate_chrome()
            return self.computer.close_tab()

        # CLOSE_WINDOW
        if action == "CLOSE_WINDOW":
            return self.computer.close_window()

        # CLOSE_CHROME
        if action == "CLOSE_CHROME":
            return self.computer.close_chrome()

        # GOOGLE_SEARCH
        if action.startswith("GOOGLE_SEARCH:"):

            query = action.split(":", 1)[1].strip()

            if query:
                return self.computer.google_search(query)

            return None

        # YOUTUBE_SEARCH
        if action.startswith("YOUTUBE_SEARCH:"):

            query = action.split(":", 1)[1].strip()

            if query:
                return self.computer.youtube_search(query)

            return None

        # CHAT — handled by the caller
        return None

    # ==================================================
    # LOCAL AI CONVERSATION
    # ==================================================

    def _ask_local_ai(self, text: str) -> str:
        """
        Send the user's message to the local Ollama AI and return the response.
        """

        try:

            response = requests.post(

                self.url,

                json={
                    "model": self.model,
                    "messages": [
                        {
                            "role": "system",
                            "content": (
                                "You are JARVIS 4.0, "
                                "a helpful personal AI assistant. "
                                "You are running locally through Ollama "
                                "on a Windows computer. "
                                "Answer clearly and naturally. "
                                "Keep responses concise unless "
                                "the user asks for details."
                            )
                        },
                        {
                            "role": "user",
                            "content": text
                        }
                    ],
                    "stream": False
                },

                timeout=self.timeout
            )

            response.raise_for_status()

            data = response.json()
            return data["message"]["content"]

        except requests.exceptions.ConnectionError:

            return (
                "I cannot connect to my local AI brain. "
                "Please make sure Ollama is running."
            )

        except requests.exceptions.Timeout:

            return "The local AI took too long to respond."

        except Exception as e:

            print(f"[JARVIS AI ERROR] {e}")
            return f"AI error: {e}"