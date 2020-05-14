import os
import time
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_socketio import SocketIO, join_room, leave_room, send


# Configure app
app = Flask(__name__)
socketio = SocketIO(app)

rooms = ["lounge", "news", "games", "coding"]


@app.route("/")
def index():
    return render_template("chat.html", rooms=rooms)

@app.route("/getRooms", methods=["GET"])
def getRooms():
    return jsonify(ROOMS)

@socketio.on('incoming-msg')
def on_message(data):
    """Broadcast messages"""

    msg = data["msg"]
    username = data["username"]
    room = data["room"]
    time_stamp = time.strftime('%b-%d %I:%M%p', time.localtime())
    send({"username": username, "msg": msg, "time_stamp": time_stamp}, room=room)

@socketio.on("create_room")
def createChannel(data):
    if data['room'] not in ROOMS:
        user = data['user']
        ROOMS.append(data['room'])
        join_room(data['room'])
        data = user + " has entered the room";
        send({"msg": user + " has joined the " + data['room'] + " room."}, room=room)
    else:
        return flash('Room already exists')

@socketio.on('join')
def on_join(data):
    username = data["username"]
    room = data["room"]
    join_room(room)

    # Broadcast that new user has joined
    send({"msg": username + " has joined the " + room + " room."}, room=room)


@socketio.on('leave')
def on_leave(data):
    username = data['username']
    room = data['room']
    leave_room(room)
    send({"msg": username + " has left the room"}, room=room)

if __name__ == "__main__":
    app.run(debug=True)
