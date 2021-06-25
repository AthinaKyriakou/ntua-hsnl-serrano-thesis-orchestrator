from faust_app import faust_app
from src.models import ComponentsRecord
from src.config import kafka_cfg, DEPLOY_ACTION
from src.resource_optimization_toolkit.rot_algorithm import dummy_algorithm
import copy

# register the used topics in the faust app
print('ROT - global checks')
rto_topic = faust_app.topic(kafka_cfg['resource_optimization_toolkit'], value_type=ComponentsRecord)
orchestrator_topic = faust_app.topic(kafka_cfg['orchestrator'], value_type=ComponentsRecord)

# TODO: add RTO logic         
@faust_app.agent(rto_topic)
async def process_requests(requests):
    async for req in requests:
        print('Resource Optimization Toolkit - data received')
        if(req.action == DEPLOY_ACTION):
            # the algorithm to add labels regarding (a) selected CO site, (b) node preferences per app component
            try:
                configured_yamlSpec = dummy_algorithm(copy.deepcopy(req.yamlSpec))
                req.yamlSpec = configured_yamlSpec
            except Exception as e:
                print('Resource Optimization Toolkit - exception: %s in algorithm implementation, no labels added' % (e))
            await orchestrator_topic.send(value=req)