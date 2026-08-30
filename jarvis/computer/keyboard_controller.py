import logging
from typing import List, Union

try:
    import pyautogui
except ImportError:
    pyautogui = None

logger = logging.getLogger("jarvis.computer.keyboard")


class KeyboardController:
    """
    Safely executes keystrokes, shortcuts, text typing, and window hotkeys.
    """

    def __init__(self):
        if pyautogui:
            pyautogui.FAILSAFE = True

    def type_text(self, text: str, interval: float = 0.02) -> bool:
        """Type arbitrary string into currently active element."""
        try:
            pyautogui.write(text, interval=interval)
            return True
        except Exception as e:
            logger.error(f"Error typing text: {e}")
            return False

    def press_hotkey(self, *keys: str) -> bool:
        """Execute a combination key sequence (e.g. 'ctrl', 'c')."""
        try:
            pyautogui.hotkey(*keys)
            return True
        except Exception as e:
            logger.error(f"Error pressing hotkey {keys}: {e}")
            return False

    def minimize_active_window(self) -> bool:
        return self.press_hotkey("win", "down")

    def maximize_active_window(self) -> bool:
        return self.press_hotkey("win", "up")

    def close_active_window(self) -> bool:
        return self.press_hotkey("alt", "f4")
