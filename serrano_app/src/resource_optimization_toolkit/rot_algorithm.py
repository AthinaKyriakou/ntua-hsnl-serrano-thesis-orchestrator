import requests
import os
import ast
import copy
import sys

import yaml
from config import telemetry_cfg, dummy_algorithm_cfg, SWARM, K8s
from src.resource_optimization_toolkit.helpers import TelemetryHandlerException, CustomException

## ONLY FOR TEST
#from helpers import TelemetryHandlerException, CustomException
# import from parent dir: https://codeolives.com/2020/01/10/python-reference-module-in-parent-directory/
#import inspect
#currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
#parentdir = os.path.dirname(currentdir)
#sys.path.insert(0, parentdir)
#from config import telemetry_cfg, dummy_algorithm_cfg, SWARM, K8s

def get_site_info(siteID):
    # call to the telemetry endpoint to get info about the available sites
    postPath = os.path.join(telemetry_cfg['endpoint'], telemetry_cfg['node.uri'])
    postPath = os.path.join(postPath, siteID)
    res = requests.get(postPath)
    return res

def get_sites_info():
    # call to the telemetry endpoint to get info about the available sites
    postPath = os.path.join(telemetry_cfg['endpoint'], telemetry_cfg['clusters.uri'])
    print('telemetry post to postPath: %s' %(postPath))
    res = requests.get(postPath)
    return res

def normalized_value(dval, min_observed, max_observed):
    val = (dval - min_observed)/(max_observed - min_observed)
    return val

def criterion_value(weight_RAM, weight_storage, available_RAM, app_RAM, min_RAM, max_RAM, available_storage, app_storage, min_storage, max_storage):
    normalized_RAM = normalized_value(available_RAM - app_RAM, min_RAM, max_RAM)
    normalized_storage = normalized_value(available_storage - app_storage, min_storage, max_storage)
    val = (weight_RAM * normalized_RAM + weight_storage * normalized_storage)/(weight_RAM + weight_storage)
    return val

def find_site(sites_dict, yamlSpec):
    print('Resource Optimization Toolkit - rot_algorithm - choose site')
    #print(sites_dict)
    
    # find max RAM and storage values for normalization
    max_RAM = 0
    max_storage = 0

    for siteID, siteInfo in sites_dict.items():
        site_available_RAM = 0
        site_available_storage = 0

        for w in siteInfo['worker_nodes']:
            site_available_RAM = site_available_RAM + w['available_ram_GB']
            site_available_storage = site_available_storage + w['available_storage_GB']
        if(site_available_RAM > max_RAM):
            max_RAM = site_available_RAM
        if(site_available_storage > max_storage):
            max_storage = site_available_storage
        print('Site %s: available RAM: %s, available storage: %s' % (siteID, site_available_RAM, site_available_storage))

    #print('max_RAM_GB: %s - max_storage_GB: %s' %(max_RAM, max_storage))

    # find optimal site
    app_cores = yamlSpec['appCores']
    app_RAM = yamlSpec['appRAMGB']
    app_storage = yamlSpec['appStorageGB']
    weight_RAM = dummy_algorithm_cfg['weight_RAM']
    weight_storage = dummy_algorithm_cfg['weight_storage']
    max_value = 0
    found_siteID = None
    
    for siteID, siteInfo in sites_dict.items():
        site_cores = siteInfo['total_cpus']
        site_available_RAM = 0
        site_available_storage = 0

        for w in siteInfo['worker_nodes']:
            site_available_RAM = site_available_RAM + w['available_ram_GB']
            site_available_storage = site_available_storage + w['available_storage_GB']
        
        # if the site has enough total cores, RAM and storage for the app
        if(site_cores >= app_cores and site_available_RAM > app_RAM and site_available_storage > app_storage):
            site_val = criterion_value(weight_RAM, weight_storage, site_available_RAM, app_RAM, 0, max_RAM, site_available_storage, app_storage, 0, max_storage)
            if(site_val > max_value):
                max_value = site_val
                found_siteID = siteID

    return found_siteID

