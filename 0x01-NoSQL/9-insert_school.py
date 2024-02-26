#!/usr/bin/env python3
"""9-insert_school"""


from pymongo import MongoClient


client = MongoClient("localhost", 27017)
collection = client.my_db.mongo_collection


def insert_school(mongo_collection, **kwargs):
    """
    Inserts a new document in a collection based on kwargs
    """

    result = mongo_collection.insert_one(kwargs)

    return result.inserted_id


client.close()
