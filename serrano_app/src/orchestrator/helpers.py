from src.config import SWARM, K8s

def filter_yamlSpec(yamlSpec, selected_orchestrator):
    res = {}
    res['comp_preferences'] = yamlSpec['comp_preferences']

    if(selected_orchestrator == SWARM):
        res['spec'] = yamlSpec['swarmSpec']
    elif(selected_orchestrator == K8s): 
        res['spec'] = yamlSpec['kubernetesSpec']
    return res