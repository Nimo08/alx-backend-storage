#!/usr/bin/env python3
"""101-students"""


from pymongo import MongoClient


def top_students(mongo_collection):
    """Returns all students sorted by average score"""
    result = mongo_collection.aggregate([
        {
            "$project": {
                "name": "$name",
                "averageScore": {"$avg": "$topics.score"}
            }
        },
        {"$sort": {"averageScore": -1}}
    ])
    return result
