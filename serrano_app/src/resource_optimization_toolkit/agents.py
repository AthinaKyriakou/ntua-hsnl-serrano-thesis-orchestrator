from faust_app import faust_app
from src.models import DeploymentPlan
from src.config import kafka_cfg, DEPLOY_ACTION

# register the used topics in the faust app
print('ROT - global checks')
rto_topic = faust_app.topic(kafka_cfg['resource_optimization_toolkit'], value_type=DeploymentPlan)
orchestrator_topic = faust_app.topic(kafka_cfg['orchestrator'], value_type=DeploymentPlan)

# TODO: add RTO logic         
@faust_app.agent(rto_topic)
async def process_plans(plans):
    async for plan in plans:
        print("Resource Optimization Toolkit - data received")
        if(plan.action == DEPLOY_ACTION):
            await orchestrator_topic.send(value=plan)