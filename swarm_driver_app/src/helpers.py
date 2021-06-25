import json
from pymongo import MongoClient
from config import DEPLOYED_STATE

PREFERRED = 'preferences'
IP = 'ip'

def get_db_client(connection_uri, db_name):
    client = MongoClient(connection_uri)
    return client[db_name]

def query_by_requestUUID(connection_uri, db_name, db_collection, requestUUID):
    db_client = get_db_client(connection_uri, db_name)
    db_collection = db_client[db_collection]
    return db_collection.find_one({'requestUUID': requestUUID})

def query_by_stack_name(connection_uri, db_name, db_collection, stack_name, resource):
    db_client = get_db_client(connection_uri, db_name)
    db_collection = db_client[db_collection]
    return db_collection.find_one({'name': stack_name, 'resource': resource, 'state': DEPLOYED_STATE})

def record_to_string(rec):
    rec_dict = vars(rec)
    rec_dict.pop('__evaluated_fields__', None)
    rec_str = json.dumps(rec_dict)
    return rec_str

def remove_added_labels(yamlSpec):
    yamlSpec.pop('name')
    yamlSpec.pop('orchestrator')
    return yamlSpec

#def add_placement_specs(spec, key, value, type):
    # TODO: write