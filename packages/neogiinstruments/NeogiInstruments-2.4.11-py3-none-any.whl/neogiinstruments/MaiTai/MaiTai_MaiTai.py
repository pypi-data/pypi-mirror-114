# -*- coding: utf-8 -*-
"""
Created on Mon Sep 21 11:29:27 2020

@author: Mai Tai
"""
import panel.widgets
import pyvisa
from time import sleep

name = "MaiTai"
hwid = ["10C4:EA60"]
serial_number = ["0001"]


class instrument:
    OnButton = panel.widgets.Button(name="On")
    OffButton = panel.widgets.Button(name="Off")

    def __init__(self, port):
        rm = pyvisa.ResourceManager()
        current_port = port.name
        self.MaiTai = rm.open_resource(f'ASRL/dev/{current_port}::INSTR')
        self.MaiTai.baud_rate = 115200
        self.OnButton.on_click(self.On)
        self.OffButton.on_click(self.Off)
    def Shutter(self, val=0):
        '''Returns print string'''
        if val == 1:
            self.MaiTai.write("SHUT 1")
            # print("Shutter Opened")
        else:
            self.MaiTai.write("SHUT 0")
            # print("Shutter Closed")

    def Get_Wavelength(self):
        """Helper function for instrumental to avoid clutter and make code
        more readable
        returns int"""

        w = int(self.MaiTai.query("WAV?").split('n')[0])
        return w

    def Set_Wavelength(self, position):
        """Helper function for instrumental to avoid clutter and make code
        more readable
        Note that this function always shutters the laser
        returns null"""
        if 690 <= position <= 1040:
            self.Shutter(0)
            self.MaiTai.write(f"WAV {position}")
            sleep(10)
        else:
            print('Invalid Wavelength')

    def On(self, event=None):
        self.MaiTai.write('ON')
        n = 0
        while n < 100:
            n = self.CheckWarm()
            print(f"{n}% warmed up")

    def Off(self, event=None):
        self.Shutter(0)
        self.MaiTai.write("OFF")

    def CheckWarm(self):
        return self.MaiTai.query('PCTW?').split("%")[0]

    def CheckStatus(self):
        status_byte = int(self.MaiTai.query('*STB?').split('n')[0])
        if status_byte == 1:
            print('Emission is possible')
        elif status_byte == 2:
            print('MaiTai is modelocked')
        elif status_byte == 3:
            print('Emission is possible and MaiTai is modelocked')
        elif status_byte == 4:
            print('The shutter is open')
        elif status_byte == 5:
            print('Emission is possible and the shutter is open')
        elif status_byte == 6:
            print('MaiTai is modelocked and the shutter is open')
        elif status_byte == 7:
            print('Emission is possible, MaiTai is modelocked, and the shutter is open')
        elif status_byte == 8:
            print('A warning is active')
        elif status_byte == 16:
            print('A falut condition exists')

        # elif status_
        else:
            print('Unknown status byte returned, contact Spectra-Physics support')

        return status_byte

    def widgets(self):
        return panel.Column(self.OffButton, self.OnButton)
