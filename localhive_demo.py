import streamlit as st
import re
from datetime import datetime
import os
from dotenv import load_dotenv
import google.generativeai as genai # Import Google Generative AI library

# --- Configuration ---
# Hardcoded responses for onboarding and system prompts for LLM
HARDCODED_RESPONSES = {
    "onboarding_welcome": "Welcome to LocalHive! I'm your assistant for community events and services. To get started, please tell me your name and your locality (e.g., 'My name is Alice and I live in Bhopal, India').",
    "onboarding_thanks_geolocation": "Thanks, {name}! I'm now getting the coordinates for {locality}. Please wait a moment.",
    "onboarding_complete": "Great, {name}! I've saved your location ({locality}). You are now fully onboarded and ready to use LocalHive! How can I help you today?",
    "onboarding_name_locality_fail": "I couldn't understand your name and locality. Please try again in the format: 'My name is [Your Name] and I live in [Your Locality]'.",
    # System prompts for dynamic LLM responses for each agent role
    "event_planner_system_prompt": "You are an expert event planner for local communities. Given a user's request, suggest creative event ideas and a brief outline (purpose, audience, activities, key considerations). Focus on community or local events. Keep responses concise and helpful.",
    "local_resource_system_prompt": "You are a local resource and logistics expert for Bhopal, Madhya Pradesh, India. Given a user's request, suggest relevant local venues, equipment, or service providers. Provide realistic, concise suggestions based on common local needs.",
    "sponsorship_finance_system_prompt": "You are a finance and sponsorship advisor for community projects in Bhopal, Madhya Pradesh, India. Given a user's request, provide concise advice on budgeting, fundraising, or securing local sponsorships. Suggest common approaches.",
    "local_service_exchange_system_prompt": "You are a facilitator for a local peer-to-peer service exchange in Bhopal, Madhya Pradesh, India. Given a user's request to offer or find a service, provide concise guidance on how to do so, or suggest common services available/needed in a community. Do not actually register or find real services, just explain the process.",
    "general_llm_fallback_system_prompt": "You are a helpful assistant for LocalHive, designed for local event planning and service exchange in communities. Your current location is Bhopal, Madhya Pradesh, India. The current time is {current_time_str}. If the user asks about something outside these domains, provide a polite and general helpful response, or suggest how they can use LocalHive. Keep responses concise and helpful."
}

# Simulated Geolocation for Bhopal, India
SIMULATED_LATITUDE = 23.2599
SIMULATED_LONGITUDE = 77.4126

# --- Gemini API Configuration ---

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Configure the Gemini API
if GEMINI_API_KEY == "YOUR_GEMINI_API_KEY" or not GEMINI_API_KEY:
    st.error("Please set your Google Gemini API Key in the `GEMINI_API_KEY` variable.")
    st.stop() # Stop the app if API key is not set
else:
    genai.configure(api_key=GEMINI_API_KEY)
    # Initialize the Gemini model
    try:
        gemini_model = genai.GenerativeModel('gemini-2.0-flash') # Using gemini-pro for general chat
    except Exception as e:
        st.error(f"Failed to initialize Gemini model: {e}. Check your API key and network connection.")
        st.stop()


# --- Streamlit Page Configuration ---
st.set_page_config(
    page_title="LocalHive Demo",
    page_icon="🏡",
    layout="centered",
    initial_sidebar_state="expanded",
)

st.title("🏡 LocalHive AI Demo")
st.markdown("Your intelligent assistant for community event planning and service exchange.")

# --- Session State Initialization ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
    st.session_state.onboarding_step = 0  # 0: not started, 1: asked name/locality, 2: geolocation sent, 3: onboarding complete
    st.session_state.user_data = {"name": None, "locality": None, "latitude": None, "longitude": None}

