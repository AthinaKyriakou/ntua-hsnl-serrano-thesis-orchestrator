from typing import Dict
import faust

class DeploymentPlan(faust.Record):
    requestUUID: str #TODO: check if I should change the name field
    action: str
    payload: Dict[object, object] # yaml deployment plan loaded as python dict

class DatabaseRecord(faust.Record):
    requestUUID: str 
    state: str
    resource: str
    yamlSpec: Dict[object, object] # yaml deployment plan loaded as python dict
    appID: str
    appName: str