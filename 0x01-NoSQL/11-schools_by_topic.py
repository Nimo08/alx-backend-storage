#!/usr/bin/env python3
"""11-schools_by_topic"""


from pymongo import MongoClient


client = MongoClient("localhost", 27017)
collection = client.my_db.mongo_collection


def schools_by_topic(mongo_collection, topic):
    """
    Returns the list of school having a specific topic
    """
    return mongo_collection.find({"topics": topic})


client.close()
