from pymongo import MongoClient
import os


db_url = os.environ["MONGO_URL"]
client = MongoClient(db_url)

