# ==================================================
# JARVIS AI — Productivity & Memory Tools
# ==================================================

from datetime import datetime
from typing import Optional
from jarvis.config.constants import PermissionScope
from jarvis.memory.long_term_memory import long_term_memory
from jarvis.memory.conversation_history import conversation_history
from jarvis.tools.base_tool import BaseTool, ToolParameter, ToolResult
from jarvis.tools.registry import tool_registry


# --------------------------------------------------
# Manage Memory Tool
# --------------------------------------------------
class ManageMemoryTool(BaseTool):
    name = "manage_memory"
    description = "Store, recall, search, or delete persistent memories about the user."
    parameters = [
        ToolParameter(
            name="action",
            type="string",
            description="Memory action: 'remember', 'recall', 'search', 'delete', or 'clear'.",
            enum=["remember", "recall", "search", "delete", "clear"],
            required=True,
        ),
        ToolParameter(
            name="content",
            type="string",
            description="Content to remember, search query, or memory ID to delete.",
            required=False,
        ),
    ]
    required_permissions = [PermissionScope.FILE_WRITE]

    async def execute(self, action: str, content: Optional[str] = None, **kwargs) -> ToolResult:
        if action == "remember":
            if not content:
                return ToolResult(success=False, error="No content specified to remember.")
            item = long_term_memory.add(content)
            return ToolResult(
                success=True,
                message=f"I have saved that to my memory: '{content}'",
                data=item,
            )

        elif action == "recall":
            items = long_term_memory.all()
            if not items:
                return ToolResult(success=True, message="I don't have any saved memories yet.", data=[])
            summary = "\n".join(f"{m.get('id', i+1)}. {m.get('text', '')}" for i, m in enumerate(items))
            return ToolResult(success=True, message=f"Saved memories:\n{summary}", data=items)

        elif action == "search":
            if not content:
                return ToolResult(success=False, error="Search query is required.")
            results = long_term_memory.search(content)
            if not results:
                return ToolResult(success=True, message=f"No memories matched '{content}'.", data=[])
            summary = "\n".join(f"{m.get('id')}: {m.get('text')}" for m in results)
            return ToolResult(success=True, message=f"Matching memories:\n{summary}", data=results)

        elif action == "delete":
            if not content:
                return ToolResult(success=False, error="Please provide memory ID or index to delete.")
            deleted = long_term_memory.remove(content)
            if deleted:
                return ToolResult(success=True, message=f"Memory '{content}' has been removed.")
            return ToolResult(success=False, error=f"Could not find memory '{content}'.")

        elif action == "clear":
            long_term_memory.clear()
            return ToolResult(success=True, message="All persistent memories have been wiped.")

        return ToolResult(success=False, error=f"Invalid action: {action}")


# --------------------------------------------------
# Get Time Tool
# --------------------------------------------------
class GetTimeTool(BaseTool):
    name = "get_current_time"
    description = "Get the current local system date and time."
    parameters = []
    required_permissions = []

    async def execute(self, **kwargs) -> ToolResult:
        now = datetime.now()
        time_str = now.strftime("%I:%M %p")
        date_str = now.strftime("%A, %B %d, %Y")
        return ToolResult(
            success=True,
            message=f"The time is {time_str} on {date_str}.",
            data={"time": time_str, "date": date_str},
        )


# Register productivity tools
tool_registry.register(ManageMemoryTool())
tool_registry.register(GetTimeTool())
