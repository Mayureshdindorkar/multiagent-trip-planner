import json
from dotenv import load_dotenv
import os
from crewai.tools import BaseTool
from langchain_community.tools import DuckDuckGoSearchRun

class MyCustomDuckDuckGoTool(BaseTool):
    name: str = "DuckDuckGo Search Tool"
    description: str = "Search the web for a given query."

    def _run(self, query: str) -> str:
        duckduckgo_tool = DuckDuckGoSearchRun()
        response = duckduckgo_tool.invoke(query)
        return response



