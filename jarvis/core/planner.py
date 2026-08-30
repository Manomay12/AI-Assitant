# ==================================================
# JARVIS AI — Multi-Step Task Planner & Execution Engine
# ==================================================

import asyncio
import logging
from typing import Any, Callable, Dict, List, Optional
from pydantic import BaseModel, Field
from jarvis.core.permission_manager import permission_manager
from jarvis.tools.base_tool import ToolResult
from jarvis.tools.registry import tool_registry

logger = logging.getLogger("jarvis.core.planner")


class TaskStep(BaseModel):
    id: int
    title: str
    tool_name: str
    args: Dict[str, Any] = Field(default_factory=dict)
    status: str = "pending"  # "pending", "in_progress", "completed", "failed", "skipped"
    result: Optional[ToolResult] = None


class ExecutionPlan(BaseModel):
    plan_id: str
    goal: str
    steps: List[TaskStep]
    status: str = "created"  # "created", "executing", "completed", "failed"
    current_step_index: int = 0


class AgentPlanner:
    """
    Decomposes multi-step goals into verified execution graphs,
    checks tool permissions before each step, and publishes live progress.
    """

    def __init__(self, on_progress_callback: Optional[Callable] = None):
        self.on_progress = on_progress_callback

    def set_progress_callback(self, callback: Callable):
        self.on_progress = callback

    async def execute_plan(self, plan: ExecutionPlan) -> List[ToolResult]:
        """Execute each step in the task plan sequentially with validation."""
        plan.status = "executing"
        results: List[ToolResult] = []

        for idx, step in enumerate(plan.steps):
            plan.current_step_index = idx
            step.status = "in_progress"
            if self.on_progress:
                await self.on_progress(plan)

            tool = tool_registry.get(step.tool_name)
            if not tool:
                step.status = "failed"
                res = ToolResult(
                    success=False,
                    error=f"Tool '{step.tool_name}' not found.",
                    message=f"Plan failed at step {idx+1}: '{step.title}'",
                )
                step.result = res
                results.append(res)
                plan.status = "failed"
                if self.on_progress:
                    await self.on_progress(plan)
                return results

            # Check permissions
            if tool.required_permissions:
                allowed = await permission_manager.check_and_request(
                    scopes=tool.required_permissions,
                    action_description=step.title,
                )
                if not allowed:
                    step.status = "failed"
                    res = ToolResult(
                        success=False,
                        error="Permission denied by user.",
                        message=f"Permission denied for step: '{step.title}'",
                    )
                    step.result = res
                    results.append(res)
                    plan.status = "failed"
                    if self.on_progress:
                        await self.on_progress(plan)
                    return results

            # Execute tool
            try:
                res = await tool.execute(**step.args)
                step.result = res
                results.append(res)

                if res.success:
                    step.status = "completed"
                else:
                    step.status = "failed"
                    plan.status = "failed"
                    if self.on_progress:
                        await self.on_progress(plan)
                    return results

            except Exception as e:
                logger.exception(f"Step execution error: {e}")
                step.status = "failed"
                res = ToolResult(success=False, error=str(e), message=f"Error executing '{step.title}': {e}")
                step.result = res
                results.append(res)
                plan.status = "failed"
                if self.on_progress:
                    await self.on_progress(plan)
                return results

            if self.on_progress:
                await self.on_progress(plan)
            await asyncio.sleep(0.3)

        plan.status = "completed"
        if self.on_progress:
            await self.on_progress(plan)
        return results
