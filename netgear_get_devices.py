from pynetgear import Netgear
import json
import time
import queue
import sys

PASSWORD = ''
DEVICES = 'devices'
LABEL = 'label'
NAME = 'name'
MAC = 'mac'


def get_config_devices():
    config_devices = []
    with open('config.json') as config_json:
        config = json.load(config_json)
        if len(config[DEVICES]) == 0:
            print("No devices in config file")
            sys.exit()
        for device in config[DEVICES]:
            config_devices.append((device[LABEL], device[NAME], device[MAC]))

    return config_devices

def get_attached_devices(netgear):
    # sample response:
    # Device(signal=100, ip='10.0.0.5', name='eth4mbp', mac='DC:A9:04:75:34:ED', type='wireless', link_rate=263, allow_or_block='Allow', device_type=None, device_model=None, ssid=None, conn_ap_mac=None)
    attached_devices = []
    for device in netgear.get_attached_devices():
        attached_devices.append((device[2], device[3]))

    if len(attached_devices) == 0:
        print("No devices online")
        sys.exit()
    return attached_devices


def check(config_devices, attached_devices):
    print(config_devices)
    print(attached_devices)


def main():
    netgear = Netgear(password=PASSWORD)
    check(get_config_devices(), get_attached_devices(netgear))

if __name__ == "__main__":
    main()

