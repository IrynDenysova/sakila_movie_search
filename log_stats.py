from log_writer import logs_collection


def get_unique_queries(limit=5):
    unique_queries = [
            {"$sort": {"timestamp": 1}},
            {"$group": {"_id": "$params",
                "last_time": {"$first": "$timestamp"},
                "type": {"$first": "$search_type"}} },
            {"$sort": {"last_time": 1}},
            {"$limit": limit}]
    print("--- Last queries ---")
    for id, query in enumerate(logs_collection.aggregate(unique_queries),1):
        print(f"{id}.{query["last_time"]} Type: {query["type"]} | Parameters: {query["_id"]}")


def get_stats_queries(limit=5):
    stats_queries = [
            {"$group":{"_id": "$params", "count": {"$sum":1}}},
            {"$sort": {"count":-1}},
            {"$limit": limit}
    ]

    print("--- Last 5 queries ---")
    for id, query in enumerate(logs_collection.aggregate(stats_queries),1):
        print(f"{id}. {query["_id"]} {query["count"]} time(s)")