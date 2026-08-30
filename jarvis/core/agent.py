# ==================================================
# JARVIS AI — Master Autonomous Agent
# ==================================================

import asyncio
import logging
from typing import Any, Callable, Dict, List, Optional
from jarvis.core.brain import brain
from jarvis.core.conversation import ConversationManager
from jarvis.core.permission_manager import permission_manager
from jarvis.core.planner import AgentPlanner, ExecutionPlan, TaskStep
from jarvis.memory.short_term_memory import ShortTermMemory
from jarvis.tools.registry import tool_registry
from jarvis.tools.base_tool import ToolResult

logger = logging.getLogger("jarvis.core.agent")


class JarvisAgent:
    """
    Master Orchestrator. Coordinates perception, intent detection,
    permission checking, planning, execution verification, and response generation.
    """

    def __init__(self):
        self.stm = ShortTermMemory(max_turns=12)
        self.conversation = ConversationManager(self.stm)
        self.planner = AgentPlanner()
        self.brain = brain
        self._hud_broadcaster: Optional[Callable] = None

    def set_hud_broadcaster(self, broadcaster: Callable):
        self._hud_broadcaster = broadcaster
        self.planner.set_progress_callback(self._on_plan_progress)

    async def _on_plan_progress(self, plan: ExecutionPlan):
        if self._hud_broadcaster:
            await self._hud_broadcaster({
                "type": "plan_update",
                "plan": plan.model_dump(),
            })

    async def process_input(self, user_text: str) -> str:
        """
        Main entrypoint for processing user commands / chat messages.
        Always returns verified execution feedback.
        """
        text = user_text.strip()
        if not text:
            return ""

        # Record user message in conversation memory
        self.conversation.add_user_message(text)

        if self._hud_broadcaster:
            await self._hud_broadcaster({"type": "user_input", "text": text})

        # 1. Check Fast Deterministic Route
        route = self.brain.fast_route(text)
        if route:
            tool_name, kwargs = route

            if tool_name == "exit":
                msg = "Shutting down JARVIS systems. Goodbye."
                self.conversation.add_assistant_response(msg)
                return msg

            # Execute tool directly
            tool = tool_registry.get(tool_name)
            if tool:
                # Permission check
                if tool.required_permissions:
                    allowed = await permission_manager.check_and_request(
                        scopes=tool.required_permissions,
                        action_description=f"Run {tool_name}",
                    )
                    if not allowed:
                        msg = f"Permission was denied for tool '{tool_name}'."
                        self.conversation.add_assistant_response(msg)
                        return msg

                # Execute with verification
                result: ToolResult = await tool.execute(**kwargs)
                response_text = result.message or (result.error if not result.success else "Action completed.")
                
                self.conversation.add_assistant_response(
                    response_text,
                    tool_calls=[{"tool": tool_name, "args": kwargs, "success": result.success}],
                )

                if self._hud_broadcaster:
                    await self._hud_broadcaster({
                        "type": "tool_executed",
                        "tool": tool_name,
                        "result": result.to_dict(),
                    })

                return response_text

        # 2. General AI Reasoning / Conversation
        chat_history = self.conversation.get_context_prompt_messages()
        ai_response = self.brain.generate_response(text, chat_history=chat_history)
        
        self.conversation.add_assistant_response(ai_response)
        return ai_response


agent = JarvisAgent()
