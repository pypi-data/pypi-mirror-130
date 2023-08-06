from subprocess import Popen

import click
import typing
from chattyraspi.client import Client
from chattyraspi.device import DevicesConfiguration


@click.command()
@click.option('--config-file', help='configuration file', required=True)
@click.option('--on-cmd', help='Script to run when the device is on', required=True)
@click.option('--off-cmd', help='Script to run when the device is off', required=True)
@click.option('--is-on-cmd', help='Script that returns nonzero in case of the `on-cmd` script has been run')
@click.option('--shell', help='Shell to run the command, default `/bin/sh -c`', default='/bin/sh -c')
def main(config_file: str, on_cmd: str, off_cmd: str, shell: str, is_on_cmd: typing.Optional[str] = None):
    config = DevicesConfiguration(config_file)
    client = Client(config)

    config.get_configuration()
    statuses = dict()

    def _turn_on(device_id: str):
        print('Device {} turned ON'.format(device_id))
        retval = _run_cmd(on_cmd)
        if not retval:
            statuses[device_id] = True

    def _turn_off(device_id: str):
        print('Device {} turned OFF'.format(device_id))
        retval = _run_cmd(off_cmd)
        if not retval:
            statuses[device_id] = False

    def _fetch_is_power_on(device_id: str) -> bool:
        print('Device {} requested power status'.format(device_id))
        if is_on_cmd:
            retval = _run_cmd(is_on_cmd)
            status = not retval
        else:
            status = statuses[device_id]
        print('Returning', status)
        return status

    _start_listening(_fetch_is_power_on, _turn_off, _turn_on, client, config, statuses)

    def _run_cmd(cmdline: str):
        r = shell.split(' ')
        r.append(cmdline)
        return Popen(r)


def _start_listening(_fetch_is_power_on, _turn_off, _turn_on, client, config, statuses):
    for device_id in map(lambda d: d['device_id'], config.get_configuration()['Devices']):
        statuses[device_id] = False
        client.set_on_turn_on(device_id, _turn_on)
        client.set_on_turn_off(device_id, _turn_off)
        client.set_fetch_is_power_on(device_id, _fetch_is_power_on)
    client.listen()
