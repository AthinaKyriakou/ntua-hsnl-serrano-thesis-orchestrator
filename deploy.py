# post a yaml file to flask endpoint
import requests
        
def main():
    print('deploy - dummy yaml deployment')
    with open('/home/athina/Desktop/thesis/code/ntua_diploma_thesis/app-swarm.yaml') as fp:
        content = fp.read()
        response = requests.post('http://127.0.0.1:5000/deploy/app-swarm.yaml', data=content)
    print(response)

if __name__ == "__main__":
    main()