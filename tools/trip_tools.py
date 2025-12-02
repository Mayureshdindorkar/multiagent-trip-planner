from crewai.tools import BaseTool
from langchain_community.tools import DuckDuckGoSearchRun

class MyCustomDuckDuckGoTool(BaseTool):
    name: str = "DuckDuckGo Search Tool"
    description: str = "Search the web for a given query."
    
    def __init__(self):
        super().__init__()
        self.duckduckgo_tool = DuckDuckGoSearchRun(region="us-en")

    def _run(self, query: str) -> str:
        try:
            response = self.duckduckgo_tool.invoke(query)
            return response
        except Exception as e:
            return f"Search error: {str(e)}"



