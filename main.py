import sys
from drivers.kubernetes import KubernetesDriver

sys.path.append('.')

def main():
    print('\nInstantiating a K8s driver')
    k8s_driver = KubernetesDriver(kubeconfig_yaml='/home/athina/.kube/config')

    print('\nMake a deployment')
    k8s_driver.deploy(deployment_yaml='/home/athina/Desktop/thesis/code/ntua_diploma_thesis/nginx-deployment.yaml', namespace='default')

    print('Listing pods with their IPs')
    k8s_driver.get_pods(namespace = 'default')

if __name__ == '__main__':
    main()