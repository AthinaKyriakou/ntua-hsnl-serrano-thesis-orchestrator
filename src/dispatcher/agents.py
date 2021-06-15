from faust_app import faust_app
from confluent_kafka import Producer
from src.config import kafka_cfg, DEPLOY_ACTION, INSPECT_ACTION, DISPATCHED_STATE
from src.models import DeploymentPlan, DatabaseRecord
from src.utils.faust_helpers import record_to_string

# register the used topics in the faust app
dispatcher = faust_app.topic(kafka_cfg['dispatcher'], value_type=DeploymentPlan)
resource_optimization_toolkit = faust_app.topic(kafka_cfg['resource_optimization_toolkit'], value_type=DeploymentPlan)

# TODO: add dispatcher logic        
@faust_app.agent(dispatcher)
async def process_plans(plans):
    p = Producer({'bootstrap.servers': kafka_cfg['bootstrap.servers']})
    async for plan in plans:
        print("Dispatcher - data received")
        
        if(plan.action == DEPLOY_ACTION or plan.action == INSPECT_ACTION):

            # write to ROT topic
            await resource_optimization_toolkit.send(value=plan)

            # write to db_consumer topic - TODO: add and remove later a deployment/stack name label
            db_rec = DatabaseRecord(requestUUID=plan.requestUUID, state=DISPATCHED_STATE, resource=None, yamlSpec=plan.yamlSpec, appID=None, appName=None)
            db_rec_str = record_to_string(db_rec)
            p.produce(topic=kafka_cfg['db_consumer'], value=db_rec_str)
            p.flush()

