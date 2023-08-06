# -*- coding: utf-8 -*-
"""
Created on Mon Sep 21 11:21:23 2020

@author: Mai Tai
"""

import nidaqmx
from nidaqmx.constants import TerminalConfiguration
import numpy as np

'''Needs to be rewritten in class structure'''

name = "Photodiode"
hwid = ["software"]


def get_devices(dev="Dev1"):
    devices_all = nidaqmx.system.Device(dev).ai_physical_chans
    devices = [device.name for device in devices_all]
    '''
    for device in devices_all:
        with nidaqmx.Task() as task:
            task.ai_channels.add_ai_voltage_chan(device.name)
            r = task.read(number_of_samples_per_channel=1000)
            if np.mean(r) > 0:
                devices.append(device)
    #if you wantecd to test devices
    '''
    return devices


class instrument():
    def __init__(self, port):
        self.name = port
        pass

    def gather_data(self):
        with nidaqmx.Task() as task:
            self.ai_channel = task.ai_channels.add_ai_voltage_chan(self.name)
            r = task.read(number_of_samples_per_channel=1000)
            m = np.mean(r)
            delta = np.std(r)
            return m, delta
