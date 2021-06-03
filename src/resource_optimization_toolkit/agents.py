from faust_app import faust_app
from src.models import DeploymentPlan

# TODO: read topic names from config file
# register the used topics in the faust app
rto_topic = faust_app.topic('resource_optimization_toolkit', value_type=DeploymentPlan)
orchestrator_topic = faust_app.topic('orchestrator', value_type=DeploymentPlan)

# TODO: add RTO logic         
@faust_app.agent(rto_topic)
async def process_plans(plans):
    async for plan in plans:
        print("Resource Optimization Toolkit - data received")
        await orchestrator_topic.send(value=plan)