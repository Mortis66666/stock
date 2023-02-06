import re
from pymongo import MongoClient
import os
from typing import Any, Tuple, Union
from random import choices
from iteration_utilities import unique_everseen


db_url = os.environ["MONGO_URL"]
client = MongoClient(db_url)

profiles = client.stocks.profiles

os.system("cls")


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
    elif len(username) > 15:
        return False, "Username cannot be more than 15 characters"
    elif not username.replace("_","").isalnum():
        return False, "Username can only contain alphabets, numbers and \"_\""
    elif password != confirm_password:
        return False, "Password must be the same"
    elif len(password) < 6:
        return False, "Password must be atleast 6 characters"
    elif "zhiheng" in username.replace("_", "").lower():
        return False, "Inappropriate username"




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
        "random_stocks": list(random_stocks()),
        "history": []
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


    for stock in stocks:
        if stock["name"] == stock_owner:
            stock["amount"] += amount
            break
    else:
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

def add_history(username, amt):

    profiles.update_one(
        {
            "username": username
        },
        {
            "$push": {
                "history": {
                    "$each": [ amt ],
                    "$slice": -100
                }
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

    return dict(**(result or {}))

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
    users = [*map(dict,profiles.find())]
    pairs = []

    for user in users:
        pairs.append([user["username"], get_net_worth(user["username"])])

    pairs.sort(key=lambda pair: -pair[1])

    return pairs

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
