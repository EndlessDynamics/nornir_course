import logging
from nornir import InitNornir
from nornir.core.filter import F
from nornir.plugins.functions.text import print_result  # noqa
from nornir.plugins.tasks.networking import netmiko_send_command

logger = logging.getLogger("nornir")


def main():

    nr = InitNornir(config_file="config.yaml")
    ios_filt = F(groups__contains="ios")
    nr = nr.filter(ios_filt)

    logger.info("Testing...")
    logger.info("Testing...")
    logger.info("Testing...")

    # Set one of the devices to an invalid password
    nr.inventory.hosts["cisco3"].password = "bogus"
    my_results = nr.run(
        task=netmiko_send_command, command_string="show ip int brief"
    )  # noqa


if __name__ == "__main__":
    main()
