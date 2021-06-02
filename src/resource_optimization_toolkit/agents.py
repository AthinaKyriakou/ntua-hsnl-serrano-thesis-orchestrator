from faust_app import faust_app
import yaml
from src.orchestrator.models import OrchestratorPlan

rto_topic = faust_app.topic('resource_optimization_toolkit', value_type=int)
orchestrator_topic = faust_app.topic('orchestrator', value_type=OrchestratorPlan)
        
@faust_app.agent(rto_topic)
async def process_requests(requests):
    async for r in requests:
        #print(f"Request received is {r}")
        # convert deployment yaml file to dictionary & publish to the orchestrator topic
        yaml_file_dict = yaml.safe_load(open('/home/athina/Desktop/thesis/code/ntua_diploma_thesis/nginx-deployment.yaml'))
        tmp = OrchestratorPlan(appUUID='hello',serviceUUID='world',plan=yaml_file_dict)
        await orchestrator_topic.send(value=tmp)