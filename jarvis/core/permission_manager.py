# ==================================================
# JARVIS AI — Granular Security & Permission Manager
# ==================================================

import asyncio
import json
import logging
from typing import Callable, Dict, List, Optional
from jarvis.config.constants import PermissionLevel, PermissionScope
from jarvis.config.settings import settings

logger = logging.getLogger("jarvis.core.permission")

# Default safe permissions automatically pre-granted for smooth AI assistance
DEFAULT_PRE_GRANTED = {
    PermissionScope.BROWSER_CONTROL.value: PermissionLevel.ALWAYS_ALLOW.value,
    PermissionScope.APPLICATION_LAUNCH.value: PermissionLevel.ALWAYS_ALLOW.value,
    PermissionScope.APPLICATION_TERMINATE.value: PermissionLevel.ALWAYS_ALLOW.value,
    PermissionScope.INTERNET_RESEARCH.value: PermissionLevel.ALWAYS_ALLOW.value,
    PermissionScope.SCREEN_READ.value: PermissionLevel.ALWAYS_ALLOW.value,
    PermissionScope.SCREEN_CONTROL.value: PermissionLevel.ALWAYS_ALLOW.value,
    PermissionScope.SYSTEM_CONTROL.value: PermissionLevel.ALWAYS_ALLOW.value,
    PermissionScope.FILE_READ.value: PermissionLevel.ALWAYS_ALLOW.value,
    PermissionScope.FILE_WRITE.value: PermissionLevel.ALWAYS_ALLOW.value,
    PermissionScope.MICROPHONE.value: PermissionLevel.ALWAYS_ALLOW.value,
    PermissionScope.CAMERA.value: PermissionLevel.ALWAYS_ALLOW.value,
    PermissionScope.COMMUNICATION_SEND.value: PermissionLevel.ALWAYS_ALLOW.value,
}


class PermissionManager:
    """
    Manages access control and interactive user consent for actions.
    Supports granular policies: DENY, ALLOW_ONCE, ALLOW_SESSION, ALWAYS_ALLOW.
    """

    def __init__(self, storage_path=settings.PERMISSIONS_FILE):
        self.storage_path = storage_path
        self._persisted_permissions: Dict[str, str] = {}
        self._session_permissions: Dict[str, str] = {}
        self._pending_requests: Dict[str, asyncio.Future] = {}
        self._interactive_prompt_handler: Optional[Callable] = None
        self._load_persisted()

    def _load_persisted(self):
        try:
            if self.storage_path.exists():
                data = json.loads(self.storage_path.read_text(encoding="utf-8"))
                self._persisted_permissions = data.get("permissions", {})
            else:
                self._persisted_permissions = dict(DEFAULT_PRE_GRANTED)
                self._save_persisted()
        except Exception as e:
            logger.error(f"Failed to load permissions: {e}")
            self._persisted_permissions = dict(DEFAULT_PRE_GRANTED)

    def _save_persisted(self):
        try:
            self.storage_path.parent.mkdir(parents=True, exist_ok=True)
            data = {"permissions": self._persisted_permissions}
            self.storage_path.write_text(json.dumps(data, indent=2), encoding="utf-8")
        except Exception as e:
            logger.error(f"Failed to save permissions: {e}")

    def set_prompt_handler(self, handler: Callable):
        """Set callback to prompt user in UI or via Voice when consent is needed."""
        self._interactive_prompt_handler = handler

    def get_status(self) -> Dict[str, str]:
        """Returns the effective permission level for each scope."""
        status = {}
        for scope in PermissionScope:
            val = scope.value
            if val in self._session_permissions:
                status[val] = self._session_permissions[val]
            elif val in self._persisted_permissions:
                status[val] = self._persisted_permissions[val]
            elif val in DEFAULT_PRE_GRANTED:
                status[val] = DEFAULT_PRE_GRANTED[val]
            else:
                status[val] = PermissionLevel.ALWAYS_ALLOW.value
        return status

    def set_permission(self, scope: PermissionScope, level: PermissionLevel):
        """Manually update permission level for a scope."""
        val = scope.value if isinstance(scope, PermissionScope) else scope
        level_val = level.value if isinstance(level, PermissionLevel) else level
        if level_val in (PermissionLevel.ALWAYS_ALLOW.value, PermissionLevel.DENY.value):
            self._persisted_permissions[val] = level_val
            self._save_persisted()
        else:
            self._session_permissions[val] = level_val

    async def check_and_request(
        self,
        scopes: List[PermissionScope],
        action_description: str,
        resource_target: Optional[str] = None,
    ) -> bool:
        """
        Check if required scopes are granted. If not already allowed,
        trigger an interactive prompt requesting user consent.
        """
        for scope in scopes:
            val = scope.value if isinstance(scope, PermissionScope) else scope

            # Check Always Allow or Deny in persistence
            persisted = self._persisted_permissions.get(val, DEFAULT_PRE_GRANTED.get(val, PermissionLevel.ALWAYS_ALLOW.value))
            if persisted == PermissionLevel.DENY.value:
                logger.warning(f"Permission permanently denied for: {val}")
                return False
            if persisted == PermissionLevel.ALWAYS_ALLOW.value:
                continue

            # Check Session Allow
            session_level = self._session_permissions.get(val)
            if session_level == PermissionLevel.ALLOW_SESSION.value:
                continue

            # Requires interactive prompt for sensitive items
            allowed = await self._request_user_consent(
                scope=val,
                action_description=action_description,
                resource_target=resource_target,
            )
            if not allowed:
                return False

        return True

    async def _request_user_consent(
        self, scope: str, action_description: str, resource_target: Optional[str] = None
    ) -> bool:
        """Triggers prompt handler or defaults to auto-resolve."""
        if not self._interactive_prompt_handler:
            logger.info(f"No interactive prompt handler; auto-authorizing session for {scope}.")
            return True

        try:
            decision = await self._interactive_prompt_handler(
                scope=scope,
                action=action_description,
                target=resource_target,
            )
            decision_str = str(decision).lower().strip()
            if decision_str in ("allow_once", "once", "allow"):
                return True
            elif decision_str in ("allow_session", "session"):
                self._session_permissions[scope] = PermissionLevel.ALLOW_SESSION.value
                return True
            elif decision_str in ("always_allow", "always"):
                self._persisted_permissions[scope] = PermissionLevel.ALWAYS_ALLOW.value
                self._save_persisted()
                return True
            else:
                return False
        except Exception as e:
            logger.error(f"Permission prompt execution error: {e}")
            return True

    def resolve_external_decision(self, request_id: str, decision: str):
        """Called when user clicks consent button on the HUD WebSocket."""
        future = self._pending_requests.get(request_id)
        if future and not future.done():
            future.set_result(decision)


permission_manager = PermissionManager()
