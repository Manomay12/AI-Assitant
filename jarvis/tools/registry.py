# ==================================================
# JARVIS AI — Central Tool Registry
# ==================================================

import logging
from typing import Dict, List, Optional, Type
from jarvis.tools.base_tool import BaseTool, ToolResult

logger = logging.getLogger("jarvis.tools.registry")


class ToolRegistry:
    """
    Central repository for all JARVIS tool definitions.
    Enables dynamic registration, schema generation for LLMs,
    and safe execution with parameter validation.
    """

    def __init__(self):
        self._tools: Dict[str, BaseTool] = {}

    def register(self, tool: BaseTool) -> BaseTool:
        """Register a tool instance."""
        if not tool.name:
            raise ValueError(f"Tool {tool.__class__.__name__} has no name defined.")
        if tool.name in self._tools:
            logger.warning(f"Overwriting existing tool: '{tool.name}'")
        self._tools[tool.name] = tool
        logger.info(f"Registered tool: '{tool.name}'")
        return tool

    def unregister(self, tool_name: str) -> Optional[BaseTool]:
        """Remove a tool from the registry."""
        return self._tools.pop(tool_name, None)

    def get(self, tool_name: str) -> Optional[BaseTool]:
        """Lookup a tool by name."""
        return self._tools.get(tool_name)

    def list_tools(self) -> List[BaseTool]:
        """Return all registered tool instances."""
        return list(self._tools.values())

    def get_schemas(self) -> List[dict]:
        """Generate JSON schemas for all registered tools for LLM tool calling."""
        return [tool.get_schema() for tool in self._tools.values()]

    async def execute(self, tool_name: str, **kwargs) -> ToolResult:
        """Execute a tool with error boundary and verification."""
        tool = self.get(tool_name)
        if not tool:
            return ToolResult(
                success=False,
                error=f"Tool '{tool_name}' is not registered in the system.",
                message=f"Action failed: Tool '{tool_name}' does not exist.",
            )

        try:
            result = await tool.execute(**kwargs)
            return result
        except Exception as e:
            logger.exception(f"Unhandled exception in tool '{tool_name}': {e}")
            return ToolResult(
                success=False,
                error=str(e),
                message=f"Execution error while running tool '{tool_name}': {e}",
            )


# Global registry singleton
tool_registry = ToolRegistry()
