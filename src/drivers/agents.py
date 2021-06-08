from faust_app import faust_app
from config import kafka_cfg
from src.models import DeploymentPlan
from src.drivers.kubernetes import K8sDriver

#TODO: read from config file, check that k8s driver class is singleton
kafka_conf = {
    'bootstrap.servers': kafka_cfg['bootstrap.servers'],
    'group.id': kafka_cfg['group.id'],
    'auto.offset.reset': kafka_cfg['auto.offset.reset']
    }
k8s_driver = K8sDriver(kubeconfig_yaml=kafka_cfg['kubeconfig_yaml'], kafka_conf=kafka_conf)
k8s_topic = faust_app.topic(kafka_cfg['kubernetes'], value_type=DeploymentPlan)

#TODO: implement k8s driver logic
@faust_app.agent(k8s_topic)
async def deploy_to_k8s(plans):
    async for p in plans:
        print(f"Kubernetes Driver - data for appUUID: {p.appUUID} received")
        print(type(p.payload))
        #submit job to kubernetes
        k8s_driver.deploy(dep_dict=p.payload, namespace=kafka_cfg['default'])