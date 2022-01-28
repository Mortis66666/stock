from hashlib import new
from pymongo import MongoClient
import os
from typing import Tuple, Union
import logging
from random import choices, randint
import time


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
        "last_claim": 0
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

def get_user_info(username: str) -> dict:
    
    result = profiles.find_one(
        filter = {
            "username": username
        }
    )

    return result

def random_stocks():

    stocks = list(profiles.find())
    stocks = filter(lambda stock:stock["stock_left"], stocks)

    ranstocks = choices(
        stocks,
        k = 5
    )

    return list(set(ranstocks))

def task():

    # Start changing stock value after 1 minute when the app starts

    time.sleep(60)

    while True:

        results = profiles.find()

        for result in results: # loop through every profile

            status = result["status"]
            streak = result["streak"]
            username = result["username"]
            
            new_status = None
            match status:

                case "inc":

                    new_status = choices(
                        population = [
                            "inc",
                            "dec",
                            "rem"
                        ],
                        weights = [
                            30 + streak,
                            20,
                            35
                        ]
                    )

                case "dec":

                    new_status = choices(
                        population = [
                            "inc",
                            "dec",
                            "rem"
                        ],
                        weights = [
                            20,
                            30 + streak,
                            35
                        ]
                    )

                case "rem":


                    new_status = choices(
                        population = [
                            "inc",
                            "dec",
                            "rem"
                        ],
                        weights = [
                            30,
                            30,
                            35 + streak
                        ]
                    )

                case None:

                    new_status = choices(
                        population = [
                            "inc",
                            "dec",
                            "rem"
                        ],
                        weights = [
                            30,
                            30,
                            35
                        ]
                    )
            amt = randint(1,3)
            match new_status:
                case "dec":
                    amt *= -1
                case "rem":
                    amt *= 0
            if status == new_status:
                add_streak(username, amt)
            else:
                add_streak(username,-streak)

            change_status(username, new_status)
            add_stock_value(username, amt)

        time.sleep(10) # 10 seconds delay after checking each stock



