# ==================================================
# JARVIS AI — Conversation History Store
# ==================================================

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional
from jarvis.config.settings import settings

logger = logging.getLogger("jarvis.memory.conversation")


class ConversationHistory:
    """
    Persists full chat logs with role, timestamps, metadata, and tool execution links.
    Supports session archiving, querying by keyword/date, and history wiping.
    """

    def __init__(self, storage_path: Path = settings.CONVERSATION_FILE):
        self.storage_path = Path(storage_path)
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        self._history: List[Dict[str, Any]] = []
        self._load()

    def _load(self):
        try:
            if self.storage_path.exists():
                content = self.storage_path.read_text(encoding="utf-8").strip()
                if content:
                    data = json.loads(content)
                    self._history = data.get("messages", [])
                else:
                    self._history = []
            else:
                self._history = []
                self._save()
        except Exception as e:
            logger.error(f"Error loading conversation history: {e}")
            self._history = []

    def _save(self):
        try:
            payload = {"messages": self._history[-500:]}  # Keep last 500 records
            self.storage_path.write_text(
                json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8"
            )
        except Exception as e:
            logger.error(f"Error saving conversation history: {e}")

    def append(self, role: str, message: str, tool_calls: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
        """Record a chat message."""
        entry = {
            "id": f"msg_{len(self._history) + 1}",
            "role": role,
            "message": message,
            "timestamp": datetime.now().isoformat(),
            "tool_calls": tool_calls or [],
        }
        self._history.append(entry)
        self._save()
        return entry

    def get_all(self) -> List[Dict[str, Any]]:
        return list(self._history)

    def get_recent(self, count: int = 50) -> List[Dict[str, Any]]:
        return self._history[-count:]

    def clear(self):
        self._history = []
        self._save()


conversation_history = ConversationHistory()
