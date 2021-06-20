from pymongo import MongoClient

def get_db_client(connection_uri, db_name):
    client = MongoClient(connection_uri)
    return client[db_name]


def query_by_requestUUID(connection_uri, db_name, db_collection, requestUUID):
    db_client = get_db_client(connection_uri, db_name)
    db_collection = db_client[db_collection]
    return db_collection.find_one({'requestUUID': requestUUID})

