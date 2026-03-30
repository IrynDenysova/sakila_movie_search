from pymongo import MongoClient, errors
from datetime import datetime
import os
from dotenv import load_dotenv
load_dotenv()


mongo_collection = os.getenv("MONGO_COLLECTION")
client = MongoClient(os.getenv("MONGO_URI"),
serverSelectionTimeoutMS=5000)

logs_collection = client[os.getenv("MONGO_DB_NAME")][mongo_collection]


def log_film(search_type, params, count):

    try:
        logs_collection.insert_one({
                "timestamp": datetime.now(),
                "search_type": search_type,
                "params": params,
                "results_count": count
                    })
    except errors.ConnectionFailure:
        print("Connection Failure")
    except errors.ServerSelectionTimeoutError:
        print("Server Selection Timeout")
    except errors.PyMongoError:
        print("PyMongo Error")

