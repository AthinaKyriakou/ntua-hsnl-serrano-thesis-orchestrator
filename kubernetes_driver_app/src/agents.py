import faust
from faust_app import faust_app
from confluent_kafka import Producer
from config import kafka_cfg, DEPLOYED_STATE, FAILED_STATE, REMOVED_STATE, DEPLOY_ACTION, REMOVE_ACTION, K8s
from models import KubernetesRecord, DatabaseRecord
from kubernetes_driver import K8sDriver
from helpers import record_to_string
import datetime
import json

print('kubernetes_driver_app - agents - creating k8s driver')
k8s_topic = faust_app.topic(kafka_cfg['kubernetes'], value_type=KubernetesRecord)
k8s_driver = K8sDriver(kubeconfig_yaml=kafka_cfg['kubeconfig_yaml'])

@faust_app.agent(k8s_topic)
async def process_requests(requests):
    p = Producer({'bootstrap.servers': kafka_cfg['bootstrap.servers']})
    async for req in requests:
        
        if(req.action == DEPLOY_ACTION):
            print('kubernetes_driver_app - agents - data for requestUUID: %s received' % (req.requestUUID))
            ret = k8s_driver.deploy(dep_dict=req.yamlSpec, namespace=req.namespace)

            # write to db_consumer topic
            namespace = req.yamlSpec.get('namespace')
            name = req.yamlSpec.get('name')
            timestamp = json.dumps(datetime.datetime.now(), indent=4, sort_keys=True, default=str)
            
            if(ret==201):
                db_rec = DatabaseRecord(requestUUID=req.requestUUID, namespace=namespace, name=name, state=DEPLOYED_STATE, resource=K8s, yamlSpec=req.yamlSpec, timestamp=timestamp)
            else:
                db_rec = DatabaseRecord(requestUUID=req.requestUUID, namespace=namespace, name=name, state=FAILED_STATE, resource=K8s, yamlSpec=req.yamlSpec, timestamp=timestamp)
            db_rec_str = record_to_string(db_rec)
            p.produce(topic=kafka_cfg['db_consumer'], value=db_rec_str)
            p.flush()

        elif(req.action == REMOVE_ACTION):
            print('kubernetes_driver_app - agents - termination for requestUUID: %s received' % (req.requestUUID))
            ret = k8s_driver.delete_deployment(namespace=req.namespace, name=req.name)
            # write to db_consumer topic
            timestamp = json.dumps(datetime.datetime.now(), indent=4, sort_keys=True, default=str)
            if(ret == 201):
                db_rec = DatabaseRecord(requestUUID=req.requestUUID, namespace=req.namespace, name=req.name, state=REMOVED_STATE, resource=K8s, yamlSpec=req.yamlSpec, timestamp=timestamp)
                db_rec_str = record_to_string(db_rec)
                p.produce(topic=kafka_cfg['db_consumer'], value=db_rec_str)
                p.flush()
            else:
                print('kubernetes_driver_app - agents - termination for requestUUID: %s failed with return code: %s' % (req.requestUUID, ret))
        
        else:
            print('kubernetes_driver_app - agents - %s action not supported!' % req.action)