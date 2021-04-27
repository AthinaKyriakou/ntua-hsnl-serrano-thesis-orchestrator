from os import path
from pprint import pprint
import yaml
from kubernetes import client, config
from kubernetes.client import Configuration
from kubernetes.config import kube_config

class KubernetesDriver(object):
    
    def __init__(self, kubeconfig_yaml):
        self.kubeconfig_yaml = kubeconfig_yaml
        self._kubeconfig_yaml = None
        
        # configuration setup
        k8_loader = kube_config.KubeConfigLoader(self.config)
        call_config = type.__call__(Configuration)
        k8_loader.load_and_set(call_config)
        Configuration.set_default(call_config)

    @property
    def config(self):
        with open(self.kubeconfig_yaml, 'r') as f:
            if self._kubeconfig_yaml is None:
                self._kubeconfig_yaml = yaml.safe_load(f)
        return self._kubeconfig_yaml

    def get_pods(self, namespace):
        core_v1 = client.CoreV1Api()
        pods = core_v1.list_pod_for_all_namespaces(watch=False)
        for i in pods.items:
            if(i.metadata.namespace == namespace):
                print('%s\t%s\t%s' % (i.status.pod_ip, i.metadata.namespace, i.metadata.name))
    
    
    def deploy(self, deployment_yaml, namespace):
        with open(path.join(path.dirname(__file__), deployment_yaml)) as f:
            dep = yaml.safe_load(f)
            apps_v1 = client.AppsV1Api()
            try:
                api_response = apps_v1.create_namespaced_deployment(body=dep, namespace=namespace)
                pprint(api_response)
                #print("Deployment created. status='%s'" % resp.metadata.name)
            except client.exceptions.ApiException as e:
                print("Deployment exception: %s" % e)