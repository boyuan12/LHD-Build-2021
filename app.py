from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

conn = sqlite3.connect("db.sqlite3")
c = conn.cursor()


@app.route("/")
def index():
    if request.method == "POST":
        item = request.form.get("item")
        c.execute("INSERT INTO items (item) VALUES (:item)", {"item": item})
        conn.commit()
        return redirect("/")
    items = c.execute("SELECT * FROM items").fetchall()
    return render_template("index.html", items=items)
