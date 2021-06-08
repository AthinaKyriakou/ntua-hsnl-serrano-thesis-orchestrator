from faust_app import faust_app
from src.models import DeploymentPlan
from config import kafka_cfg
        
# register the used topics in the faust app
orchestrator_topic = faust_app.topic(kafka_cfg['orchestrator'], value_type=DeploymentPlan)
k8s_topic = faust_app.topic(kafka_cfg['kubernetes'], value_type=DeploymentPlan)

# TODO: add orchestrator logic  
@faust_app.agent(orchestrator_topic)
async def process_plans(plans):
    async for plan in plans:
        print("Orchestrator - data received")
        await k8s_topic.send(value=plan)