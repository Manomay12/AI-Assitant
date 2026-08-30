# ==================================================
# JARVIS 4.0 — Memory (Long-Term Persistence)
# ==================================================

import json
from pathlib import Path

from config.settings import MEMORY_FILE


class Memory:

    def __init__(self, path=MEMORY_FILE):

        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

        if not self.path.exists():
            self.path.write_text("[]", encoding="utf-8")

    def all(self):
        """Return all saved memory items as a list of strings."""
        try:
            return json.loads(self.path.read_text(encoding="utf-8"))
        except Exception:
            return []

    def add(self, text: str):
        """Append a new item to memory."""
        items = self.all()
        items.append(text)
        self.path.write_text(
            json.dumps(items, indent=2, ensure_ascii=False),
            encoding="utf-8"
        )

    def remove(self, index: int):
        """Remove a memory item by 0-based index. Returns True if successful."""
        items = self.all()
        if 0 <= index < len(items):
            items.pop(index)
            self.path.write_text(
                json.dumps(items, indent=2, ensure_ascii=False),
                encoding="utf-8"
            )
            return True
        return False

    def clear(self):
        """Delete all saved memories."""
        self.path.write_text("[]", encoding="utf-8")
