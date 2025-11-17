# 🚀 Voice Agent AI Receptionist: Conversational Booking & Automation Suite

A modern AI-powered appointment receptionist and scheduler with full voice/chat dashboard, real-time Google Calendar integration, n8n workflow automation, live email notifications, and seamless VAPI voice calling.

---

## 🌐 Live Demo

<!-- If deploying, add DEMO link here or keep as code-only -->

---

## 📸 Screenshots

- **Dashboard Overview:**  
  ![dashboard](screenshots/dashboard.png)
  *Beautiful conversational UI with live transcripts, statistics, and floating VAPI widget.*

- **n8n Automation Workflow:**  
  ![n8n workflow](screenshots/n8n-workflow.png)
  *Pipeline triggers for email/send and event marking.*

- **Booking Confirmation Email:**  
  ![Gmail Email](screenshots/email.png)
  *Automated Gmail confirmation of successful appointment.*

- **Google Calendar Appointment:**  
  ![Google Calendar](screenshots/calendar.png)
  *Event marked directly via AI voice agent.*

- **VAPI Voice Call in Action:**  
  ![VAPI Calling](screenshots/vapi-call.png)
  *Realtime AI call for seamless hands-free scheduling.*

> _Replace the image URLs/paths above with your real screenshot filenames once uploaded to your GitHub repository’s `/screenshots` folder._

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
      git clone https://github.com/your_username/voice-agent-project.git
   cd voice-agent-project
2. **Install dependencies:**
     python -m venv venv
     source venv/bin/activate # or venv\Scripts\activate on Windows
     pip install -r requirements.txt
3.3. **Configure Google API:**
   - Place your `credentials.json` in the project root.

4. **Run n8n (for automation):**
     n8n start 
5. **Start the agent backend:**
    python main_pipeline.py

6. **Open Dashboard:**
- Go to [http://localhost:5000](http://localhost:5000)
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

- **Lead Developer:** _Your Name_
- **Contributors:** _List others if any_
- **Special Thanks:** [VAPI](https://vapi.ai/), [Ollama](https://ollama.com/), [n8n](https://n8n.io/)

---

## 🛡️ License

MIT (or your chosen license)

