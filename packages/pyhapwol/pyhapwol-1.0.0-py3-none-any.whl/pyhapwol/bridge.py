from .switch import Switch
from logging import info
from pyhap.accessory import Bridge
from pyhap.accessory_driver import AccessoryDriver
from pyhapwol import __version__
from re import match
from signal import signal, SIGTERM
from sys import exit, stderr


def start(config, persist_file):
    """Initialize and start WoL service for HomeKit."""
    if not __validate_config(config):
        print('Invalid configuration.\n', file=stderr)
        exit(1)

    driver = AccessoryDriver(port=51826, persist_file=persist_file)
    bridge = Bridge(driver, 'Bridge')
    bridge.set_info_service(str(__version__), 'RabelCraft', 'PyHAP Bridge',
                            'BR-WoL-01')

    for item in config:
        info('Initializing switch for %s [%s]', item['name'], item['mac'])
        bridge.add_accessory(Switch(item, driver, item['name']))

    driver.add_accessory(accessory=bridge)

    signal(SIGTERM, driver.signal_handler)
    driver.start()


def __validate_config(config):
    if len(config) < 1:
        return False
    for item in config:
        if 'name' not in item:
            print('name is missing\n', file=stderr)
            return False
        if 'mac' not in item:
            print('mac is missing\n', file=stderr)
            return False
        if not match(r'^([a-f0-9]{2}:){5}[a-f0-9]{2}$', item['mac'].lower()):
            print('bad mac format\n', file=stderr)
            return False
        if 'broadcast' not in item:
            print('broadcast is missing\n', file=stderr)
            return False
        if not match(r'^([0-9]{1,3}\.){3}[0-9]{1,3}/[0-9]+$',
                     item['broadcast']):
            print('bad broadcast format\n')
            return False
        if 'ip' in item:
            if not match(r'^([0-9]{1,3}\.){3}[0-9]{1,3}$', item['ip']):
                print('bad ip format\n', file=stderr)
                return False
        if 'port' in item:
            if not match(r'^[0-9]+$', str(item['port'])):
                print('bad port format\n', file=stderr)
                return False
    return True
