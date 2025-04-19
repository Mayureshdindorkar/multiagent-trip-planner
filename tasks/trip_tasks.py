from crewai import Task
from textwrap import dedent

class TripTasks:

    def gather_task(self, agent, start_city, destination_city, interests, start_date, end_date):
        return Task(
            description=dedent(f"""
                As a local expert on "{destination_city}" city you must compile an 
                in-depth guide for someone traveling there and wanting 
                to have THE BEST trip ever!
                Gather information about key attractions, local customs,
                special events, and daily activity recommendations.
                Find the best spots to go to, the kind of place only a
                local would know.
                This guide should provide a thorough overview of what 
                the city has to offer, including hidden gems, cultural
                hotspots, must-visit landmarks, weather forecasts, and
                high level costs.
                
                The final answer must be a comprehensive city guide, 
                rich in cultural insights and practical tips, 
                tailored to enhance the travel experience.
                {self.__tip_section()}

                Trip Start Date: {start_date}
                Trip End Date: {end_date}
                Traveling from: {start_city}
                Traveler Interests: {interests}
            """),
            agent=agent,
            expected_output="Comprehensive city guide including hidden gems, cultural hotspots, and practical travel tips"
        )

    def plan_task(self, agent, start_city, destination_city, interests, start_date, end_date):
        trip_duration = (end_date - start_date).days + 1
        return Task(
            description=dedent(f"""
                Expand this guide into a full **{trip_duration}-day travel itinerary** 
                with detailed per-day plans, including:
                - Weather forecasts
                - Places to eat
                - Packing suggestions
                - A budget breakdown

                You MUST suggest **actual** places to visit, **actual** hotels 
                to stay at, and **actual** restaurants to dine in.

                This itinerary should cover all aspects of the trip, 
                from **arrival to departure**, integrating city guide 
                information with practical travel logistics.

                **Your final answer MUST be a complete expanded travel plan,**
                formatted as **markdown**, encompassing:
                - A **daily schedule**
                - **Anticipated weather conditions**
                - **Recommended clothing & items to pack**
                - **A detailed budget breakdown**

                Ensure this trip is **THE BEST EXPERIENCE POSSIBLE** by providing:
                - Specific recommendations with reasons why each place is special
                - Cultural insights and hidden gems
                - Must-know travel tips for smooth navigation {self.__tip_section()}

                ---
                **Trip Details**  
                - **Trip Duration:** {trip_duration} days  
                - **Trip Date:** {start_date.strftime('%B %d, %Y')} to {end_date.strftime('%B %d, %Y')}  
                - **Traveling From:** {start_city}  
                - **Destination:** {destination_city}  
                - **Traveler Interests:** {', '.join(interests) if isinstance(interests, list) else interests}
                ---
            """),
            agent=agent,
            expected_output=f"Complete {trip_duration}-day expanded travel plan with daily schedule, weather conditions, packing suggestions, and budget breakdown"
        )

    def __tip_section(self):
        return "If you do your BEST WORK, I'll tip you 100"
