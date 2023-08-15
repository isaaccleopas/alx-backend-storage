#!/usr/bin/env python3
"""
Script to display stats about Nginx logs stored in MongoDB.
"""

from pymongo import MongoClient

def get_logs_stats(collection):
    """Get the total number of logs"""
    total_logs = collection.count_documents({})

    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    method_stats = {}
    for method in methods:
        count = collection.count_documents({"method": method})
        method_stats[method] = count

    status_check_count = collection.count_documents({"method": "GET", "path": "/status"})

    return total_logs, method_stats, status_check_count
