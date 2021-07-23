#!/usr/bin/env python3

# KEY_DELAY = 0.03   # default 0.03 - fastest thru wombat
KEY_DELAY = 0.03

# RETURN_DELAY = additional pause after return key  # use 0.4 for 1 mhz iie at basic prompt
RETURN_DELAY = 0  

# PORT = "/dev/cu.usbserial-AH06S2CK" # whatever your device port is in /dev/ is
PORT = "/dev/cu.usbserial-D309F5OT"

# BAUD = However the Hagstrom device is configured 
BAUD = 19200

# Hagstrom device mode (ASC232, USBtoUSB)
hagstrom_keynumber_mode = True

# Pi USB gadget mode (NOT YET IMPLEMENTED)
pi_gadget_mode = False


