from faust_app import faust_app
from config import kafka_cfg
from src.models import DeploymentPlan

# register the used topics in the faust app
dispatcher = faust_app.topic(kafka_cfg['dispatcher'], value_type=DeploymentPlan)
resource_optimization_toolkit = faust_app.topic(kafka_cfg['resource_optimization_toolkit'], value_type=DeploymentPlan)

# TODO: add dispatcher logic        
@faust_app.agent(dispatcher)
async def process_plans(plans):
    async for plan in plans:
        print("Dispatcher - data received")
        #print(f"Data received is {plan}")
        #print(f"Type of data received is {type(plan)}")
        await resource_optimization_toolkit.send(value=plan)