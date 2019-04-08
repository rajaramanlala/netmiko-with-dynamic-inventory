import netmiko
from myhelper import read_yaml, form_connection_params_from_yaml
import logging

logging.basicConfig(filename='dynamic.log', level=logging.DEBUG)
logger = logging.getLogger("netmiko")


#path = input("Enter the name of command file:")
COMMANDS_LIST = [
      "show config | display set | no-more"
]


def collect_outputs(devices, commands):
    """
    Collects commands from the dictionary of devices
    Args:
        devices (dict): dictionary, where key is the hostname, value is
            netmiko connection dictionary
        commands (list): list of commands to be executed on every device
    Returns:
        dict: key is the hostname, value is string with all outputs
    """
    for device in devices:
        hostname = device.pop("hostname")
        connection = netmiko.ConnectHandler(**device)
        print(hostname)

        for command in commands:
            print(command)
            command_result = connection.send_command(command, delay_factor=10)
            with open(hostname , "a") as f:
                 f.write(command)
                 f.write(command_result)
                 connection.disconnect
                 yield command_result

def getdevicename(parsed_yaml):
     parsed_yaml = read_yaml()
     for site_dict in parsed_yaml["all"]["sites"]:
         for host in site_dict["hosts"]:
              device_name = host.get('hostname')
              yield device_name


def main():
    parsed_yaml = read_yaml()
    connection_params = form_connection_params_from_yaml(parsed_yaml)
    for device_output in collect_outputs(connection_params, COMMANDS_LIST):
        #print(device_output)  
        print("Capturing output to a file named after device in your local directory")
              

if __name__ == "__main__":
    main()
