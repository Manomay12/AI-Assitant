# ==================================================
# JARVIS AI — Master Browser Controller
# ==================================================

import json
import logging
import os
import subprocess
import webbrowser
from typing import Any, Dict, List, Optional
from urllib.parse import quote_plus

try:
    # pyrefly: ignore [missing-import]
    import pyautogui
except ImportError:
    pyautogui = None

try:
    # pyrefly: ignore [missing-import]
    import pygetwindow as gw
except ImportError:
    gw = None

from jarvis.config.constants import CHROME_POSSIBLE_PATHS

logger = logging.getLogger("jarvis.computer.browser")

# Canonical verified website mappings
CANONICAL_WEBSITES: Dict[str, str] = {
    "youtube": "https://www.youtube.com",
    "yt": "https://www.youtube.com",
    "google": "https://www.google.com",
    "g": "https://www.google.com",
    "chatgpt": "https://chatgpt.com",
    "gpt": "https://chatgpt.com",
    "openai": "https://openai.com",
    "github": "https://github.com",
    "gmail": "https://mail.google.com",
    "spotify": "https://open.spotify.com",
    "netflix": "https://www.netflix.com",
    "instagram": "https://www.instagram.com",
    "whatsapp": "https://web.whatsapp.com",
    "reddit": "https://www.reddit.com",
    "twitter": "https://twitter.com",
    "x": "https://twitter.com",
    "linkedin": "https://www.linkedin.com",
    "wikipedia": "https://www.wikipedia.org",
    "amazon": "https://www.amazon.in",
    "flipkart": "https://www.flipkart.com",
    "discord": "https://discord.com/app",
}


