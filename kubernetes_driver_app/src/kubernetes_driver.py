from os import path
from pprint import pprint
import yaml
from kubernetes import client
from kubernetes.client import Configuration
from kubernetes.config import kube_config
from helpers import add_node_affinity
import copy

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
    
    def deploy(self, dep_dict, namespace):
        # TODO: select spec file to keep, add preference labels if specified, create each service & deployment
        core_v1 = client.CoreV1Api()
        apps_v1 = client.AppsV1Api()
        try:
            # create namespace
            api_response = core_v1.create_namespace(client.V1Namespace(metadata=client.V1ObjectMeta(name=namespace)))
            print('K8sDriver - namespace %s created with status=%s' % (namespace, api_response.metadata.name))

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

    # delete deployment by name and namespace
    def delete_deployment(self, namespace, name):
        apps_v1 = client.AppsV1Api()
        try:
            print('K8s Driver namespace: %s, name: %s' %(namespace, name))
            api_response = apps_v1.delete_namespaced_deployment(name=name, namespace=namespace)
            #pprint(api_response)
            return 201
        except client.exceptions.ApiException as e:
            print('K8sDriver - termination of %s exception: %s' % (name, e))
            return 400
