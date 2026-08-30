# ==================================================
# JARVIS AI — User Preferences & Custom Workflows
# ==================================================

import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional
from jarvis.config.settings import settings

logger = logging.getLogger("jarvis.memory.preferences")


class UserPreferences:
    """
    Stores user customized configurations, aliases, preferred language,
    favorite apps, and saved multi-step automation workflows (e.g. 'Study Mode').
    """

    DEFAULT_PREFERENCES = {
        "user_name": "Sir",
        "preferred_language": "en",
        "theme": "jarvis_cyan",  # "jarvis_cyan", "ultron_gold", "cyber_crimson"
        "voice_enabled": True,
        "voice_speed": 175,
        "voice_volume": 1.0,
        "wake_word_enabled": True,
        "auto_screenshot_analysis": False,
        "saved_workflows": {
            "study mode": [
                {"tool": "open_app", "args": {"app_name": "code"}},
                {"tool": "open_website", "args": {"website": "chatgpt"}},
                {"tool": "youtube_search", "args": {"query": "lofi chill study beats"}},
            ],
            "work mode": [
                {"tool": "open_app", "args": {"app_name": "chrome"}},
                {"tool": "open_website", "args": {"website": "gmail"}},
                {"tool": "open_website", "args": {"website": "github"}},
            ],
        },
        "custom_aliases": {
            "browser": "chrome",
            "editor": "code",
        },
    }

    def __init__(self, storage_path: Path = settings.PREFERENCES_FILE):
        self.storage_path = Path(storage_path)
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        self._data: Dict[str, Any] = {}
        self._load()

    def _load(self):
        try:
            if self.storage_path.exists():
                content = self.storage_path.read_text(encoding="utf-8").strip()
                if content:
                    self._data = json.loads(content)
                else:
                    self._data = self.DEFAULT_PREFERENCES.copy()
            else:
                self._data = self.DEFAULT_PREFERENCES.copy()
                self._save()
        except Exception as e:
            logger.error(f"Error loading preferences: {e}")
            self._data = self.DEFAULT_PREFERENCES.copy()

    def _save(self):
        try:
            self.storage_path.write_text(
                json.dumps(self._data, indent=2, ensure_ascii=False), encoding="utf-8"
            )
        except Exception as e:
            logger.error(f"Error saving preferences: {e}")

    def get(self, key: str, default: Any = None) -> Any:
        return self._data.get(key, default)

    def set(self, key: str, value: Any):
        self._data[key] = value
        self._save()

    def get_all(self) -> Dict[str, Any]:
        return dict(self._data)

    def save_workflow(self, name: str, steps: List[Dict[str, Any]]):
        """Save or update a multi-step routine with user consent."""
        workflows = self._data.setdefault("saved_workflows", {})
        workflows[name.lower().strip()] = steps
        self._save()

    def get_workflow(self, name: str) -> Optional[List[Dict[str, Any]]]:
        workflows = self._data.get("saved_workflows", {})
        return workflows.get(name.lower().strip())

    def list_workflows(self) -> List[str]:
        return list(self._data.get("saved_workflows", {}).keys())


user_preferences = UserPreferences()
