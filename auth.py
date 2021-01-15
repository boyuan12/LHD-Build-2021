from flask import Flask, request, session, render_template, redirect
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3

app = Flask(__name__)

conn = sqlite3.connect("db.sqlite3")
c = conn.cursor()


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        _ = c.execute("SELECT * FROM users WHERE email=:email", {
            "email": email
        }).fetchall()

        if len(_) != 0:
            return render_template("error.html", message="Invalid email, email already exist!")

        pwhash = generate_password_hash(password, method="pbkdf2:sha256", salt_length=8)

        c.execute("INSERT INTO users (email, password) VALUES (:email, :password)", {
            "email": email,
            "password": pwhash,
        })
        conn.commit()

        user = c.execute("SELECT * FROM users WHERE email=:email", {"email": email}).fetchall()
        session["user_id"] = user[0][0]

        c.execute("INSERT INTO balance (user_id, balance) VALUES (:user_id, :bal)", {
            "user_id": session.get("user_id"),
            "bal": 500
        })
        conn.commit()

        return redirect("/")
    else:
        return render_template("signup.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = c.execute("SELECT * FROM users WHERE email=:email", {
            "email": email
        }).fetchall()

        if len(user) != 1:
            return render_template("error.html", message="Invalid email, please try again!")

        if not check_password_hash(user[0][2], password):
            return render_template("error.html", message="Invalid password, please try again!")

        session["user_id"] = user[0][0]

        return redirect("/")
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")