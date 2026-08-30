# ==================================================
# JARVIS AI — Long-Term Structured Memory
# ==================================================

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional
from jarvis.config.settings import settings

logger = logging.getLogger("jarvis.memory.long_term")


class LongTermMemory:
    """
    Persistent memory store for facts, preferences, user knowledge, and notes.
    Provides methods to add, retrieve, query, remove, and clear items safely.
    """

    def __init__(self, storage_path: Path = settings.MEMORY_FILE):
        self.storage_path = Path(storage_path)
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        self._memories: List[Dict[str, Any]] = []
        self._load()

    def _load(self):
        try:
            if self.storage_path.exists():
                content = self.storage_path.read_text(encoding="utf-8").strip()
                if content:
                    data = json.loads(content)
                    if isinstance(data, list):
                        # Convert legacy plain strings to structured dicts if needed
                        self._memories = [
                            m if isinstance(m, dict) else {"id": str(i + 1), "text": m, "timestamp": datetime.now().isoformat()}
                            for i, m in enumerate(data)
                        ]
                    elif isinstance(data, dict):
                        self._memories = data.get("memories", [])
                else:
                    self._memories = []
            else:
                self._memories = []
                self._save()
        except Exception as e:
            logger.error(f"Error loading long term memory: {e}")
            self._memories = []

    def _save(self):
        try:
            payload = {"memories": self._memories}
            self.storage_path.write_text(
                json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8"
            )
        except Exception as e:
            logger.error(f"Error saving long term memory: {e}")

    def all(self) -> List[Dict[str, Any]]:
        """Return all memories."""
        return list(self._memories)

    def add(self, text: str, category: str = "general", metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Save a new memory item."""
        new_id = str(len(self._memories) + 1)
        item = {
            "id": new_id,
            "text": text.strip(),
            "category": category,
            "timestamp": datetime.now().isoformat(),
            "metadata": metadata or {},
        }
        self._memories.append(item)
        self._save()
        return item

    def search(self, query: str) -> List[Dict[str, Any]]:
        """Search memories matching keywords."""
        q_lower = query.lower()
        return [m for m in self._memories if q_lower in m.get("text", "").lower()]

    def remove(self, memory_id_or_index: Any) -> bool:
        """Remove a memory by its ID or integer index."""
        try:
            # Check by index first if int
            if isinstance(memory_id_or_index, int) and 0 <= memory_id_or_index < len(self._memories):
                self._memories.pop(memory_id_or_index)
                self._save()
                return True

            # Match by ID string or text
            str_val = str(memory_id_or_index)
            for i, m in enumerate(self._memories):
                if m.get("id") == str_val or m.get("text", "").lower() == str_val.lower():
                    self._memories.pop(i)
                    self._save()
                    return True
            return False
        except Exception as e:
            logger.error(f"Failed to remove memory: {e}")
            return False

    def clear(self):
        """Clear all stored long-term memories."""
        self._memories = []
        self._save()


long_term_memory = LongTermMemory()
