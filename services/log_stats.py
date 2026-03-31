from .log_writer import logs_collection
from tabulate import tabulate

def format_params(params: dict):
    """ Convert a dictionary of parameters into a string like:
        key1=value1, key2=value2 """
    return ", ".join(f"{key}={value}" for key, value in params.items())


def get_unique_queries(limit=5):
    """ Get the most recent unique queries based on params.
        Groups by params and keeps the latest timestamp. """
    unique_query = [
        {"$sort": {"timestamp": -1}}, # Sort logs by newest first
        {"$group": {
            "_id": "$params", # Group by query parameters
            "last_time": {"$first": "$timestamp"}, # Take latest timestamp
            "type": {"$first": "$search_type"} # Take corresponding search type
        }},
        {"$sort": {"last_time": -1}}, # Sort again by latest time
        {"$limit": limit} # Limit number of results
    ]

    rows = []

    # Print section header
    print("\n" + "*" * 50)
    print("LAST QUERIES")
    print("*" * 50)

    # Execute aggregation and format results
    for i, query in enumerate(logs_collection.aggregate(unique_query), 1):
        rows.append([
            i,
            query["last_time"],
            query["type"],
            format_params(query["_id"]) # Format params dict into string
        ])
    # Print table
    print(tabulate(rows,headers=["#", "Last time", "Type", "Params"],tablefmt="fancy_grid"))



def get_stats_queries(limit=5):
    """ Get the most frequent queries based on params.
        Counts how many times each query appears. """
    stats_query = [
        {"$group": {"_id": "$params", "count": {"$sum": 1}}}, # Count occurrences
        {"$sort": {"count": -1}}, # Sort by most frequent
        {"$limit": limit} # Limit results
    ]

    rows = []

    print("\n" + "*" * 50)
    print("TOP QUERIES")
    print("*" * 50)

    # Execute aggregation and format results
    for i, query in enumerate(logs_collection.aggregate(stats_query), 1):
        rows.append([
            i,
            format_params(query["_id"]), # Convert params to string
            query["count"]
        ])

    print(tabulate(rows,headers=["#", "Params", "Count"],tablefmt="fancy_grid"))
