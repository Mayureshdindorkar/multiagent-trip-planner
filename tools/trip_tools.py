from crewai.tools import BaseTool
from ddgs import DDGS
from pydantic import Field
import time

class MyCustomDuckDuckGoTool(BaseTool):
    name: str = "DuckDuckGo Search Tool"
    description: str = "Search the web for a given query."

    def _run(self, query: str) -> str:
        try:
            results = DDGS().text(query, max_results=5)
            if not results:
                return "No search results found"
            
            formatted_results = "\n".join([f"- {r['title']}: {r['body']}" for r in results])
            time.sleep(1)  # Rate limiting
            return formatted_results
        except Exception as e:
            return f"Search error: {str(e)}"
