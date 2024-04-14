#!/usr/bin/env python3

# Simple tool to switch the Creative BT-W5 Bluetooth Audio dongle between AptX Adaptive **Low Latency** or **High Quality** mode.
# Of course, only works with Bluetooth headphones that support AptX Adaptive, such as the Tranya X3
# Reverse engineered based on communication between Creative's desktop app for Windows and the BT-W5
# Might also set other settings as a whole config data array is sent without taking account the existing config.
#
# Usage: sudo ./btw5-switch.py ll  (for low-latency mode)
#        sudo ./btw5-switch.py hq  (for high-quality mode)
#
# requires either sudo or adjusting the permissions on the /dev/bus/usb/... device

import sys
import usb.core

dev = usb.core.find(idVendor=0x041e, idProduct=0x3130)
if dev is None:
    raise ValueError('Device not found')

cfg = dev[0]
intf = cfg[(0, 0)]
ep = intf[0]
i = intf.bInterfaceNumber

if dev.is_kernel_driver_active(i):
    dev.detach_kernel_driver(i)

data_hq = [0x03, 0x5a, 0x6b, 0x03, 0x0a, 0x03, 0x40]  # HQ
data_ll = [0x03, 0x5a, 0x6b, 0x03, 0x0a, 0x03, 0x20]  # LL
if len(sys.argv) > 1 and sys.argv[1] == "hq":
    data = data_hq
    print("Enabling AptX Adaptive High Quality mode")
else:
    data = data_ll
    print("Enabling AptX Adaptive Low Latency mode")
data += [0x00] * (65 - len(data))
result = dev.ctrl_transfer(0x21, 0x09, wValue=0x203, wIndex=0x00, data_or_wLength=data)
