# -*- coding: utf-8 -*-
"""
Created on Sun Sep 20 21:55:20 2020

@author: Mai Tai
"""

import pyvisa
import time
import numpy as np
from ..ports import find_ports

rm = pyvisa.ResourceManager()
name = "PowerMeter"
hwid = ["0403:6011"]


def test_port(name):
    Pmeter = rm.open_resource(f'ASRL/dev/{name}::INSTR')
    try:
        Pread = Pmeter.query("*READPOWER:")
        PowerPM = float(Pread.split('e')[0].split('+')[1])
        return True
    except:
        return False


def get_devices():
    devices_all = find_ports()
    return [device for device in devices_all if test_port(device.name)]


class instrument:
    def __init__(self, port):

        self.Pmeter = rm.open_resource(
            f'ASRL/dev/{port.name}::INSTR')  # HARDCODING BAD BUT NECESSARY: SEE BELOW #Just use tty0, I'll add the test in later
        """
        IMPORTANT: Linux enumerates tty ports willy-nilly and pyvisa hates finding symlinks in /dev/tty so getting fancy with udev is a no-go.
        If ever this module appears to be broken, use pyvisa to query each resource with "*READPOWER:"
        until you get a response. Once the correct path string has been determined, replace the string in rm.open_resources() above
        accordingly.
        """

    def Power(self) -> float:
        """Reads power from Gentec TPM300 via VISA commands
        The while loop avoids outputting invalid token
        >>>returns float

        to-do: incorporate different power ranges (itteratively check all avaliable
        ranges and chose the best fit. Log this choice)"""

        while True:
            try:
                Pread = self.Pmeter.query("*READPOWER:")
                PowerPM = float(Pread.split('e')[0].split('+')[1])
                return PowerPM
            except:
                continue

    def PowAvg(self):
        P = []
        for i in range(0, 5, 1):
            p = self.Power()
            P.append(p)
            time.sleep(1)
        PowerAvg = np.mean(P)
        PowerStd = np.std(P)
        return PowerAvg, PowerStd
