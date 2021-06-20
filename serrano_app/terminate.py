# terminate a deployment / stack by requestUUID
import requests
import sys
from src.config import flask_cfg, TERMINATE_ACTION
import os

def main():
    print('terminate')
    args = sys.argv[1:]
    if len(args) == 4 and args[0] == '-requestUUID' and args[2] == '-env':
        requestUUID = args[1]
        env = args[3]
        deployPath = os.path.join(TERMINATE_ACTION, requestUUID)
        postPath = None
        if(env == 'local'):
            # for local dev
            postPath = os.path.join(flask_cfg['endpoint_local'], deployPath)
        elif(env == 'prod'):
            # for prod
            postPath = os.path.join(flask_cfg['endpoint_prod'], deployPath)
        print('postPath: ', postPath)
        response = requests.post(postPath, data=requestUUID)
        print('terminate -', response)
    else:
        print('Use: python3 terminate.py -requestUUID <requestUUID> -env <local/prod>')

if __name__ == '__main__':
    main()
