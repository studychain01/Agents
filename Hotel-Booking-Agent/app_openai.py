import sys
import datetime 
import streamlit as st 
import os 
from crewai import Crew, Agent, Process, Task, Agent 
from browserbase import browserbase_tool 
from kayak import kayak_hotels 
from dotenv import load_dotenv 

st.set_page_config(page_title="🏨 HotelFinding Agent", layout="wide")

st.markdown("<h1 style='color: #0066cc;'>🏨 HotelFinder Pro</h1>", unsafe_allow_html=True)
st.subheader("Powered by Browserbase and CrewAI")

with st.sidebar: 
    col1, col2 = st.columns([1,3])
    with col1: 
        st.write("")
        #st.image("./assets/browser-base.png", width=65)
    with col2: 
        st.header("API Configuration")
    
    st.markdown("### OpenAI API Key")
    st.markdown("[Get your API key](https://platform.openai.com/account/api-keys)", unsafe_allow_html=True)
    openai_api_key = st.text_input("Enter your OpenAI API Key", type="password")
    
    if openai_api_key: 
        os.environ["OPENAI_API_KEY"] = openai_api_key
        st.success("OpenAI API Key saved successfully")
    
    st.markdown("### Browserbase API Key")
    st.markdown("[Get your API key](https://browserbase.ai)", unsafe_allow_html=True)
    browserbase_api_key = st.text_input("Enter your Browserbase API Key", type="password")

    if browserbase_api_key: 
        os.environ["BROWSERBASE_API_KEY"] = browserbase_api_key
        st.success("Browserbase API Key saved successfully")

load_dotenv()

st.markdown("---")

st.header("Search for Hotels")
col1, col2 = st.columns(2)


with col1:
    location = st.text_input("Location", placeholder="Enter city, area, or landmark")
    num_adults = st.number_input("Number of Adults", min_value=1, max_value=10, value=2)

#will be displayed to the right of column 1
with col2: 
    check_in_date = st.date_input("Check-In Date", datetime.date.today())
    check_out_date = st.date_input("Check-Out Date", datetime.date.today() + datetime.timedelta(days=1))

search_button = st.button("Search Hotels")

#Initialize agents 
hotels_agent = Agent(
    role="Hotels",
    goal="Search hotels",
    backstory="I am an agent that can search for hotels and find the best accomodations.",
    tools=[kayak_hotels, browserbase_tool],
    allow_delegation=False,
)

summarize_agent = Agent(
    role="Summarize",
    goal="Summarize hotel information",
    backstory="I am an agent that can summarize hotel details and ammenities.",
    allow_delegation=False,
)

output_search_example = """
Here are our top 5 hotels in New York for September 21-22, 2024:
1. Hilton Times Square: 
   - Rating: 4.5/5
   - Price: $200/night
   - Location: Times Square 
   - Amenities: Pool, Spa, Restaurant
   - Booking: https://www.kayak.com/hotels/hilton-times-square
"""

search_task = Task(
    description=(
        "Search hotels according to criteria {request}. Current year: {current_year}"
),
    expected_output=output_search_example,
    agent=hotels_agent,
)

output_providers_example = """
Detailed information for hotels in New York (September 21-22, 2024):
1. Hilton Times Square: 
   - Room Types: Deluxe King, Double Queen
   - Price Range: $299-$499/night 
   - Special Offers: Free breakfast, Free cancellation 
   - Booking Options: 
     * Kayak: $299/night
     * Hotels.com: $315/night
     * Direct: $325/night
"""

search_booking_providers_task = Task(
    description="Load hotel details and find available booking providers with their rates",
    expected_output=output_providers_example, 
    agent=hotels_agent,
)

#Once Search button is pressed 
if search_button: 
    if not os.environ.get("OPENAI_API_KEY"):
        st.error("Please enter your OpenAI API Key in the sidebar first!")
    
    elif not os.environ.get("BROWSERBASE_API_KEY"):
        st.error("Please enter your Browserbase API Key in the sidebar first!")
    
    elif check_out_date <= check_in_date: 
        st.error("Check-Out Date must be after Check-In Date")
    
    else: 
        with st.spinner("Searching for hotels... This may take a few minutes."):
            request = f"hotels in {location} from {check_in_date.strftime('%B %d')} to {check_out_date.strftime('%B %d')} for {num_adults} adults"
            crew = Crew(
                agents=[hotels_agent, summarize_agent],
                tasks=[search_task, search_booking_providers_task],
                #max rpm is the maximum number of requests per minute to API
                max_rpm=100,
                #verbose=True, shows the full output of the agents and tasks in console
                verbose=True,
                #Enables the planning module inside CrewAI.

                #With planning on, CrewAI can decide the order of task execution dynamically instead of just following the list in sequence.
                #If set to False, tasks are typically executed in the exact order you provide
                planning=True,
            )

            try: 
                result = crew.kickoff(
                    #input parameters for search task 
                    inputs={
                        "request": request,
                        "current_year": datetime.date.today().year,
                    }
                )

                st.success("Search completed!")
                st.markdown("## Hotel Results")
                st.markdown(result)
            except Exception as e: 
                st.error(f"An error occured during the search: {str(e)}")
            
st.markdown("---")
st.markdown("""
### About HotelFinder Pro 
This application uses AI agents to search for hotels and find the best accommodations for you.
Simply enter your desired location, dates, and number of guests to get started.

Features:
- Real-time hotel availability
- Comprehensive price comparison
- Detailed hotel information and amenities
- Multiple booking options
""")