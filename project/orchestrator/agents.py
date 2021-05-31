import sys
from app import app
from project.orchestrator.models import OrchestratorPlan
        
# register the used topics in the faust app
# TODO: add them to config file
print('\nIn the orchestrator')
orchestrator_topic = app.topic('orchestrator', value_type=OrchestratorPlan)
kubernetes_topic = app.topic('kubernetes', value_type=OrchestratorPlan)
        
@app.agent(orchestrator_topic)
async def process_plans(plans):
    async for plan in plans:
        print(f"Data recieved is {plan}")
        await kubernetes_topic.send(value=plan)