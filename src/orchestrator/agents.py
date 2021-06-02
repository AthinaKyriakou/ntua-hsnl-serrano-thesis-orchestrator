from app import app
from src.orchestrator.models import OrchestratorPlan
        
# register the used topics in the faust app
# TODO: add them to config file
orchestrator_topic = app.topic('orchestrator', value_type=OrchestratorPlan)
k8s_topic = app.topic('kubernetes', value_type=OrchestratorPlan)
        
@app.agent(orchestrator_topic)
async def process_plans(plans):
    async for plan in plans:
        #print(f"Data received is {plan}")
        await k8s_topic.send(value=plan)