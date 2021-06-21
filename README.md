# [add thesis title]

## Installations (for local development in Linux)
1. [Go](https://golang.org/dl/)
2. [kind - Kubernetes in Docker](https://kind.sigs.k8s.io/docs/user/quick-start/)
3. Project requirements (preferably in a Python virtual env):
```bash
pip install -r requirements.txt
``` 
## Install MongoDB Kafka Connector

### Establish the MongoDB Sink connection (for upsert)
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

## Quickstart

1. Run Docker Compose on a terminal: ```docker-compose up -d ```

2. Check that everything is up and running: ```docker-compose ps```

3. Start the faust app: ```/home/athina/python-virtual-environments/thesis/bin/python /home/athina/Desktop/thesis/code/ntua_diploma_thesis/src/__main__.py worker --loglevel=INFO```

4. Start the flask app: ```./flask-start.sh``` from project's root

4. To deploy by a yaml file, specify the yaml file in ```/home/athina/python-virtual-environments/thesis/bin/python /home/athina/Desktop/thesis/code/ntua_diploma_thesis/deploy.py```

5. To check that data is published to the topics:
* ```kafkacat -b localhost:9092 -t dispatcher```
* ```kafkacat -b localhost:9092 -t resource_optimization_toolkit```
* ```kafkacat -b localhost:9092 -t orchestrator```
* ```kafkacat -b localhost:9092 -t swarm```
* ```kafkacat -b localhost:9092 -t kubernetes```

6. Check deployments in Kubernetes: ```kubectl get deployments```

## Project Layout
| Folder/File                       | Description                                                       |
| --------------------------------- | ----------------------------------------------------------------- |
| flask-start.sh                    | script to run the flask app (mod +x)                              |
| src/main.py                       | faust application entrypoint                                      |
| src/faust_app.py                  | creates an instance of the Faust for stream processing            |
| src/flask_app.py                  | creates an instance of the Flask                                  |
| src/models.py                     | faust models to describe the data in streams                      |
| src/helpers.py                    | helping functions                                                 |
| src/resource_optimization_toolkit | top level dir of the resource optimization toolkit service        |
| src/orchestrator                  | top level dir of the central orchestrator service                 |
| src/drivers                       | top level dir of the drivers services                             |
| src/drivers/agents.py             | faust async stream processors of drivers' topics                  |
| src/drivers/kubernetes.py         | K8sDriver class to connect and interact with a kubernetes cluster |

## Useful Commands

### Kubernetes with kind

Create a cluster:
```bash	
kind create cluster
kind get clusters (dflt name for created clusters: kind)
```
To have terminal interaction with the created Kubernetes objects, mainly for debugging, install [kubectl](https://kubernetes.io/docs/reference/kubectl/kubectl/).

### Kafka
Create topic
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

Check a topic's content
```bash
kafkacat -b localhost:9092 -t <topic_name>
```

Write to a topic
```bash
kafkacat -b localhost:9092 -t orchestrator -P
{"appUUID": "tmp", "serviceUUID": "hello1"}
```

### Docker

CLI [Documentation](https://docs.docker.com/engine/reference/commandline/docker/)

Get deployed services
```bash
docker service ls
```

Delete a service
```bash
docker service rm <service_name>
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

tocheck:
[1](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)
[2](https://www.mirantis.com/blog/introduction-to-yaml-creating-a-kubernetes-deployment/)
[3](https://kubernetes.io/docs/concepts/overview/working-with-objects/)

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




//tmp for prod
1. run the faust app in kafka machine: 
cd serrano_app
python3 ./src/__main__.py worker --loglevel=INFO
(can use python of your venv)

2. run the flask app
cd serrano_app
./flask-start.sh

3. deploy
python3 ./deploy.py -yamlSpec /home/serrano/athina-thesis/ntua-thesis-orchestrator/serrano_app/app-k8s.yaml -env prod

--> add kubeconfig note for k8s driver

4. remove local:
/home/athina/python-virtual-environments/thesis/bin/python /home/athina/Desktop/thesis/code/ntua_diploma_thesis/serrano_app/remove.py -requestUUID 9d4abde019d64013810f6fa91c029e65 -env local

5. deploy local:
 /home/athina/python-virtual-environments/thesis/bin/python /home/athina/Desktop/thesis/code/ntua_diploma_thesis/serrano_app/deploy.py -yamlSpec /home/athina/Desktop/thesis/code/ntua_diploma_thesis/serrano_app/app-k8s.yaml -env local