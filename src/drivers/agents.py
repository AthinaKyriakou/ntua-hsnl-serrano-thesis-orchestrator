from faust_app import faust_app
from src.models import DeploymentPlan
from src.drivers.kubernetes import K8sDriver

#TODO: read from config file, check that k8s driver class is singleton
kafka_conf = {'bootstrap.servers': "localhost:9092",'group.id': "ntua_diploma_thesis",'auto.offset.reset': "smallest"}
k8s_driver = K8sDriver(kubeconfig_yaml='/home/athina/.kube/config', kafka_conf=kafka_conf)
k8s_topic = faust_app.topic('kubernetes', value_type=DeploymentPlan)

#TODO: implement k8s driver logic
@faust_app.agent(k8s_topic)
async def deploy_to_k8s(plans):
    async for p in plans:
        print(f"Kubernetes Driver - data for appUUID: {p.appUUID} received")
        print(type(p.payload))
        #submit job to kubernetes
        k8s_driver.deploy(dep_dict=p.payload, namespace='default')