# project entry point
import sys
from confluent_kafka.admin import AdminClient, NewTopic
from app import app

sys.path.append('.')

def main():    
    print('\nCreate orchestrator and kubernetes topics.')
    admin_client = AdminClient({'bootstrap.servers': 'localhost:9092'})
    topic_list = []
    topic_list.append(NewTopic('resource_optimization_toolkit', 1, 1))
    topic_list.append(NewTopic('orchestrator', 1, 1))
    topic_list.append(NewTopic('kubernetes', 1, 1))
    admin_client.create_topics(topic_list)

if __name__ == '__main__':
    main()
    app.main()
