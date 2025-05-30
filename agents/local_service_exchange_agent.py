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
local_service_exchange_agent = Agent(name="LocalServiceExchangeAgent", seed="service_exchange_recovery_phrase")
chat_protocol = Protocol(spec=chat_protocol_spec)

# --- MESSAGE HANDLERS ---

@chat_protocol.on_message(ChatMessage)
async def handle_service_request(ctx: Context, sender: str, msg: ChatMessage):
    """
    Handles local service exchange requests and provides hardcoded information.
    """
    ctx.logger.info(f"LocalServiceExchangeAgent received request from {sender}: {msg.content}")

    user_query = ''
    for item in msg.content:
        if isinstance(item, TextContent):
            user_query += item.text.lower()

    # Hardcoded responses based on simple keyword matching
    if "photographer" in user_query or "photos" in user_query:
        response = "Looking for a photographer in Bhopal? Check out 'Creative Lens Photography' or 'Pixel Perfect Studio'. You might also find local talent in community art groups."
    elif "gardener" in user_query or "gardening" in user_query:
        response = "Need gardening help? 'Green Thumb Services' offers basic gardening. For community volunteers, try posting on local social media groups."
    elif "tutor" in user_query or "teaching" in user_query:
        response = "For tutoring services in Bhopal: 1. 'Success Tutorials' (various subjects). 2. Local college students often offer private tuition. Specify subject and level for best matches."
    elif "offer" in user_query and "service" in user_query:
        response = "Great! To offer a service, please tell me what you offer and your general availability. We'll connect you with community members who need your skills."
    else:
        response = "I can help you find or offer local services. Please tell me what service you need (e.g., 'I need a gardener') or what you want to offer (e.g., 'I offer tutoring services')."

    await ctx.send(
        sender,
        ChatMessage(
            timestamp=datetime.utcnow(),
            msg_id=uuid4(),
            content=[TextContent(type="text", text=response)]
        )
    )
    ctx.logger.info(f"LocalServiceExchangeAgent sent response to {sender}.")

@chat_protocol.on_message(ChatAcknowledgement)
async def handle_ack(ctx: Context, sender: str, msg: ChatAcknowledgement):
    ctx.logger.info(f"Received acknowledgement from {sender} for message ID: {msg.acknowledged_msg_id}")

local_service_exchange_agent.include(chat_protocol, publish_manifest=True)
