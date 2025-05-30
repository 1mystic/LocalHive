from datetime import datetime
from uuid import uuid4

from uagents import Agent, Context, Protocol, Model
from uagents_core.contrib.protocols.chat import (
    ChatAcknowledgement,
    ChatMessage,
    TextContent,
)

# Define a custom model for user profile data (must match Porter's UserProfileData)
class UserProfileData(ChatMessage):
    user_name: str
    locality: str
    latitude: float
    longitude: float

# --- AGENT SETUP ---
data_manager_agent = Agent(name="DataManagerAgent", seed="data_manager_recovery_phrase")

# Define a protocol for handling UserProfileData and acknowledgements
data_protocol = Protocol()
data_protocol.add_message(UserProfileData, replies=ChatAcknowledgement)
data_protocol.add_message(ChatAcknowledgement)

# --- MESSAGE HANDLERS ---

@data_protocol.on_message(UserProfileData)
async def handle_user_profile_data(ctx: Context, sender: str, msg: UserProfileData):
    """
    Receives user profile data from the PorterAgent and stores it.
    """
    user_key = f"{msg.user_name.replace(' ', '_').lower()}_{msg.locality.replace(' ', '_').lower()}"

    user_data_to_store = {
        "name": msg.user_name,
        "locality": msg.locality,
        "latitude": msg.latitude,
        "longitude": msg.longitude,
        "last_updated": datetime.now().isoformat()
    }

    ctx.storage.set(user_key, user_data_to_store)
    ctx.logger.info(f"Stored user data for '{msg.user_name}' ({msg.locality}) under key '{user_key}'.")
    ctx.logger.info(f"Full stored data: {ctx.storage.get(user_key)}")

    await ctx.send(
        sender,
        ChatAcknowledgement(timestamp=datetime.now(), acknowledged_msg_id=msg.msg_id),
    )

@data_protocol.on_message(ChatAcknowledgement)
async def handle_ack(ctx: Context, sender: str, msg: ChatAcknowledgement):
    """
    Handles acknowledgements from other agents.
    """
    ctx.logger.info(f"Received acknowledgement from {sender} for message ID: {msg.acknowledged_msg_id}")

data_manager_agent.include(data_protocol, publish_manifest=True)
