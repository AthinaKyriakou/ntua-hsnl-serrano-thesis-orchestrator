from typing import Dict
import faust

class DeploymentPlan(faust.Record):
    appUUID: str
    action: str
    payload: Dict[object, object] #yaml deployment plan loaded as python dict