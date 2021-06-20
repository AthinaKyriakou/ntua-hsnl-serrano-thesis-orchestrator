from faust_app import faust_app
from confluent_kafka import Producer
from src.config import kafka_cfg, DEPLOY_ACTION, INSPECT_ACTION, REMOVE_ACTION, DISPATCHED_STATE
from src.models import ComponentsRecord, DatabaseRecord
from src.utils.faust_helpers import record_to_string
import datetime
import json

# register the used topics in the faust app
print('Dispatcher - global checks')
dispatcher = faust_app.topic(kafka_cfg['dispatcher'], value_type=ComponentsRecord)
resource_optimization_toolkit = faust_app.topic(kafka_cfg['resource_optimization_toolkit'], value_type=ComponentsRecord)
orchestrator = faust_app.topic(kafka_cfg['orchestrator'], value_type=ComponentsRecord)
       
@faust_app.agent(dispatcher)
async def process_requests(requests):
    p = Producer({'bootstrap.servers': kafka_cfg['bootstrap.servers']})
    async for req in requests:
        print('Dispatcher - data received')
        
        if(req.action == DEPLOY_ACTION or req.action == INSPECT_ACTION):

            # write to ROT topic
            await resource_optimization_toolkit.send(value=req)

            # write to db_consumer topic - TODO: add and remove later a deployment/stack name label
            namespace = req.yamlSpec.get('namespace')
            name = req.yamlSpec.get('name')
            timestamp = json.dumps(datetime.datetime.now(), indent=4, sort_keys=True, default=str)
            db_rec = DatabaseRecord(requestUUID=req.requestUUID, namespace=namespace, name=name, state=DISPATCHED_STATE, resource=None, yamlSpec=req.yamlSpec, timestamp=timestamp)
            db_rec_str = record_to_string(db_rec)
            p.produce(topic=kafka_cfg['db_consumer'], value=db_rec_str)
            p.flush()
        
        elif(req.action == REMOVE_ACTION):
            # write to orchestrator topic
            await orchestrator.send(value=req)
