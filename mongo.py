import re
from pymongo import MongoClient
import os
from typing import Any, Tuple, Union
import logging
from random import choices, randint
import time
from iteration_utilities import unique_everseen


db_url = os.environ["MONGO_URL"]
client = MongoClient(db_url)

profiles = client.stocks.profiles


def valid_login(username: str, password: str) -> Tuple[bool,str]:

    results = profiles.find_one({
        "username": username,
        "password": password
    })

    if results is None:
        return False, "Incorrect username or password"
    else:
        return True, "Success"
    


def valid_signup(username: str, password: str, confirm_password: str) -> Tuple[bool,str]:

    if len(username) < 6:
        return False, "Username must have at least 4 characters"    
    if len(username) > 15:
        return False, "Username cannot be more than 15 characters"
    if not username.replace("_","").isalnum():
        return False, "Username can only contain alphabets, numbers and \"_\""
    if password != confirm_password:
        return False, "Password must be the same"
    if len(password) < 6:
        return False, "Password must be atleast 6 characters"




    result = profiles.count_documents(
        filter = {
            "username": username
        }
    )

    if result:
        return False, "Username already taken"

    return True, "Success"


def sign_up(username, password):

    post = {
        "username": username,
        "password": password,
        "coins": 100,
        "stocks": [],
        "stock_value": 50,
        "status": None,
        "streak": 0,
        "stock_left": 100,
        "last_refresh": 0,
        "last_claim": 0,
        "random_stocks": list(random_stocks())
    }

    profiles.insert_one(post)

    


def get_bal(username: str) -> Union[int,None]:
    result = profiles.find_one(
        filter = {
            "username": username
        }
    )

    if result is None:
        return result
    else:
        return result["coins"]


def add_bal(username: str, amount: int) -> None:
    profiles.update_one(
        filter = {
            "username": username
        },
        update = {
            "$inc": {
                "coins": amount
            }
        }
    )

def add_stock_value(username: str, amount: int) -> None:
    profiles.update_one(
        filter = {
            "username": username
        },
        update = {
            "$inc": {
                "stock_value": amount
            }
        }
    )

def add_streak(username: str, amount: int) -> None:
    profiles.update_one(
        filter = {
            "username": username
        },
        update = {
            "$inc": {
                "streak": amount
            }
        }
    )

def add_stock(buyer: str, stock_owner: str, amount: int) -> None:

    buyer_info = get_user_info(buyer)
    stocks = list(buyer_info["stocks"])

    inserted = False

    for stock in stocks:
        if stock["name"] == stock_owner:
            stock["amount"] += amount
            inserted = True
            break
    
    if not inserted:
        stocks.append(
            {
                "name": stock_owner,
                "amount": amount
            }
        )

    set_to(buyer, "stocks", stocks)

    profiles.update_one(
        {
            "username": stock_owner
        },
        {
            "$inc": {
                "stock_left": -amount
            }
        }
    )

def change_status(username: str, new_status: str) -> None:
    profiles.update_one(
        filter = {
            "username": username
        },
        update = {
            "$set": {
                "status": new_status
            }
        }
    )

def set_to(username: str, key: str, value: Any) -> int:
    res =  profiles.update_one(
        {
            "username": username
        },
        {
            "$set": {
                key: value
            }
        }
    )

    return res.matched_count

def get_user_info(username: str) -> dict:
    
    result = profiles.find_one(
        filter = {
            "username": username
        }
    )

    return dict(**result)

def random_stocks():

    stocks = list(profiles.find())
    stocks = list(filter(lambda stock:stock["stock_left"], stocks))

    ranstocks = choices(
        stocks,
        k = 5
    )

    for random_stock in unique_everseen(ranstocks):
        yield random_stock["username"]

def get_net_worth(username: str) -> int:
    
    info = get_user_info(username)
    bal = info["coins"]
    stocks = info["stocks"]

    for stock in stocks:
        stock_owner = stock["name"]
        amount = stock["amount"]

        value = get_user_info(stock_owner)["stock_value"]
        worth = value * amount

        bal += worth

    return bal

def get_top() -> list:

    leaderboard = []

    users = [*map(dict,profiles.find())]
    users.sort(key=lambda x:get_net_worth(x["username"]), reverse=True)

    for n, user in enumerate(users,1):
        if n == 11:
            break
        else:
            leaderboard.append([user["username"],get_net_worth(user["username"])])

    return leaderboard

def get_stocks():

    for stock in profiles.find():
        yield {
            "username": stock["username"],
            "stock_value": stock["stock_value"]
        }

def search_for(username):

    return profiles.find(
        {
            "username": re.compile(
                username, re.IGNORECASE
            )
        },
        {
            "username": 1,
            "stock_value": 1
        }
    )


def task():

    # Start changing stock value after 1 minute when the app starts

    logging.warn("Task started!")
    time.sleep(60)

    while True:

        results = profiles.find()

        for result in results: # loop through every profile

            status = result["status"]
            streak = result["streak"]
            username = result["username"]
            stock_left = result["stock_left"]
            stock_value = result["stock_value"]
            
            new_status = None

            bonus = 0

            for x in profiles.find():
                for xstock in x["stocks"]:
                    if xstock["name"] == username and xstock["amount"]:
                        bonus += 1

            match status:

                case "inc":

                    new_status = choices(
                        population = [
                            "inc",
                            "dec",
                            "rem"
                        ],
                        weights = [
                            30 + streak + bonus,
                            25 + stock_left/100,
                            35
                        ]
                    )[0]

                case "dec":

                    new_status = choices(
                        population = [
                            "inc",
                            "dec",
                            "rem"
                        ],
                        weights = [
                            25 + bonus,
                            30 + streak + stock_left/100,
                            35
                        ]
                    )[0]

                case "rem":


                    new_status = choices(
                        population = [
                            "inc",
                            "dec",
                            "rem"
                        ],
                        weights = [
                            30 + bonus,
                            30 + stock_left/100,
                            40 + streak
                        ]
                    )[0]

                case None:

                    new_status = choices(
                        population = [
                            "inc",
                            "dec",
                            "rem"
                        ],
                        weights = [
                            30 + bonus,
                            30 + stock_left/100,
                            40
                        ]
                    )[0]
            amt = randint(1,3)
            match new_status:
                case "dec":
                    amt *= -1
                case "rem":
                    amt *= 0
            if status == new_status:
                add_streak(username, 1)
            else:
                add_streak(username,-streak)

            if -amt > stock_value:
                amt = -stock_value

            change_status(username, new_status)
            add_stock_value(username, amt)

            print(f"{username} status: {status} -> {new_status}")
            print(f"{username} stock price: {stock_value} -> {stock_value+amt}")

            stocks = list(result["stocks"])

            for stock in stocks:
                if not stock["amount"]:
                    stocks.remove(stock)
                    print(f"Removed {stock['name']} from {username}")
            
            set_to(username, "stocks", stocks)

        time.sleep(10) # 10 seconds delay after checking each stock
