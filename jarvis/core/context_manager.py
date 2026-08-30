from datetime import datetime
from typing import Any, Dict

try:
    import psutil
except ImportError:
    psutil = None

from jarvis.memory.short_term_memory import ShortTermMemory
from jarvis.memory.user_preferences import user_preferences
from jarvis.vision.screen_reader import screen_reader


class ContextManager:
    """
    Synthesizes real-time device context, active window state,
    recent conversation turns, and user preferences.
    """

    def __init__(self, short_term_memory: ShortTermMemory):
        self.stm = short_term_memory

    def get_full_context(self) -> Dict[str, Any]:
        """Compile a complete situational snapshot."""
        active_win = screen_reader.get_active_window_info()
        recent_turns = self.stm.get_recent_turns(count=5)
        prefs = user_preferences.get_all()

        return {
            "current_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "active_window": active_win.get("title", ""),
            "user_name": prefs.get("user_name", "Sir"),
            "preferred_language": prefs.get("preferred_language", "en"),
            "recent_turns": recent_turns,
            "cpu_usage": psutil.cpu_percent() if psutil else 10.0,
            "ram_usage": psutil.virtual_memory().percent if psutil else 40.0,
        }
