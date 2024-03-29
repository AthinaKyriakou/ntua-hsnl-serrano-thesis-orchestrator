# project entry point
import sys
from confluent_kafka.admin import AdminClient, NewTopic
from config import kafka_cfg
from faust_app import faust_app

sys.path.append('.')

def main():    
    print('swarm_driver_app - __main__ - creating swarm topic & starting faust app')
    admin_client = AdminClient({'bootstrap.servers': kafka_cfg['bootstrap.servers']})
    topic_list = []
    topic_list.append(NewTopic(kafka_cfg['swarm'], 1, 1))
    admin_client.create_topics(topic_list)


if __name__ == '__main__':
    main()
    faust_app.main()