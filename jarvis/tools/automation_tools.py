# ==================================================
# JARVIS AI — Automation & Workflow Tools
# ==================================================

from typing import Any, Dict, List, Optional
from jarvis.config.constants import PermissionScope
from jarvis.memory.user_preferences import user_preferences
from jarvis.tools.base_tool import BaseTool, ToolParameter, ToolResult
from jarvis.tools.registry import tool_registry


class ExecuteWorkflowTool(BaseTool):
    name = "execute_workflow"
    description = "Execute a saved multi-step automation workflow by name (e.g. 'study mode', 'work mode')."
    parameters = [
        ToolParameter(
            name="workflow_name",
            type="string",
            description="The name of the saved workflow.",
            required=True,
        )
    ]
    required_permissions = [PermissionScope.APPLICATION_LAUNCH, PermissionScope.BROWSER_CONTROL]

    async def execute(self, workflow_name: str, **kwargs) -> ToolResult:
        steps = user_preferences.get_workflow(workflow_name)
        if not steps:
            available = ", ".join(user_preferences.list_workflows())
            return ToolResult(
                success=False,
                error=f"Workflow '{workflow_name}' not found. Available workflows: {available}",
            )

        executed = []
        for step in steps:
            tool_name = step.get("tool")
            args = step.get("args", {})
            res = await tool_registry.execute(tool_name, **args)
            executed.append({"tool": tool_name, "success": res.success, "message": res.message})

        return ToolResult(
            success=True,
            message=f"Activated workflow '{workflow_name}'. All {len(steps)} steps processed.",
            data={"workflow": workflow_name, "results": executed},
        )


class SaveWorkflowTool(BaseTool):
    name = "save_workflow"
    description = "Save a new custom automation workflow containing a series of tool steps."
    parameters = [
        ToolParameter(
            name="workflow_name",
            type="string",
            description="The name to identify this workflow.",
            required=True,
        ),
        ToolParameter(
            name="steps",
            type="array",
            description="List of tool actions with tool names and arguments.",
            required=True,
        ),
    ]
    required_permissions = [PermissionScope.FILE_WRITE]

    async def execute(self, workflow_name: str, steps: List[Dict[str, Any]], **kwargs) -> ToolResult:
        user_preferences.save_workflow(workflow_name, steps)
        return ToolResult(
            success=True,
            message=f"Workflow '{workflow_name}' has been saved successfully.",
            data={"workflow_name": workflow_name, "steps": steps},
        )


tool_registry.register(ExecuteWorkflowTool())
tool_registry.register(SaveWorkflowTool())
