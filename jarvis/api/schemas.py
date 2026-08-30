# ==================================================
# JARVIS AI — API Data Models & Schemas
# ==================================================

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str
    mode: str = "text"  # "text", "voice"
    device_id: Optional[str] = "desktop"


class ChatResponse(BaseModel):
    response: str
    success: bool = True
    tool_calls: List[Dict[str, Any]] = Field(default_factory=list)


class PermissionDecisionRequest(BaseModel):
    scope: str
    decision: str  # "allow_once", "allow_session", "always_allow", "deny"


class WorkflowCreateRequest(BaseModel):
    name: str
    steps: List[Dict[str, Any]]


class SystemStatusResponse(BaseModel):
    cpu_percent: float
    ram_percent: float
    disk_percent: float
    battery: str
    ai_provider: str
    active_tools_count: int
    online: bool = True
