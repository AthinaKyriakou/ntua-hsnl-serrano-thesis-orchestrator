from faust_app import faust_app
from src.models import DeploymentPlan
        
# TODO: read topic names from config file
# register the used topics in the faust app
dispatcher = faust_app.topic('dispatcher', value_type=DeploymentPlan)
resource_optimization_toolkit = faust_app.topic('resource_optimization_toolkit', value_type=DeploymentPlan)
        
# TODO
@faust_app.agent(dispatcher)
async def process_plans(plans):
    async for plan in plans:
        print(f"Data received is {plan}")
        print(f"Type of data received is {type(plan)}")
#        await resource_optimization_toolkit.send(value=plan)