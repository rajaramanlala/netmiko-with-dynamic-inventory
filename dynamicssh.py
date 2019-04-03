import netmiko
from myhelper import read_yaml, form_connection_params_from_yaml
import logging

logging.basicConfig(filename='dynamic.log', level=logging.DEBUG)
logger = logging.getLogger("netmiko")

#SITE_NAME = "SJ-HQ"

COMMANDS_LIST = [
     "show bgp summary"
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
        #hostname = device.pop("hostname")
        connection = netmiko.ConnectHandler(**device)
        #device_result = ["{0} {1} {0}".format("=" * 20)]

        for command in commands:
            command_result = connection.send_command(command, delay_factor=10)
            #print(command_result)
            #device_result.append("{0} {1} {0}".format("=" * 20, command))
            #device_result.append(command_result)

        #device_result_string = "\n\n".join(device_result)
        connection.disconnect()
        yield command_result


def main():
    parsed_yaml = read_yaml()
    connection_params = form_connection_params_from_yaml(parsed_yaml)
    for command_result in collect_outputs(connection_params, COMMANDS_LIST):
        print(command_result)


if __name__ == "__main__":
    main()
