import logging
from typing import Optional, Tuple

try:
    import pyautogui
except ImportError:
    pyautogui = None

logger = logging.getLogger("jarvis.computer.mouse")


class MouseController:
    """
    Handles mouse movements, verified target clicks, and scrolling.
    Includes bounds checking to avoid clicks outside display coordinates.
    """

    def __init__(self):
        if pyautogui:
            pyautogui.FAILSAFE = True
            self.screen_width, self.screen_height = pyautogui.size()
        else:
            self.screen_width, self.screen_height = (1920, 1080)

    def click(self, x: int, y: int, button: str = "left", clicks: int = 1) -> bool:
        """Click at specific coordinates with bounds protection."""
        if not (0 <= x <= self.screen_width and 0 <= y <= self.screen_height):
            logger.error(f"Mouse click coordinate ({x}, {y}) out of screen bounds ({self.screen_width}x{self.screen_height})")
            return False

        try:
            pyautogui.click(x=x, y=y, clicks=clicks, button=button)
            return True
        except Exception as e:
            logger.error(f"Error clicking mouse at ({x}, {y}): {e}")
            return False

    def scroll(self, clicks: int) -> bool:
        """Scroll mouse wheel vertically (positive = up, negative = down)."""
        try:
            pyautogui.scroll(clicks)
            return True
        except Exception as e:
            logger.error(f"Error scrolling mouse: {e}")
            return False

    def get_position(self) -> Tuple[int, int]:
        return pyautogui.position()
