# This file was auto generated; Do not modify, if you value your sanity!
import ctypes

try: # 1
    from ethernet_network_status_t import ethernet_network_status_t
except:
    from ics.structures.ethernet_network_status_t import ethernet_network_status_t

class ics_fire2_device_status(ctypes.Structure):
    _fields_ = [
        ('backupPowerGood', ctypes.c_uint8), 
        ('backupPowerEnabled', ctypes.c_uint8), 
        ('usbHostPowerEnabled', ctypes.c_uint8), 
        ('ethernetActivationLineEnabled', ctypes.c_uint8), 
        ('ethernetStatus', ethernet_network_status_t), 
    ]

# Extra names go here:
icsFire2DeviceStatus = ics_fire2_device_status
# End of extra names

