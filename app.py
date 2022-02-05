from flask import Flask, redirect, render_template, request, url_for, session
from mongo import *
from threading import Thread
import secrets
import time

app = Flask(__name__)
app.secret_key = secrets.token_hex()
app.jinja_env.globals.update(get_user_info=get_user_info)

stock_task = Thread(target=task)

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

    return render_template("home.html", message=session.get("homemsg", ""), **infos)

@app.route('/success') # success route
def success():

    return render_template("success.html")

@app.route('/mystocks')
def mystocks():
    if "username" not in session:
        return redirect(url_for("login"))
    username = session["username"]
    infos = get_user_info(username)

    return render_template("mystocks.html", message=session.get("msmsg", ""), **infos)

@app.route('/search')
def search():
    if "username" not in session:
        return redirect(url_for("login"))
    username = session["username"]
    infos = get_user_info(username)

    return render_template("search.html", **infos)

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

@app.route('/oops')
def oops():

    return render_template("oops.html")


# Routes for verifiying user data
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


@app.route('/buy')
def buy():

    if request.method == "GET":

        try:

            form = request.args
            
            buyer = session["username"]
            stock_owner = form["user"]
            amount = int(form["amount"])
            price = amount * get_user_info(stock_owner)["stock_value"]
            buyer_bal = get_user_info(buyer)["coins"]
            stock_left = get_user_info(stock_owner)["stock_left"]

            if buyer_bal >= price and amount <= stock_left:
                add_bal(buyer, -price)
                add_stock(buyer, stock_owner, amount)
                session["homemsg"] = ""
                return redirect(url_for('home'))
            elif buyer_bal < price:
                session["homemsg"] = "Not enough coins"
                return redirect(url_for("home"))
            else:
                session["homemsg"] = f"{stock_owner} stock not enough..."
                return redirect(url_for("home"))

        except Exception as e:
            app.logger.error(e)
            return redirect(url_for("oops"))
    
    else:
        app.logger.warning("Wrong method")
        return redirect(url_for("oops"))

    
@app.route('/sell')
def sell():

    if request.method == "GET":

        try:

            form = request.args
            
            user = session["username"]
            stock_owner = form["user"]
            amount = int(form["amount"])
            earn = amount * get_user_info(stock_owner)["stock_value"]
            have = 0

            for stock in get_user_info(user)["stocks"]:
                if stock["name"] == stock_owner:
                    have = stock["amount"]
            
            if amount <= have:
                add_stock(user, stock_owner, -amount)
                add_bal(user, earn)
                session.pop("msmsg", None)
            
            else:
                session["msmsg"] = "You don't have so much stocks!"

            return redirect(url_for('mystocks'))


        except Exception as e:
            app.logger.error(e)
            return redirect(url_for("oops"))
    
    else:
        app.logger.warning("Wrong method")
        return redirect(url_for("oops"))


@app.route('/refresh')
def refresh():

    try:
        user = session["username"]
        info = get_user_info(user)
        last_refresh = info["last_refresh"]

        now = time.time()
        diff = now - last_refresh

        if diff > 10:

            set_to(user, "random_stocks", list(random_stocks()))
            set_to(user, "last_refresh", now)        

            session.pop("homemsg", None)

        else:
            session["homemsg"] = f"You still need to wait for {round(10-diff)} seconds to refresh"

        return redirect(url_for('home'))

    except Exception as error:
        app.logger.error(error)
        return redirect(url_for('login'))


@app.route('/claim')
def claim():

    try:
        user = session["username"]
        info = get_user_info(user)
        last_claim = info["last_claim"]

        now = time.time()
        diff = now - last_claim

        if diff > 60*60*24:

            add_bal(user, 100)
            set_to(user, "last_claim", now)

            session["homemsg"] = "Daily claimed!\nYou received 100 coins"
        
        else:
            diff = round(60*60*24-diff)

            hours = diff // 3600
            diff %= 3600

            minutes = diff // 60
            diff %= 60

            seconds = diff

            message_template = "You need to wait for {} to claim your daily"
            wait = []

            if hours:
                wait.append(f"{hours} hour{'s' if hours>1 else ''}")
            if minutes:
                wait.append(f"{minutes} minute{'s' if minutes>1 else ''}")
            if seconds:
                wait.append(f"{seconds} second{'s' if seconds>1 else ''}")

            session["homemsg"] = message_template.format(", ".join(wait))
        
        return redirect(url_for('home'))

    except KeyError:
        return redirect(url_for('login'))


# Error handling
@app.errorhandler(404)
def page_not_found(error):

    return render_template("page_not_found.html"), 404

if __name__ == "__main__":
    stock_task.start()
    app.run()