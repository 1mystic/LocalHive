LocalHive: Your Community AI Assistant
LocalHive is an intelligent, localized assistant designed to empower communities through seamless event planning and peer-to-peer service exchange. It simplifies complex coordination tasks by orchestrating a network of specialized AI agents, making community engagement and local help more accessible and efficient.

Inspiration
Our inspiration for LocalHive stemmed from a desire to address a common pain point in every community: the struggle to organize local events and facilitate mutual aid efficiently. Whether it's a neighborhood cleanup, a local festival, or simply finding someone to help with a small task, the coordination can be daunting. We envisioned a solution that leverages AI to empower individuals and groups, making community engagement seamless and accessible, ultimately fostering stronger, more connected local environments.

What it does
LocalHive acts as your intelligent, localized assistant for all things community-related. It's designed to:

Simplify Event Planning: From brainstorming creative ideas to outlining logistics and even assisting with sponsorship outreach, LocalHive streamlines the entire event organization process for local gatherings.

Facilitate Peer-to-Peer Service Exchange: It creates a dynamic marketplace where community members can easily offer their skills (e.g., dog walking, gardening, tutoring) and find help for their needs, fostering a culture of mutual support.

Provide Smart Coordination: By understanding natural language requests, it intelligently delegates tasks to specialized AI agents, reducing manual effort and making complex coordination surprisingly simple.

Essentially, LocalHive is your go-to platform for fostering vibrant, active, and supportive local communities.

How we built it
LocalHive is built on the uAgents framework, leveraging a multi-agent architecture to break down complex tasks into manageable components handled by specialized AI agents.

Agent-Based Design: A core Porter (Supervisor) Agent serves as the central intelligent hub, receiving user requests and orchestrating communication with other specialized agents.

LLM Integration: The Porter agent directly integrates with the ASI:One LLM for powerful natural language understanding, intent recognition, and generating intelligent responses.

Data Management: A dedicated DataManagerAgent securely stores user profiles, including names and geocoded localities obtained from a marketplace Geolocation Agent.

Specialized Agents: We developed custom agents for specific functionalities:

EventIdeationPlannerAgent: Brainstorms and structures event ideas.

LocalResourceLogisticsAgent: Focuses on finding local resources and venues.

SponsorshipFinanceAgent: Assists with budgeting and sponsorship inquiries.

LocalServiceExchangeAgent: Manages the peer-to-peer offering and finding of local services.

Inter-Agent Communication: All agents communicate seamlessly using the Agentchatprotocol v0.3.0, ensuring robust and reliable message exchange.

External Marketplace Integrations: For enhanced capabilities, LocalHive integrates with key external marketplace agents, such as the Google API Geolocation Agent for precise location data.

Challenges we ran into
Precise Intent Recognition: Accurately discerning user intent from varied natural language inputs.

State Management across Agents: Maintaining conversational state and profile information consistently across multiple interacting agents.

Seamless Agent-to-Agent Communication: Ensuring correct routing, acknowledgment, and processing of messages.

API Key Management: Securely handling and configuring multiple API keys across different agents.

Onboarding Flow Robustness: Designing an intuitive and resilient onboarding process.

Accomplishments that we're proud of
Functional Multi-Agent System: Successfully building and deploying a cohesive multi-agent system.

Seamless Onboarding Experience: Implementing a user-friendly onboarding flow with geocoding.

Direct ASI:One LLM Integration: Achieving effective integration with the ASI:One LLM for general intelligence.

Real-time Task Delegation: The ability of the Porter Agent to accurately interpret user needs and delegate tasks.

Foundational Data Management: Establishing a basic, yet scalable, data management system for user profiles.

What we learned
The Power of Multi-Agent Architectures: Breaking down complex problems into specialized agents leads to robust and scalable applications.

Importance of Protocol Design: Well-defined communication protocols are critical for reliable inter-agent interactions.

LLM Integration Best Practices: Refined knowledge of prompt engineering and integrating LLMs effectively.

State Management Strategies: Learned the importance of thoughtful state management across distributed agents.

Iterative Development with AI: The value of an iterative development approach for stable systems.

What's next for LocalHive
Enhanced Personalization: Leverage stored user data for highly personalized recommendations.

Proactive Community Engagement: Develop agents that proactively suggest events or services.

Integration with Real-world Services: Deepen integrations with ticketing platforms, local directories, or payment gateways.

Advanced Event Management Features: Incorporate budget tracking, volunteer coordination, and attendee management.

Reputation and Trust System: Implement a reputation or review system for service providers.

Mobile Application: Develop a user-friendly mobile application for accessibility.

Getting Started
To run LocalHive locally, follow these steps:

Prerequisites
Python 3.9+

An ASI:One API Key

A Google Geocoding API Key (only if you plan to use the custom_geolocation_agent.py instead of the marketplace agent)

Setup
Clone the repository:

git clone https://github.com/your-username/LocalHive.git
cd LocalHive

Create a virtual environment:

python3 -m venv venv

Activate the virtual environment:

On macOS/Linux:

source venv/bin/activate

On Windows:

.\venv\Scripts\activate

Install dependencies:

pip install -r requirements.txt

Configure API Keys:
Open each agent file in the agents/ directory and replace 'INSERT_YOUR_ASI_ONE_API_KEY_HERE' and 'YOUR_GOOGLE_GEOCODING_API_KEY' (if applicable) with your actual API keys.

Update Agent Addresses:
After deploying each agent on the Agentverse IDE, copy its unique agent address and update the CONFIGURATION section in agents/porter_agent.py with the correct addresses for DATA_MANAGER_AGENT_ADDRESS, EVENT_PLANNER_AGENT_ADDRESS, LOCAL_RESOURCE_AGENT_ADDRESS, SPONSORSHIP_FINANCE_AGENT_ADDRESS, and LOCAL_SERVICE_EXCHANGE_AGENT_ADDRESS. The GEOLOCATION_AGENT_ADDRESS is pre-filled for the marketplace agent.

Running the Agents
You can run these agents either directly in the Agentverse IDE or locally. For a full demo, deploying them to Agentverse is recommended for inter-agent communication.

To run locally (for development/testing):

Navigate to the agents/ directory and run each agent in a separate terminal:

# In terminal 1
python porter_agent.py

# In terminal 2
python data_manager_agent.py

# In terminal 3
python event_ideation_planner_agent.py

# In terminal 4
python local_resource_logistics_agent.py

# In terminal 5
python sponsorship_finance_agent.py

# In terminal 6
python local_service_exchange_agent.py

Note: For local testing, inter-agent communication might require additional setup (e.g., using a local mailbox server or ensuring agents are registered and discoverable). For a seamless demo, Agentverse deployment is ideal.

License
This project is licensed under the MIT License.