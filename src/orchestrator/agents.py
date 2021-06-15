from faust_app import faust_app
from confluent_kafka import Producer
from src.config import kafka_cfg, SWARM, K8s, PENDING_STATE
from src.models import DeploymentPlan, DatabaseRecord
from src.utils.faust_helpers import record_to_string
        
# register the used topics in the faust app
orchestrator_topic = faust_app.topic(kafka_cfg['orchestrator'], value_type=DeploymentPlan)
swarm_topic = faust_app.topic(kafka_cfg['swarm'], value_type=DeploymentPlan)
k8s_topic = faust_app.topic(kafka_cfg['kubernetes'], value_type=DeploymentPlan)

# TODO: add orchestrator logic  
@faust_app.agent(orchestrator_topic)
async def process_plans(plans):
    p = Producer({'bootstrap.servers': kafka_cfg['bootstrap.servers']})
    async for plan in plans:
        print('Orchestrator - data received')

        # TODO: handle if the field is not specified
        selected_orchestrator = plan.yamlSpec.get('orchestrator')
        plan.yamlSpec.pop('orchestrator')
        if(selected_orchestrator == SWARM):
            await swarm_topic.send(value=plan)
        elif (selected_orchestrator== K8s):
            await k8s_topic.send(value=plan)
        else:
            print('Orchestrator - no driver for %s found' %(selected_orchestrator))
        
        # write to db_consumer topic - TODO: add and remove later a deployment/stack name label
        if(selected_orchestrator == SWARM or selected_orchestrator== K8s):
            db_rec = DatabaseRecord(requestUUID=plan.requestUUID, state=PENDING_STATE, resource=None, yamlSpec=plan.yamlSpec, appID=None, appName=None)
            db_rec_str = record_to_string(db_rec)
            p.produce(topic=kafka_cfg['db_consumer'], value=db_rec_str)
            p.flush()