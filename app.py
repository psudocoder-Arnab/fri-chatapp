from flask import Flask, render_template, request
from flask_socketio import SocketIO
import json

app = Flask(__name__)
socketio = SocketIO(app)

CHAT_FILE = 'chat_messages.txt'

try:
    with open(CHAT_FILE, 'r') as file:
        messages = json.load(file)
except FileNotFoundError:
    messages = []

@app.route('/')
def index():
    return render_template('index.html', messages=messages)

@socketio.on('message')
def handle_message(data):
    messages.append(data)
    
    with open(CHAT_FILE, 'w') as file:
        json.dump(messages, file)
    
    socketio.emit('update_chat', messages)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', debug=True)
