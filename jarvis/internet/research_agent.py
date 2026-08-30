# ==================================================
# JARVIS AI — Web Research Agent & Summarizer
# ==================================================

import logging
from typing import Any, Dict, List
from jarvis.config.constants import PermissionScope
from jarvis.internet.web_search import web_search
from jarvis.tools.base_tool import BaseTool, ToolParameter, ToolResult
from jarvis.tools.registry import tool_registry

logger = logging.getLogger("jarvis.internet.research")


class ResearchAgent:
    """
    Performs multi-step research on a topic, compiles facts from multiple sources,
    and returns a structured summary.
    """

    def __init__(self):
        self.search_engine = web_search

    def research_topic(self, topic: str) -> Dict[str, Any]:
        """Collect and format research results on a topic."""
        results = self.search_engine.search(topic, max_results=4)
        
        snippets = []
        sources = []
        for r in results:
            snippets.append(f"• **{r['title']}**: {r['snippet']}")
            if r.get("url"):
                sources.append(r["url"])

        summary = f"### Research Findings for: *{topic}*\n\n" + "\n\n".join(snippets)
        if sources:
            summary += "\n\n**Sources:**\n" + "\n".join(f"- {url}" for url in sources[:3])

        return {
            "topic": topic,
            "summary": summary,
            "results_count": len(results),
            "sources": sources,
        }


class WebResearchTool(BaseTool):
    name = "web_research"
    description = "Search the internet across multiple sources and synthesize a research summary."
    parameters = [
        ToolParameter(
            name="query",
            type="string",
            description="The topic, question, or comparison to research.",
            required=True,
        )
    ]
    required_permissions = [PermissionScope.INTERNET_RESEARCH]

    async def execute(self, query: str, **kwargs) -> ToolResult:
        agent = ResearchAgent()
        res = agent.research_topic(query)
        return ToolResult(
            success=True,
            message=res["summary"],
            data=res,
        )


tool_registry.register(WebResearchTool())
