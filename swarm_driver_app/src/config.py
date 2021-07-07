#!/usr/bin/env python
import os

# supported user actions
DEPLOY_ACTION = 'deploy'
REMOVE_ACTION = 'remove'
INSPECT_ACTION = 'inspect'

# states of requests
NEW_STATE = 'new'
DISPATCHED_STATE = 'dispatched'
PENDING_STATE = 'pending'
DEPLOYED_STATE = 'deployed'
FAILED_STATE = 'failed'
REMOVED_STATE = 'removed'

SWARM = 'swarm'
SWARM_DEPL_DIR = os.path.join(os.path.abspath(os.getcwd()), 'swarm_deployments')

kafka_cfg = {
    # kafka producer
    # local:
    #'bootstrap.servers': 'localhost:9092',
    # prod:
    'bootstrap.servers': '147.102.16.113:9092',

    # faust config
    # local: 
    #'broker': 'kafka://localhost:9092',
    # prod:
    'broker': 'kafka://147.102.16.113:9092',
    'version': 1,
    'project': 'ntua_diploma_thesis',
    'origin': 'src',

    # topic names
    'dispatcher': 'dispatcher',
    'resource_optimization_toolkit': 'resource_optimization_toolkit',
    'orchestrator': 'orchestrator',
    'swarm': 'swarm',
    'db_consumer': 'db_consumer',
}

mongodb_cfg = {
    'connection.uri': 'mongodb://athina_kyriakou:123@ntua-thesis-cluster-shard-00-00.xcgej.mongodb.net:27017,ntua-thesis-cluster-shard-00-01.xcgej.mongodb.net:27017,ntua-thesis-cluster-shard-00-02.xcgej.mongodb.net:27017/myFirstDatabase?ssl=true&replicaSet=atlas-xirr44-shard-0&authSource=admin&retryWrites=true&w=majority',
    'db_name': 'thesisdb',
    'db_collection': 'db_consumer',
}
