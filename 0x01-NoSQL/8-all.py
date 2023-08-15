#!/usr/bin/env python3
"""Lists all documents in a collection."""

def list_all(mongo_collection):
    """Find all documents in the collection"""
    documents = list(mongo_collection.find({}))
    
    return documents
