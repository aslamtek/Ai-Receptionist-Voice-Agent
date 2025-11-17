import whisper
import requests
from gtts import gTTS
import pygame
import os
import speech_recognition as sr
import threading
import queue
import re
import time
import uuid
import json
import logging

# Google Calendar imports
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from datetime import datetime, timedelta
import pickle

# Flask imports
from flask import Flask, render_template
from flask_socketio import SocketIO, emit

# ===== LOGGING SETUP =====
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ===== CONFIGURATION =====
N8N_WEBHOOK_URL = "http://localhost:5678/webhook/from-agent"
OLLAMA_API_URL = "http://localhost:11434/api/generate"
FLASK_PORT = 5000
WHISPER_MODEL = "tiny"
OLLAMA_MODEL = "phi3"

SCOPES = ['https://www.googleapis.com/auth/calendar']

SYSTEM_PROMPT = (
    "You are Sarah, a professional receptionist with Google Calendar access. "
    "You can check and create appointments. "
    "When booking, ask for date, time, and purpose if not provided. "
    "Keep responses SHORT (1-2 sentences). Stay professional and helpful."
)

FORBIDDEN_WORDS = [
    "victorian", "elizabeth", "librarian", "patron", "thee", "thy",
    "dost", "hath", "instruction", "follow up", "user:", "example:",
    "solution:", "question:", "textbook"
]

# ===== GLOBAL STATE =====
device = "cuda"
whisper_model = whisper.load_model(WHISPER_MODEL)
pygame.mixer.init()

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

dashboard_history = []
conversation_history = []
tts_queue = queue.Queue()

# ===== N8N INTEGRATION =====
def push_to_n8n(data):
    """Send event data to n8n webhook"""
    try:
        response = requests.post(N8N_WEBHOOK_URL, json=data, timeout=5)
        logger.info(f"✅ n8n webhook sent - Status: {response.status_code}")
    except Exception as e:
        logger.error(f"❌ n8n push failed: {e}")

# ===== FLASK & SOCKETIO =====
@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@socketio.on('connect')
def handle_connect():
    """Send history to newly connected client"""
    emit('history', {'data': dashboard_history})
    logger.info("✅ Client connected to dashboard")

def broadcast_transcript(user_text):
    """Broadcast user transcription to dashboard"""
    dashboard_history.append({'type': 'user', 'text': user_text, 'timestamp': datetime.now().isoformat()})
    socketio.emit('transcript', {'type': 'user', 'text': user_text})

def broadcast_response(ai_text):
    """Broadcast AI response to dashboard"""
    dashboard_history.append({'type': 'ai', 'text': ai_text, 'timestamp': datetime.now().isoformat()})
    socketio.emit('transcript', {'type': 'ai', 'text': ai_text})

def start_flask_server():
    """Start Flask server in daemon thread"""
    def run_flask():
        socketio.run(app, port=FLASK_PORT, debug=False, use_reloader=False)
    
    thread = threading.Thread(target=run_flask, daemon=True)
    thread.start()
    logger.info(f"📊 Dashboard running at http://localhost:{FLASK_PORT}")

# ===== TEXT-TO-SPEECH =====
def tts_worker():
    """Background TTS worker thread"""
    while True:
        text = tts_queue.get()
        if text is None:
            break
        
        audio_file = None
        try:
            if text.strip():
                file_id = str(uuid.uuid4())
                audio_file = f"speech_{file_id}.mp3"
                
                # Generate and play audio
                tts = gTTS(text=text.strip(), lang='en', slow=False)
                tts.save(audio_file)
                
                pygame.mixer.music.load(audio_file)
                pygame.mixer.music.play()
                
                while pygame.mixer.music.get_busy():
                    pygame.time.Clock().tick(10)
                
                pygame.mixer.music.unload()
                time.sleep(0.1)
                
                if os.path.exists(audio_file):
                    os.remove(audio_file)
                    
        except Exception as e:
            logger.error(f"🔇 TTS error: {e}")
            if audio_file and os.path.exists(audio_file):
                try:
                    pygame.mixer.music.unload()
                    time.sleep(0.1)
                    os.remove(audio_file)
                except:
                    pass
        finally:
            tts_queue.task_done()

