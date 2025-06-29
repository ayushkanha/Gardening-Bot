# 🌱 Gardening-Bot

Automate plant care reminders with email, voice, calendar invites, and graphs using Python!

## 🚀 Features

- 📧 Email reminders when it's time to water your plants
- 🔊 Voice alerts using text-to-speech
- 📊 Visualize watering activity with graphs
- 📅 Automatically schedule meetings/reminders for watering
- 🌐 Optional web scraping for environmental data

## 🧩 Getting Started

### Prerequisites

- Python 3.8 or higher
- Internet connection for sending emails and web scraping
- SMTP credentials (e.g., Gmail)
- [Optional] Google Calendar API credentials for scheduling events

### Installation

```bash
git clone https://github.com/ayushkanha/Gardening-Bot.git
cd Gardening-Bot
python -m venv venv
source venv/bin/activate  # On Windows use venv\Scripts\activate
pip install -r requirements.txt
```


📂 Project Structure
File	Description
app.py	Main script to run reminders and alerts
data.py	Configuration and state logging
graphs.py	Generates visual charts of watering history
mailsender.py	Handles sending email reminders
voice.py	Converts text to voice (text-to-speech)
meetingsheduler.py	Adds reminders to your calendar
webscraper.py	(Optional) Fetches external data

🛠️ Contributing
Fork the project

Create a feature branch: git checkout -b feature/your-feature

Commit changes

Push to your fork

Open a Pull Request

📄 License
This project is licensed under the MIT License – feel free to use, modify, and distribute.

📬 Contact
Made with 💚 by Ayush Sahu
