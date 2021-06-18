import os, sys, yaml, inspect
from docker.api import swarm
#from swarm import SwarmDriver
import uuid

# import from parent dir: https://codeolives.com/2020/01/10/python-reference-module-in-parent-directory/
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
import config

#home/athina/python-virtual-environments/thesis/bin/python /home/athina/Desktop/thesis/code/ntua_diploma_thesis/src/drivers/test.py

def main():   
    print(type(uuid.uuid4().hex)) 
    #print('test - initializing swarm driver')
    #swarm_driver = SwarmDriver()
    #swarm_driver.get_containers()
    #swarm_driver.get_services()

    # dummy deployment
    #with open('/home/athina/Desktop/thesis/code/ntua_diploma_thesis/app-swarm.yaml', 'r') as stream:
    #    dep_dict = yaml.safe_load(stream)
    #    swarm_driver.deploy(dep_dict)

    #swarm_driver.get_stacks()
    
if __name__ == '__main__':
    main()