from typing import Dict
import faust
from app import app

class OrchestratorPlan(faust.Record):
    appUUID: str
    serviceUUID: str
    plan: Dict[object, object] #yaml deployment plan loaded as python dict