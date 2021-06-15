from faust_app import faust_app
from confluent_kafka import Producer
from src.config import kafka_cfg, DEPLOYED_STATE, FAILED_STATE
from src.models import DeploymentPlan, DatabaseRecord
from src.drivers.kubernetes import K8sDriver
from src.drivers.swarm import SwarmDriver
from src.utils.faust_helpers import record_to_string

#TODO: check that driver classes are singletons
kafka_conf = {
    'bootstrap.servers': kafka_cfg['bootstrap.servers'],
    'group.id': kafka_cfg['group.id'],
    'auto.offset.reset': kafka_cfg['auto.offset.reset']
    }

k8s_driver = K8sDriver(kubeconfig_yaml=kafka_cfg['kubeconfig_yaml'], kafka_conf=kafka_conf)
k8s_topic = faust_app.topic(kafka_cfg['kubernetes'], value_type=DeploymentPlan)

swarm_driver = SwarmDriver()
swarm_topic = faust_app.topic(kafka_cfg['swarm'], value_type=DeploymentPlan)

#TODO: implement k8s driver logic
@faust_app.agent(k8s_topic)
async def deploy_to_k8s(plans):
    p = Producer({'bootstrap.servers': kafka_cfg['bootstrap.servers']})
    async for plan in plans:
        print(f"Kubernetes Driver - data for requestUUID: {plan.requestUUID} received")
        # submit job to kubernetes
        ret = k8s_driver.deploy(dep_dict=plan.yamlSpec, namespace='default')
        # write to db_consumer topic - TODO: add and remove later a deployment/stack name label, add success code to config file
        print(type(ret))
        if(ret==201):
            db_rec = DatabaseRecord(requestUUID=plan.requestUUID, state=DEPLOYED_STATE, resource=None, yamlSpec=plan.yamlSpec, appID=None, appName=None)
        else:
            db_rec = DatabaseRecord(requestUUID=plan.requestUUID, state=FAILED_STATE, resource=None, yamlSpec=plan.yamlSpec, appID=None, appName=None)
        db_rec_str = record_to_string(db_rec)
        p.produce(topic=kafka_cfg['db_consumer'], value=db_rec_str)
        p.flush()

#TODO: implement swarm driver logic
@faust_app.agent(swarm_topic)
async def deploy_to_swarm(plans):
    p = Producer({'bootstrap.servers': kafka_cfg['bootstrap.servers']})
    async for plan in plans:
        print(f"Swarm Driver - data for requestUUID: {plan.requestUUID} received")
        #submit job to swarm
        ret = swarm_driver.deploy(dep_dict=plan.yamlSpec)
        # write to db_consumer topic - TODO: add and remove later a deployment/stack name label, add success code to config file
        if(ret==201):
            db_rec = DatabaseRecord(requestUUID=plan.requestUUID, state=DEPLOYED_STATE, resource=None, yamlSpec=plan.yamlSpec, appID=None, appName=None)
        else:
            db_rec = DatabaseRecord(requestUUID=plan.requestUUID, state=FAILED_STATE, resource=None, yamlSpec=plan.yamlSpec, appID=None, appName=None)
        db_rec_str = record_to_string(db_rec)
        p.produce(topic=kafka_cfg['db_consumer'], value=db_rec_str)
        p.flush()