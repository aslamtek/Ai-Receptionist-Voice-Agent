from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/')
def index():
    return "Flask SocketIO Server Works!"

if __name__ == "__main__":
    print("If you see this, Flask server is about to start!")
    socketio.run(app, port=5000, debug=True)
