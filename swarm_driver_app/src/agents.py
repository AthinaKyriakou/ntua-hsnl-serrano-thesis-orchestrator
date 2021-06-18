from faust_app import faust_app
from confluent_kafka import Producer
from config import kafka_cfg, DEPLOYED_STATE, FAILED_STATE
from models import DeploymentPlan, DatabaseRecord
from swarm_driver import SwarmDriver
from helpers import record_to_string
import datetime
import json

print('swarm_driver_app - agents - creating swarm driver')
swarm_topic = faust_app.topic(kafka_cfg['swarm'], value_type=DeploymentPlan)
swarm_driver = SwarmDriver()

@faust_app.agent(swarm_topic)
async def deploy_to_swarm(plans):
    p = Producer({'bootstrap.servers': kafka_cfg['bootstrap.servers']})
    async for plan in plans:
        print('swarm_driver_app - agents - data for requestUUID: %s received' % (plan.requestUUID))
        ret = swarm_driver.deploy(dep_dict=plan.yamlSpec)
        
        # write to db_consumer topic - TODO: add and remove later a deployment/stack name label, add success code to config file
        timestamp = json.dumps(datetime.datetime.now(), indent=4, sort_keys=True, default=str)
        if(ret==201):
            db_rec = DatabaseRecord(requestUUID=plan.requestUUID, state=DEPLOYED_STATE, resource=None, yamlSpec=plan.yamlSpec, appID=None, appName=None, timestamp=timestamp)
        else:
            db_rec = DatabaseRecord(requestUUID=plan.requestUUID, state=FAILED_STATE, resource=None, yamlSpec=plan.yamlSpec, appID=None, appName=None, timestamp=timestamp)
        db_rec_str = record_to_string(db_rec)
        p.produce(topic=kafka_cfg['db_consumer'], value=db_rec_str)
        p.flush()