# ==================================================
# JARVIS 4.0 — Computer Tools (Windows)
# ==================================================

import os
import subprocess
import time

import pyautogui
import pygetwindow as gw

from urllib.parse import quote_plus

from config.settings import CHROME_PROFILE, SCREENSHOT_FILENAME
from config.constants import (
    CHROME_POSSIBLE_PATHS,
    ALLOWED_WEBSITES,
)


class ComputerTools:

    def __init__(self):

        # Locate the Chrome executable automatically
        self.chrome_path = None

        for path in CHROME_POSSIBLE_PATHS:
            if os.path.exists(path):
                self.chrome_path = path
                break

        self.chrome_profile = CHROME_PROFILE

        print("=" * 44)
        if self.chrome_path:
            print(f"[JARVIS] Chrome found at: {self.chrome_path}")
        else:
            print("[JARVIS] WARNING: Google Chrome was not found.")
        print(f"[JARVIS] Chrome profile: {self.chrome_profile}")
        print("=" * 44)


    # ==========================================
    # OPEN APPLICATIONS
    # ==========================================

    def open_app(self, app: str) -> str:
        """Launch a named application. Only allowed apps will be opened."""

        try:

            app = app.lower().strip()

            if app == "chrome":

                if not self.chrome_path:
                    return "Google Chrome was not found on this computer."

                subprocess.Popen(
                    [
                        self.chrome_path,
                        f"--profile-directory={self.chrome_profile}"
                    ],
                    shell=False
                )

                time.sleep(2)
                self.activate_chrome()

                return "Opening Google Chrome."

            elif app == "notepad":

                subprocess.Popen(["notepad.exe"])
                return "Opening Notepad."

            elif app == "calculator":

                subprocess.Popen(["calc.exe"])
                return "Opening Calculator."

            return f"I don't know how to open '{app}' yet."

        except Exception as e:

            print(f"[JARVIS APP ERROR] {e}")
            return f"I couldn't open '{app}': {e}"


    # ==========================================
    # ACTIVATE CHROME WINDOW
    # ==========================================

    def activate_chrome(self) -> bool:
        """Bring the most recent Chrome window to the foreground."""

        try:

            chrome_windows = [
                w for w in gw.getAllWindows()
                if "chrome" in w.title.lower()
            ]

            if not chrome_windows:
                return False

            window = chrome_windows[-1]

            if window.isMinimized:
                window.restore()

            try:
                window.activate()
            except Exception:
                pass

            return True

        except Exception as e:

            print(f"[JARVIS WINDOW ERROR] {e}")
            return False


    # ==========================================
    # OPEN URL IN CHROME
    # ==========================================

    def open_url_in_chrome(self, url: str) -> str:
        """Open a specific URL in Chrome using the configured profile."""

        try:

            if not self.chrome_path:
                return "Google Chrome was not found on this computer."

            print(f"[JARVIS] Opening URL: {url}")

            subprocess.Popen(
                [
                    self.chrome_path,
                    f"--profile-directory={self.chrome_profile}",
                    "--new-tab",
                    url
                ],
                shell=False
            )

            time.sleep(2)
            self.activate_chrome()

            return "The page has been opened in Google Chrome."

        except Exception as e:

            print(f"[JARVIS CHROME ERROR] {e}")
            return f"Chrome error: {e}"


    # ==========================================
    # CLOSE GOOGLE CHROME
    # ==========================================

    def close_chrome(self) -> str:
        """Forcefully close all Chrome windows."""

        try:

            result = subprocess.run(
                ["taskkill", "/F", "/IM", "chrome.exe"],
                capture_output=True,
                text=True
            )

            if result.returncode == 0:
                return "Google Chrome has been closed."

            return "Google Chrome is not currently running."

        except Exception as e:

            return f"I couldn't close Google Chrome: {e}"


    # ==========================================
    # CLOSE ANY APPLICATION BY PROCESS NAME
    # ==========================================

    def close_app_process(self, process_name: str, display_name: str) -> str:
        """
        Close an application by its Windows process name.
        'process_name' is the .exe filename (e.g. 'notepad.exe').
        'display_name' is what to say to the user (e.g. 'Notepad').
        """

        try:

            result = subprocess.run(
                ["taskkill", "/F", "/IM", process_name],
                capture_output=True,
                text=True
            )

            if result.returncode == 0:
                return f"{display_name} has been closed."

            if display_name.lower() == "calculator":
                for alt_proc in ["Calculator.exe", "calc.exe"]:
                    alt_result = subprocess.run(
                        ["taskkill", "/F", "/IM", alt_proc],
                        capture_output=True,
                        text=True
                    )
                    if alt_result.returncode == 0:
                        return f"{display_name} has been closed."

            return f"{display_name} is not currently running."

        except Exception as e:

            print(f"[JARVIS CLOSE ERROR] {e}")
            return f"I couldn't close {display_name}: {e}"


    # ==========================================
    # OPEN WEBSITES
    # ==========================================

    def open_website(self, website: str) -> str:
        """Open a named website. Only websites in the allowlist are permitted."""

        website = website.lower().strip()

        if website not in ALLOWED_WEBSITES:
            return f"I don't have '{website}' in my allowed websites list."

        return self.open_url_in_chrome(ALLOWED_WEBSITES[website])


    # ==========================================
    # GOOGLE SEARCH
    # ==========================================

    def google_search(self, query: str) -> str:
        """Perform a Google search in Chrome."""

        url = "https://www.google.com/search?q=" + quote_plus(query)
        return self.open_url_in_chrome(url)


    # ==========================================
    # YOUTUBE SEARCH
    # ==========================================

    def youtube_search(self, query: str) -> str:
        """Perform a YouTube search in Chrome."""

        url = (
            "https://www.youtube.com/results?search_query="
            + quote_plus(query)
        )
        return self.open_url_in_chrome(url)


    # ==========================================
    # TAB CONTROLS
    # ==========================================

    def close_tab(self) -> str:
        pyautogui.hotkey("ctrl", "w")
        return "Closing the current tab."

    def new_tab(self) -> str:
        pyautogui.hotkey("ctrl", "t")
        return "Opening a new tab."

    def reopen_tab(self) -> str:
        pyautogui.hotkey("ctrl", "shift", "t")
        return "Reopening the last closed tab."

    def next_tab(self) -> str:
        pyautogui.hotkey("ctrl", "tab")
        return "Switching to the next tab."

    def previous_tab(self) -> str:
        pyautogui.hotkey("ctrl", "shift", "tab")
        return "Switching to the previous tab."


    # ==========================================
    # WINDOW CONTROLS
    # ==========================================

    def close_window(self) -> str:
        pyautogui.hotkey("alt", "f4")
        return "Closing the current window."

    def minimize_window(self) -> str:
        pyautogui.hotkey("win", "down")
        return "Minimizing the current window."

    def maximize_window(self) -> str:
        pyautogui.hotkey("win", "up")
        return "Maximizing the current window."


    # ==========================================
    # SCREENSHOT
    # ==========================================

    def screenshot(self) -> str:
        """Capture the full screen and save it to disk."""

        try:

            image = pyautogui.screenshot()
            image.save(SCREENSHOT_FILENAME)
            return f"Screenshot saved as '{SCREENSHOT_FILENAME}'."

        except Exception as e:

            print(f"[JARVIS SCREENSHOT ERROR] {e}")
            return f"I couldn't take a screenshot: {e}"