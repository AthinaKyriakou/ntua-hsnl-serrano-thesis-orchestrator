import sys
from confluent_kafka import Producer
from drivers.kubernetes import K8sDriver

sys.path.append('.')

def main():

    # Kafka configuration for local development
    
    #TODO: read from config file
    kafka_conf = {'bootstrap.servers': "localhost:9092",
            'group.id': "foo", 
            'auto.offset.reset': "smallest"}

    #dummy producer
    p = Producer({'bootstrap.servers': "localhost:9092"})
    dummy_source = ['1', '2', '3', '4']
    for data in dummy_source:
        p.produce('kdriver', data.encode('utf-8'))

    print('\nInstantiating a K8s driver')
    k8s_driver = K8sDriver(kubeconfig_yaml='/home/athina/.kube/config', kafka_conf=kafka_conf, consumer_topics=['kdriver'])

    print('\nListing pods with their IPs')
    #k8s_driver.get_pods(namespace = 'default')

    print('\nMake a deployment')
    #k8s_driver.deploy(deployment_yaml='/home/athina/Desktop/thesis/code/ntua_diploma_thesis/nginx-deployment.yaml', namespace='default')

if __name__ == '__main__':
    main()