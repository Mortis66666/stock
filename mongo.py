from unittest import result
from pymongo import MongoClient
import os
from typing import Tuple, Union
import logging


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
        "stock_left": 100
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

def get_user_info(username: str) -> dict:
    
    result = profiles.find_one(
        filter = {
            "username": username
        }
    )

    return result