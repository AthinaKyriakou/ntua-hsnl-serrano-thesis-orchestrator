from faust_app import faust_app
from confluent_kafka import Producer
from config import kafka_cfg, DEPLOYED_STATE, FAILED_STATE, REMOVED_STATE, DEPLOY_ACTION, REMOVE_ACTION, SWARM
from models import SwarmRecord, DatabaseRecord
from swarm_driver import SwarmDriver
from helpers import record_to_string
import datetime
import json

print('swarm_driver_app - agents - creating swarm driver')
swarm_topic = faust_app.topic(kafka_cfg['swarm'], value_type=SwarmRecord)
swarm_driver = SwarmDriver()

@faust_app.agent(swarm_topic)
async def process_requests(requests):
    p = Producer({'bootstrap.servers': kafka_cfg['bootstrap.servers']})
    async for req in requests:
        
        if(req.action == DEPLOY_ACTION):
            print('swarm_driver_app - agents - data for requestUUID: %s received' % (req.requestUUID))
            ret = swarm_driver.deploy(req.requestUUID, dep_dict=req.yamlSpec)
            
            # write to db_consumer topic
            namespace = req.yamlSpec.get('namespace')       # no namespace supported for swarm, should be none
            name = req.yamlSpec.get('name')
            timestamp = json.dumps(datetime.datetime.now(), indent=4, sort_keys=True, default=str)
            if(ret==201):
                db_rec = DatabaseRecord(requestUUID=req.requestUUID, namespace=namespace, name=name, state=DEPLOYED_STATE, resource=SWARM, yamlSpec=req.yamlSpec, timestamp=timestamp)
            else:
                db_rec = DatabaseRecord(requestUUID=req.requestUUID, namespace=namespace, name=name, state=FAILED_STATE, resource=SWARM, yamlSpec=req.yamlSpec, timestamp=timestamp)
            db_rec_str = record_to_string(db_rec)
            p.produce(topic=kafka_cfg['db_consumer'], value=db_rec_str)
            p.flush()


# write the terminate function

# check models + config