#!/usr/bin/env python
import os

# supported user actions
DEPLOY_ACTION = 'deploy'
TERMINATE_ACTION = 'terminate'
INSPECT_ACTION = 'inspect'

# states of requests
NEW_STATE = 'new'
DISPATCHED_STATE = 'dispatched'

SWARM = 'swarm'
SWARM_DEPL_DIR = os.path.join(os.path.abspath(os.getcwd()), 'swarm_deployments')

K8s = 'k8s'

kafka_cfg = {
    # kafka producer, k8s driver
    'bootstrap.servers': 'localhost:9092',
    'kubeconfig_yaml': '/home/athina/.kube/config',
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
    'autodiscover': ['drivers', 'orchestrator',],

    # topic names
    'dispatcher': 'dispatcher',
    'resource_optimization_toolkit': 'resource_optimization_toolkit',
    'orchestrator': 'orchestrator',
    'kubernetes': 'kubernetes',
    'swarm': 'swarm',
    'db_consumer': 'db_consumer',
}