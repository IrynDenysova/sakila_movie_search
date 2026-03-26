from log_writer import logs_collection

from tabulate import tabulate

def format_params(params: dict):
    return ", ".join(f"{key}={value}" for key, value in params.items())


def get_unique_queries(limit=5):
    unique_query = [
        {"$sort": {"timestamp": 1}},
        {"$group": {
            "_id": "$params",
            "last_time": {"$first": "$timestamp"},
            "type": {"$first": "$search_type"}
        }},
        {"$sort": {"last_time": 1}},
        {"$limit": limit}
    ]

    rows = []

    print("\n" + "*" * 50)
    print("LAST QUERIES")
    print("*" * 50)

    for i, query in enumerate(logs_collection.aggregate(unique_query), 1):
        rows.append([
            i,
            query["last_time"],
            query["type"],
            format_params(query["_id"])
        ])

    print(tabulate(rows,headers=["#", "Last time", "Type", "Params"],tablefmt="grid"))



def get_stats_queries(limit=5):
    stats_query = [
        {"$group": {"_id": "$params", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": limit}
    ]

    rows = []

    print("\n" + "*" * 50)
    print("TOP QUERIES")
    print("*" * 50)


    for i, query in enumerate(logs_collection.aggregate(stats_query), 1):
        rows.append([
            i,
            format_params(query["_id"]),
            query["count"]
        ])

    print(tabulate(rows,headers=["#", "Params", "Count"],tablefmt="grid"))