def start_tts_thread():
    """Start background TTS worker"""
    thread = threading.Thread(target=tts_worker, daemon=True)
    thread.start()

def speak_text(text):
    """Queue text for TTS (non-blocking)"""
    if text and text.strip():
        tts_queue.put(text.strip())

# ===== GOOGLE CALENDAR INTEGRATION =====
def get_calendar_service():
    """Authenticate and return Google Calendar service"""
    creds = None
    
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    
    return build('calendar', 'v3', credentials=creds)

def create_appointment(summary, start_time_str, duration_minutes=30):
    """Create Google Calendar event"""
    try:
        service = get_calendar_service()
        
        # Parse time
        if "tomorrow" in start_time_str.lower():
            start = datetime.now() + timedelta(days=1)
            start = start.replace(hour=10, minute=0, second=0)
        else:
            start = datetime.fromisoformat(start_time_str)
        
        end = start + timedelta(minutes=duration_minutes)
        
        event = {
            'summary': summary,
            'start': {'dateTime': start.isoformat(), 'timeZone': 'Asia/Kolkata'},
            'end': {'dateTime': end.isoformat(), 'timeZone': 'Asia/Kolkata'},
        }
        
        service.events().insert(calendarId='primary', body=event).execute()
        return f"✅ Appointment created for {start.strftime('%B %d at %I:%M %p')}"
    except Exception as e:
        return f"❌ Error creating appointment: {str(e)}"

