from os import path
from pprint import pprint
import yaml
from confluent_kafka import Consumer, KafkaException, KafkaError
from kubernetes import client, config
from kubernetes.client import Configuration
from kubernetes.config import kube_config

SUCCESS = 'SUCCESS'
FAILURE = 'FAILURE'

class K8sDriver(object):
    
    def __init__(self, kubeconfig_yaml, kafka_conf, consumer_topics):
        self.kubeconfig_yaml = kubeconfig_yaml
        self._kubeconfig_yaml = None

        # Kubernetes connector configuration setup
        self.k8s_connect = self.k8s_config
        print("Kubernetes connector configuration:", self.k8s_connect)

        #Kafka consumer loop
        #consumer not thread safe
        if(self.k8s_connect == SUCCESS):
            self.consumer = Consumer(kafka_conf)
            self.consumer_topics = consumer_topics
            self.consume_loop


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
                    print("Failure to connect to the Kubernetes cluster: %s" % e)
                    return(FAILURE)
        except IOError as err:
            print("IOError:", err)
            return(FAILURE)

    @property
    #dummy consuming loop
    def consume_loop(self):
        try:
            self.consumer.subscribe(self.consumer_topics)
            while True:
                #print("Waiting for a message from kdriver topic...")
                msg = self.consumer.poll(timeout=1.0)
                if msg is None: continue
                if msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        # End of partition event
                        sys.stderr.write('%% %s [%d] reached end at offset %d\n' %
                                        (msg.topic(), msg.partition(), msg.offset()))
                    elif msg.error():
                        raise KafkaException(msg.error())
                else:
                    #msg_process(msg)
                    print(msg)
        except KafkaException as e:
            print("Failure to initialize Kafka consumer: %s" % e)
        finally:
            # Close down consumer to commit final offsets.
            self.consumer.close()

    def get_pods(self, namespace):
        core_v1 = client.CoreV1Api()
        api_response = core_v1.list_pod_for_all_namespaces(watch=False)
        #pprint(api_response)
        for i in api_response.items:
            if(i.metadata.namespace == namespace):
                print('%s\t%s\t%s' % (i.status.pod_ip, i.metadata.namespace, i.metadata.name))
    
    
    def deploy(self, deployment_yaml, namespace):
        with open(path.join(path.dirname(__file__), deployment_yaml)) as f:
            dep = yaml.safe_load(f)
            apps_v1 = client.AppsV1Api()
            try:
                api_response = apps_v1.create_namespaced_deployment(body=dep, namespace=namespace)
                #pprint(api_response)
                print("Deployment created. status='%s'" % api_response.metadata.name)
            except client.exceptions.ApiException as e:
                print("Deployment exception: %s" % e)