import os
import datetime
import random

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import login_required

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

db = SQL("sqlite:///environ.db")

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route("/", methods=["POST", "GET"])
def index():
    n = random.randint(1, 15)
    quote = db.execute("SELECT message FROM quotes WHERE id=?", n)
    if request.method == "GET":
        rows = db.execute("SELECT * FROM shared")
        random.shuffle(rows)
        return render_template("index.html", quote=quote[0], rows=rows)

    else:
        q = request.form.get("search")
        rows = db.execute("SELECT * FROM shared WHERE title LIKE ?", "%" + q + "%")
        rows1 = db.execute("SELECT * FROM shared WHERE def LIKE ?", "%" + q + "%")
        rows2 = db.execute("SELECT * FROM shared WHERE type LIKE ?", "%" + q + "%")
        rows3 = db.execute("SELECT * FROM shared WHERE user LIKE ?", "%" + q + "%")
        for item in rows1:
            rows.append(item)
        for item in rows2:
            rows.append(item)
        for item in rows3:
            rows.append(item)

        return render_template("index.html", quote=quote[0], rows=rows, result=q)

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    n = random.randint(1, 15)
    quote = db.execute("SELECT message FROM quotes WHERE id=?", n)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return render_template("login.html", message="Please fill all fields!", quote=quote[0])

        # Ensure password was submitted
        elif not request.form.get("password"):
            return render_template("login.html", message="Please fill all fields!", quote=quote[0])

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return render_template("login.html", message="Incorrect username or password!", quote=quote[0])

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/") #########################################

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html", quote=quote[0])

@app.route("/register", methods=["GET", "POST"])
def register():
    n = random.randint(1, 15)
    quote = db.execute("SELECT message FROM quotes WHERE id=?", n)
    if request.method == "GET":
        return render_template("register.html", quote=quote[0])

    else:
        if not request.form.get("username"):
             return render_template("register.html", message="Fill all fields")

        if not request.form.get("password"):
             return render_template("register.html", message="Fill all fields")

        if not request.form.get("confirmpass"):
             return render_template("register.html", message="Fill all fields")

        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmpass")

        data = db.execute("SELECT * FROM users WHERE username=?", username)

        if len(data) != 0:
            return render_template("register.html", message="Username already exists!")

        if password != confirmation:
            return render_template("register.html", message="Re-enter passwords...")

        hashed = generate_password_hash(confirmation)

        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, hashed)
        return redirect("/login")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/developer")
def developer():
    n = random.randint(1, 15)
    quote = db.execute("SELECT message FROM quotes WHERE id=?", n)
    return render_template("developer.html", quote=quote[0])

@app.route("/share", methods=["GET", "POST"])
@login_required
def share():
    n = random.randint(1, 15)
    quote = db.execute("SELECT message FROM quotes WHERE id=?", n)
    if request.method == "GET":
        return render_template("share.html", quote=quote[0])

    if request.method == "POST":
        shareType = request.form.get("type")
        title = request.form.get("title")
        defi = request.form.get("description")
        content = request.form.get("content")
        message = "Please fill all fields!"

        if not shareType or not title or not defi or not content:
            return render_template("share.html", message=message, quote=quote[0])

        users = db.execute("SELECT username FROM users WHERE id=?", session["user_id"])
        username = users[0]["username"]
        db.execute("INSERT INTO shared (user, type, title, def, content, time) VALUES (?, ?, ?, ?, ?, ?)", username, shareType, title, defi, content, datetime.datetime.now())


        return redirect("/")

@app.route("/content", methods=["POST", "GET"])
def content():
    images = ["/static/content1.jpg", "/static/content2.jpeg", "/static/content3.jpeg", "/static/content4.jpeg", "/static/content5.jpeg", "/static/content6.jpeg", "/static/content7.jpeg", "/static/content8.jpeg"]
    random.shuffle(images)
    n = random.randint(1, 15)
    quote = db.execute("SELECT message FROM quotes WHERE id=?", n)
    id = request.form.get("num")
    data = db.execute("SELECT * FROM shared WHERE id=?", id)
    print(images)
    return render_template("content.html", data=data[0], quote=quote[0], image=images[0])

@app.route("/about")
def about():
    n = random.randint(1, 15)
    quote = db.execute("SELECT message FROM quotes WHERE id=?", n)
    return render_template("about.html", quote=quote[0])

@app.route("/yourShare")
@login_required
def yourShare():
    n = random.randint(1, 15)
    quote = db.execute("SELECT message FROM quotes WHERE id=?", n)
    users = db.execute("SELECT username FROM users WHERE id=?", session["user_id"])
    data = db.execute("SELECT * FROM shared WHERE user=?", users[0]["username"])
    return render_template("yourShare.html", rows=data, quote=quote[0])

@app.route("/specific")
def specific():
    specify = request.args.get("types")
    n = random.randint(1, 15)
    quote = db.execute("SELECT message FROM quotes WHERE id=?", n)
    types = ['idea', 'contribution', 'awareness', 'experience', 'fact']
    for item in types:
        if specify == item:
            rows = db.execute("SELECT * FROM shared WHERE type=?", item)
            random.shuffle(rows)
            return render_template("index.html", quote=quote[0], rows=rows, result=item)
        if specify == "all":
            rows = db.execute("SELECT * FROM shared")
            random.shuffle(rows)
            return render_template("index.html", quote=quote[0], rows=rows)
