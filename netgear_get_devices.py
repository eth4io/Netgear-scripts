from pynetgear import Netgear
import json
import time
import queue
import sys

ROUTER_ADMIN_PASSWORD = 'router_admin_password'
DEVICES = 'devices'
LABEL = 'label'
NAME = 'name'
MAC = 'mac'


class Device:
    def __init__(self, mac, label = '', name = '', is_attached = False):
        self.label = label
        self.name = name
        self.mac = mac
        self.is_attached = is_attached
    def __eq__(self, other):
        if isinstance(other, Device):
            return self.mac == other.mac
        return false
    def __str__(self):
        return self.label + ", " + self.name + ", " + self.mac + ", " + str(self.is_attached)


def get_router_admin_password():
    with open('config.json') as config_json:
        config = json.load(config_json)
        return config[ROUTER_ADMIN_PASSWORD]

def get_config_devices():
    config_devices = []
    with open('config.json') as config_json:
        config = json.load(config_json)
        if len(config[DEVICES]) == 0:
            print("No devices in config file")
            sys.exit()
        for device in config[DEVICES]:
            config_devices.append(Device(mac = device[MAC], label = device[LABEL],
                name = device[NAME]))

    return config_devices

def get_attached_devices(netgear):
    # sample response:
    # Device(signal=100, ip='10.0.0.5', name='eth4mbp', mac='DC:A9:04:75:34:ED', type='wireless', link_rate=263, allow_or_block='Allow', device_type=None, device_model=None, ssid=None, conn_ap_mac=None)
    attached_devices = []
    for device in netgear.get_attached_devices():
        attached_devices.append(Device(mac = device[3], name = device[2], is_attached = True))

    if len(attached_devices) == 0:
        print("No devices online")
        sys.exit()
    return attached_devices


def check(config_devices, attached_devices):
    for device in config_devices:
        if device in attached_devices:
            device.is_attached = True
    return config_devices




def main():
    netgear = Netgear(password=get_router_admin_password())
    config_devices = check(get_config_devices(), get_attached_devices(netgear))

    for device in config_devices:
        if device.is_attached:
            print(device.label + ": Online" )
        else:
            print(device.label + ": Offline" )


if __name__ == "__main__":
    main()

