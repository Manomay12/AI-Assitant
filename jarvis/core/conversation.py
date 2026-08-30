# ==================================================
# JARVIS AI — Conversation Session Manager
# ==================================================

from typing import Any, Dict, List, Optional
from jarvis.memory.conversation_history import conversation_history
from jarvis.memory.short_term_memory import ShortTermMemory
from jarvis.memory.long_term_memory import long_term_memory


class ConversationManager:
    """
    Manages ongoing conversational context, multi-turn follow-ups,
    and automatic retrieval of relevant long-term memories.
    """

    def __init__(self, short_term_memory: ShortTermMemory):
        self.stm = short_term_memory
        self.history = conversation_history
        self.ltm = long_term_memory

    def add_user_message(self, text: str) -> None:
        self.stm.add_turn(role="user", content=text)
        self.history.append(role="user", message=text)

    def add_assistant_response(self, text: str, tool_calls: Optional[List[Dict[str, Any]]] = None) -> None:
        self.stm.add_turn(role="assistant", content=text, metadata={"tool_calls": tool_calls or []})
        self.history.append(role="assistant", message=text, tool_calls=tool_calls)

    def get_context_prompt_messages(self) -> List[Dict[str, str]]:
        """Constructs chat message array for LLM context window."""
        messages = []
        recent = self.stm.get_recent_turns(count=6)
        for turn in recent:
            messages.append({"role": turn["role"], "content": turn["content"]})
        return messages

    def find_relevant_memories(self, query: str) -> List[Dict[str, Any]]:
        return self.ltm.search(query)
