from datetime import datetime
from uuid import uuid4

from openai import OpenAI # Used for ASI:One LLM integration
from uagents import Context, Protocol, Agent
from uagents_core.contrib.protocols.chat import (
    ChatAcknowledgement,
    ChatMessage,
    EndSessionContent,
    TextContent,
    chat_protocol_spec,
)
from uagents.protocols.geolocation import GeolocationRequest, GeolocationResponse

# Define a custom model for sending user data to the DataManagerAgent
class UserProfileData(ChatMessage):
    user_name: str
    locality: str
    latitude: float
    longitude: float

# --- CONFIGURATION ---
# IMPORTANT: Replace with your actual ASI:One API Key
ASI_ONE_API_KEY = 'INSERT_YOUR_ASI_ONE_API_KEY_HERE' 

# IMPORTANT: Replace these with the actual deployed addresses from YOUR Agentverse account
# You will get these addresses after deploying each agent below.
GEOLOCATION_AGENT_ADDRESS = "agent1qvnpu46exfw4jazkhwxdqpq48kcdg0u0ak3mz36yg93ej06xntklsxcwplc" # Marketplace Google API Geolocation Agent
DATA_MANAGER_AGENT_ADDRESS = "agent1q..." # YOUR DataManagerAgent address
EVENT_PLANNER_AGENT_ADDRESS = "agent1q..." # YOUR EventIdeationPlannerAgent address
LOCAL_RESOURCE_AGENT_ADDRESS = "agent1q..." # YOUR LocalResourceLogisticsAgent address
SPONSORSHIP_FINANCE_AGENT_ADDRESS = "agent1q..." # YOUR SponsorshipFinanceAgent address
LOCAL_SERVICE_EXCHANGE_AGENT_ADDRESS = "agent1q..." # YOUR LocalServiceExchangeAgent address

# --- AGENT SETUP ---
porter_agent = Agent(name="PorterAgent", seed="porter_recovery_phrase")
chat_protocol = Protocol(spec=chat_protocol_spec)

# Initialize ASI:One LLM client
llm_client = OpenAI(
    base_url='https://api.asi1.ai/v1',
    api_key=ASI_ONE_API_KEY,
)

# --- MESSAGE HANDLERS ---

