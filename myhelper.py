import yaml
import os

#SITES = {"sjc": 1, "bru": 2}

#DEVICE_TYPES = {"csr1000v": 1, "iosv-l2": 2}

#DEVICE_ROLES = {"access": 1, "edge": 2, "core": 3}

#site_name="opc"

path="inventory.yml"

def read_yaml(path="inventory.yml"):
     with open(path) as f:
          yaml_content = yaml.load(f.read())
          return yaml_content

def form_connection_params_from_yaml(parsed_yaml):
    global_params = parsed_yaml["all"]["vars"]
    found = False
    for site_dict in parsed_yaml["all"]["sites"]:
        for host in site_dict["hosts"]:
                #print(host)
                host_dict = {}
                if "device_type_netmiko" in host:
                    host["device_type"] = host.pop("device_type_netmiko")
                host_dict.update(global_params)
                host_dict.update(host)
                host_dict.pop("device_role")
                host_dict.pop("hostname")
                found = True
                yield host_dict

#if site_name is not None and not found:
   #raise KeyError(
     # "Site {} is not specified in inventory YAML file".format(site_name)
   #)   

#def main():
#parsed_yaml = read_yaml()
#connection_params = form_connection_params_from_yaml(parsed_yaml, site_name="opc")
#print(connection_params)
