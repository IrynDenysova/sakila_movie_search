import pymongo
from datetime import datetime
from pymongo import MongoClient, errors
import os
from dotenv import load_dotenv
load_dotenv()



mongo_collection = os.getenv("MONGO_COLLECTION")
client = MongoClient(os.getenv("MONGO_URI"),
serverSelectionTimeoutMS=5000)

logs_collection = client[os.getenv("MONGO_DB_NAME")][mongo_collection]


def log_film(search_type, params, count):
    """ Save information about a search request into MongoDB.
        :param search_type: Type of search (e.g., 'keyword', 'rating', etc.)
        :param params: Dictionary of search parameters
        :param count: Number of results returned """

    try:
        # Insert a new document into the logs collection
        logs_collection.insert_one({
                # Current date and time of the request
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                # Type/category of the search
                "search_type": search_type, 
                # Search parameters (stored as a dictionary)
                "params": params,   
                # Number of results found
                "results_count": count  
                    })
    # Handle connection-related errors
    except errors.ConnectionFailure:
        print("Connection Failure") # Raised when DB connection is lost
    # Handle server timeout errors
    except errors.ServerSelectionTimeoutError:
        print("Server Selection Timeout") # Server not reachable in time
    # Handle any other PyMongo-related errors
    except errors.PyMongoError:
        print("PyMongo Error")