@chat_protocol.on_message(ChatMessage)
async def handle_user_message(ctx: Context, sender: str, msg: ChatMessage):
    """
    Handles incoming chat messages from the user, performs intent recognition,
    and delegates tasks to specialized agents. Also manages the onboarding flow.
    """
    await ctx.send(sender, ChatAcknowledgement(timestamp=datetime.now(), acknowledged_msg_id=msg.msg_id))

    user_state = ctx.storage.get(sender)
    if user_state is None:
        user_state = {"onboarding_step": 0, "name": None, "locality": None}
        ctx.storage.set(sender, user_state)
        ctx.logger.info(f"New user detected: {sender}. Starting onboarding.")

    user_query = ''
    for item in msg.content:
        if isinstance(item, TextContent):
            user_query += item.text.lower()

    ctx.logger.info(f"PorterAgent received query: '{user_query}' from {sender}")
    response_text = "I'm sorry, I couldn't understand your request. Can you please rephrase?"

    # --- Onboarding Flow ---
    if user_state["onboarding_step"] == 0:
        response_text = "Welcome to LocalHive! I'm your assistant for community events and services. To get started, please tell me your name and your locality (e.g., 'My name is Alice and I live in Bhopal, India')."
        user_state["onboarding_step"] = 1
        ctx.storage.set(sender, user_state)
    elif user_state["onboarding_step"] == 1:
        # Simple parsing for name and locality
        name_match = None
        locality_match = None
        if "my name is" in user_query:
            name_parts = user_query.split("my name is", 1)
            if len(name_parts) > 1:
                remaining = name_parts[1].strip()
                if " and i live in" in remaining:
                    name_end_idx = remaining.find(" and i live in")
                    name_match = remaining[:name_end_idx].strip().title()
                    locality_match = remaining[name_end_idx + len(" and i live in"):].strip().title()
                else:
                    name_match = remaining.split(" and ", 1)[0].strip().title() # Simple split if only name given after "my name is"
                    # If locality isn't clearly provided, prompt again
                    response_text = "I got your name, but please tell me your locality too (e.g., 'I live in Bhopal, India')."
                    await ctx.send(sender, ChatMessage(timestamp=datetime.utcnow(), msg_id=uuid4(), content=[TextContent(type="text", text=response_text)]))
                    return

        if name_match and locality_match:
            user_state["name"] = name_match
            user_state["locality"] = locality_match
            ctx.storage.set(sender, user_state)
            ctx.logger.info(f"User {sender} provided name: {name_match}, locality: {locality_match}. Requesting geolocation.")

            if GEOLOCATION_AGENT_ADDRESS != "agent1q...": # Check if address is set
                await ctx.send(GEOLOCATION_AGENT_ADDRESS, GeolocationRequest(
                    location_name=locality_match,
                    current_location=False
                ))
                response_text = f"Thanks, {name_match}! I'm now getting the coordinates for {locality_match}. Please wait a moment."
                user_state["onboarding_step"] = 2 # Waiting for geolocation response
                ctx.storage.set(sender, user_state)
            else:
                response_text = "I received your name and locality, but the geolocation service is not configured. Please contact support."
                user_state["onboarding_step"] = 3 # Skip geolocation if agent not configured
                ctx.storage.set(sender, user_state)
        else:
            response_text = "I couldn't understand your name and locality. Please try again in the format: 'My name is [Your Name] and I live in [Your Locality]'."
    elif user_state["onboarding_step"] == 2:
        response_text = "Still getting your location details. Please wait a moment."
    elif user_state["onboarding_step"] == 3:
        # --- Onboarding complete, proceed with main functionality ---
        ctx.logger.info(f"User {user_state['name']} ({user_state['locality']}) is onboarded. Processing general query.")

        # --- Basic Intent Recognition and Delegation ---
        if "event" in user_query or "organize" in user_query or "plan" in user_query:
            if EVENT_PLANNER_AGENT_ADDRESS != "agent1q...":
                ctx.logger.info(f"Delegating '{user_query}' to EventIdeationPlannerAgent...")
                await ctx.send(EVENT_PLANNER_AGENT_ADDRESS, ChatMessage(
                    timestamp=datetime.utcnow(), msg_id=uuid4(), content=[TextContent(type="text", text=user_query)]
                ))
                response_text = "Okay, I'll connect you with the event planning expert. What kind of event are you thinking of?"
            else:
                response_text = "My event planning expert isn't online yet."
        elif "service" in user_query or "help" in user_query or "find" in user_query:
            if LOCAL_SERVICE_EXCHANGE_AGENT_ADDRESS != "agent1q...":
                ctx.logger.info(f"Delegating '{user_query}' to LocalServiceExchangeAgent...")
                await ctx.send(LOCAL_SERVICE_EXCHANGE_AGENT_ADDRESS, ChatMessage(
                    timestamp=datetime.utcnow(), msg_id=uuid4(), content=[TextContent(type="text", text=user_query)]
                ))
                response_text = "Understood. I'll check with the local service exchange. What type of service are you looking for, or offering?"
            else:
                response_text = "The local service exchange isn't fully set up yet."
        elif "budget" in user_query or "sponsor" in user_query or "finance" in user_query:
            if SPONSORSHIP_FINANCE_AGENT_ADDRESS != "agent1q...":
                ctx.logger.info(f"Delegating '{user_query}' to SponsorshipFinanceAgent...")
                await ctx.send(SPONSORSHIP_FINANCE_AGENT_ADDRESS, ChatMessage(
                    timestamp=datetime.utcnow(), msg_id=uuid4(), content=[TextContent(type="text", text=user_query)]
                ))
                response_text = "Alright, let me connect you with the finance and sponsorship expert."
            else:
                response_text = "My finance expert isn't available right now."
        elif "location" in user_query or "venue" in user_query or "map" in user_query:
            if LOCAL_RESOURCE_AGENT_ADDRESS != "agent1q...": # Using LocalResourceAgent for locations/venues
                 ctx.logger.info(f"Delegating '{user_query}' to LocalResourceLogisticsAgent...")
                 await ctx.send(LOCAL_RESOURCE_AGENT_ADDRESS, ChatMessage(
                    timestamp=datetime.utcnow(), msg_id=uuid4(), content=[TextContent(type="text", text=user_query)]
                 ))
                 response_text = f"Searching for locations or venues for you. What specific place or type of venue are you looking for?"
            else:
                 response_text = "I can help with locations, but the resource agent isn't configured yet."
        else:
            # Fallback: If no specific intent, directly use ASI:One LLM for a general response
            ctx.logger.info(f"Using internal ASI:One LLM for general query: '{user_query}'")
            try:
                r = llm_client.chat.completions.create(
                    model="asi1-mini",
                    messages=[
                        {"role": "system", "content": f"""
                        You are a helpful assistant for LocalHive, designed for local event planning and service exchange in communities.
                        Your current location is Bhopal, Madhya Pradesh, India. The current time is {datetime.now().strftime('%A, %B %d, %Y at %I:%M:%S %p %Z')}.
                        If the user asks about something outside these domains, provide a polite and general helpful response,
                        or suggest how they can use LocalHive.
                        """},
                        {"role": "user", "content": user_query},
                    ],
                    max_tokens=200,
                )
                response_text = str(r.choices[0].message.content)
            except Exception as e:
                ctx.logger.error(f"Error querying internal ASI:One LLM: {e}")
                response_text = "I'm having trouble processing your general request with my AI brain at the moment."

    await ctx.send(sender, ChatMessage(timestamp=datetime.utcnow(), msg_id=uuid4(), content=[TextContent(type="text", text=response_text)]))

