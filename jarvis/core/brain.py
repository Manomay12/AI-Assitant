# ==================================================
# JARVIS AI — Master Brain & Intent Orchestrator
# ==================================================

import json
import logging
import re
from typing import Any, Dict, List, Optional, Tuple
import requests
from jarvis.config.constants import DEFAULT_APPS, DEFAULT_WEBSITES, EXIT_PHRASES
from jarvis.config.settings import settings
from jarvis.memory.long_term_memory import long_term_memory
from jarvis.tools.registry import tool_registry

logger = logging.getLogger("jarvis.core.brain")

# Canonical aliases
WEBSITE_MAP: Dict[str, str] = {
    "yt": "youtube",
    "youtube": "youtube",
    "google": "google",
    "g": "google",
    "chatgpt": "chatgpt",
    "gpt": "chatgpt",
    "openai": "chatgpt",
    "github": "github",
    "git": "github",
    "gmail": "gmail",
    "mail": "gmail",
    "spotify": "spotify",
    "music": "spotify",
    "instagram": "instagram",
    "insta": "instagram",
    "ig": "instagram",
    "netflix": "netflix",
    "wikipedia": "wikipedia",
    "wiki": "wikipedia",
    "reddit": "reddit",
    "twitter": "twitter",
    "x": "twitter",
    "linkedin": "linkedin",
    "whatsapp": "whatsapp",
    "amazon": "amazon",
    "flipkart": "flipkart",
    "discord": "discord",
}

APP_MAP: Dict[str, str] = {
    "notepad": "notepad",
    "calculator": "calculator",
    "calc": "calculator",
    "chrome": "chrome",
    "google chrome": "chrome",
    "vscode": "code",
    "vs code": "code",
    "code": "code",
    "visual studio code": "code",
    "paint": "paint",
    "mspaint": "paint",
    "cmd": "cmd",
    "command prompt": "cmd",
    "terminal": "powershell",
    "powershell": "powershell",
    "taskmgr": "taskmgr",
    "task manager": "taskmgr",
    "explorer": "explorer",
    "file explorer": "explorer",
    "settings": "settings",
    "camera": "camera",
    "word": "word",
    "excel": "excel",
    "powerpoint": "powerpoint",
}


def parse_account_and_clean_target(text: str) -> Tuple[str, Optional[str]]:
    """
    Safely extract account / profile modifiers and return (cleaned_text, profile).
    e.g. 'open youtube in manomay account' -> ('open youtube', 'manomay')
         'youtube in college account' -> ('youtube', 'college')
         'open youtube in chrome' -> ('open youtube', None)
    """
    raw = text.strip()

    # 1. Check for specific account names: manomay, asha, college, somaiya, personal, work, default, profile \d+
    m = re.search(
        r"\s+(?:in|on|with|using)\s+(?:my\s+)?(?:account\s+)?(manomay|asha|college|somaiya|personal|work|profile\s*\d+|default)(?:\s+(?:account|profile|id))?$",
        raw,
        re.IGNORECASE,
    )
    if m:
        profile_name = m.group(1).strip()
        cleaned = raw[: m.start()].strip()
        return cleaned, profile_name

    # 2. Clean out generic "in chrome" / "in browser" / "on chrome" suffixes
    cleaned = re.sub(
        r"\s+(?:in|on|with|using)\s+(?:google\s+)?(?:chrome|browser)$",
        "",
        raw,
        flags=re.IGNORECASE,
    ).strip()

    return cleaned, None


