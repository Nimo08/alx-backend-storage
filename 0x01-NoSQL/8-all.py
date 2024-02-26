#!/usr/bin/env python3
"""8-all"""


from pymongo import MongoClient

client = MongoClient("localhost", 27017)
collection = client.my_db.mongo_collection


def list_all(mongo_collection):
    """
    Lists all documents in a collection
    Return an empty list if no document in the collection
    """
    docs = mongo_collection.find()
    if docs:
        return list(docs)
    else:
        return []


client.close()
