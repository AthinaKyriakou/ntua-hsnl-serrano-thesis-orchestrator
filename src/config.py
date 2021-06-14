#!/usr/bin/env python
import os

DEPLOY_ACTION = 'deploy'
TERMINATE_ACTION = 'terminate'
INSPECT_ACTION = 'inspect'

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