class JarvisBrain:
    """
    Central intelligence orchestrator.
    Deterministic high-speed routing for system & browser control with zero URL corruption.
    """

    def __init__(self):
        self.provider = settings.AI_PROVIDER
        self.system_prompt = (
            "You are JARVIS, an advanced, highly capable personal AI assistant and digital companion "
            "with holographic interface capabilities inspired by Sci-Fi HUD systems. "
            "You control computer functions, manage research, productivity, memory, and conversation. "
            "Always be concise, precise, intelligent, and helpful. "
            "Never hallucinate having completed a real-world task without using the appropriate tools."
        )

    # ==================================================
    # DETERMINISTIC FAST INTENT ROUTER
    # ==================================================

    def fast_route(self, text: str) -> Optional[Tuple[str, Dict[str, Any]]]:
        """
        Evaluate instant deterministic commands without LLM network roundtrips.
        Returns (tool_name, kwargs) or None if requires general conversation.
        """
        raw = text.strip()
        lower = raw.lower()

        # Remove polite prefixes / wake words
        clean = re.sub(r"^(hey\s+)?(jarvis|ultron)[\s,:]*", "", lower).strip()
        clean = re.sub(r"^(please|can\s+you|could\s+you|just|i\s+want\s+you\s+to|i\s+want\s+to)\s+", "", clean).strip()

        if not clean:
            return None

        # 1. Exit / Shutdown
        if clean in EXIT_PHRASES or lower in EXIT_PHRASES:
            return ("exit", {})

        # 2. Time & Date
        if any(clean == p or clean.startswith(p) for p in ("time", "what time", "tell me the time", "current time", "samay", "time kya", "date", "what is today's date", "today's date")):
            return ("get_current_time", {})

        # 3. Screenshot & Screen Analysis
        if any(p in clean for p in ("take screenshot", "take a screenshot", "screenshot le lo", "capture screen", "screenshot")):
            return ("take_screenshot", {})
        if any(p in clean for p in ("analyze screen", "read screen", "screen pe kya hai", "what is on my screen")):
            return ("screen_analysis", {})

        # 4. System Status & Accounts
        if clean in ("system status", "status", "hardware stats", "pc status", "battery status", "cpu status", "battery", "ram status"):
            return ("get_system_status", {})
        if any(clean == p for p in ("list chrome profiles", "chrome profiles", "show accounts", "list accounts", "my accounts", "show profiles", "list profiles")):
            return ("list_chrome_profiles", {})

        # 5. Desktop Browser Tab Controls
        if any(clean == p for p in ("new tab", "open new tab", "naya tab kholo", "open a tab", "add tab", "open a new tab")):
            return ("tab_controls", {"action": "new_tab"})
        if any(clean == p for p in ("close tab", "close this tab", "tab band karo", "tab close karo", "close the tab")):
            return ("tab_controls", {"action": "close_tab"})
        if any(clean == p for p in ("reopen tab", "restore tab", "undo close tab", "reopen closed tab", "reopen the previous tab")):
            return ("tab_controls", {"action": "reopen_tab"})
        if any(clean == p for p in ("next tab", "switch tab", "agla tab", "switch to next tab")):
            return ("tab_controls", {"action": "next_tab"})
        if any(clean == p for p in ("previous tab", "prev tab", "pichhla tab", "switch to previous tab")):
            return ("tab_controls", {"action": "previous_tab"})

        # 6. Window Controls
        if any(clean == p for p in ("minimize window", "minimize", "chhota karo", "minimize this window")):
            return ("window_controls", {"action": "minimize"})
        if any(clean == p for p in ("maximize window", "maximize", "bada karo", "maximize this window")):
            return ("window_controls", {"action": "maximize"})
        if any(clean == p for p in ("close window", "window band karo", "close this window")):
            return ("window_controls", {"action": "close"})

        # 7. YouTube Search (English & Hinglish)
        yt_hinglish = re.search(r"^(?:youtube|yt)\s+(?:pe|par)\s+(.+?)(?:\s+(?:search\s+karo|search|dekho|chalao|dikhao))?$", clean)
        if yt_hinglish:
            q_part = yt_hinglish.group(1).strip()
            q_clean, profile = parse_account_and_clean_target(q_part)
            if q_clean:
                kwargs = {"query": q_clean}
                if profile:
                    kwargs["profile"] = profile
                return ("youtube_search", kwargs)

        yt_search_pattern = r"^(?:open\s+(?:youtube|yt)\s+(?:and\s+)?(?:search\s+(?:for\s+)?|play\s+)|search\s+(?:on\s+)?(?:youtube|yt)\s+for\s+|search\s+(?:youtube|yt)\s+for\s+|play\s+on\s+(?:youtube|yt)\s+|play\s+|watch\s+)(.+)$"
        yt_m = re.match(yt_search_pattern, clean)
        if yt_m:
            query_part = yt_m.group(1).strip()
            query_clean, profile = parse_account_and_clean_target(query_part)
            query_clean = re.sub(r"\s+(?:on\s+youtube|karo|dikhao|chalao|search)$", "", query_clean).strip()
            if query_clean:
                kwargs = {"query": query_clean}
                if profile:
                    kwargs["profile"] = profile
                return ("youtube_search", kwargs)

        # 8. Google Search (English & Hinglish)
        g_hinglish = re.search(r"^(?:google|g)\s+(?:pe|par)\s+(.+?)(?:\s+(?:search\s+karo|search|dekho|dikhao))?$", clean)
        if g_hinglish:
            q_part = g_hinglish.group(1).strip()
            q_clean, profile = parse_account_and_clean_target(q_part)
            if q_clean:
                kwargs = {"query": q_clean}
                if profile:
                    kwargs["profile"] = profile
                return ("browser_search", kwargs)

        google_search_pattern = r"^(?:search\s+google\s+for\s+|google\s+search\s+for\s+|google\s+pe\s+search\s+karo\s+|search\s+for\s+|search\s+)(.+)$"
        g_m = re.match(google_search_pattern, clean)
        if g_m:
            query_part = g_m.group(1).strip()
            query_clean, profile = parse_account_and_clean_target(query_part)
            if query_clean and not any(query_clean.startswith(k) for k in ("youtube", "yt")):
                kwargs = {"query": query_clean}
                if profile:
                    kwargs["profile"] = profile
                return ("browser_search", kwargs)

        # 9. Open Website or Application
        # e.g. "open youtube in manomay account", "open youtube in chrome", "open notepad", "youtube", "chrome"
        open_cmd_pattern = r"^(?:open|launch|start|go\s+to|visit)\s+(?:the\s+)?(.+)$"
        open_m = re.match(open_cmd_pattern, clean)
        if open_m:
            target_raw = open_m.group(1).strip()
            target_clean, profile = parse_account_and_clean_target(target_raw)

            # Check website map
            if target_clean in WEBSITE_MAP:
                kwargs = {"website": WEBSITE_MAP[target_clean]}
                if profile:
                    kwargs["profile"] = profile
                return ("open_website", kwargs)

            # Check direct domain (e.g. "github.com", "google.com")
            if "." in target_clean or target_clean.startswith("http"):
                kwargs = {"website": target_clean}
                if profile:
                    kwargs["profile"] = profile
                return ("open_website", kwargs)

            # Check application map
            if target_clean in APP_MAP:
                return ("open_application", {"app_name": APP_MAP[target_clean]})

            # Default to website
            kwargs = {"website": target_clean}
            if profile:
                kwargs["profile"] = profile
            return ("open_website", kwargs)

        # Direct Single-Keyword Triggers (e.g. "youtube", "yt", "notepad", "calculator", "chrome")
        clean_target, profile = parse_account_and_clean_target(clean)
        if clean_target in WEBSITE_MAP:
            kwargs = {"website": WEBSITE_MAP[clean_target]}
            if profile:
                kwargs["profile"] = profile
            return ("open_website", kwargs)
        if clean_target in APP_MAP:
            return ("open_application", {"app_name": APP_MAP[clean_target]})

        # 10. Close Application
        close_m = re.match(r"^(?:close|quit|kill|stop|terminate)\s+(?:the\s+)?(.+)$", clean)
        if close_m:
            target = close_m.group(1).strip()
            target_clean, _ = parse_account_and_clean_target(target)
            if target_clean in APP_MAP:
                return ("close_application", {"app_name": APP_MAP[target_clean]})
            if target_clean in DEFAULT_APPS:
                return ("close_application", {"app_name": target_clean})

        # 11. Memory Commands
        if clean.startswith("remember ") or clean.startswith("yaad rakho ") or clean.startswith("remember that "):
            content = re.sub(r"^(remember that|remember|yaad rakho)\s+", "", clean).strip()
            return ("manage_memory", {"action": "remember", "content": content})
        if clean in ("memories", "show memories", "what do you remember", "kya yaad hai", "list memories", "my memories"):
            return ("manage_memory", {"action": "recall"})

        # 12. Workflows
        if clean in ("study mode", "activate study mode", "start study mode"):
            return ("execute_workflow", {"workflow_name": "study mode"})
        if clean in ("work mode", "activate work mode", "start work mode"):
            return ("execute_workflow", {"workflow_name": "work mode"})

        # 13. Internet Research
        research_match = re.search(r"^(?:research|find information on|tell me about|who is|what is|compare)\s+(.+)", clean)
        if research_match:
            subject = research_match.group(1).strip()
            if len(subject) > 2 and not any(k in subject for k in ("time", "status", "tab", "window")):
                return ("web_research", {"query": clean})

        return None

    # ==================================================
    # AI LLM INFERENCE (NVIDIA / OLLAMA / GEMINI / OPENAI)
    # ==================================================

    def generate_response(self, user_message: str, chat_history: Optional[List[Dict[str, str]]] = None) -> str:
        """Query the configured AI provider or fallback smoothly."""
        msg_clean = user_message.lower().strip()
        if msg_clean in ("hello", "hi", "hey", "namaste", "hey jarvis", "hey ultron"):
            return "Hello Sir! JARVIS systems are fully operational and ready for your command."

        if msg_clean in ("who are you", "what is your name", "kya naam hai"):
            return "I am JARVIS, your personal next-generation AI companion integrated with the holographic Ultron interface."

        if msg_clean in ("help", "what can you do", "features"):
            return (
                "I can assist with real-world computer control (opening apps & websites in Chrome across any Google account, tab controls, screenshots), "
                "YouTube & Google searching, multi-source web research, memory management, "
                "custom automation workflows, and real-time voice & gesture interactions."
            )

        # 1. Try NVIDIA Free API first if configured
        if settings.NVIDIA_API_KEY and len(settings.NVIDIA_API_KEY.strip()) > 10:
            res = self._call_nvidia_api(user_message, chat_history)
            if res:
                return res

        # 2. Try Gemini if configured
        if settings.GEMINI_API_KEY and len(settings.GEMINI_API_KEY.strip()) > 10:
            res = self._call_gemini_api(user_message)
            if res:
                return res

        # 3. Try Local Ollama
        res = self._call_ollama(user_message, chat_history)
        if res:
            return res

        # 4. Fallback
        return f"Understood: '{user_message}'. I am processing your request."

    def _call_nvidia_api(self, user_message: str, history: Optional[List[Dict[str, str]]] = None) -> Optional[str]:
        """Query NVIDIA NIM API (OpenAI-compatible endpoint)."""
        try:
            headers = {
                "Authorization": f"Bearer {settings.NVIDIA_API_KEY}",
                "Content-Type": "application/json",
            }
            messages = [{"role": "system", "content": self.system_prompt}]
            if history:
                messages.extend(history[-6:])
            messages.append({"role": "user", "content": user_message})

            url = f"{settings.NVIDIA_BASE_URL.rstrip('/')}/chat/completions"
            payload = {
                "model": settings.NVIDIA_MODEL,
                "messages": messages,
                "temperature": 0.5,
                "max_tokens": 512,
            }
            resp = requests.post(url, headers=headers, json=payload, timeout=20)
            if resp.status_code == 200:
                data = resp.json()
                return data["choices"][0]["message"]["content"].strip()
            else:
                logger.warning(f"NVIDIA API status {resp.status_code}: {resp.text}")
        except Exception as e:
            logger.error(f"NVIDIA API call error: {e}")
        return None

    def _call_gemini_api(self, user_message: str) -> Optional[str]:
        """Query Google Gemini API."""
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{settings.GEMINI_MODEL}:generateContent?key={settings.GEMINI_API_KEY}"
            payload = {
                "contents": [
                    {
                        "parts": [
                            {"text": f"{self.system_prompt}\n\nUser: {user_message}"}
                        ]
                    }
                ]
            }
            resp = requests.post(url, json=payload, timeout=20)
            if resp.status_code == 200:
                data = resp.json()
                candidates = data.get("candidates", [])
                if candidates:
                    return candidates[0]["content"]["parts"][0]["text"].strip()
        except Exception as e:
            logger.error(f"Gemini API error: {e}")
        return None

    def _call_ollama(self, user_message: str, history: Optional[List[Dict[str, str]]] = None) -> Optional[str]:
        """Query Local Ollama API."""
        try:
            messages = [{"role": "system", "content": self.system_prompt}]
            if history:
                messages.extend(history[-6:])
            messages.append({"role": "user", "content": user_message})

            resp = requests.post(
                settings.OLLAMA_URL,
                json={
                    "model": settings.OLLAMA_MODEL,
                    "messages": messages,
                    "stream": False,
                    "options": {"temperature": 0.5},
                },
                timeout=settings.OLLAMA_TIMEOUT,
            )
            if resp.status_code == 200:
                data = resp.json()
                return data["message"]["content"].strip()
        except Exception as e:
            logger.debug(f"Ollama local AI error: {e}")
        return None


brain = JarvisBrain()
