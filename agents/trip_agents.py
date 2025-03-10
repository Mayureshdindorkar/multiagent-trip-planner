from crewai import Agent, LLM
from tools.trip_tools import TripTools
from dotenv import load_dotenv
import os
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

torch.classes.__path__ = [os.path.join(torch.__path__[0], torch.classes.__file__)]  # To avoid a error

class TripAgents:

    def __init__(self):
        load_dotenv()
        self.hf_api_key = st.secrets["HUGGINGFACE_API_KEY"] # os.getenv("HUGGINGFACE_API_KEY") 

        if not self.hf_api_key:
            raise ValueError("HUGGINGFACE_API_KEY is missing. Please set it in your environment variables.")

        # Hugging Face Model ID
        self.model_id = "huggingface/mistralai/Mistral-7B-Instruct-v0.3"

    def local_expert_agent(self):
        return Agent(
            role='Local Expert at this city',
            goal='Provide the BEST insights about the selected city',
            backstory="""A knowledgeable local guide with extensive information
            about the city, its attractions, and customs.""",
            tools=[TripTools.search_internet],
            llm=LLM(model=self.model_id, api_key=self.hf_api_key),
            verbose=True,
            allow_delegation=False,
            max_iter=4,
        )

    def travel_concierge_agent(self):
        return Agent(
            role='Amazing Travel Concierge',
            goal="""Create the most amazing travel itineraries with budget and 
            packing suggestions for the city""",
            backstory="""Specialist in travel planning and logistics with 
            decades of experience""",
            tools=[TripTools.search_internet],
            llm=LLM(model=self.model_id, api_key=self.hf_api_key),
            verbose=True,
            allow_delegation=False,
            max_iter=4,
        )
