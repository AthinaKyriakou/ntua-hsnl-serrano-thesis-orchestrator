from typing import Dict
import faust

class ComponentsRecord(faust.Record):
    requestUUID: str 
    action: str
    yamlSpec: Dict[object, object] = None   # yaml deployment plan loaded as python dict, specified when action == DEPLOY_ACTION

class DatabaseRecord(faust.Record):
    requestUUID: str 
    namespace: str
    name: str
    state: str
    resource: str                           # for multi-RO apps, convert this to list of strings
    yamlSpec: Dict[object, object]          # yaml deployment plan loaded as python dict
    timestamp: str

class SwarmRecord(faust.Record):
    requestUUID: str
    #clusterInfo: str
    namespace: str
    name: str
    yamlSpec: Dict[object, object]
    action: str

class KubernetesRecord(faust.Record):
    requestUUID: str
    #clusterInfo: str
    namespace: str
    name: str
    yamlSpec: Dict[object, object]
    action: str
