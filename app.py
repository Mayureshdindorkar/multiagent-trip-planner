########### To avoid an error that occurs while deploying the app to streamlit cloud ###########
__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
################################################################################################

import streamlit as st
from agents.trip_agents import TripAgents
from tasks.trip_tasks import TripTasks
from datetime import date
from crewai import Crew, Process
from dotenv import load_dotenv
import torch
import os

load_dotenv()
########### To avoid an error due to streamlit ###########
torch.classes.__path__ = [os.path.join(torch.__path__[0], torch.classes.__file__)]
##########################################################

class TripCrew:
    def __init__(self, start_city, destination_city, start_date, end_date, interests):
        self.start_city = start_city
        self.destination_city = destination_city
        self.start_date = start_date
        self.end_date = end_date
        self.interests = interests

    def run(self):
        # Instantiating the agents and tasks objects
        all_agents = TripAgents()
        all_tasks = TripTasks()

        # Obtaining the agents
        local_expert_agent = all_agents.local_expert_agent()
        travel_concierge_agent = all_agents.travel_concierge_agent()

        # Obtaining the tasks
        gather_task = all_tasks.gather_task(local_expert_agent, self.start_city, self.destination_city, self.interests, self.start_date, self.end_date)
        plan_task = all_tasks.plan_task(travel_concierge_agent, self.start_city, self.destination_city, self.interests, self.start_date, self.end_date)

        # Creating the crew
        crew = Crew(
            agents=[local_expert_agent, travel_concierge_agent],
            tasks=[gather_task, plan_task],
            verbose=True,
            full_output=True,
            process=Process.sequential,
        )

        # Running the crew
        return crew.kickoff()


# Streamlit UI
st.title("🌍 AI-Powered Travel Trip Planner")
st.subheader("Plan your perfect trip effortlessly!")

# Initialize session state for all inputs if not already set
if "start_city" not in st.session_state:
    st.session_state.start_city = ""
if "destination_city" not in st.session_state:
    st.session_state.destination_city = ""
if "start_date" not in st.session_state:
    st.session_state.start_date = date.today()
if "end_date" not in st.session_state:
    st.session_state.end_date = date.today()
if "interests" not in st.session_state:
    st.session_state.interests = ""

# User inputs
start_city = st.text_input("From where will you be traveling?")
destination_city = st.text_input("What is the destination city?")
col1, col2 = st.columns(2)
with col1:
    start_date = st.date_input("Start Date", min_value=date.today())
with col2:
    end_date = st.date_input("End Date", min_value=start_date)
interests = st.text_area("What are your high-level interests and hobbies?")

# Initialize session state for button
if "processing" not in st.session_state:
    st.session_state.processing = False
if "trip_plan" not in st.session_state:
    st.session_state.trip_plan = None

# Disable button while processing
generate_disabled = st.session_state.processing

# Generate trip plan
if st.button("Generate Trip Plan", disabled=generate_disabled):
    if not start_city or not destination_city or not start_date or not end_date or not interests:
        st.error("⚠️ Please fill in all fields before generating the trip plan.")
    else:
        # Save current inputs in session state
        st.session_state.start_city = start_city
        st.session_state.destination_city = destination_city
        st.session_state.start_date = start_date
        st.session_state.end_date = end_date
        st.session_state.interests = interests

        st.session_state.processing = True  # Disable button
        st.rerun()  # Rerun script

if st.session_state.processing:
    with st.spinner("Generating your trip plan..."):
        trip_crew = TripCrew(
            st.session_state.start_city,
            st.session_state.destination_city,
            st.session_state.start_date,
            st.session_state.end_date,
            st.session_state.interests
        )
        result = trip_crew.run()
        st.session_state.trip_plan = result
        st.session_state.processing = False
        st.rerun()

# Display the trip plan if available
if st.session_state.trip_plan:
    st.subheader("🏝️ Your Personalized Trip Plan:")
    st.markdown(st.session_state.trip_plan, unsafe_allow_html=True)

    trip_filename = f"Trip_Plan_{st.session_state.start_city}_to_{st.session_state.destination_city}.md"
    st.download_button(
        label="📥 Download Trip Plan",
        data=str(st.session_state.trip_plan),
        file_name=trip_filename,
        mime="text/markdown"
    )
