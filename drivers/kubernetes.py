from os import path
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

    #@property
    #def client(self):
    #    return client.CoreV1Api()
    def get_pods(self):
        CoreV1Api = client.CoreV1Api()
        ret = CoreV1Api.list_pod_for_all_namespaces(watch=False)
        for i in ret.items:
            print('%s\t%s\t%s' % (i.status.pod_ip, i.metadata.namespace, i.metadata.name))
    
    
    def deploy(self, deployment_yaml):
        with open(path.join(path.dirname(__file__), deployment_yaml)) as f:
            dep = yaml.safe_load(f)
            k8s_apps_v1 = client.AppsV1Api()
            resp = k8s_apps_v1.create_namespaced_deployment(body=dep, namespace="default")
            print("Deployment created. status='%s'" % resp.metadata.name)
