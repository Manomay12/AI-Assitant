# ==================================================
# JARVIS AI — Short-Term Working Memory
# ==================================================

from collections import deque
from datetime import datetime
from typing import Any, Dict, List, Optional


class ShortTermMemory:
    """
    Maintains ephemeral context of the current session in a sliding window.
    Stores recent turns, currently active application/window context,
    pending follow-ups, and intermediate tool results.
    """

    def __init__(self, max_turns: int = 10):
        self.max_turns = max_turns
        self._turns: deque = deque(maxlen=max_turns)
        self._scratchpad: Dict[str, Any] = {}
        self._active_context: Dict[str, Any] = {
            "current_app": None,
            "active_topic": None,
            "last_action": None,
            "last_action_result": None,
        }

    def add_turn(self, role: str, content: str, metadata: Optional[Dict[str, Any]] = None):
        """Append an interaction turn (user or assistant)."""
        turn = {
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat(),
            "metadata": metadata or {},
        }
        self._turns.append(turn)

    def get_recent_turns(self, count: Optional[int] = None) -> List[Dict[str, Any]]:
        """Retrieve recent interaction turns."""
        turns = list(self._turns)
        if count is not None and count > 0:
            return turns[-count:]
        return turns

    def set_active_context(self, key: str, value: Any):
        """Update a contextual property (e.g. active window title, search query)."""
        self._active_context[key] = value

    def get_active_context(self, key: str, default: Any = None) -> Any:
        return self._active_context.get(key, default)

    def set_scratchpad(self, key: str, value: Any):
        """Store transient variable for multi-step task planning."""
        self._scratchpad[key] = value

    def get_scratchpad(self, key: str, default: Any = None) -> Any:
        return self._scratchpad.get(key, default)

    def clear(self):
        """Reset short term buffer."""
        self._turns.clear()
        self._scratchpad.clear()
        self._active_context.clear()
