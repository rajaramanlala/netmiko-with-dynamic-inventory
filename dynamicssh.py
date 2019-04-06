import netmiko
from myhelper import read_yaml, form_connection_params_from_yaml
import logging

#logging.basicConfig(filename='dynamic.log', level=logging.DEBUG)
#logger = logging.getLogger("netmiko")

#SITE_NAME = "SJ-HQ"

path = raw_input("Enter the name of command file:")
COMMANDS_LIST = open(path).readlines()


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
       #print(hostname)
        connection = netmiko.ConnectHandler(**device)
        output = ["{0} {1} {0}".format("-" * 10, hostname)]

        for command in commands:
           # print(command)
            command_result = connection.send_command(command, delay_factor=10)
            #print(command_result)
            output.append("{0}".format(command))
            output.append(command_result)

        output_result = "\n".join(output)
        connection.disconnect()
        yield output_result


def main():
    parsed_yaml = read_yaml()
    connection_params = form_connection_params_from_yaml(parsed_yaml)
    for device_output in collect_outputs(connection_params, COMMANDS_LIST):
        print(device_output)


if __name__ == "__main__":
    main()
