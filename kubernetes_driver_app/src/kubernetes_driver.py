from os import path
from pprint import pprint
import yaml
from kubernetes import client
from kubernetes.client import Configuration
from kubernetes.config import kube_config
from helpers import add_node_affinity
import copy
import ast

SUCCESS = 'SUCCESS'
FAILURE = 'FAILURE'
PREFERRED = 'preferredDuringSchedulingIgnoredDuringExecution'
IN_OPP = 'In'
IP = 'ip'

class K8sDriver(object):
    
    def __init__(self, kubeconfig_yaml):
        self.kubeconfig_yaml = kubeconfig_yaml
        self._kubeconfig_yaml = None
        # Kubernetes connector configuration setup
        self.k8s_connect = self.k8s_config
        print('K8sDriver - Kubernetes connector configuration:', self.k8s_connect)

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
                    print('K8sDriver - failure to connect to the Kubernetes cluster: %s' % e)
                    return(FAILURE)
        except IOError as err:
            print('K8sDriver - IOError:', err)
            return(FAILURE)

    def get_pods(self, namespace):
        core_v1 = client.CoreV1Api()
        api_response = core_v1.list_pod_for_all_namespaces(watch=False)
        #pprint(api_response)
        for i in api_response.items:
            if(i.metadata.namespace == namespace):
                print('%s\t%s\t%s' % (i.status.pod_ip, i.metadata.namespace, i.metadata.name))
    
    
    def check_if_namespace_exists(self, namespace):
        core_v1 = client.CoreV1Api()
        namespace_list = core_v1.list_namespace()
        for n in namespace_list.items:
            name = n.metadata.name
            if(name == namespace):
                return True
        return False


    def deploy(self, dep_dict, namespace):
        core_v1 = client.CoreV1Api()
        apps_v1 = client.AppsV1Api()
        try:
            # create namespace, if it does not exist
            if(not self.check_if_namespace_exists(namespace)):
                api_response = core_v1.create_namespace(client.V1Namespace(metadata=client.V1ObjectMeta(name=namespace)))
                print('K8sDriver - namespace %s created with status=%s' % (namespace, api_response.metadata.name))
            else:
                print('K8sDriver - namespace %s exists' % namespace)

            k8s_services = dep_dict['spec']['services']
            k8s_deployments = dep_dict['spec']['deployments']
            comp_preferences = dep_dict['comp_preferences']

            # configure the labels in the deployments
            for dep, info in k8s_deployments.items():
                yamlSpec = info['yamlSpec']
                nodeIP = comp_preferences[dep]
                info['yamlSpec'] = add_node_affinity(copy.deepcopy(yamlSpec), IP, nodeIP, IN_OPP, PREFERRED, 100)

            # create the services
            for s, info in k8s_services.items():
                service_dict = info['yamlSpec']
                api_response = core_v1.create_namespaced_service(body=service_dict, namespace=namespace)
                print('K8sDriver - service %s created with status=%s' % (s, api_response.metadata.name))

            # create the deployments
            for d, info in k8s_deployments.items():
                dep_dict = info['yamlSpec']
                api_response = apps_v1.create_namespaced_deployment(body=dep_dict, namespace=namespace)
                print('K8sDriver - deployment %s created with status=%s' % (d, api_response.metadata.name))
            
            return 201
        except client.exceptions.ApiException as e:
            print('K8sDriver - deployment exception: %s' % e)
            return 400

    def remove(self, app_name, namespace, serv_dict, dep_dict):
        core_v1 = client.CoreV1Api()
        apps_v1 = client.AppsV1Api()
        try:
            # delete services by name and namespace
            for s, info in serv_dict.items():
                api_response = core_v1.delete_namespaced_service(name=s, namespace=namespace)
                #pprint(api_response)

            # delete deployments by name and namespace
            for dep, info in dep_dict.items():
                api_response = apps_v1.delete_namespaced_deployment(name=dep, namespace=namespace)
                #pprint(api_response)

            return 201
        except client.exceptions.ApiException as e:
            print('K8sDriver - termination of %s exception: %s' % (app_name, e))
            return 400


    
