from os import path
from pprint import pprint
import yaml
from kubernetes import client
from kubernetes.client import Configuration
from kubernetes.config import kube_config

SUCCESS = 'SUCCESS'
FAILURE = 'FAILURE'

class K8sDriver(object):
    
    #TODO: check if I need the kafka_conf
    def __init__(self, kubeconfig_yaml, kafka_conf):
        self.kubeconfig_yaml = kubeconfig_yaml
        self._kubeconfig_yaml = None
        # Kubernetes connector configuration setup
        self.k8s_connect = self.k8s_config
        print("K8sDriver - Kubernetes connector configuration:", self.k8s_connect)

    @property
    def k8s_config(self):
        try:
            with open(self.kubeconfig_yaml, 'r') as (f):
                if self._kubeconfig_yaml is None:
                    self._kubeconfig_yaml = yaml.safe_load(f)
                try: 
                    k8_loader = kube_config.KubeConfigLoader(self._kubeconfig_yaml)
                    call_config = type.__call__(Configuration)
                    k8_loader.load_and_set(call_config)
                    Configuration.set_default(call_config)
                    return(SUCCESS)
                except client.exceptions.ApiException as e:
                    print("K8sDriver - failure to connect to the Kubernetes cluster: %s" % e)
                    return(FAILURE)
        except IOError as err:
            print("K8sDriver - IOError:", err)
            return(FAILURE)

    def get_pods(self, namespace):
        core_v1 = client.CoreV1Api()
        api_response = core_v1.list_pod_for_all_namespaces(watch=False)
        #pprint(api_response)
        for i in api_response.items:
            if(i.metadata.namespace == namespace):
                print('%s\t%s\t%s' % (i.status.pod_ip, i.metadata.namespace, i.metadata.name))
    
    def deploy(self, dep_dict, namespace):
        apps_v1 = client.AppsV1Api()
        try:
            api_response = apps_v1.create_namespaced_deployment(body=dep_dict, namespace=namespace)
            #pprint(api_response)
            print("K8sDriver - deployment created with status='%s'" % api_response.metadata.name)
            return 201
        except client.exceptions.ApiException as e:
            print("K8sDriver - deployment exception: %s" % e)
            return 400