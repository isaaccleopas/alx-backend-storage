#!/usr/bin/env python3
"""Returns the list of school having a specific topic."""

def schools_by_topic(mongo_collection, topic):
    """Returns topic searched"""
    searched_topic = mongo_collection.find({"topic": topic})

    return searched_topic
