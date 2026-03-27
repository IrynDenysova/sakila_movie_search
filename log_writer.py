from pymongo import MongoClient
from datetime import datetime
import os
from dotenv import load_dotenv
load_dotenv()


mongo_collection = os.getenv("MONGO_COLLECTION")
client = MongoClient(os.getenv("MONGO_URI"))
logs_collection = client[os.getenv("MONGO_DB_NAME")][mongo_collection]


def log_film(search_type, params, count):
    logs_collection.insert_one({
            "timestamp": datetime.now(),
            "search_type": search_type,
            "params": params,
            "results_count": count
            })
