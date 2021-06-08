#!/usr/bin/env python

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
    'db_consumer': 'db_consumer',
}