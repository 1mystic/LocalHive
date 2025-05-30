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
sponsorship_finance_agent = Agent(name="SponsorshipFinanceAgent", seed="finance_recovery_phrase")
chat_protocol = Protocol(spec=chat_protocol_spec)

# --- MESSAGE HANDLERS ---

@chat_protocol.on_message(ChatMessage)
async def handle_finance_request(ctx: Context, sender: str, msg: ChatMessage):
    """
    Handles finance and sponsorship requests and provides hardcoded advice.
    """
    ctx.logger.info(f"SponsorshipFinanceAgent received request from {sender}: {msg.content}")

    user_query = ''
    for item in msg.content:
        if isinstance(item, TextContent):
            user_query += item.text.lower()

    # Hardcoded responses based on simple keyword matching
    if "sponsorship" in user_query or "sponsor" in user_query:
        response = "To secure sponsorship for your event in Bhopal, consider: 1. Local businesses (restaurants, shops). 2. Community banks/credit unions. 3. Local political representatives. Prepare a clear proposal outlining benefits for sponsors."
    elif "budget" in user_query or "cost" in user_query:
        response = "For event budgeting: 1. Estimate all expenses (venue, food, marketing, equipment). 2. Add a 10-15% contingency. 3. Track all income sources (tickets, sponsorships). Focus on maximizing value for money."
    elif "fundraising" in user_query:
        response = "Fundraising ideas for community projects: 1. Online crowdfunding. 2. Local bake sales or car washes. 3. Partnership with local non-profits. 4. Small donation drives at local gatherings."
    else:
        response = "I can offer basic financial and sponsorship advice. What specific area are you interested in (e.g., 'getting sponsors', 'creating a budget', 'fundraising')?"

    await ctx.send(
        sender,
        ChatMessage(
            timestamp=datetime.utcnow(),
            msg_id=uuid4(),
            content=[TextContent(type="text", text=response)]
        )
    )
    ctx.logger.info(f"SponsorshipFinanceAgent sent response to {sender}.")

@chat_protocol.on_message(ChatAcknowledgement)
async def handle_ack(ctx: Context, sender: str, msg: ChatAcknowledgement):
    ctx.logger.info(f"Received acknowledgement from {sender} for message ID: {msg.acknowledged_msg_id}")

sponsorship_finance_agent.include(chat_protocol, publish_manifest=True)
