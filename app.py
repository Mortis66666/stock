from flask import Flask, redirect, render_template, request, url_for, session
from mongo import *
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex()


# Routing
@app.route('/') # index route
def index():
    
    return render_template("index.html")

@app.route('/login') # login route
def login():
    warning = session.get("login_warning","")
    return render_template("login.html", warning=warning)


@app.route('/signup') # signup route
def signup():
    warning = session.get("signup_warning","")
    return render_template("signup.html", warning=warning)

@app.route('/home') # home route
def home():
    if "username" not in session:
        return redirect(url_for("login"))
    username = session["username"]
    infos = get_user_info(username)

    return render_template("home.html", **infos)

@app.route('/success') # success route
def success():

    return render_template("success.html")

@app.route('/mystocks')
def mystocks():
    if "username" not in session:
        return redirect(url_for("login"))
    username = session["username"]
    infos = get_user_info(username)

    return render_template("mystocks.html", **infos)

@app.route('/search')
def search():
    if "username" not in session:
        return redirect(url_for("login"))
    username = session["username"]
    infos = get_user_info(username)

    ranstocks = random_stocks()
    logging.warn(ranstocks)
    for stock in ranstocks:
        logging.warn(stock)
    return render_template("search.html", random_stocks = ranstocks, **infos)

@app.route('/leaderboard')
def leaderboard():
    if "username" not in session:
        return redirect(url_for("login"))
    username = session["username"]
    infos = get_user_info(username)

    return render_template("leaderboard.html", **infos)

@app.route('/faq')
def faq():

    return render_template("faq.html")

@app.route('/profile')
def profile():

    # TODO render template and kwargs for profile
    pass

@app.route('/stock/<username>')
def stock(username):

    # TODO Get the user info and send to html
    pass

@app.route('/login_validator', methods = ["POST", "GET"])
def login_validator():

    if request.method == "POST":
        form = request.form
        username = form["username"]
        password = form["password"]
        valid, message = valid_login(username, password)
        if valid:
            session["username"] = username
            session.pop("login_warning", None)
            return redirect(url_for('home'))
        print(message)
        session["login_warning"] = message
        return redirect(url_for('login'))
    session["login_warning"] = "Please login first"
    return redirect(url_for('login'))


@app.route('/signup_validator', methods = ["POST", "GET"])
def signup_validator():

    if request.method == "POST":
        form = request.form
        username = form["username"]
        password = form["password"]
        confirm_password = form["cpassword"]
        valid, message = valid_signup(username, password, confirm_password)
        if valid:
            sign_up(username,password)
            session.pop("signup_warning", None)
            return redirect(url_for('success'))
        print(message)
        session["signup_warning"] = message
        return redirect(url_for('signup'))
    session["signup_warning"] = "Please sign up first"
    return redirect(url_for('signup'))




# Error handling
@app.errorhandler(404)
def page_not_found(error):

    return render_template("page_not_found.html"), 404

if __name__ == "__main__":
    app.run()