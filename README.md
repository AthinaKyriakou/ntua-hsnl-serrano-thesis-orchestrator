# [add thesis title]

## Installations (for local development in Linux)
1. [Go](https://golang.org/dl/)
2. [kind - Kubernetes in Docker](https://kind.sigs.k8s.io/docs/user/quick-start/)
3. Project requirements (preferably in a Python virtual env):
```bash
pip install -r requirements.txt
``` 

## Quickstart

1. Run Docker Compose on a terminal: ```docker-compose up -d ```

2. Check that everything is up and running: ```docker-compose ps```

3. Start the faust app: ```/home/athina/python-virtual-environments/thesis/bin/python /home/athina/Desktop/thesis/code/ntua_diploma_thesis/src/__main__.py worker --loglevel=INFO```

4. Start the flask app: ```flask-start.sh``` from project's root

4. Deploy the nginx-deployment.yaml file: ```/home/athina/python-virtual-environments/thesis/bin/python /home/athina/Desktop/thesis/code/ntua_diploma_thesis/deploy.py```

5. To check that data is published to the topics:
* ```kafkacat -b localhost:9092 -t dispatcher```
* ```kafkacat -b localhost:9092 -t resource_optimization_toolkit```
* ```kafkacat -b localhost:9092 -t orchestrator```
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

## Useful Resources

### Kafka
* [Kafka CheatSheet](https://docs.confluent.io/platform/current/quickstart/cos-docker-quickstart.html)
* [Getting Started with Apache Kafka in Python](https://towardsdatascience.com/getting-started-with-apache-kafka-in-python-604b3250aa05)
* [Basic stream processing using Kafka and Faust](https://abhishekbose550.medium.com/basic-stream-processing-using-kafka-and-faust-7de07ed0ea77)

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