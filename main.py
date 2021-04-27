import sys
from drivers.kubernetes import KubernetesDriver

sys.path.append('.')

def main():
    print('Instantiating a K8s driver')
    k8s_driver = KubernetesDriver(kubeconfig_yaml='/home/athina/.kube/config')

    print('Make a deployment')

    print('Listing pods with their IPs:')
    k8s_driver.get_pods()

if __name__ == '__main__':
    main()