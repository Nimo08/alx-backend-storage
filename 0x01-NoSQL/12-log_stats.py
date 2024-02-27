#!/usr/bin/env python3
"""
Provides some stats about Nginx logs stored in MongoDB
"""


from pymongo import MongoClient


client = MongoClient("localhost", 27017)
db = client.logs
collection = db.nginx

total_logs = collection.nginx.count_documents({})

if __name__ == "__main__":
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    method_count = {}
    for method in methods:
        method_count[method] = collection.count_documents({"method": method})
    status_check_count = collection.count_documents({"method": "GET",
                                                    "path": "/status"})
    print(f"{total_logs} logs")
    print("Methods:")
    for method, count in method_count.items():
        print(f"    method {method}: {count}")
    print(f"{status_check_count} status check")


client.close()
