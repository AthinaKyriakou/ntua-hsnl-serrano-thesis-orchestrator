import re
from flask import Flask, request, abort
from confluent_kafka import Producer
import uuid
import yaml
import datetime
import json
import sys
from src.config import kafka_cfg, mongodb_cfg, DEPLOY_ACTION, TERMINATE_ACTION, NEW_STATE, DEPLOYED_STATE, FAILED_STATE
from src.models import DeploymentPlan, DatabaseRecord, TerminationRequest
from src.utils.faust_helpers import record_to_string
from src.utils.avro_schema import send_avro_record
from src.utils.mongodb_helpers import get_db_client

print('flask_app - creating an instance of the flask library')
app = Flask(__name__)

@app.route("/")
def instructions():
    return "<p>Possible actions: submit, inspect, terminate</p>"

# get a yaml file for deployment
@app.route("/deploy/<filename>", methods=["POST"])
def submit_deployment(filename):
    try:
        payload_bytes = request.data
        # TODO: do some syntax checks in the deployment file
        payload_dict = yaml.safe_load(payload_bytes)
        
        # UUID as a 32-character hexadecimal string
        requestUUID = uuid.uuid4().hex

        # TODO: fix Avro
        p = Producer({'bootstrap.servers': kafka_cfg['bootstrap.servers']})

        # write to dispatcher topic
        dp = DeploymentPlan(requestUUID=requestUUID, action=DEPLOY_ACTION, yamlSpec=payload_dict)
        dp_str = record_to_string(dp)
        p.produce(topic=kafka_cfg['dispatcher'], value=dp_str)
        p.flush()

        # write to db_consumer topic - TODO: add and remove later a deployment/stack name label
        timestamp = json.dumps(datetime.datetime.now(), indent=4, sort_keys=True, default=str)
        db_rec = DatabaseRecord(requestUUID=requestUUID, state=NEW_STATE, resource=None, yamlSpec=payload_dict, appID=None, appName=None, timestamp=timestamp)
        db_rec_str = record_to_string(db_rec)
        p.produce(topic=kafka_cfg['db_consumer'], value=db_rec_str)
        p.flush()
        #send_avro_record(schema_file_path=kafka_cfg['schema_file_path'], topic=kafka_cfg['db_consumer'], key=request_UUID, value=db_rec_str)

    except Exception as e:
        # return 400 BAD REQUEST
        print(e)
        abort(400,e)
    # return 201 CREATED
    return "", 201


# terminate based on requestUUID (32-character hexadecimal string)
@app.route("/terminate/<requestUUID>", methods=["POST"])
def terminate_deployment(requestUUID):
    try:
        payload_bytes = request.data
        requestUUID = payload_bytes.decode('UTF-8')
        print('serrano_app - request to terminate deployment with UUID: %s' %(requestUUID))

        # query MongoDB to check if requestUUID is valid (deployment state == deployed)
        db_client = get_db_client(mongodb_cfg['connection.uri'], mongodb_cfg['db_name'])
        db_collection = db_client[mongodb_cfg['db_collection']]
        depl_dict = db_collection.find_one({'requestUUID': requestUUID})

        if(depl_dict == None):
            print('serrano_app - deployment with UUID: %s does not exist' %(requestUUID))
        
        elif(depl_dict['state'] == FAILED_STATE):
            print('serrano_app - deployment with UUID: %s has already failed' %(requestUUID))
        
        elif(depl_dict['state'] == DEPLOYED_STATE):
            p = Producer({'bootstrap.servers': kafka_cfg['bootstrap.servers']})
            term_req = TerminationRequest(requestUUID=requestUUID, action=TERMINATE_ACTION, resource=depl_dict['resource'])
        
        # TODO: prevent deployment if it has not happend
        else:
            print('TODO: prevent deployment if it has not happend')


    except Exception as e:
        # return 400 BAD REQUEST
        print(e)
        abort(400,e)
    # return 201 CREATED
    return "", 201