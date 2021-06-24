import yaml
from rot_algorithm import dummy_algorithm

#/home/athina/python-virtual-environments/thesis/bin/python /home/athina/Desktop/thesis/code/ntua_diploma_thesis/serrano_app/src/resource_optimization_toolkit/test.py

def main():

    # test of dummy algorithm
    with open('/home/athina/Desktop/thesis/code/ntua_diploma_thesis/serrano_app/app.yaml') as f:
        yamlSpec = yaml.safe_load(f)
    updated_yamlSpec = dummy_algorithm(yamlSpec)
    print('\n\n@@@@ UPDATED YAML SPEC @@@')
    print(updated_yamlSpec)

if __name__ == '__main__':
    main()