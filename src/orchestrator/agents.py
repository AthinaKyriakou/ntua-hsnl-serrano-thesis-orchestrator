from faust_app import faust_app
from src.models import DeploymentPlan
from src.config import kafka_cfg, SWARM, K8s
        
# register the used topics in the faust app
orchestrator_topic = faust_app.topic(kafka_cfg['orchestrator'], value_type=DeploymentPlan)
swarm_topic = faust_app.topic(kafka_cfg['swarm'], value_type=DeploymentPlan)
k8s_topic = faust_app.topic(kafka_cfg['kubernetes'], value_type=DeploymentPlan)

# TODO: add orchestrator logic  
@faust_app.agent(orchestrator_topic)
async def process_plans(plans):
    async for plan in plans:
        print('Orchestrator - data received')
        # TODO: handle if the field is not specified
        selected_orchestrator = plan.payload.get('orchestrator')
        plan.payload.pop('orchestrator')
        if(selected_orchestrator == SWARM):
            await swarm_topic.send(value=plan)
        elif (selected_orchestrator== K8s):
            await k8s_topic.send(value=plan)
        else:
            print('Orchestrator - no driver for %s found' %(selected_orchestrator))
