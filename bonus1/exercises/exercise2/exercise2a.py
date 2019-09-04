import os
from nornir import InitNornir
from nornir.core.filter import F
from nornir.plugins.tasks import networking
from nornir.plugins.functions.text import print_result


PASSWORD = os.environ.get("NORNIR_PASSWORD", None)  # for testing purposes


def transform_ansible_inventory(host):
    host.password = PASSWORD or host["ansible_ssh_pass"]
    if "nxos" in host.groups:
        netmiko_params = host.get_connection_parameters("netmiko")
        netmiko_params.platform = "cisco_nxos"
        host.connection_options["netmiko"] = netmiko_params
    elif "cisco" in host.groups:
        netmiko_params = host.get_connection_parameters("netmiko")
        netmiko_params.platform = "cisco_ios"
        host.connection_options["netmiko"] = netmiko_params
    elif "arista" in host.groups:
        netmiko_params = host.get_connection_parameters("netmiko")
        netmiko_params.platform = "arista_eos"
        netmiko_params.extras["global_delay_factor"] = 4
        host.connection_options["netmiko"] = netmiko_params
    elif "juniper" in host.groups:
        netmiko_params = host.get_connection_parameters("netmiko")
        netmiko_params.platform = "juniper_junos"
        host.connection_options["netmiko"] = netmiko_params


def main():
    nr = InitNornir(config_file="config_a.yaml")
    nr = nr.filter(~F(name__contains="localhost"))
    agg_result = nr.run(
        task=networking.netmiko_send_command, command_string="show version"
    )
    print_result(agg_result)


if __name__ == "__main__":
    main()