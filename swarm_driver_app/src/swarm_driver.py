import docker
import yaml
import os
import subprocess
from config import SWARM_DEPL_DIR
from helpers import remove_added_labels, add_placement_specs
import copy

PREFERRED = 'preferences'
IP = 'ip'

class SwarmDriver(object):
    
    def __init__(self):
        # TODO: customize the base_url parameter
        self.client = docker.APIClient()
        os.makedirs(SWARM_DEPL_DIR, exist_ok=True) 
        # print(self.client.version())
    
    def get_containers(self):
        print('\nlist containers')
        containers = self.client.containers()
        # each returned container is a dict
        for i in containers:
            print('id: %s\tname: %s\timage: %s\tstate: %s\tstatus: %s\n' % (i.get('Id'), i.get('Names'), i.get('Image'), i.get('State'), i.get('Status')))

    def get_services(self):
        print('\nlist services')
        services = self.client.services()
        # each returned service is a dict
        for i in services:
            print('id: %s\tname: %s\n' % (i.get('ID'), i.get('Spec').get('Name')))            
    
    def get_stacks(self):
        try:
            subprocess.run('docker stack ls', check=True, shell=True)
        except subprocess.CalledProcessError as e:
            print('SwarmDriver - get_stacks exception: %s' % e)

    def deploy(self, requestUUID, dep_dict, stack_name):
        try:
            # configure the labels in the services
            swarm_spec = dep_dict['spec']
            swarm_services = dep_dict['spec']['services']
            comp_preferences = dep_dict['comp_preferences']

            for s, info in swarm_services.items():
                nodeIP = comp_preferences.get(s)
                if(nodeIP != None):
                    dep_dict['spec']['services'][s] = add_placement_specs(copy.deepcopy(info), IP, nodeIP, PREFERRED)

            # create the stack
            yamlName = requestUUID + '.yaml'
            compose_file_path = os.path.join(SWARM_DEPL_DIR, yamlName)
            with open(compose_file_path, 'w') as yaml_file:
                yaml.dump(swarm_spec, yaml_file, default_flow_style=False)
            
            subprocess.run('docker stack deploy --compose-file %s --orchestrator swarm %s' %(compose_file_path, stack_name), check=True, shell=True)
            print('SwarmDriver - stack %s created' %(stack_name))
            return 201
        except subprocess.CalledProcessError as e:
            print('SwarmDriver - deployment exception: %s' % e)
            return 400

    # delete stack by name
    def delete_stack(self, name):
        try:
            print('Swarm Driver name: %s' %(name))
            subprocess.run('docker stack rm %s --orchestrator swarm' %(name), check=True, shell=True)
            return 201
        except subprocess.CalledProcessError as e:
            print('SwarmDriver - termination of %s exception: %s' % (name, e))
            return 400