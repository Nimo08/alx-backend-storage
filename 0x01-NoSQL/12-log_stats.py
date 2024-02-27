#!/usr/bin/env python3
"""
Provides some stats about Nginx logs stored in MongoDB
"""


from pymongo import MongoClient


if __name__ == "__main__":
    client = MongoClient("localhost", 27017)
    collection = client.logs.nginx

    total_logs = collection.nginx.count_documents({})
    print(f"{total_logs} logs")
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    print("Methods:")
    for method in methods:
        result = collection.nginx.count_documents({"method": method})
        print(f"\tmethod {method}: {result}")
        status_check_count = collection.count_documents({"method": "GET",
                                                        "path": "/status"})
    print(f"{status_check_count} status check")
