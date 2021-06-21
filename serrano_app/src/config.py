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
K8s = 'k8s'

flask_cfg = {
    'endpoint_local': 'http://127.0.0.1:5000',
    'endpoint_prod': 'http://147.102.16.113:5000',
}

kafka_cfg = {
    # kafka producer, k8s driver
    'bootstrap.servers': 'localhost:9092',
    # for local: 
    'kubeconfig_yaml': '/home/athina/.kube/config',
    # for prod:
    #'kubeconfig_yaml': '/home/serrano/.kube/config',
    'group.id': 'ntua_diploma_thesis',
    'auto.offset.reset': 'smallest',
    'namespace': ['default'],

    # schema registry
    'schema.registry.url': 'localhost:8081',
    'schema_file_path': '/home/athina/Desktop/thesis/code/ntua_diploma_thesis/src/avro/Deployment.avsc',

    # faust config
    'broker': 'kafka://localhost:9092',
    'version': 1,
    'project': 'ntua_diploma_thesis',
    'origin': 'src',
    'autodiscover': ['dispatcher', 'resource_optimization_toolkit', 'orchestrator',],

    # topic names
    'dispatcher': 'dispatcher',
    'resource_optimization_toolkit': 'resource_optimization_toolkit',
    'orchestrator': 'orchestrator',
    'kubernetes': 'kubernetes',
    'swarm': 'swarm',
    'db_consumer': 'db_consumer',
}

mongodb_cfg = {
    'connection.uri': 'mongodb://athina_kyriakou:123@ntua-thesis-cluster-shard-00-00.xcgej.mongodb.net:27017,ntua-thesis-cluster-shard-00-01.xcgej.mongodb.net:27017,ntua-thesis-cluster-shard-00-02.xcgej.mongodb.net:27017/myFirstDatabase?ssl=true&replicaSet=atlas-xirr44-shard-0&authSource=admin&retryWrites=true&w=majority',
    'db_name': 'thesisdb',
    'db_collection': 'db_consumer',
}