# LocalHive: Empowering Communities with AI

**LocalHive** is an intelligent, community-focused assistant designed to streamline event planning and peer-to-peer service exchange. By orchestrating a network of specialized AI agents, LocalHive transforms complex coordination into a seamless, accessible experience—empowering vibrant, connected communities.

---

## 🚀 Inspiration

Every community faces challenges in organizing events and facilitating mutual aid. From neighborhood cleanups to local festivals or finding help for everyday tasks, coordination can be daunting. LocalHive was born from the vision to leverage AI for effortless community engagement, making local collaboration easy, inclusive, and impactful.

---

## 🧠 What is LocalHive?

LocalHive is your intelligent, localized assistant for all things community:

- **Effortless Event Planning:** Brainstorm, organize, and manage logistics for local gatherings with ease.
- **Peer-to-Peer Service Exchange:** Connects neighbors to offer and request services (e.g., dog walking, tutoring, gardening).
- **Smart Coordination:** Understands natural language requests and delegates tasks to specialized AI agents, reducing manual effort.

**LocalHive is your go-to platform for building stronger, more supportive local networks.**

---

## 🏗️ How It Works

LocalHive is built on the [uAgents](https://github.com/fetchai/uAgents) framework, using a robust multi-agent architecture:

- **Porter (Supervisor) Agent:** Central hub that receives user requests and orchestrates communication.
- **LLM Integration:** Direct connection to ASI:One LLM for advanced natural language understanding and intelligent responses.
- **Data Management:** Securely stores user profiles and geocoded locations via a dedicated DataManagerAgent.
- **Specialized Agents:**
    - **EventIdeationPlannerAgent:** Brainstorms and structures event ideas.
    - **LocalResourceLogisticsAgent:** Finds local resources and venues.
    - **SponsorshipFinanceAgent:** Handles budgeting and sponsorships.
    - **LocalServiceExchangeAgent:** Manages peer-to-peer service offerings.
- **Inter-Agent Communication:** Utilizes Agentchatprotocol v0.3.0 for reliable messaging.
- **Marketplace Integrations:** Integrates with external agents (e.g., Google Geolocation) for enhanced capabilities.

---

## ⚡ Key Challenges

- Accurate intent recognition from diverse user inputs
- Consistent state management across distributed agents
- Reliable agent-to-agent communication
- Secure API key management
- Robust, intuitive onboarding flow

---

## 🏆 Accomplishments (not yet ready)

- Fully functional multi-agent system
- Seamless onboarding with geocoding
- Direct ASI:One LLM integration
- Real-time, intelligent task delegation
- Scalable data management for user profiles

---

## 💡 What We Learned

- The power and scalability of multi-agent architectures
- Importance of well-defined communication protocols
- Best practices for LLM integration and prompt engineering
- Strategies for distributed state management
- Value of iterative, AI-driven development

---

## 🔮 What's Next

- **Personalized Recommendations:** Leverage user data for tailored suggestions
- **Proactive Engagement:** Agents that suggest events/services automatically
- **Deeper Integrations:** Ticketing, local directories, payment gateways
- **Advanced Event Management:** Budgeting, volunteer coordination, attendee tracking
- **Reputation System:** Trust and review features for service providers
- **Mobile App:** User-friendly mobile experience

---

## 🛠️ Getting Started

### Prerequisites

- Python 3.9+
- ASI:One API Key
- Google Geocoding API Key (if using `custom_geolocation_agent.py`)

### Setup

1. **Clone the repository:**
     ```bash
     git clone https://github.com/your-username/LocalHive.git
     cd LocalHive
     ```

2. **Create and activate a virtual environment:**
     ```bash
     python3 -m venv venv
     # On macOS/Linux
     source venv/bin/activate
     # On Windows
     .\venv\Scripts\activate
     ```

3. **Install dependencies:**
     ```bash
     pip install -r requirements.txt
     ```

4. **Configure API Keys:**
     - Open each agent file in `agents/` and replace `'INSERT_YOUR_ASI_ONE_API_KEY_HERE'` and `'YOUR_GOOGLE_GEOCODING_API_KEY'` as needed.

5. **Update Agent Addresses:**
     - After deploying agents in Agentverse IDE, update the addresses in `agents/porter_agent.py` under the CONFIGURATION section.

---

### Running the Agents

You can run agents in the [Agentverse IDE](https://agentverse.ai/) (recommended) or locally for development:

**To run locally:**

Open a terminal for each agent in the `agents/` directory:

```bash
# Terminal 1
python porter_agent.py

# Terminal 2
python data_manager_agent.py

# Terminal 3
python event_ideation_planner_agent.py

# Terminal 4
python local_resource_logistics_agent.py

# Terminal 5
python sponsorship_finance_agent.py

# Terminal 6
python local_service_exchange_agent.py
```

> **Note:** Local inter-agent communication may require additional setup (e.g., mailbox server, agent registration). For best results, use Agentverse deployment.

---

## 📄 License

This project is note licensed yet.

---

**Connect. Collaborate. Empower your community with LocalHive.**