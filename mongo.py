from pymongo import MongoClient
import os
from typing import Tuple, Union
import logging


db_url = os.environ["MONGO_URL"]
client = MongoClient(db_url)

collection = client.stocks.profile


def valid_login(username: str, password: str) -> Tuple[bool,str]:

    results = collection.find_one({
        "username": username,
        "password": password
    })

    if results is None:
        return False, "Incorrect username or password"
    else:
        return True, "Success"
    


def valid_signup(username: str, password: str, confirm_password: str) -> Tuple[bool,str]:
    
    if password != confirm_password:
        return False, "Password must be the same"
    if len(password) < 6:
        return False, "Password must be atleast 6 characters"
    


def get_bal(username: str) -> Union[int,None]:
    pass


def add_bal(username: str) -> None:
    pass

