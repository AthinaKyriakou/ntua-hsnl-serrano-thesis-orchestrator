import yaml
from models import DatabaseRecord
from utils.faust_helpers import record_to_string
from config import kafka_cfg, DISPATCHED_STATE, NEW_STATE
from confluent_kafka import Producer

#/home/athina/python-virtual-environments/thesis/bin/python /home/athina/Desktop/thesis/code/ntua_diploma_thesis/src/test.py

def main():

    # dummy test upsert
    p = Producer({'bootstrap.servers': kafka_cfg['bootstrap.servers']})
    requestUUID = '1f2a82ff16c84684b1ad2c1653aa0507'
    with open('/home/athina/Desktop/thesis/code/ntua_diploma_thesis/app-k8s.yaml') as f:
        payload_dict = yaml.safe_load(f)
    db_rec = DatabaseRecord(requestUUID=requestUUID, state=DISPATCHED_STATE, resource=None, yamlSpec=payload_dict, appID=None, appName=None)
    db_rec_str = record_to_string(db_rec)
    p.produce(topic=kafka_cfg['db_consumer'], value=db_rec_str)
    p.flush()

if __name__ == '__main__':
    main()