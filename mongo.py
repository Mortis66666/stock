from pymongo import MongoClient
import os
from typing import List, Union
import logging


db_url = os.environ["MONGO_URL"]
raise TypeError(db_url)
client = MongoClient(db_url)

collection = client.stocks.profile


def valid_login(username: str, password: str) -> List[bool,str]:

    results = collection.find_one({
        "username": username,
        "password": password
    })

    if results is None:
        return False, "Incorrect username or password"
    else:
        return True, "Success"
    


def valid_signup(username: str, password: str, confirm_password: str) -> List[bool,str]:
    pass


def get_bal(username: str) -> Union[int,None]:
    pass


def add_bal(username: str) -> None:
    pass

