# ==================================================
# JARVIS AI — Multi-Source Web Search Engine
# ==================================================

import logging
import urllib.parse
import urllib.request
import json
from typing import Any, Dict, List
import requests

logger = logging.getLogger("jarvis.internet.search")


class WebSearchEngine:
    """
    Performs multi-source web searches (DuckDuckGo Instant Answer / HTML API, Wikipedia, etc.)
    Returns structured results including titles, snippets, and URLs.
    """

    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }

    def search_duckduckgo(self, query: str, max_results: int = 5) -> List[Dict[str, str]]:
        """Search DuckDuckGo API."""
        try:
            url = f"https://api.duckduckgo.com/?q={urllib.parse.quote_plus(query)}&format=json&no_html=1&skip_disambig=1"
            req = urllib.request.Request(url, headers=self.headers)
            with urllib.request.urlopen(req, timeout=5) as resp:
                data = json.loads(resp.read().decode("utf-8"))

            results = []
            abstract = data.get("AbstractText")
            if abstract:
                results.append({
                    "title": data.get("Heading", "Direct Answer"),
                    "snippet": abstract,
                    "url": data.get("AbstractURL", ""),
                })

            for topic in data.get("RelatedTopics", [])[:max_results]:
                if isinstance(topic, dict) and "Text" in topic:
                    results.append({
                        "title": topic.get("Text", "").split(" - ")[0],
                        "snippet": topic.get("Text", ""),
                        "url": topic.get("FirstURL", ""),
                    })

            return results
        except Exception as e:
            logger.error(f"DuckDuckGo search error: {e}")
            return []

    def search_wikipedia(self, query: str) -> List[Dict[str, str]]:
        """Search Wikipedia API summary."""
        try:
            url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{urllib.parse.quote_plus(query)}"
            resp = requests.get(url, headers=self.headers, timeout=5)
            if resp.status_code == 200:
                data = resp.json()
                return [{
                    "title": data.get("title", ""),
                    "snippet": data.get("extract", ""),
                    "url": data.get("content_urls", {}).get("desktop", {}).get("page", ""),
                }]
        except Exception as e:
            logger.error(f"Wikipedia search error: {e}")
        return []

    def search(self, query: str, max_results: int = 5) -> List[Dict[str, str]]:
        """Unified search aggregator."""
        wiki_res = self.search_wikipedia(query)
        ddg_res = self.search_duckduckgo(query, max_results=max_results)
        
        combined = wiki_res + ddg_res
        if not combined:
            # Fallback default Google search link
            return [{
                "title": f"Google Search: {query}",
                "snippet": f"No direct API snippets returned. Click URL to view Google results for '{query}'.",
                "url": f"https://www.google.com/search?q={urllib.parse.quote_plus(query)}",
            }]
        return combined[:max_results]


web_search = WebSearchEngine()
