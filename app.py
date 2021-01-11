from flask import Flask, request, session, render_template, redirect
from werkzeug.security import check_password_hash, generate_password_hash
import os
import requests
from datetime import datetime

app = Flask(__name__)

FINNHUB_IO_API_KEY = os.getenv("FINNHUB_IO_API_KEY")

app.config["SECRET_KEY"] = "secretkey"

if not os.getenv('DATABASE_URL'):
    import sqlite3
    conn = sqlite3.connect("db.sqlite3", check_same_thread=False)
    c = conn.cursor()
else:
    from sqlalchemy import create_engine
    from sqlalchemy.orm import scoped_session, sessionmaker
    engine = create_engine(os.getenv("DATABASE_URL"))
    db = scoped_session(sessionmaker(bind=engine))
    conn = db()
    c = conn


def get_current_stock_price(symbol):
    r = requests.get(f'https://finnhub.io/api/v1/quote?symbol={symbol}&token={FINNHUB_IO_API_KEY}')
    return r.json()["c"]


def current_timestamp():
    dateTimeObj = datetime.now()
    string = str(dateTimeObj.year) + '/' + str(dateTimeObj.month) + '/' + str(dateTimeObj.day) + " " +  str(dateTimeObj.hour) + ':' + str(dateTimeObj.minute), ':' + str(dateTimeObj.second)
    return str(string)


@app.route("/")
def index():
    if not session.get("user_id"):
        return render_template("index.html")
    else:
        stocks = c.execute("SELECT * FROM stocks WHERE user_id=:user_id", {
            "user_id": session.get("user_id")
        }).fetchall()

        total = 0

        for d in stocks:
            price = get_current_stock_price(d[2])
            total += price * d[2]

        return render_template("dashboard.html", stocks=stocks, total=total)


@app.route("/stocks")
def view_all_stock():
    pass


@app.route("/transactions")
def view_all_trans():
    pass


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


@app.route("/<string:symbol>")
def view_stock(symbol):
    r = requests.get(f'https://finnhub.io/api/v1/stock/profile2?symbol={symbol}&token={FINNHUB_IO_API_KEY}')

    amount = 0
    current_price = get_current_stock_price(symbol)

    stock = c.execute("SELECT * FROM stocks WHERE user_id=:user_id", {
        "user_id": session.get("user_id"),
        "symbol": symbol
    }).fetchall()

    if len(stock) != 0:
        amount = stock[0][2] * current_price

    return render_template("buy.html", data=r.json(), price=current_price, amount=amount)


@app.route("/search")
def search():
    if request.args.get("q"):
        r = requests.get(f'https://finnhub.io/api/v1/search?q={request.args.get("q")}&token={FINNHUB_IO_API_KEY}')
        return render_template("searched.html", data=r.json(), q=request.args.get("q"))
    else:
        return render_template("search.html")


@app.route("/buy/<string:symbol>", methods=["POST"])
def buy(symbol):
    amount = float(request.form.get("amount"))
    amount_available = c.execute("SELECT balance FROM balance WHERE user_id=:user_id", {
        "user_id": session.get("user_id")
    }).fetchall()[0][0]

    if amount_available < float(amount):
        return render_template("error.html", message="Too much to purchase")

    price = get_current_stock_price(symbol)

    share = amount / price

    c.execute("INSERT INTO stocks (user_id, symbol, share) VALUES (:user_id, :symbol, :share)", {
        "user_id": session.get("user_id"),
        "symbol": symbol,
        "share": share
    })
    conn.commit()

    c.execute("INSERT INTO transactions (user_id, type, symbol, share, amount, timestamp) VALUES (:user_id, :type, :symbol, :share, :amount, :ts)", {
        "user_id": session.get("user_id"),
        "type": "buy",
        "symbol": symbol,
        "share": share,
        "amount": amount,
        "ts": current_timestamp()
    })
    conn.commit()

    c.execute("UPDATE balance SET balance=:bal WHERE user_id=:user_id", {
        "bal": amount_available-amount,
        "user_id": session.get("user_id")
    })
    conn.commit()

    return render_template("success.html", message=f"Success! You bought {share} of {symbol} for ${amount}")


@app.route("/sell/<string:symbol>", methods=["POST"])
def sell(symbol):
    amount = float(request.form.get("amount"))
    share = c.execute("SELECT share FROM stocks WHERE symbol=:symbol AND user_id=:user_id", {
        "symbol": symbol,
        "user_id": session.get("user_id")
    }).fetchall()

    if len(share) == 0:
        return render_template("error.html", message=f"You don't have any {symbol} stock")

    share = share[0][0]
    current_price = get_current_stock_price(symbol)
    total = current_price * share

    if amount > total:
        return render_template("error.html", message="You don't have that much fo stock worth to sell")

    new_share = share - amount / current_price

    if new_share == 0:
        c.execute("DELETE FROM stocks WHERE user_id=:user_id AND symbol=:symbol", {
            "user_id": session.get("user_id"),
            "symbol": symbol
        })
        conn.commit()
    else:
        c.execute("UPDATE stocks SET share=:share WHERE user_id=:user_id", {
            "user_id": session.get("user_id"),
            "share": new_share
        })
        conn.commit()

    c.execute("INSERT INTO transactions (user_id, type, symbol, share, amount, timestamp) VALUES (:user_id, :type, :symbol, :share, :amount, :ts)", {
        "user_id": session.get("user_id"),
        "type": "sell",
        "symbol": symbol,
        "share": share - new_share,
        "amount": amount,
        "ts": current_timestamp()
    })

    bal = c.execute("SELECT balance FROM balance WHERE user_id=:user_id", {
        "user_id": session.get("user_id")
    }).fetchall()[0][0]

    c.execute("UPDATE balance SET balance=:bal WHERE user_id=:user_id", {
        "bal": bal + amount,
        "user_id": session.get("user_id")
    })

    conn.commit()

    return render_template("success.html", message=f"Success! You sold {share} of {symbol} for ${amount}")

