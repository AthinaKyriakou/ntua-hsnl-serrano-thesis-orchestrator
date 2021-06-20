# post a yaml file to flask endpoint
import requests
import sys
from src.config import flask_cfg, DEPLOY_ACTION
import os

def main():
    print('deploy')
    args = sys.argv[1:]
    if len(args) == 4 and args[0] == '-yamlSpec' and args[2] == '-env':
        yamlSpec = args[1]
        env = args[3]
        with open(yamlSpec) as fp:
            content = fp.read()
            postPath = None
            if(env == 'local'):
                # for local dev
                postPath = os.path.join(flask_cfg['endpoint_local'], DEPLOY_ACTION)
            elif(env == 'prod'):
                # for prod
                postPath = os.path.join(flask_cfg['endpoint_prod'], DEPLOY_ACTION)
            print('deploy to postPath: ', postPath)
            response = requests.post(postPath, data=content)
            print('deploy -', response)
    else:
        print('Use: python3 deploy.py -yamlSpec <absolute_local_file_path> -env <local/prod>')

if __name__ == '__main__':
    main()
