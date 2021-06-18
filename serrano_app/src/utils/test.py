import os, sys, inspect
import yaml
import uuid

# import from parent dir: https://codeolives.com/2020/01/10/python-reference-module-in-parent-directory/
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from models import DatabaseRecord, DeploymentPlan
from config import kafka_cfg, NEW_STATE, DEPLOY_ACTION
from utils.faust_helpers import record_to_string
from utils.avro_schema import send_avro_record

#/home/athina/python-virtual-environments/thesis/bin/python /home/athina/Desktop/thesis/code/ntua_diploma_thesis/src/utils/test.py

def main():
    payload_dict = yaml.safe_load('/home/athina/Desktop/thesis/code/ntua_diploma_thesis/app-k8s.yaml')
    requestUUID = uuid.uuid4().hex
    #print(type(request_UUID))

    # write to db_consumer topic as Avro record - TODO: add and remove later a deployment/stack name label
    db_rec = DatabaseRecord(requestUUID=requestUUID, state=NEW_STATE, resource=None, yamlSpec=payload_dict, appID=None, appName=None)
    db_rec_str = record_to_string(db_rec)
    send_avro_record(schema_file_path=kafka_cfg['schema_file_path'], topic=kafka_cfg['db_consumer'], key=requestUUID, value=db_rec_str)
    
if __name__ == '__main__':
    main()