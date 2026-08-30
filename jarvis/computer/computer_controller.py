# ==================================================
# JARVIS AI — Unified Computer Controller
# ==================================================

import logging
from typing import Any, Dict, List, Optional
from jarvis.computer.application_manager import ApplicationManager
from jarvis.computer.browser_controller import BrowserController
from jarvis.computer.keyboard_controller import KeyboardController
from jarvis.computer.mouse_controller import MouseController

logger = logging.getLogger("jarvis.computer")


class ComputerController:
    """
    Unified coordinator for all computer control actions.
    Aggregates application lifecycle, browser navigation, keyboard, and mouse control.
    """

    def __init__(self):
        self.app_manager = ApplicationManager()
        self.browser = BrowserController()
        self.keyboard = KeyboardController()
        self.mouse = MouseController()

    def open_app(self, app_name: str) -> Dict[str, Any]:
        return self.app_manager.open_application(app_name)

    def close_app(self, app_name: str) -> Dict[str, Any]:
        return self.app_manager.close_application(app_name)

    def open_url(self, url: str, profile: Optional[str] = None) -> Dict[str, Any]:
        return self.browser.open_url(url, profile=profile)

    def open_website(self, site_key: str, profile: Optional[str] = None) -> Dict[str, Any]:
        return self.browser.open_website(site_key, profile=profile)

    def google_search(self, query: str, profile: Optional[str] = None) -> Dict[str, Any]:
        return self.browser.search_google(query, profile=profile)

    def youtube_search(self, query: str, profile: Optional[str] = None) -> Dict[str, Any]:
        return self.browser.search_youtube(query, profile=profile)

    def list_chrome_profiles(self) -> Dict[str, Dict[str, Any]]:
        return self.browser.get_chrome_profiles()

    def minimize_window(self) -> Dict[str, Any]:
        success = self.keyboard.minimize_active_window()
        return {"success": success, "message": "Minimizing current window."}

    def maximize_window(self) -> Dict[str, Any]:
        success = self.keyboard.maximize_active_window()
        return {"success": success, "message": "Maximizing current window."}

    def close_window(self) -> Dict[str, Any]:
        success = self.keyboard.close_active_window()
        return {"success": success, "message": "Closing current window."}

    def list_open_windows(self) -> List[str]:
        return self.app_manager.get_open_windows()


computer_controller = ComputerController()
