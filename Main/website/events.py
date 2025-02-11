import socketio
from flask_socketio import send, disconnect
from flask import request
from flask_login import current_user
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

nltk.download('vader_lexicon')
sia = SentimentIntensityAnalyzer()

users = {}

def calculate_points(message):
    sentiment = sia.polarity_scores(message)
    compound_score = sentiment['compound']
    
    if compound_score >= 0.5:
        return 3
    if compound_score > 0.1:
        return 2
    return 1

@socketio.on('connect')
def handle_connect():
    if current_user.is_authenticated:
        users[request.sid] = current_user.username
        print(f"{current_user.username} connected")
    else:
        disconnect()

@socketio.on('disconnect')
def handle_disconnect():
    username = users.pop(request.sid, None)
    if username:
        print(f"{username} disconnected")

@socketio.on('message')
def handle_message(msg):
    if request.sid not in users:
        return
    
    username = users[request.sid]
    full_msg = f"{username}: {msg}"
    send(full_msg, broadcast=True)
    
    points = calculate_points(msg)
    user = current_user._get_current_object()
    user.update_points(points)