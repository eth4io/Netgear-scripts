from pynetgear import Netgear

netgear = Netgear(password='enlightenedBAF7890')

#for i in netgear.get_attached_devices():
#    print(i)

traffic = netgear.get_traffic_meter()
print(traffic)
