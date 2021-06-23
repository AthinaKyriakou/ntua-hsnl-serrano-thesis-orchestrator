from faust_app import faust_app
from confluent_kafka import Producer
from config import kafka_cfg, DEPLOYED_STATE, FAILED_STATE, REMOVED_STATE, REMOVED_STATE, DEPLOY_ACTION, REMOVE_ACTION, SWARM, mongodb_cfg
from models import SwarmRecord, DatabaseRecord
from swarm_driver import SwarmDriver
from helpers import record_to_string, query_by_stack_name
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

            # mark the previous version of the stack in the db, if exists, as removed
            prev_version_dict = query_by_stack_name(mongodb_cfg['connection.uri'], mongodb_cfg['db_name'], mongodb_cfg['db_collection'], req.name, SWARM)
            if(prev_version_dict != None):
                timestamp = json.dumps(datetime.datetime.now(), indent=4, sort_keys=True, default=str)
                db_rec = DatabaseRecord(requestUUID=prev_version_dict.get('requestUUID'), namespace=prev_version_dict.get('namespace'), name=prev_version_dict.get('name'), state=REMOVED_STATE, resource=SWARM, yamlSpec=prev_version_dict.get('yamlSpec'), timestamp=timestamp)
                db_rec_str = record_to_string(db_rec)
                p.produce(topic=kafka_cfg['db_consumer'], value=db_rec_str)
                p.flush()

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

        elif(req.action == REMOVE_ACTION):
            print('swarm_driver_app - agents - termination for requestUUID: %s received' % (req.requestUUID))
            ret = swarm_driver.delete_stack(name=req.name)
            
            # write to db_consumer topic
            timestamp = json.dumps(datetime.datetime.now(), indent=4, sort_keys=True, default=str)
            if(ret == 201):
                db_rec = DatabaseRecord(requestUUID=req.requestUUID, namespace=req.namespace, name=req.name, state=REMOVED_STATE, resource=SWARM, yamlSpec=req.yamlSpec, timestamp=timestamp)
                db_rec_str = record_to_string(db_rec)
                p.produce(topic=kafka_cfg['db_consumer'], value=db_rec_str)
                p.flush()
            else:
                print('swarm_driver_app - agents - termination for requestUUID: %s failed with return code: %s' % (req.requestUUID, ret))
        
        else:
            print('swarm_driver_app - agents - %s action not supported!' % req.action)