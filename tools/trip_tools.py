import json
from langchain.tools import tool
from dotenv import load_dotenv
import os
# from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.utilities import GoogleSerperAPIWrapper

class TripTools:
    
    # @staticmethod
    # @tool("Search the internet")
    # def search_internet(query):
    #     """Useful to search the internet about a given topic and return relevant results."""

    #     if isinstance(query, dict):
    #         query = query.get("description", "")

    #     duckduckgo_tool = DuckDuckGoSearchRun(num_results=3, verbose=True)
    #     search_results = duckduckgo_tool.run(query)

    #     if not search_results:
    #         return "Sorry, I couldn't find anything about that."

    #     return search_results

    @staticmethod
    @tool("Search the internet")
    def search_internet(query):
        """Uses Google Search via SerpAPI to return relevant results."""

        if isinstance(query, dict):
            query = query.get("description", "")

        search = GoogleSerperAPIWrapper(type="search")
        search_results = search.run(query)

        if not search_results:
            return "Sorry, I couldn't find anything about that."

        return search_results


