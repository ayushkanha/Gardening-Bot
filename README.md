# 🌿 Gardening Assistant Pro-Bot

> *Your intelligent companion for cultivating greener spaces with AI-powered insights and automation*

An advanced, all-in-one AI assistant crafted for gardening enthusiasts who want to nurture their plants with expert guidance, real-time data, and seamless task automation. Built on cutting-edge technologies including Streamlit, LangChain, and Groq LLM, this bot transforms your gardening experience by combining conversational intelligence with powerful practical tools.

---

## ✨ Key Features

### 🤖 Intelligent Gardening Chatbot

**RAG-Powered Expertise**  
Leverages a specialized knowledge base stored in ChromaDB to deliver accurate, contextual answers about planting schedules, pest management, soil nutrition, pruning techniques, and seasonal care strategies.

**Voice-Enabled Interaction**  
Communicate naturally with Speech-to-Text input and Text-to-Speech responses, perfect for hands-free gardening while working in your garden.

**Context-Aware Conversations**  
Maintains conversation history to provide coherent, personalized guidance that builds on previous interactions.

---

### 🛠️ Smart Utility Tools

**Real-Time Weather Intelligence**  
Fetches current weather conditions via WeatherAPI, helping you make informed decisions about watering schedules, planting windows, and frost protection.

**Smart Shopping Assistant**  
Automatically scrapes Google Shopping to compare prices and find the best deals on seeds, fertilizers, tools, and gardening equipment.

**Data Visualization Suite**  
Upload your gardening logs (CSV/Excel format) and watch as the bot generates insightful charts and visualizations using Matplotlib and Seaborn, revealing patterns in growth rates, harvest yields, and seasonal trends.

---

### 📅 Automation & Productivity

**Email Notifications**  
Send reminders, care instructions, or harvest updates directly through Gmail integration—all from within the chat interface.

**Calendar Integration**  
Schedule planting dates, fertilization reminders, and garden maintenance tasks directly to your Google Calendar with a simple command.

---

### 🔐 Secure Access

**User Authentication**  
Protected by a secure login system ensuring your gardening data and preferences remain private.

---

## 📂 Project Architecture

| File | Purpose |
|------|---------|
| `app.py` | Core Streamlit application managing UI, tools orchestration, and agent logic |
| `data.py` | Initializes ChromaDB Vector Store with curated gardening documents for RAG |
| `graphs.py` | Generates intelligent data visualizations from uploaded datasets using LLM agents |
| `mailsender.py` | Handles Gmail API for emails and Google Calendar API for event scheduling |
| `voice.py` | Speech-to-Text (SpeechRecognition) and Text-to-Speech (gTTS) utilities |
| `websraper.py` | SerpApi integration for Google Shopping product searches |
| `requirements.txt` | Complete list of Python dependencies |

---

## ⚙️ Installation Guide

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/ayushkanha/pro-bot.git
cd pro-bot
```

### 2️⃣ Set Up Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Configure API Keys & Credentials

#### Create Streamlit Secrets File

Create `.streamlit/secrets.toml` in the project root:

```toml
Groq_API_KEY = "your_groq_api_key"
WETHER_API_KEY = "your_weather_api_key"
```

#### Set Up Environment Variables

Create a `.env` file for web scraping:

```env
SECRAPER_API_KEY=your_serpapi_key
```

#### Google Workspace Credentials

Place your `credentials.json` (OAuth 2.0 Client ID) in the project root directory to enable Gmail and Google Calendar functionality.

---

## 🚀 Getting Started

### Launch the Application

```bash
streamlit run app.py
```

### Login Credentials

Use these default credentials (configurable in `app.py`):

- **User 1:** Username: `ayushkanha` | Password: `ayush`
- **User 2:** Username: `kanha` | Password: `1234`

### Explore the Features

**💬 Conversational Queries**  
- "How do I care for tomato plants in summer?"
- "What's the best fertilizer for roses?"
- "When should I prune my fruit trees?"

**📊 Data Analysis**  
Upload a CSV file via the sidebar and ask: *"Generate graphs showing my monthly harvest yields"*

**🌤️ Weather & Shopping**  
- "Check the weather in Bhilai"
- "Find prices for organic neem oil"
- "Compare prices for garden hoses"

**📧 Productivity Commands**  
- "Send an email to gardener@example.com with this week's care schedule"
- "Schedule a fertilization reminder for next Monday at 9 AM"

---

## 🛠️ Technology Stack

| Category | Technologies |
|----------|-------------|
| **Frontend** | Streamlit |
| **AI/LLM** | Groq (Mistral-Saba-24b) |
| **Orchestration** | LangChain (Agents, Chains, Tools) |
| **Vector Database** | ChromaDB |
| **APIs** | Google Gmail, Google Calendar, WeatherAPI, SerpApi |
| **Data Science** | Pandas, Matplotlib, Seaborn |
| **Voice** | SpeechRecognition, gTTS |

---

## 🤝 Contributing

We welcome contributions from the community! Whether you're fixing bugs, adding features, or improving documentation, your help makes this project better.

### How to Contribute

1. **Fork the Repository**
2. **Create a Feature Branch**
   ```bash
   git checkout -b feature/AmazingFeature
   ```
3. **Commit Your Changes**
   ```bash
   git commit -m 'Add some AmazingFeature'
   ```
4. **Push to Your Branch**
   ```bash
   git push origin feature/AmazingFeature
   ```
5. **Open a Pull Request**

---

## 📄 License

This project is distributed under the **MIT License**. See `LICENSE` file for complete details.

---

## 🌟 Acknowledgments

Built with passion for gardeners, by developers who love to see things grow—both in code and in the garden.

---

## 📧 Contact & Support

For questions, suggestions, or support, please open an issue on GitHub or reach out to the maintainers.

**Happy Gardening! 🌱**
