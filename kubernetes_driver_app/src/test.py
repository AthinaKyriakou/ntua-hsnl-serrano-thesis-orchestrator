import os, sys, yaml, inspect
from docker.api import swarm
from helpers import add_node_affinity
import uuid
import copy

# import from parent dir: https://codeolives.com/2020/01/10/python-reference-module-in-parent-directory/
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
import config

#home/athina/python-virtual-environments/thesis/bin/python /home/athina/Desktop/thesis/code/ntua_diploma_thesis/kubernetes_driver_app/src/test.py

PREFERRED = 'preferredDuringSchedulingIgnoredDuringExecution'
IN_OPP = 'In'
IP = 'ip'

def main():
    with open('/home/athina/Desktop/thesis/code/ntua_diploma_thesis/serrano_app/app_test.yaml', 'r') as stream:
        yamlSpec = yaml.safe_load(stream)

        updated_yamlSpec = add_node_affinity(copy.deepcopy(yamlSpec), IP, 5, IN_OPP, PREFERRED, 100)

        file = open('/home/athina/Desktop/thesis/code/ntua_diploma_thesis/serrano_app/app_test_res.yaml', 'w')
        yaml.dump(updated_yamlSpec, file)
        file.close()
        
    
if __name__ == '__main__':
    main()