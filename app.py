from flask import Flask, redirect, render_template, request, url_for, session
from mongo import *
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex()


# Routing
@app.route('/')
def index():
    
    return render_template("index.html")

@app.route('/login')
def login():

    return render_template("login.html", warning="")


@app.route('/signup')
def signup():

    return render_template("signup.html")

@app.route('/home')
def home():
    if "username" not in session:
        return redirect(url_for("login"))
    username = session["username"]

    


@app.route('/valid', methods = ["POST", "GET"])
def valid():

    if request.method == "POST":
        form = request.form
        username = form["username"]
        password = form["password"]
        valid, message = valid_login(username, password)
        if valid:
            session["username"] = username
            return redirect(url_for('home'))
        return redirect(url_for('login'))






# Error handling
@app.errorhandler(404)
def page_not_found(error):

    return render_template("page_not_found.html"), 404

if __name__ == "__main__":
    app.run()