from flask import Flask, request, render_template, redirect
import requests

app = Flask(__name__)

@app.route("/")
def index():
    if request.args.get("q"):
        r = requests.get(f"https://api.spoonacular.com/recipes/complexSearch?q={request.args.get('q')}&apiKey=e3b4f950e6ac47e49eb340b79af4860e", headers={
            "Content-Type": "application/json"
        })
        return render_template("searched.html", data=r.json()["results"])
    else:
        return render_template("index.html")


@app.route("/<string:id>")
def view_recipe(id):
    r = requests.get(f"https://api.spoonacular.com/recipes/{id}/information?apiKey=e3b4f950e6ac47e49eb340b79af4860e").json()
    return redirect(r["sourceUrl"])

