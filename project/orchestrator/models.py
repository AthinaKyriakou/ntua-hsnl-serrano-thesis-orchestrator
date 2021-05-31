import faust

class OrchestratorPlan(faust.Record):
    appUUID: str
    serviceUUID: str