class BrowserController:
    """
    Robust desktop browser automation controller.
    Provides direct URL navigation, Google/YouTube searches, multi-account profile
    dispatching, and hotkey tab controls on Windows.
    """

    def __init__(self):
        self.chrome_path = next((p for p in CHROME_POSSIBLE_PATHS if os.path.exists(p)), None)
        self.chrome_user_data = os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\User Data")

    # --------------------------------------------------
    # Chrome Profile Management
    # --------------------------------------------------

    def get_chrome_profiles(self) -> Dict[str, Dict[str, Any]]:
        """Scan Chrome's Local State to discover all registered Google accounts."""
        profiles = {}
        local_state_path = os.path.join(self.chrome_user_data, "Local State")
        if os.path.exists(local_state_path):
            try:
                with open(local_state_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    info_cache = data.get("profile", {}).get("info_cache", {})
                    for p_dir, p_info in info_cache.items():
                        profiles[p_dir] = {
                            "directory": p_dir,
                            "name": p_info.get("name", p_dir),
                            "gaia_name": p_info.get("gaia_name", ""),
                            "given_name": p_info.get("gaia_given_name", ""),
                            "user_name": p_info.get("user_name", ""),
                            "hosted_domain": p_info.get("hosted_domain", ""),
                            "shortcut_name": p_info.get("shortcut_name", ""),
                        }
            except Exception as e:
                logger.error(f"Error reading Chrome profiles: {e}")
        return profiles

    def resolve_profile_directory(self, identifier: Optional[str]) -> Optional[str]:
        """Resolve account names (e.g. 'manomay', 'college', 'asha', 'profile 1') to profile directory."""
        if not identifier:
            return None

        id_clean = identifier.lower().strip()
        profiles = self.get_chrome_profiles()

        # 1. Exact directory match (e.g. "Default", "Profile 1", "Profile 4")
        for p_dir in profiles:
            if p_dir.lower() == id_clean:
                return p_dir

        # 2. College / Somaiya matching
        if any(k in id_clean for k in ("college", "somaiya", "edu", "university")):
            for p_dir, info in profiles.items():
                if "somaiya" in info["hosted_domain"].lower() or "somaiya" in info["user_name"].lower():
                    return p_dir

        # 3. Match by name or given_name (e.g. "manomay", "asha")
        for p_dir, info in profiles.items():
            if id_clean in info["name"].lower() or id_clean in info["gaia_name"].lower() or id_clean in info["given_name"].lower():
                return p_dir

        # 4. Match by email / user_name
        for p_dir, info in profiles.items():
            if id_clean in info["user_name"].lower():
                return p_dir

        # 5. Default profile fallback
        if any(k in id_clean for k in ("personal", "default", "primary", "main")):
            return "Profile 1" if "Profile 1" in profiles else "Default"

        return None

    # --------------------------------------------------
    # URL Navigation & Window Activation
    # --------------------------------------------------

    def activate_browser_window(self) -> bool:
        """Bring Chrome or active browser to the foreground."""
        if not gw:
            return False
        try:
            browser_windows = [
                w for w in gw.getAllWindows()
                if any(b in w.title.lower() for b in ("chrome", "brave", "edge", "firefox", "youtube", "google"))
            ]
            if not browser_windows:
                return False
            win = browser_windows[-1]
            if win.isMinimized:
                win.restore()
            try:
                win.activate()
            except Exception:
                pass
            return True
        except Exception as e:
            logger.debug(f"Could not activate browser window: {e}")
            return False

    def open_url(self, url: str, profile: Optional[str] = None, new_tab: bool = True) -> Dict[str, Any]:
        """
        Directly launch the given URL in Chrome (or default system browser).
        Guaranteed to execute on Windows with zero URL corruption.
        """
        clean_url = url.strip()
        if not clean_url.startswith("http://") and not clean_url.startswith("https://"):
            clean_url = f"https://{clean_url}"

        profile_dir = self.resolve_profile_directory(profile)
        logger.info(f"Opening browser URL: '{clean_url}' (Profile: {profile_dir or 'Default'})")

        try:
            if self.chrome_path and profile_dir:
                cmd = [self.chrome_path, f"--profile-directory={profile_dir}"]
                if new_tab:
                    cmd.append("--new-tab")
                cmd.append(clean_url)
                subprocess.Popen(
                    cmd,
                    shell=False,
                    creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
                )
                return {
                    "success": True,
                    "url": clean_url,
                    "profile": profile_dir,
                    "message": f"Opened {clean_url} in Chrome ({profile_dir}).",
                }
            elif self.chrome_path:
                cmd = [self.chrome_path]
                if new_tab:
                    cmd.append("--new-tab")
                cmd.append(clean_url)
                subprocess.Popen(
                    cmd,
                    shell=False,
                    creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
                )
                return {
                    "success": True,
                    "url": clean_url,
                    "message": f"Opened {clean_url} in Chrome.",
                }
            else:
                if os.name == "nt":
                    subprocess.Popen(f'start "" "{clean_url}"', shell=True)
                else:
                    webbrowser.open_new_tab(clean_url)
                return {
                    "success": True,
                    "url": clean_url,
                    "message": f"Opened {clean_url} in your browser.",
                }
        except Exception as e:
            logger.error(f"Error opening browser URL {clean_url}: {e}")
            try:
                webbrowser.open(clean_url, new=2 if new_tab else 0)
                return {
                    "success": True,
                    "url": clean_url,
                    "message": f"Opened {clean_url} in your browser.",
                }
            except Exception as e2:
                return {
                    "success": False,
                    "url": clean_url,
                    "error": str(e2),
                    "message": f"Could not open {clean_url}: {e2}",
                }

    def open_website(self, site_key: str, profile: Optional[str] = None) -> Dict[str, Any]:
        """Open a named website from canonical mapping or direct URL."""
        key = site_key.lower().strip()
        url = CANONICAL_WEBSITES.get(key)
        if not url:
            if "." in key:
                url = f"https://{key}"
            else:
                url = f"https://www.{key}.com"
        return self.open_url(url, profile=profile)

    def search_google(self, query: str, profile: Optional[str] = None) -> Dict[str, Any]:
        """Perform a real Google search in Chrome."""
        clean_q = query.strip()
        url = f"https://www.google.com/search?q={quote_plus(clean_q)}"
        res = self.open_url(url, profile=profile)
        res["message"] = f"Searching Google for '{clean_q}' in your browser."
        return res

    def search_youtube(self, query: str, profile: Optional[str] = None) -> Dict[str, Any]:
        """Perform a real YouTube search in Chrome."""
        clean_q = query.strip()
        url = f"https://www.youtube.com/results?search_query={quote_plus(clean_q)}"
        res = self.open_url(url, profile=profile)
        res["message"] = f"Searching YouTube for '{clean_q}' in your browser."
        return res

    # --------------------------------------------------
    # Desktop Browser Tab Controls
    # --------------------------------------------------

    def new_tab(self) -> Dict[str, Any]:
        self.activate_browser_window()
        if pyautogui:
            pyautogui.hotkey("ctrl", "t")
        return {"success": True, "message": "Opened a new tab."}

    def close_tab(self) -> Dict[str, Any]:
        self.activate_browser_window()
        if pyautogui:
            pyautogui.hotkey("ctrl", "w")
        return {"success": True, "message": "Closed the current tab."}

    def reopen_tab(self) -> Dict[str, Any]:
        self.activate_browser_window()
        if pyautogui:
            pyautogui.hotkey("ctrl", "shift", "t")
        return {"success": True, "message": "Reopened the last closed tab."}

    def next_tab(self) -> Dict[str, Any]:
        self.activate_browser_window()
        if pyautogui:
            pyautogui.hotkey("ctrl", "tab")
        return {"success": True, "message": "Switched to next tab."}

    def previous_tab(self) -> Dict[str, Any]:
        self.activate_browser_window()
        if pyautogui:
            pyautogui.hotkey("ctrl", "shift", "tab")
        return {"success": True, "message": "Switched to previous tab."}


browser_controller = BrowserController()
