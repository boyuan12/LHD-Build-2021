from flask import Flask, render_template, redirect, request, session
from flask_socketio import SocketIO, emit
import requests

import sqlite3
conn = sqlite3.connect("db.sqlite3", check_same_thread=False)
c = conn.cursor()

app = Flask(__name__)
socketio = SocketIO(app)

app.config["SECRET_KEY"] = "abcdef"

SPOTIFY_CLIENT_ID = "c2747effe16f49d8b98d150d05944e7b"
SPOTIFY_CLIENT_SECRET = "c5388834b1284f8abdd34af741e45365"


def base64_encode(message):
    import base64
    message_bytes = message.encode('ascii')
    base64_bytes = base64.b64encode(message_bytes)
    base64_message = base64_bytes.decode('ascii')
    return base64_message


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/auth/spotify")
def spotify_oauth():
    return redirect(f"https://accounts.spotify.com/authorize?client_id={SPOTIFY_CLIENT_ID}&response_type=code&redirect_uri=http://127.0.0.1:5000/auth/spotify/callback")


@app.route("/auth/spotify/callback")
def spotify_callback():
    r = requests.post("https://accounts.spotify.com/api/token", data={
        "grant_type": "authorization_code",
        "code": request.args.get("code"),
        "redirect_uri": "http://127.0.0.1:5000/auth/spotify/callback"
    }, headers={
        "Authorization": f"Basic {base64_encode(SPOTIFY_CLIENT_ID + ':' + SPOTIFY_CLIENT_SECRET)}"
    })

    print(r.json()["access_token"])

    session["SPOTIFY_ACCESS_TOKEN"] = r.json()["access_token"]

    return r.json()["access_token"]


@app.route("/create")
def create():
    c.execute("INSERT INTO room (room_id, name) VALUES ('abcdef', 'hello world!')")
    conn.commit()

    return redirect("/room/abcdef/")


@app.route("/room/<string:room_id>")
def room(room_id):

    r = requests.get("https://api.spotify.com/v1/search?q=roadhouse%20blues&type=album", headers={"Authorization": f"Bearer {session.get('SPOTIFY_ACCESS_TOKEN')}"})

    url = r.json()['albums']['items'][0]['artists'][0]['external_urls']['spotify']
    s = url.split("/")
    s.insert(3, "embed")

    return render_template("room.html", data=r.json(), url="/".join(s))


if __name__ == "__main__":
    socketio.run(app, debug=True)