# --- Chat Display ---
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- Porter Agent Logic (Simulated) ---
def simulate_porter_response(user_input):
    current_step = st.session_state.onboarding_step
    response_text = ""
    agent_role = "PorterAgent" # Default role

    if current_step == 0:
        response_text = HARDCODED_RESPONSES["onboarding_welcome"]
        st.session_state.onboarding_step = 1
    elif current_step == 1:
        # Try to parse name and locality
        name_match = None
        locality_match = None
        user_input_lower = user_input.lower()

        name_pattern = r"(my name is|i am)\s+([a-zA-Z\s]+?)(?:and i live in)?\s*([a-zA-Z\s,]+)?"
        match = re.search(name_pattern, user_input_lower)

        if match:
            # Extract name
            name_parts = match.group(2).strip().split()
            name_match = " ".join([n.capitalize() for n in name_parts])

            # Extract locality
            if match.group(3):
                locality_parts = match.group(3).strip().split(',')
                locality_match = ", ".join([p.strip().title() for p in locality_parts])
            else: # If no explicit "and I live in", try to find locality later in the string
                 locality_search = re.search(r"(?:i live in|from)\s+([a-zA-Z\s,]+)", user_input_lower)
                 if locality_search:
                     locality_parts = locality_search.group(1).strip().split(',')
                     locality_match = ", ".join([p.strip().title() for p in locality_parts])


        if name_match and locality_match:
            st.session_state.user_data["name"] = name_match
            st.session_state.user_data["locality"] = locality_match
            response_text = HARDCODED_RESPONSES["onboarding_thanks_geolocation"].format(name=name_match, locality=locality_match)
            st.session_state.onboarding_step = 2 # Move to step where geolocation would be sent
            # Simulate immediate geolocation response
            st.session_state.user_data["latitude"] = SIMULATED_LATITUDE
            st.session_state.user_data["longitude"] = SIMULATED_LONGITUDE
            response_text += f"\n\n**(Simulated Geolocation from Agent):** Location found! Lat: {SIMULATED_LATITUDE}, Lon: {SIMULATED_LONGITUDE}. \n\n"
            response_text += HARDCODED_RESPONSES["onboarding_complete"].format(name=name_match, locality=locality_match)
            st.session_state.onboarding_step = 3 # Onboarding complete
        else:
            response_text = HARDCODED_RESPONSES["onboarding_name_locality_fail"]
    elif current_step == 2:
        # User is waiting for geolocation, but we simulated it immediately
        response_text = "Just a moment... your location details are being processed."
        if st.session_state.user_data["latitude"] and st.session_state.user_data["longitude"]:
             response_text += f"\n\n**(Simulated Geolocation from Agent):** Location found! Lat: {SIMULATED_LATITUDE}, Lon: {SIMULATED_LONGITUDE}. \n\n"
             response_text += HARDCODED_RESPONSES["onboarding_complete"].format(name=st.session_state.user_data["name"], locality=st.session_state.user_data["locality"])
             st.session_state.onboarding_step = 3
    elif current_step == 3:
        # Onboarding complete, delegate based on keywords and use Gemini for dynamic responses
        user_input_lower = user_input.lower()
        system_prompt_to_use = ""

        if "event" in user_input_lower or "organize" in user_input_lower or "plan" in user_input_lower:
            agent_role = "EventPlannerAgent"
            system_prompt_to_use = HARDCODED_RESPONSES["event_planner_system_prompt"]
        elif "service" in user_input_lower or "help" in user_input_lower or "find" in user_input_lower:
            agent_role = "LocalServiceExchangeAgent"
            system_prompt_to_use = HARDCODED_RESPONSES["local_service_exchange_system_prompt"]
        elif "budget" in user_input_lower or "sponsor" in user_input_lower or "finance" in user_input_lower:
            agent_role = "SponsorshipFinanceAgent"
            system_prompt_to_use = HARDCODED_RESPONSES["sponsorship_finance_system_prompt"]
        elif "location" in user_input_lower or "venue" in user_input_lower or "map" in user_input_lower:
            agent_role = "LocalResourceAgent"
            system_prompt_to_use = HARDCODED_RESPONSES["local_resource_system_prompt"]
        else:
            # General LLM Fallback
            agent_role = "PorterAgent (Gemini LLM)"
            current_time_str = datetime.now().strftime('%A, %B %d, %Y at %I:%M:%S %p IST')
            system_prompt_to_use = HARDCODED_RESPONSES["general_llm_fallback_system_prompt"].format(current_time_str=current_time_str)

        try:
            # Use st.spinner to show a loading indicator while waiting for LLM response
            with st.spinner(f"Connecting to {agent_role}'s AI brain..."):
                response = gemini_model.generate_content(
                    contents=[
                        {"role": "user", "parts": [system_prompt_to_use]},
                        {"role": "user", "parts": [user_input]}
                    ]
                )
                response_text = response.text
        except Exception as e:
            response_text = f"I'm having trouble connecting to my AI brain right now. Error: {e}"
            st.error(f"Gemini API Error: {e}")


    return response_text, agent_role

# --- Chat Input ---
user_input = st.chat_input("Type your message here...")

if user_input:
    # Add user message to chat history
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Simulate PorterAgent's response
    porter_response, agent_name = simulate_porter_response(user_input)
    
    # Add agent's response to chat history
    st.session_state.chat_history.append({"role": "assistant", "content": f"**({agent_name}):** {porter_response}"})
    with st.chat_message("assistant"):
        st.markdown(f"**({agent_name}):** {porter_response}")

# --- Reset Button ---
if st.button("Reset Chat"):
    st.session_state.chat_history = []
    st.session_state.onboarding_step = 0
    st.session_state.user_data = {"name": None, "locality": None, "latitude": None, "longitude": None}
    st.experimental_rerun()

# --- Display Current State (for debugging/demo explanation) ---
st.sidebar.subheader("Demo State (for explaination)")
st.sidebar.write(f"**Onboarding Step:** {st.session_state.onboarding_step}")
st.sidebar.write(f"**User Data:**")
st.sidebar.json(st.session_state.user_data)
