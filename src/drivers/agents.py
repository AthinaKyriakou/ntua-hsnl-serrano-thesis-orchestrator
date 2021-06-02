from faust_app import faust_app
import yaml
from src.orchestrator.models import OrchestratorPlan
from src.drivers.kubernetes import K8sDriver

#TODO: read from config file
kafka_conf = {'bootstrap.servers': "localhost:9092",'group.id': "foo",'auto.offset.reset': "smallest"}
k8s_driver = K8sDriver(kubeconfig_yaml='/home/athina/.kube/config', kafka_conf=kafka_conf)
k8s_topic = faust_app.topic('kubernetes', value_type=OrchestratorPlan)

@faust_app.agent(k8s_topic)
async def deploy_to_k8s(plans):
    async for p in plans:
        print(f"appUUID: {p.appUUID}, serviceUUID: {p.serviceUUID}")
        #print(p.plan)
        #print(type(p.plan))
        #submit job to kubernetes
        k8s_driver.deploy(dep_dict=p.plan, namespace='default')