# [add thesis title]

## For Local Development in Linux

### Installations
1. [Go](https://golang.org/dl/)
2. [kind - Kubernetes in Docker](https://kind.sigs.k8s.io/docs/user/quick-start/)
3. Project requirements (preferably in a Python virtual env):
```bash
pip install -r requirements.txt
``` 

## Quickstart

1. Run Docker Compose on a terminal: ```docker-compose up -d ```

2. Check that everything is up and running: ```docker-compose ps```

3. Start the app (entrypoint project/__main__.py): ```/home/athina/python-virtual-environments/thesis/bin/python /home/athina/Desktop/thesis/code/ntua_diploma_thesis/__main__.py worker --loglevel=INFO```

4. Write to the orchestrator topic: ```kafkacat -b localhost:9092 -t orchestrator -P {"appUUID": "tmp", "serviceUUID": "hello1"}```

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

CLI used for debugging & testing. [Documentation] (https://docs.confluent.io/platform/current/app-development/kafkacat-usage.html)

Check a topic's content
```bash
kafkacat -b localhost:9092 -t <topic_name>
kafkacat -b localhost:9092 -t orchestrator
kafkacat -b localhost:9092 -t kubernetes
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