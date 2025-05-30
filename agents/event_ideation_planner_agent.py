from datetime import datetime
from uuid import uuid4

from uagents import Agent, Context, Protocol
from uagents_core.contrib.protocols.chat import (
    ChatAcknowledgement,
    ChatMessage,
    TextContent,
    chat_protocol_spec,
)

# --- AGENT SETUP ---
event_planner_agent = Agent(name="EventPlannerAgent", seed="event_planner_recovery_phrase")
chat_protocol = Protocol(spec=chat_protocol_spec)

# --- MESSAGE HANDLERS ---

@chat_protocol.on_message(ChatMessage)
async def handle_event_request(ctx: Context, sender: str, msg: ChatMessage):
    """
    Handles event planning requests and provides a hardcoded plan.
    """
    ctx.logger.info(f"EventPlannerAgent received request from {sender}: {msg.content}")

    user_query = ''
    for item in msg.content:
        if isinstance(item, TextContent):
            user_query += item.text.lower()

    # Hardcoded responses based on simple keyword matching
    if "picnic" in user_query:
        plan = "Great! For a community picnic, consider: 1. Date/Time: A sunny Saturday afternoon. 2. Location: Local park (check availability). 3. Activities: Games, music, food stalls. 4. Supplies: Blankets, trash bags, first aid. 5. Promotion: Local flyers, social media."
    elif "cleanup" in user_query or "clean-up" in user_query:
        plan = "For a community clean-up drive: 1. Target Area: Identify specific spots. 2. Date/Time: Early morning, cooler weather. 3. Equipment: Gloves, trash bags, grabbers. 4. Volunteers: Recruit through local groups. 5. Disposal: Coordinate with local municipality for waste collection."
    elif "festival" in user_query:
        plan = "Planning a local festival: 1. Theme: Something unique to the community. 2. Venue: Large open space or community center. 3. Attractions: Food vendors, craft stalls, live music, kids' zone. 4. Permits: Obtain all necessary local permits. 5. Marketing: Extensive local outreach."
    else:
        plan = "That sounds interesting! While I'm just an MVP, I can help you plan a general event. A basic event plan includes: 1. Define Goal. 2. Set Date & Time. 3. Choose Location. 4. Plan Activities. 5. Promote Event."

    # Send hardcoded response back to the sender (PorterAgent)
    await ctx.send(
        sender,
        ChatMessage(
            timestamp=datetime.utcnow(),
            msg_id=uuid4(),
            content=[TextContent(type="text", text=plan)]
        )
    )
    ctx.logger.info(f"EventPlannerAgent sent response to {sender}.")

@chat_protocol.on_message(ChatAcknowledgement)
async def handle_ack(ctx: Context, sender: str, msg: ChatAcknowledgement):
    ctx.logger.info(f"Received acknowledgement from {sender} for message ID: {msg.acknowledged_msg_id}")

event_planner_agent.include(chat_protocol, publish_manifest=True)
