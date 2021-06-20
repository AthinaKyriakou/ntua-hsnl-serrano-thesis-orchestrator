from pymongo import MongoClient

def get_db_client(connection_uri, db_name):
    client = MongoClient(connection_uri)
    return client[db_name]

