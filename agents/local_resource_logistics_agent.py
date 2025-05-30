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
local_resource_agent = Agent(name="LocalResourceAgent", seed="local_resource_recovery_phrase")
chat_protocol = Protocol(spec=chat_protocol_spec)

# --- MESSAGE HANDLERS ---

@chat_protocol.on_message(ChatMessage)
async def handle_resource_request(ctx: Context, sender: str, msg: ChatMessage):
    """
    Handles local resource requests and provides hardcoded information.
    """
    ctx.logger.info(f"LocalResourceAgent received request from {sender}: {msg.content}")

    user_query = ''
    for item in msg.content:
        if isinstance(item, TextContent):
            user_query += item.text.lower()

    # Hardcoded responses based on simple keyword matching
    if "park" in user_query or "venue" in user_query:
        response = "For parks in Bhopal, consider: 1. Van Vihar National Park (Large, serene). 2. Shahpura Lake Park (Good for picnics, boating). 3. Ekant Park (Playground, open space). Always check local regulations for events."
    elif "equipment" in user_query or "sound system" in user_query:
        response = "For event equipment in Bhopal, look for: 1. 'Event Solutions Bhopal' (sound, lighting). 2. 'Sharma Tent House' (tents, chairs). Local community centers might also offer basic equipment rentals."
    elif "catering" in user_query or "food" in user_query:
        response = "For catering services in Bhopal: 1. 'Bhopali Zaika Catering' (local cuisine). 2. 'Celebrations Caterers' (multi-cuisine options). 3. Small local restaurants for specific needs."
    else:
        response = "I can help with local resource suggestions. Please specify what kind of resource you're looking for (e.g., 'a venue', 'catering', 'equipment')."

    await ctx.send(
        sender,
        ChatMessage(
            timestamp=datetime.utcnow(),
            msg_id=uuid4(),
            content=[TextContent(type="text", text=response)]
        )
    )
    ctx.logger.info(f"LocalResourceAgent sent response to {sender}.")

@chat_protocol.on_message(ChatAcknowledgement)
async def handle_ack(ctx: Context, sender: str, msg: ChatAcknowledgement):
    ctx.logger.info(f"Received acknowledgement from {sender} for message ID: {msg.acknowledged_msg_id}")

local_resource_agent.include(chat_protocol, publish_manifest=True)