def list_upcoming_appointments(max_results=5):
    """Get upcoming appointments"""
    try:
        service = get_calendar_service()
        now = datetime.utcnow().isoformat() + 'Z'
        
        events_result = service.events().list(
            calendarId='primary',
            timeMin=now,
            maxResults=max_results,
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        
        events = events_result.get('items', [])
        if not events:
            return "You have no upcoming appointments."
        
        appointments = []
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            start_dt = datetime.fromisoformat(start.replace('Z', '+00:00'))
            appointments.append(f"{start_dt.strftime('%B %d at %I:%M %p')}: {event['summary']}")
        
        return "📅 Upcoming appointments: " + ", ".join(appointments)
    except Exception as e:
        return f"❌ Error fetching appointments: {str(e)}"

# ===== SPEECH RECOGNITION =====
def transcribe_audio():
    """Transcribe audio using Whisper"""
    r = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            print("\n🎤 Listening... Speak now.")
            r.adjust_for_ambient_noise(source, duration=1)
            audio = r.listen(source, timeout=10, phrase_time_limit=15)
        
        with open("temp_audio.wav", "wb") as f:
            f.write(audio.get_wav_data())
        
        result = whisper_model.transcribe("temp_audio.wav", language="en", fp16=False)
        text = result["text"].strip()
        print(f"📝 You said: {text}")
        broadcast_transcript(text)
        return text
    
    except sr.WaitTimeoutError:
        logger.warning("⏱️ No speech detected")
        return ""
    except Exception as e:
        logger.error(f"❌ Transcription error: {e}")
        return ""

# ===== LLM QUERY WITH CONTENT FILTERING =====
def query_ollama_streaming(user_text):
    """Stream LLM response with content filtering"""
    global conversation_history
    
    conversation_history.append(f"User: {user_text}")
    context = "\n".join(conversation_history[-2:])
    
    payload = {
        "model": OLLAMA_MODEL,
        "prompt": f"{SYSTEM_PROMPT}\n\n{context}\nSarah:",
        "stream": True,
        "temperature": 0.3,
        "top_p": 0.7,
        "top_k": 20,
        "repeat_penalty": 1.2,
        "stop": ["\n\n", "User:", "Instruction", "Question", "Example"],
        "options": {
            "num_ctx": 512,
            "num_predict": 100
        }
    }
    
    try:
        response = requests.post(OLLAMA_API_URL, json=payload, stream=True, timeout=10)
        
        full_response = ""
        current_sentence = ""
        word_count = 0
        
        print("💬 Sarah: ", end="", flush=True)
        
        for line in response.iter_lines():
            if line:
                chunk = json.loads(line)
                token = chunk.get("response", "")
                
                # Content filter
                if any(word in (full_response + token).lower() for word in FORBIDDEN_WORDS):
                    print("\n⚠️ [Response filtered]")
                    speak_text("I apologize, let me answer that professionally.")
                    return ""
                
                print(token, end="", flush=True)
                full_response += token
                current_sentence += token
                word_count += len(token.split())
                
                if word_count > 50:
                    print("...")
                    break
                
                # Speak complete sentences
                if re.search(r'[.!?]\s*$', current_sentence.strip()):
                    speak_text(current_sentence.strip())
                    current_sentence = ""
        
        if current_sentence.strip():
            speak_text(current_sentence.strip())
        
        print()
        
        conversation_history.append(f"Sarah: {full_response}")
        if len(conversation_history) > 4:
            conversation_history = conversation_history[-2:]
        
        broadcast_response(full_response)
        
        # Log to file
        with open("response_output.txt", "a", encoding="utf-8") as f:
            f.write(f"User: {user_text}\nSarah: {full_response}\n{'-'*50}\n")
        
        return full_response
    
    except Exception as e:
        logger.error(f"❌ LLM error: {e}")
        speak_text("Sorry, I had a technical issue. Could you repeat that?")
        return ""

# ===== MAIN CONVERSATION LOOP =====
def main():
    """Main conversation loop"""
    print("🤖 Sarah (AI Receptionist) - Conversational Mode")
    print("Say 'exit' or 'goodbye' to stop.\n")
    
    # Clean up old audio files
    for f in os.listdir("."):
        if f.startswith("speech_") and f.endswith(".mp3"):
            try:
                os.remove(f)
            except:
                pass
    
    start_tts_thread()
    
    while True:
        try:
            user_text = transcribe_audio()
            
            if not user_text or len(user_text.split()) < 2:
                print("🛑 No clear speech detected, please try again...")
                continue
            
            # Send to n8n
            push_to_n8n({"event": "transcription", "text": user_text})
            
            # Check exit conditions
            if any(word in user_text.lower() for word in ["exit", "goodbye", "stop", "quit"]):
                print("👋 Goodbye!")
                speak_text("Goodbye! Have a great day!")
                tts_queue.put(None)
                break
            
            # Handle calendar requests
            user_lower = user_text.lower()
            
            if any(word in user_lower for word in ["schedule", "appointment", "calendar"]):
                if any(word in user_lower for word in ["check", "show", "what", "list"]):
                    appointments = list_upcoming_appointments()
                    print(f"📅 {appointments}")
                    speak_text(appointments)
                    push_to_n8n({"event": "list_appointments", "user": user_text, "result": appointments})
                
                elif any(word in user_lower for word in ["book", "create", "make", "schedule"]):
                    result = create_appointment("New appointment", "tomorrow", 30)
                    print(f"📅 {result}")
                    speak_text(result)
                    push_to_n8n({"event": "appointment_created", "user": user_text, "result": result})
                
                else:
                    query_ollama_streaming(user_text)
            else:
                query_ollama_streaming(user_text)
            
            tts_queue.join()
            time.sleep(1)
        
        except KeyboardInterrupt:
            print("\n👋 Shutting down...")
            tts_queue.put(None)
            break
        except Exception as e:
            logger.error(f"❌ Main loop error: {e}")

# ===== ENTRY POINT =====
if __name__ == "__main__":
    start_flask_server()
    time.sleep(1)
    main()
