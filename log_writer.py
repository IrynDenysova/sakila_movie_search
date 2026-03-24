from itertools import count

from pymongo import MongoClient
from datetime import datetime


mongo_collection = "final_project_101025-ptm-Iryna_Denysova"

client = MongoClient("mongodb://ich_editor:verystrongpassword@mongo.itcareerhub.de/?"
                     "readPreference=primary&ssl=false&authMechanism=DEFAULT&authSource=ich_edit")

logs_collection = client["ich_edit"][mongo_collection]

def log_film(search_type,info, count):
    logs_collection.insert_one({
            "timestamp": datetime.now(),
            "search_type": search_type,
            "params": {
            "query": info
            },
            "results_count": count
            })
