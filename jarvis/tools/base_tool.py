# ==================================================
# JARVIS AI — Base Tool Interface & Data Models
# ==================================================

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field
from jarvis.config.constants import PermissionScope


class ToolResult(BaseModel):
    """Encapsulates the verified outcome of a tool execution."""
    success: bool
    data: Optional[Any] = None
    message: str = ""
    error: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump()


class ToolParameter(BaseModel):
    """Specification of an individual tool input parameter."""
    name: str
    type: str  # "string", "integer", "number", "boolean", "array", "object"
    description: str
    required: bool = True
    default: Optional[Any] = None
    enum: Optional[List[Any]] = None


class BaseTool(ABC):
    """
    Abstract base class for all JARVIS tools.
    Every tool must define its name, description, required permissions,
    and structured input parameters.
    """
    name: str = ""
    description: str = ""
    parameters: List[ToolParameter] = []
    required_permissions: List[PermissionScope] = []
    is_sensitive: bool = False

    @abstractmethod
    async def execute(self, **kwargs) -> ToolResult:
        """
        Execute the tool action asynchronously and return a verified ToolResult.
        Must NEVER claim success without verifying real execution.
        """
        pass

    def get_schema(self) -> Dict[str, Any]:
        """Returns JSON schema representation compatible with LLM function calling."""
        properties = {}
        required = []

        for p in self.parameters:
            prop: Dict[str, Any] = {
                "type": p.type,
                "description": p.description,
            }
            if p.enum:
                prop["enum"] = p.enum
            if p.default is not None:
                prop["default"] = p.default
            properties[p.name] = prop

            if p.required:
                required.append(p.name)

        return {
            "name": self.name,
            "description": self.description,
            "parameters": {
                "type": "object",
                "properties": properties,
                "required": required,
            },
            "required_permissions": [p.value for p in self.required_permissions],
            "is_sensitive": self.is_sensitive,
        }
