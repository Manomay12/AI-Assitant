# ==================================================
# JARVIS AI — Vision, Face Presence & Gesture Bridge
# ==================================================

import logging
from typing import Callable, Dict, Optional

logger = logging.getLogger("jarvis.vision.bridge")


class GestureBridge:
    """
    Receives gesture events from the Ultron Frontend MediaPipe tracker
    (e.g. 'spin', 'zoom', 'pinch', 'open_hand', 'fist') and translates them
    into system actions or HUD navigation.
    """

    def __init__(self):
        self._callbacks: Dict[str, Callable] = {}
        self.user_present: bool = False
        self.last_gesture: str = "idle"

    def update_presence(self, is_present: bool):
        self.user_present = is_present

    def handle_gesture_event(self, mode: str, hands_count: int, metadata: Optional[dict] = None):
        """Process incoming gesture data from frontend."""
        self.last_gesture = mode
        self.user_present = hands_count > 0
        logger.debug(f"Gesture event: {mode} ({hands_count} hands)")


gesture_bridge = GestureBridge()
