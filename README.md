# ntua_diploma_thesis

## Local Development

### Kafka

Run Docker Compose on a terminal
```bash
docker-compose up -d
```

Check that everything is up and running
```bash
docker-compose ps
```

Create topic
```bash
docker-compose exec broker kafka-topics \
  --create \
  --bootstrap-server localhost:9092 \
  --replication-factor 1 \
  --partitions 1 \
  --topic kdriver
```

## Useful Resources

### Kubernetes
[Kubectl Cheat Sheet](https://kubernetes.io/docs/reference/kubectl/cheatsheet/)

[How to Access a Kubernetes Cluster](https://kubernetes.io/docs/tasks/access-application-cluster/access-cluster/)

[Cluster Access Configuration](https://kubernetes.io/docs/tasks/access-application-cluster/configure-access-multiple-clusters/)

[Configure kubectl to Access Remote Kubernetes Cluster](https://acloudguru.com/hands-on-labs/configuring-kubectl-to-access-a-remote-cluster)

[Kubeconfig tips with Kubectl](https://ahmet.im/blog/mastering-kubeconfig/)

//todo
[1](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)
[2](https://www.mirantis.com/blog/introduction-to-yaml-creating-a-kubernetes-deployment/)
[3](https://kubernetes.io/docs/concepts/overview/working-with-objects/)

### Kubernetes & Python
[Python Client](https://github.com/kubernetes-client/python)

[Python Client API Endpoints](https://github.com/kubernetes-client/python/blob/master/kubernetes/README.md#documentation-for-api-endpoints)

[Get Started Kubernetes with Python](https://kubernetes.io/blog/2019/07/23/get-started-with-kubernetes-using-python/)

### Kafka
[Kafka CheatSheet](https://docs.confluent.io/platform/current/quickstart/cos-docker-quickstart.html)

### Kafka & Python
[Getting Started with Apache Kafka in Python](https://towardsdatascience.com/getting-started-with-apache-kafka-in-python-604b3250aa05)