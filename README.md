<div align="center">

# 🚀 Voice Agent AI Receptionist  
*A Modern Conversational Booking & Automation Suite*

![Python](https://img.shields.io/badge/Python-3.10-blue?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Active-success?style=for-the-badge)

</div>

---

## 📑 Table of Contents

- [Live Demo](#live-demo)
- [Screenshots](#screenshots)
- [Problem Statement](#problem-statement)
- [Key Features](#key-features)
- [Project Structure](#project-structure)
- [Quick Start](#quick-start)
- [Core Technologies](#core-technologies)
- [How It Works](#how-it-works)
- [Developer Credits](#developer-credits)
- [License](#license)

## 🌐 Live Demo

[Demo Site](https://691afb20b1ea8400082e31d5--shimmering-semolina-601af8.netlify.app/)
---

## 📸 Screenshots

- **Dashboard Overview:**  
  <img width="1142" height="978" alt="image" src="https://github.com/user-attachments/assets/397f0069-626a-4cee-847b-e78c02c20db6" />

  *Beautiful conversational UI with live transcripts, statistics, and floating VAPI widget.*
  
- **VAPI Voice Call in Action:**  
  <img width="1606" height="1062" alt="image" src="https://github.com/user-attachments/assets/cbec6955-9f40-4335-8a62-77055eb63157" />

  *Realtime AI call for seamless hands-free scheduling.*

- **n8n Automation Workflow:**  
 <img width="1357" height="553" alt="image" src="https://github.com/user-attachments/assets/e431daaa-8f17-4b23-9edd-b96ff1147fad" />

  *Pipeline triggers for email/send and event marking.*

- **Booking Confirmation Email:**  
  ![WhatsApp Image 2025-11-17 at 23 49 56_6d7a9761](https://github.com/user-attachments/assets/6b4d026f-1e00-48a2-b0ef-5bbe3fad93c1)

  *Automated Gmail confirmation of successful appointment.*

- **Google Calendar Appointment:**  
  <img width="815" height="671" alt="image" src="https://github.com/user-attachments/assets/71aa1cb7-41c1-45aa-84cc-8eb1ac409682" />

  *Event marked directly via AI voice agent.*


---

## 💡 Key Features

- **Conversational Voice or Chat Booking** using Whisper ASR, TTS, LLM backend (Ollama), and Flask real-time dashboard (Socket.IO)
- **Modern Dashboard UI** — animated gradients, stats grid, chat history, VAPI floating action
- **Google Calendar Integration** — automatic check and booking, OAuth-secure
- **n8n Workflow Automation** — triggers emails, workflows, custom actions
- **Live Email Notifications** — Google Mail workflow confirmation
- **VAPI Calling** — one-click AI phone call for instant appointment setting
- **Mobile Responsive, Dark & Light Mode**

---

## 📂 Project Structure

VOICE_AGENT_PROJECT/
├── static/
│ ├── css/dashboard.css
│ └── js/dashboard.js
├── templates/dashboard.html
├── main_pipeline.py # Backend AI + workflow logic
├── credentials.json # Google API
├── token.pickle # Google OAuth token (auto-generated)
├── venv/ # Python virtual environment


---

## ⚡ Quick Start

1. **Clone the repo:**
   ```bash
      git clone https://github.com/your_username/voice-agent-project.git
   ```
   cd voice-agent-project
   
3. **Install dependencies:**
     python -m venv venv
     source venv/bin/activate # or venv\Scripts\activate on Windows
   ```bash
     pip install -r requirements.txt
   ```
3.3. **Configure Google API:**
  ## - Place your `credentials.json` in the project root.

5. **Run n8n (for automation):**
     ##  n8n start 
6. **Start the agent backend:**
    python main_pipeline.py

7. **Open Dashboard:**
## - Go to [http://localhost:5000](http://localhost:5000)
- Start a conversation with voice or text, book appointments hands-free!

---

## ⚙️ Core Technologies

| Frontend     | Backend         | AI/NLP        | Automation |
|--------------|----------------|---------------|------------|
| HTML, CSS    | Flask          | whisper.cpp   | n8n        |
| JS, SocketIO | Python         | gTTS, Ollama  | VAPI       |
| Responsive   | REST, SocketIO | ASR, LLM      | Google API |

---

## 📝 How it Works

1. **Dashboard listens** for chat or VAPI voice calls.
2. **Speech instructions** are transcribed, intent parsed, and used to check/book via Google Calendar API.
3. **n8n workflows** trigger automated confirmation emails.
4. **Everything is tracked** in real-time—transcripts, stats, voice waveforms.

---

## 🧑‍💻 Developer Credits

**Mohammed Aslam**

## 🏅 Special Thanks

- **[Ollama](https://ollama.com/)** — Local LLM for instant conversation
- **[gTTS](https://pypi.org/project/gTTS/)** — Google Text-to-Speech Python library
- **[VAPI](https://vapi.ai/)** — Voice AI agent for conversational interface
- **[n8n](https://n8n.io/)** — Automation/workflow engine
- **[REST API](https://en.wikipedia.org/wiki/Representational_state_transfer)** — Backend API integration
- **[Flask](https://flask.palletsprojects.com/)** — Python web framework/dashboard
- **[Whisper AI](https://github.com/openai/whisper)** — ASR and audio transcription
- **[google-auth](https://pypi.org/project/google-auth/)** — Secure Google API/OAuth integration
- **Natural Language Processing (NLP)** — All underlying language understanding/runtime

---

## 🛡️ License

MIT 

