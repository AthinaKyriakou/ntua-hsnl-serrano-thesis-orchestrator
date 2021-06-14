from flask import Flask, request, abort
from src.config import kafka_cfg
import uuid
import yaml
from src.models import DeploymentPlan
from confluent_kafka import Producer
import json

DEPLOY_ACTION = 'deploy'

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
        app_UUID = uuid.uuid4().hex
        dp = DeploymentPlan(appUUID=app_UUID,action=DEPLOY_ACTION,payload=payload_dict)
        dp_dict = vars(dp)
        dp_dict.pop('__evaluated_fields__', None)
        dp_str = json.dumps(dp_dict)
        
        p = Producer({'bootstrap.servers': kafka_cfg['bootstrap.servers']})
        p.produce(topic=kafka_cfg['dispatcher'], value=dp_str)
        p.flush()
    except Exception as e:
        # return 400 BAD REQUEST
        abort(400,e)
    # return 201 CREATED
    return "", 201