# Development of Resource Orchestration Mechanisms for Heterogeneous Computing Infrastructures

Thesis(text mostly in greek with abstract in english): [link](https://dspace.lib.ntua.gr/xmlui/handle/123456789/55086)

## Installations

### For Local Development in Linux
1. [Go](https://golang.org/dl/)
2. [Docker](https://docs.docker.com/engine/install/ubuntu/)
3. [Docker Compose](https://docs.docker.com/compose/install/)
4. [kind - Kubernetes in Docker](https://kind.sigs.k8s.io/docs/user/quick-start/)
5. Install the project's requirements, preferably in a Python virtual env:
  ```bash
  pip install -r requirements.txt
  ```

### For a Production Environment
1. Create a [swarm cluster](https://docs.docker.com/engine/swarm/swarm-tutorial/create-swarm/) and clone the repo to the master node
2. Create a [Kubernetes cluster](https://kubernetes.io/docs/setup/production-environment/) and clone the repo to the master node
3. Install the project's requirements in each cluster, preferably in a Python virtual env:
  ```bash
  pip install -r requirements_production.txt
  ``` 

### Configs to switch from prod to local and vice versa
| Folder/File                       | Description                                  |
| --------------------------------- | -------------------------------------------- |
| /serrano_app/docker-compose.yaml  | environment/KAFKA_ADVERTISED_LISTENERS       |
| /serrano_app/flask-start.sh       | flask run                                    |
| /serrano_app/config/              | kafka_cfg/kubeconfig_yaml                    |
| /kubernetes_driver_app/config/    | kafka_cfg/bootstrap.servers                  |
| /kubernetes_driver_app/config/    | kafka_cfg/kubeconfig_yaml                    |
| /kubernetes_driver_app/config/    | kafka_cfg/broker                             |
| /swarm_driver_app/config/         | kafka_cfg/bootstrap.servers                  |
| /swarm_driver_app/config/         | kafka_cfg/broker                             |

## Quickstart
1. Run Docker Compose on a terminal:
    ```bash
    cd serrano_app/
    docker-compose up -d
    ``` 

2. Check that everything is up and running:
    ```bash
    docker-compose ps
    ``` 

3. Establish the [MongoDB Sink connection](#establish-the-mongodb-sink-connection)

4. To start the **serrano_app**, from the /serrano_app folder:
    - Start the Faust agents for the Dispatcher, Resource Optimization Toolkit and Orchestrator components:  
      ```bash
      <python3_path> ./src/__main__.py worker --loglevel=INFO
      ``` 
    - Start the Flask app to receive requests for an app deployment or termination:  
      ```bash
      ./flask-start.sh
      ``` 
5. Create an application request:
    - Deployment
      ```bash
      <python3_path> ./deploy.py -yamlSpec <absolute path to a YAML file> -env <local or prod>
      ``` 
    - Termination
      ```bash
      <python3_path> ./remove.py -requestUUID <requestUUID> -env <local or prod>
      ```  

6. Activate the Faust agent of the swarm or the Kubernetes driver to process the request:
    - For the **swarm driver**, connect to the manager node and from the swarm_driver_app folder:
      ```bash
      <python3_path> ./src/__main__.py worker --loglevel=INFO
      ``` 
    - For the **Kubernetes driver**, connect to the manager node and from the kubernetes_driver_app folder:
      ```bash
      <python3_path> ./src/__main__.py worker --loglevel=INFO
      ``` 

7. To check that data is published to the respective topics:
    * ```kafkacat -b localhost:9092 -t dispatcher```
    * ```kafkacat -b localhost:9092 -t resource_optimization_toolkit```
    * ```kafkacat -b localhost:9092 -t orchestrator```
    * ```kafkacat -b localhost:9092 -t swarm```
    * ```kafkacat -b localhost:9092 -t kubernetes```

8. Check created namespace, services and deployments in Kubernetes:
    ```bash
    kubectl get namespaces
    kubectl get services
    kubectl get deployments
    ``` 
9. Check stack creation in the swarm:
    ```bash
    docker stack ls
    ``` 

## Files' & Folders' Highlights
| Folder/File                       | Description                                                                                 |
| --------------------------------- | ------------------------------------------------------------------------------------------- |
| /serrano_app                      | implementation of the Dispatcher, Resource Optimization Toolkit and Orchestrator components |
| /swarm_driver_app                 | implementation of the swarm driver component                                                |
| /kubernetes_driver_app            | implementation of the Kubernetes driver component                                           |
| flask-start.sh                    | script to run the flask app (mod +x)                                                        |
| src/main.py                       | faust application entrypoint                                                                |
| src/faust_app.py                  | creates an instance of the Faust for stream processing                                      |
| src/flask_app.py                  | creates an instance of the Flask                                                            |
| models.py                         | Faust models to describe the data in the streams                                            |
| helpers.py                        | helping functions                                                                           |
| agents.py                         | Faust async stream processors of the Kafka topics                                           |
| swarm_driver.py                   | SwarmDriver class to connect and interact with a swarm                                      | 
| kubernetes_driver.py              | K8sDriver class to connect and interact with a Kubernetes cluster                           |

## Establish the MongoDB Sink Connection (for upsert)
In this example, the MongoDB is in MongoDB Atlas.
```bash
curl -X PUT http://localhost:8083/connectors/sink-mongodb-users/config -H "Content-Type: application/json" -d ' {
      "connector.class":"com.mongodb.kafka.connect.MongoSinkConnector",
      "tasks.max":"1",
      "topics":"db_consumer",
      "connection.uri":"mongodb://athina_kyriakou:123@ntua-thesis-cluster-shard-00-00.xcgej.mongodb.net:27017,ntua-thesis-cluster-shard-00-01.xcgej.mongodb.net:27017,ntua-thesis-cluster-shard-00-02.xcgej.mongodb.net:27017/myFirstDatabase?ssl=true&replicaSet=atlas-xirr44-shard-0&authSource=admin&retryWrites=true&w=majority",
      "database":"thesisdb",
      "collection":"db_consumer",
      "key.converter":"org.apache.kafka.connect.json.JsonConverter",
      "key.converter.schemas.enable":false,
      "value.converter":"org.apache.kafka.connect.json.JsonConverter",
      "value.converter.schemas.enable":false,
      "document.id.strategy":"com.mongodb.kafka.connect.sink.processor.id.strategy.PartialValueStrategy",
      "document.id.strategy.partial.value.projection.list":"requestUUID",
      "document.id.strategy.partial.value.projection.type":"AllowList",
      "writemodel.strategy":"com.mongodb.kafka.connect.sink.writemodel.strategy.ReplaceOneBusinessKeyStrategy"
}'
``` 
Detailed info [here](https://www.mongodb.com/blog/post/getting-started-with-the-mongodb-connector-for-apache-kafka-and-mongodb-atlas)

## Useful Commands

### Kafka
Create a topic:
```bash
docker-compose exec broker kafka-topics \
  --create \
  --bootstrap-server localhost:9092 \
  --replication-factor 1 \
  --partitions 1 \
  --topic kdriver
```

### Kafkacat
CLI used for debugging & testing. [Documentation](https://docs.confluent.io/platform/current/app-development/kafkacat-usage.html)

Check a topic's content:
```bash
kafkacat -b localhost:9092 -t <topic_name>
```

Write to the orchestrator topic:
```bash
kafkacat -b localhost:9092 -t orchestrator -P
{"requestUUID": XX, "action": XXX, "yamlSpec":XXXX}
```

### Swarm
CLI [Documentation](https://docs.docker.com/engine/reference/commandline/docker/)

Get created stacks:
```bash
docker stack ls
```

Delete a stack:
```bash
docker stack rm <stack name>
```

Check nodes' information (engine version, hostname, status, availability, manager status):
```bash
docker node ls
```

Check the labels of a node (and other info):
```bash
docker node inspect <node hostname> --pretty
```

Add a label to a node:
```bash
docker node update --label-add <label name>=<value>
```

Check the node that a service is running on:
```bash
docker service ps <service name>
```

Create a swarm stack based on a YAML file:
```bash
docker stack deploy --compose-file <yaml file path> <stack name>
```

### Kubernetes with kind

Create a cluster:
```bash	
kind create cluster
kind get clusters (dflt name for created clusters: kind)
```
To have terminal interaction with the created Kubernetes objects, mainly for debugging, install [kubectl](https://kubernetes.io/docs/reference/kubectl/kubectl/).

### Kubernetes with kubectl

Get deployments in a namespace:
```bash
kubectl get deployments --namespace=<name>
```

Check in which nodes a namespace's pods are runnning:
```bash
kubectl get pod -o wide --namespace=<name>
```

Show the nodes' labels:
```bash
kubectl get nodes --show-labels
```

Add a label to a node:
```bash
kubectl label nodes <node name> <label name>=<value>
```

Create Kubernetes resources based on a YAML file:
```bash
kubectl apply -f <yaml file path>
```

## Useful Resources

### Kafka
* [Kafka CheatSheet](https://docs.confluent.io/platform/current/quickstart/cos-docker-quickstart.html)
* [Getting Started with Apache Kafka in Python](https://towardsdatascience.com/getting-started-with-apache-kafka-in-python-604b3250aa05)
* [Basic stream processing using Kafka and Faust](https://abhishekbose550.medium.com/basic-stream-processing-using-kafka-and-faust-7de07ed0ea77)
* [Kafka: Consumer API vs Streams API](https://stackoverflow.com/questions/44014975/kafka-consumer-api-vs-streams-api)

### Kubernetes
* [Kubectl Cheat Sheet](https://kubernetes.io/docs/reference/kubectl/cheatsheet/)
* [How to Access a Kubernetes Cluster](https://kubernetes.io/docs/tasks/access-application-cluster/access-cluster/)
* [Cluster Access Configuration](https://kubernetes.io/docs/tasks/access-application-cluster/configure-access-multiple-clusters/)
* [Configure kubectl to Access Remote Kubernetes Cluster](https://acloudguru.com/hands-on-labs/configuring-kubectl-to-access-a-remote-cluster)
* [Kubeconfig tips with Kubectl](https://ahmet.im/blog/mastering-kubeconfig/)

### Kubernetes & Python
* [Python Client](https://github.com/kubernetes-client/python)
* [Python Client API Endpoints](https://github.com/kubernetes-client/python/blob/master/kubernetes/README.md#documentation-for-api-endpoints)
* [Get Started Kubernetes with Python](https://kubernetes.io/blog/2019/07/23/get-started-with-kubernetes-using-python/)

### Faust
* [The App - Define your Faust project](https://faust.readthedocs.io/en/latest/userguide/application.html#medium-large-projects): Spot the suggested structure of medium/large projects [here](https://faust.readthedocs.io/en/latest/userguide/application.html#medium-large-projects)
* [Example of medium project structure implementation](https://www.8mincode.com/posts/how-to-stream-data-with-kafka-and-faust-streaming-pipeline/)
* [Models, Serialization, and Codecs](https://faust.readthedocs.io/en/latest/userguide/models.html)
* [Stream processing with Python Faust: Part II – Streaming pipeline](https://www.8mincode.com/posts/how-to-stream-data-with-kafka-and-faust-streaming-pipeline/)

### Kafka Source - MongoDB Sink 
* [MongoDB Kafka Connector](https://docs.mongodb.com/kafka-connector/current/)
* Create a Database in MongoDB Using the CLI with MongoDB Atlas: [here](https://www.mongodb.com/basics/create-database) & [here](https://docs.atlas.mongodb.com/mongo-shell-connection/)
* [MongoDB Write Model Strategies](https://docs.mongodb.com/kafka-connector/current/kafka-sink-postprocessors/#custom-write-model-strategy)
* Kafka Connector used strategy for upsert: [ReplaceOneBusinessKeyStrategy](https://docs.mongodb.com/kafka-connector/current/kafka-sink-postprocessors/#std-label-replaceonebusinesskey-example)
* [DeleteOne write model strategy](https://www.mongodb.com/blog/post/mongodb-connector-apache-kafka-available-now)

### Avro
* [Introduction to Schemas in Apache Kafka with the Confluent Schema Registry](https://medium.com/@stephane.maarek/introduction-to-schemas-in-apache-kafka-with-the-confluent-schema-registry-3bf55e401321)
* [Create Avro Producers With Python and the Confluent Kafka Library](https://betterprogramming.pub/avro-producer-with-python-and-confluent-kafka-library-4a1a2ed91a24)
* [Consume Messages From Kafka Topics Using Python and Avro Consumer](https://betterprogramming.pub/consume-messages-from-kafka-topic-using-python-and-avro-consumer-eda5aad64230)
* [How to deserialize AVRO messages in Python Faust?](https://medium.com/swlh/how-to-deserialize-avro-messages-in-python-faust-400118843447)
