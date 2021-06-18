#!/usr/bin/env python
import os

# supported user actions
DEPLOY_ACTION = 'deploy'
TERMINATE_ACTION = 'terminate'
INSPECT_ACTION = 'inspect'

# states of requests
NEW_STATE = 'new'
DISPATCHED_STATE = 'dispatched'
PENDING_STATE = 'pending'
DEPLOYED_STATE = 'deployed'
FAILED_STATE = 'failed'

SWARM = 'swarm'
SWARM_DEPL_DIR = os.path.join(os.path.abspath(os.getcwd()), 'swarm_deployments')

kafka_cfg = {
    # kafka producer
    # local:
    # 'bootstrap.servers': 'localhost:9092',
    # prod:
    'bootstrap.servers': '147.102.16.113:9092',

    # faust config
    # local: 
    # 'broker': 'kafka://localhost:9092',
    # prod:
    'broker': 'kafka://147.102.16.113:9092',
    'version': 1,
    'project': 'ntua_diploma_thesis',
    'origin': 'src',

    # topic names
    'dispatcher': 'dispatcher',
    'resource_optimization_toolkit': 'resource_optimization_toolkit',
    'orchestrator': 'orchestrator',
    'kubernetes': 'kubernetes',
    'swarm': 'swarm',
    'db_consumer': 'db_consumer',
}