@porter_agent.on_message(model=GeolocationResponse)
async def handle_geolocation_response(ctx: Context, sender: str, msg: GeolocationResponse):
    """
    Handles the response from the Google API Geolocation Agent.
    Stores the geocoded locality in the DataManagerAgent.
    """
    ctx.logger.info(f"Received GeolocationResponse from {sender}: Lat={msg.latitude}, Lon={msg.longitude}")

    user_address_for_geolocation = None
    for user_addr, user_state in ctx.storage.items():
        if user_state.get("onboarding_step") == 2:
            user_address_for_geolocation = user_addr
            break

    if user_address_for_geolocation:
        user_state = ctx.storage.get(user_address_for_geolocation)
        user_name = user_state.get("name", "there")
        locality = user_state.get("locality", "your location")

        if DATA_MANAGER_AGENT_ADDRESS != "agent1q...":
            try:
                await ctx.send(DATA_MANAGER_AGENT_ADDRESS, UserProfileData(
                    timestamp=datetime.utcnow(),
                    msg_id=uuid4(),
                    content=[TextContent(type="text", text="User profile data for storage")],
                    user_name=user_name,
                    locality=locality,
                    latitude=msg.latitude,
                    longitude=msg.longitude
                ))
                response_text = f"Great, {user_name}! I've saved your location ({locality}). You are now fully onboarded and ready to use LocalHive! How can I help you today?"
                user_state["onboarding_step"] = 3
                ctx.storage.set(user_address_for_geolocation, user_state)
            except Exception as e:
                ctx.logger.error(f"Error sending user data to DataManagerAgent: {e}")
                response_text = f"Welcome, {user_name}! I got your location, but had trouble saving your profile. You are now onboarded. How can I help you today?"
                user_state["onboarding_step"] = 3
                ctx.storage.set(user_address_for_geolocation, user_state)
        else:
            response_text = f"Welcome, {user_name}! I got your location, but the Data Manager Agent is not configured. You are now onboarded. How can I help you today?"
            user_state["onboarding_step"] = 3
            ctx.storage.set(user_address_for_geolocation, user_state)

        await ctx.send(user_address_for_geolocation, ChatMessage(timestamp=datetime.utcnow(), msg_id=uuid4(), content=[TextContent(type="text", text=response_text)]))
    else:
        ctx.logger.warning("Received GeolocationResponse but could not find matching user in onboarding state.")

@chat_protocol.on_message(ChatMessage)
async def handle_response_from_other_agent(ctx: Context, sender: str, msg: ChatMessage):
    """
    Handles responses from other agents and forwards them back to the user.
    (This simple forward assumes a direct one-to-one reply and doesn't handle complex threading).
    """
    response_content = ''
    for item in msg.content:
        if isinstance(item, TextContent):
            response_content += item.text

    ctx.logger.info(f"PorterAgent received response from {sender}: {response_content}")

    # Acknowledge the message from the other agent
    await ctx.send(sender, ChatAcknowledgement(timestamp=datetime.now(), acknowledged_msg_id=msg.msg_id))

    # Try to find the original user to forward the response
    # In a real system, you'd associate the original user_address with delegated messages
    # For MVP, we'll just log and assume direct user interaction.
    # If the sender is not the user and not the geolocation agent, we assume it's a sub-agent's reply
    # and we forward it to the user who triggered the delegation.
    # This requires a more robust state management to map sender to original user.
    # For a simple demo, we'll assume the Porter is talking directly to the user.
    
    # A simple (but not robust) way to forward might be to check if the sender is not a known sub-agent and forward to the
    # current active user (if only one user is expected for demo).
    # A more robust approach would be to store original_user_address when delegating.
    # For now, we'll just log that a response was received from a sub-agent.
    # The `handle_user_message` already sends an initial response.
    pass # No direct forwarding to user here for simplicity, Porter handles the user-facing response.


@chat_protocol.on_message(ChatAcknowledgement)
async def handle_ack(ctx: Context, sender: str, msg: ChatAcknowledgement):
    """
    Handles acknowledgements from other agents, confirming message receipt.
    """
    ctx.logger.info(f"Received acknowledgement from {sender} for message ID: {msg.acknowledged_msg_id}")

porter_agent.include(chat_protocol, publish_manifest=True)