def set_node_preferences(yamlSpec, site_dict):
    
    print('Resource Optimization Toolkit - rot_algorithm - set node preferences per service')
    app_comp_reqs = yamlSpec['app_comp_reqs']

    # find the max values for normalization
    max_comp_RAM = 0
    min_comp_RAM = sys.float_info.max
    max_comp_storage = 0
    min_comp_storage = sys.float_info.max

    for comp,info in app_comp_reqs.items():
        comp_RAM = info['RAMGB']
        comp_storage = info['storageGB']
        if(comp_RAM > max_comp_RAM):
            max_comp_RAM = comp_RAM
        if(comp_RAM < min_comp_RAM):
            min_comp_RAM = comp_RAM
        if(comp_storage > max_comp_storage):
            max_comp_storage = comp_storage
        if(comp_storage < min_comp_storage):
            min_comp_storage = comp_storage

    # find the criterion values per component
    weight_RAM = dummy_algorithm_cfg['weight_RAM']
    weight_storage = dummy_algorithm_cfg['weight_storage']
    comp_values_list = []
    for comp,info in app_comp_reqs.items():
        comp_RAM = info['RAMGB']
        comp_storage = info['storageGB']
        val = criterion_value(weight_RAM, weight_storage, comp_RAM, 0, min_comp_RAM, max_comp_RAM, comp_storage, 0, min_comp_storage, max_comp_storage)
        comp_values_list.append((comp,val))
    
    # sort in decreasing order
    comp_values_list = sorted(comp_values_list, key=lambda x: x[1], reverse=True)
    #print(comp_values_list)

    worker_nodes = {}
    for w in site_dict['worker_nodes']:
        ip = w['ip']
        worker_nodes[ip] = w
    #print(worker_nodes)
    
    # find max for normalization
    max_worker_RAM = 0
    max_worker_storage = 0
    for workerIP, workerInfo in worker_nodes.items():
        w_RAM = workerInfo['available_ram_GB']
        w_storage = workerInfo['available_storage_GB']
        if(w_RAM > max_worker_RAM):
            max_worker_RAM = w_RAM
        if(w_storage > max_worker_storage):
            max_worker_storage = w_storage

    yamlSpec['comp_preferences'] = {}
    for t in comp_values_list:
        comp = t[0]
        comp_workerIP = None
        comp_RAM = app_comp_reqs[comp]['RAMGB']
        comp_storage = app_comp_reqs[comp]['storageGB']
        comp_cores = app_comp_reqs[comp]['cores']
        best_val = 0
        
        for workerIP, workerInfo in worker_nodes.items():
            w_RAM = workerInfo['available_ram_GB']
            w_storage = workerInfo['available_storage_GB']
            w_cores = workerInfo['cpu_cores']

            if(w_RAM > comp_RAM and w_storage > comp_storage and  w_cores >= comp_cores):
                val = criterion_value(weight_RAM, weight_storage, w_RAM, comp_RAM, 0, max_worker_RAM, w_storage, comp_storage, 0, max_worker_storage)
                
                if (val > best_val):
                    best_val = val
                    comp_workerIP = workerIP
        
        if(comp_workerIP != None):
            # set the worker IP for the component and reduce available RAM and storage
            yamlSpec['comp_preferences'][comp] = comp_workerIP
            worker_nodes[comp_workerIP]['available_ram_GB'] = worker_nodes[comp_workerIP]['available_ram_GB'] - comp_RAM
            worker_nodes[comp_workerIP]['available_storage_GB'] = worker_nodes[comp_workerIP]['available_storage_GB'] - comp_storage

def dummy_algorithm(yamlSpec):
    print('Resource Optimization Toolkit - rot_algorithm - get sites telemetry info')
    
    ret_sites = get_sites_info()
    if(ret_sites.status_code != 200):
        print('Resource Optimization Toolkit - rot_algorithm - call to the Telemetry Handler failed')
        raise TelemetryHandlerException('Get request to Telemetry Handler API failed with status code: %s' %(ret_sites.status_code))
    general_sites_dict = ast.literal_eval(ret_sites.content.decode('utf-8'))

    if(general_sites_dict == None):
        raise TelemetryHandlerException('The Telemetry Handler found no available sites, empty returned dict!')

    # create a list of dicts, each dict is the info of a site
    detailed_sites_dict = {}
    for site in general_sites_dict['sites']:
        siteID = site['id']
        ret_siteID = get_site_info(siteID)
        if(ret_siteID.status_code != 200):
            print('Resource Optimization Toolkit - rot_algorithm - call to the Telemetry Handler failed')
            raise TelemetryHandlerException('Get request to Telemetry Handler API failed with status code: %s' %(ret_sites.status_code))
        siteID_dict = ast.literal_eval(ret_siteID.content.decode('utf-8'))
        detailed_sites_dict[siteID] = siteID_dict

    found_siteID = find_site(detailed_sites_dict, yamlSpec)
    if(found_siteID == None):
        raise CustomException('No site found to fulfill app requirements!')

    found_site_orchestrator = None
    for site in general_sites_dict['sites']:
        if(site['id'] == found_siteID):
            found_site_orchestrator = site['orchestrator']
            break

    print('Resource Optimization Toolkit - rot_algorithm - found site id %s, found site orchestrator %s' %(found_siteID, found_site_orchestrator))

    if(found_site_orchestrator == 'SWARM'):
        yamlSpec['orchestrator'] = SWARM
    
    elif(found_site_orchestrator == 'K8S'):
        yamlSpec['orchestrator'] = K8s
    
    else:
        raise CustomException('No configuration for %s local orchestrator' %(found_site_orchestrator))
    
    set_node_preferences(yamlSpec, detailed_sites_dict[found_siteID])    
    return yamlSpec