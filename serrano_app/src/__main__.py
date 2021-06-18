# project entry point
import sys
from confluent_kafka.admin import AdminClient, NewTopic
from config import kafka_cfg
from faust_app import faust_app

sys.path.append('.')

def main():    
    print('__main__ - creating kafka topics')
    admin_client = AdminClient({'bootstrap.servers': kafka_cfg['bootstrap.servers']})
    topic_list = []
    
    #TODO: change number of partitions
    topic_list.append(NewTopic(kafka_cfg['db_consumer'], 1, 1))
    topic_list.append(NewTopic(kafka_cfg['dispatcher'], 1, 1))
    topic_list.append(NewTopic(kafka_cfg['resource_optimization_toolkit'], 1, 1))
    topic_list.append(NewTopic(kafka_cfg['orchestrator'], 1, 1))
    topic_list.append(NewTopic(kafka_cfg['kubernetes'], 1, 1))
    topic_list.append(NewTopic(kafka_cfg['swarm'], 1, 1))
    admin_client.create_topics(topic_list)

if __name__ == '__main__':
    main()
    faust_app.main()
