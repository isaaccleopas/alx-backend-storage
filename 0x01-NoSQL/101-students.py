#!/usr/bin/env python3
"""Returns all students sorted by average score"""

def top_students(mongo_collection):
    """
    The top must be ordered
    """
    result = mongo_collection.aggregate([
        {"$project": {
            "name": "$name",
            "averageScore": {"$avg": "$topics.score"}
        }},
        {"$sort": {"averageScore": -1}}
    ])
    return result
