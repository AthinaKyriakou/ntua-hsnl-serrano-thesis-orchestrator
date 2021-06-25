import json
from pymongo import MongoClient

PREFERRED = 'preferredDuringSchedulingIgnoredDuringExecution'
IN_OPP = 'In'

def get_db_client(connection_uri, db_name):
    client = MongoClient(connection_uri)
    return client[db_name]

def query_by_requestUUID(connection_uri, db_name, db_collection, requestUUID):
    db_client = get_db_client(connection_uri, db_name)
    db_collection = db_client[db_collection]
    return db_collection.find_one({'requestUUID': requestUUID})

def record_to_string(rec):
    rec_dict = vars(rec)
    rec_dict.pop('__evaluated_fields__', None)
    rec_str = json.dumps(rec_dict)
    return rec_str

def add_node_affinity(yamlSpec, key, value, operator, type, weight=1):
    # location in yamlSpec: ['spec']['template']['spec']
    yamlSpec['spec']['template']['spec']['affinity'] = {}
    yamlSpec['spec']['template']['spec']['affinity']['nodeAffinity'] = {}

    preferred_dict = {}
    if(type == PREFERRED):
        yamlSpec['spec']['template']['spec']['affinity']['nodeAffinity'][PREFERRED] = []
        preferred_dict['weight'] = weight 

    preference_dict = {}
    preference_dict['matchExpressions'] = []
    
    match_expressions_dict = {}
    match_expressions_dict['key'] = key
    if(operator == IN_OPP):
        match_expressions_dict['operator'] = IN_OPP
    match_expressions_dict['values'] = [value]

    preference_dict['matchExpressions'].append(match_expressions_dict)

    preferred_dict['preference'] = preference_dict
    yamlSpec['spec']['template']['spec']['affinity']['nodeAffinity'][PREFERRED].append(preferred_dict)
    return yamlSpec

