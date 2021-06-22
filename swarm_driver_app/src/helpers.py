import json

def record_to_string(rec):
    rec_dict = vars(rec)
    rec_dict.pop('__evaluated_fields__', None)
    rec_str = json.dumps(rec_dict)
    return rec_str

def remove_added_labels(yamlSpec):
    yamlSpec.pop('namespace')
    yamlSpec.pop('name')
    yamlSpec.pop('orchestrator')
    return yamlSpec