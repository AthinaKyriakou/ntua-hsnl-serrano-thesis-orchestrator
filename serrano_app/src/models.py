from typing import Dict
import faust

class DeploymentPlan(faust.Record):
    requestUUID: str 
    action: str
    yamlSpec: Dict[object, object]  # yaml deployment plan loaded as python dict

class DatabaseRecord(faust.Record):
    requestUUID: str 
    state: str
    resource: str                   # for multi-RO apps, convert this to list of strings
    yamlSpec: Dict[object, object]  # yaml deployment plan loaded as python dict
    appID: str
    appName: str
    timestamp: str

class TerminationRequest(faust.Record):
    requestUUID: str
    action: str
    resource: str                   # for multi-RO apps, convert this to list of strings