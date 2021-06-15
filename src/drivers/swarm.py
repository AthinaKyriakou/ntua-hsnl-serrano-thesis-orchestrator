import docker
import yaml
import os
import subprocess
from src.config import SWARM_DEPL_DIR

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

    # check if a docker file is needed for custom images
    def deploy(self, dep_dict):
        try:
            # TODO: pass into configuration file + put UUID in file name
            compose_file_path = os.path.join(SWARM_DEPL_DIR, 'test.yaml')
            with open(compose_file_path, 'w') as yaml_file:
                yaml.dump(dep_dict, yaml_file, default_flow_style=False)
            stack_name = 'stack_name'
            subprocess.run('docker stack deploy --compose-file %s --orchestrator swarm %s' %(compose_file_path, stack_name), check=True, shell=True)
            print('SwarmDriver - stack %s created' %(stack_name))
            return 201
        except subprocess.CalledProcessError as e:
            print('SwarmDriver - deployment exception: %s' % e)
            return 400