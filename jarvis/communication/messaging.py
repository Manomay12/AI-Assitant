# ==================================================
# JARVIS AI — Safe Communication & Messaging Agent
# ==================================================

import logging
from typing import Optional
from jarvis.config.constants import PermissionScope
from jarvis.tools.base_tool import BaseTool, ToolParameter, ToolResult
from jarvis.tools.registry import tool_registry

logger = logging.getLogger("jarvis.communication")


class DraftMessageTool(BaseTool):
    name = "draft_message"
    description = "Draft a chat message or SMS for a recipient. Explicit confirmation is required before sending."
    parameters = [
        ToolParameter(
            name="recipient",
            type="string",
            description="The contact name or phone number.",
            required=True,
        ),
        ToolParameter(
            name="message",
            type="string",
            description="The text content of the message.",
            required=True,
        ),
    ]
    required_permissions = [PermissionScope.COMMUNICATION_SEND]
    is_sensitive = True

    async def execute(self, recipient: str, message: str, **kwargs) -> ToolResult:
        # Note: JARVIS drafts the message and requests confirmation before dispatching
        prompt_text = (
            f"I have drafted the following message for {recipient}:\n\n"
            f"\"{message}\"\n\n"
            f"Should I send this message to {recipient}?"
        )
        return ToolResult(
            success=True,
            message=prompt_text,
            data={"recipient": recipient, "message": message, "status": "drafted_needs_confirmation"},
        )


class DraftEmailTool(BaseTool):
    name = "draft_email"
    description = "Draft an email with subject and body. Requires explicit user confirmation."
    parameters = [
        ToolParameter(
            name="recipient",
            type="string",
            description="Recipient name or email address.",
            required=True,
        ),
        ToolParameter(
            name="subject",
            type="string",
            description="The email subject line.",
            required=True,
        ),
        ToolParameter(
            name="body",
            type="string",
            description="The email body message.",
            required=True,
        ),
    ]
    required_permissions = [PermissionScope.COMMUNICATION_SEND]
    is_sensitive = True

    async def execute(self, recipient: str, subject: str, body: str, **kwargs) -> ToolResult:
        prompt_text = (
            f"Email Draft for {recipient}:\n"
            f"Subject: {subject}\n"
            f"Body:\n{body}\n\n"
            f"Would you like me to send this email now?"
        )
        return ToolResult(
            success=True,
            message=prompt_text,
            data={"recipient": recipient, "subject": subject, "body": body, "status": "drafted_needs_confirmation"},
        )


tool_registry.register(DraftMessageTool())
tool_registry.register(DraftEmailTool())
