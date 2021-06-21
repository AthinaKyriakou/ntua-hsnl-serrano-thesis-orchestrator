# remove a deployment / stack by requestUUID
import requests
import sys
from src.config import flask_cfg, REMOVE_ACTION
import os

def main():
    print('remove')
    args = sys.argv[1:]
    if len(args) == 4 and args[0] == '-requestUUID' and args[2] == '-env':
        requestUUID = args[1]
        env = args[3]
        postPath = None
        if(env == 'local'):
            # for local dev
            postPath = os.path.join(flask_cfg['endpoint_local'], REMOVE_ACTION)
        elif(env == 'prod'):
            # for prod
            postPath = os.path.join(flask_cfg['endpoint_prod'], REMOVE_ACTION)
        print('remove to postPath: ', postPath)
        response = requests.post(postPath, data=requestUUID)
        print('remove -', response)
    else:
        print('Use: python3 remove.py -requestUUID <requestUUID> -env <local/prod>')

if __name__ == '__main__':
    main()
