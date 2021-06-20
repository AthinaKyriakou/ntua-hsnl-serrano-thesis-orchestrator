from datetime import time
from faust_app import faust_app
from confluent_kafka import Producer
from src.config import kafka_cfg, SWARM, K8s, PENDING_STATE, DEPLOY_ACTION, REMOVE_ACTION, mongodb_cfg
from src.models import ComponentsRecord, DatabaseRecord, KubernetesRecord, SwarmRecord
from src.utils.faust_helpers import record_to_string
from src.utils.mongodb_helpers import query_by_requestUUID
import datetime
import json
        
# register the used topics in the faust app
print('Orchestrator - global checks')
orchestrator_topic = faust_app.topic(kafka_cfg['orchestrator'], value_type=ComponentsRecord)
swarm_topic = faust_app.topic(kafka_cfg['swarm'], value_type=SwarmRecord)
k8s_topic = faust_app.topic(kafka_cfg['kubernetes'], value_type=KubernetesRecord)


@faust_app.agent(orchestrator_topic)
async def process_requests(requests):
    p = Producer({'bootstrap.servers': kafka_cfg['bootstrap.servers']})
    async for req in requests:
        print('Orchestrator - data received')
        
        if(req.action == DEPLOY_ACTION):
            
            selected_orchestrator = req.yamlSpec.get('orchestrator')
            req.yamlSpec.pop('orchestrator')

            if(selected_orchestrator == SWARM):
                await swarm_topic.send(value=req)
            elif(selected_orchestrator == K8s):
                await k8s_topic.send(value=req)
            else:
                print('Orchestrator - no driver for %s found' %(selected_orchestrator))
            
            # write to db_consumer topic - TODO: add and remove later a deployment/stack name label
            if(selected_orchestrator == SWARM or selected_orchestrator == K8s):
                namespace = req.yamlSpec.get('namespace')
                name = req.yamlSpec.get('name')
                timestamp = json.dumps(datetime.datetime.now(), indent=4, sort_keys=True, default=str)
                
                db_rec = DatabaseRecord(requestUUID=req.requestUUID, namespace=namespace, name=name, state=PENDING_STATE, resource=selected_orchestrator, yamlSpec=req.yamlSpec, timestamp=timestamp)
                db_rec_str = record_to_string(db_rec)
                p.produce(topic=kafka_cfg['db_consumer'], value=db_rec_str)
                p.flush()
       
        elif(req.action == REMOVE_ACTION):
            # get from the mongoDB the information needed to remove the stack / deployment 
            info_dict = query_by_requestUUID(mongodb_cfg['connection.uri'], mongodb_cfg['db_name'], mongodb_cfg['db_collection'], req.requestUUID)
            
            if(info_dict['resource'] == SWARM):
                record = SwarmRecord(requestUUID=req.requestUUID, name=info_dict['name'], yamlSpec=info_dict['yamlSpec'])
                await swarm_topic.send(value=record)
            elif(info_dict['resource']  == K8s):
                record = KubernetesRecord(requestUUID=req.requestUUID, namespace=info_dict['namespace'], name=info_dict['name'], yamlSpec=info_dict['yamlSpec'])
                await k8s_topic.send(value=record)         