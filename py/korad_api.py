#!/usr/bin/python
# -*- coding: <encoding name> -*-
"""
Base level API for Korad PSU units.
Implemented as both:
    - A function style interface
    - An Object oriented style interface  
04 January-2019
"""

import serial as _serial
from numbers import Real as _Real
from typing import Dict as _Dict, Union as _Union
_ver_num = (0,0,1)
__version__ = '.'.join(map(str,_ver_num))

# port condifurations
KORAD_BAUD = 9600
KORAD_PARITY = _serial.PARITY_NONE
KORAD_DATA_BITS = _serial.EIGHTBITS
KORAD_STOP_BITS = _serial.STOPBITS_ONE
KORAD_DATA_FLOW_CTRL = False
KORAD_MAX_TIMEOUT = 100e-3  # max timeout in seconds 

# API CONSTANTS
KORAD_ID_CMD = b'*IDN?'
KORAD_STATUS_CMD = b'STATUS?'
KORAD_SAVE_CMD = lambda x: 'SAV{}'.format(x).encode('utf-8')
KORAD_RECALL_CMD = lambda x: 'RCL{}'.format(x).encode('utf-8')
KORAD_OCP_CMD = lambda x: 'OCP{}'.format(x).encode('utf-8')
KORAD_OUTPUT_CMD = lambda x: 'OUT{}'.format(x).encode('utf-8')
KORAD_VSET_CMD = lambda x, y: 'VSET{}:{}'.format(x,y).encode('utf-8')
KORAD_ISET_CMD = lambda x, y: 'ISET{}:{}'.format(x,y).encode('utf-8')
KORAD_VREAD_CMD = lambda x: 'VSET{}?'.format(x).encode('utf-8')
KORAD_IREAD_CMD = lambda x: 'ISET{}?'.format(x).encode('utf-8')
KORAD_VMEAS_CMD = lambda x: 'VOUT{}?'.format(x).encode('utf-8')
KORAD_IMEAS_CMD = lambda x: 'IOUT{}?'.format(x).encode('utf-8')

# OOP Interface

class Korad:
    """
    Korad abstraction object
    """
    def __init__(self,addr:str, timeout:float=KORAD_MAX_TIMEOUT):
        self.addr = addr
        self._port = _serial.serial_for_url(addr,
                                           baudrate=KORAD_BAUD,
                                           parity=KORAD_PARITY,
                                           rtscts=KORAD_DATA_FLOW_CTRL,
                                           dsrdtr=KORAD_DATA_FLOW_CTRL,
                                           timeout=timeout
                                           )
        self.id = self._identify()
    
    @property
    def status(self)->_Dict[str, _Union[bool,str]]:
        self._port.write(KORAD_STATUS_CMD)
        status = ord(self._port.readline().rstrip().decode('utf-8'))
        print('{0:08b}'.format(status))
        # parse status as described in notes:
        status_dict = {'output':bool(status&(1<<6)),
                       'mode':'CV' if status&1 else 'CC',
                       'ocp':bool(status&(1<<5)),
                       'v_out':self.measured_voltage(),
                       'i_out':self.measured_current(),
                       'v_set':self.configured_voltage(),
                       'i_set':self.configured_current(),
                       }
        return status_dict
    
    def _identify(self)->str:
        self._port.write(KORAD_ID_CMD)
        return self._port.readline().rstrip().decode('utf-8')
    
    def measured_voltage(self,ch=1):
        self._port.write(KORAD_VMEAS_CMD(ch))
        return float(self._port.readline().rstrip().decode('utf-8'))
    
    def measured_current(self,ch=1):
        self._port.write(KORAD_IMEAS_CMD(ch))
        return float(self._port.readline().rstrip().decode('utf-8'))
    
    def configured_voltage(self,ch=1):
        self._port.write(KORAD_VREAD_CMD(ch))
        return float(self._port.readline().rstrip().decode('utf-8'))
    
    def configured_current(self,ch=1):
        self._port.write(KORAD_IREAD_CMD(ch))
        return float(self._port.readline().rstrip().decode('utf-8'))
    
    def set_voltage(self,ch,voltage):
        self._port.write(KORAD_VSET_CMD(ch,voltage))
    
    def set_current(self,ch,current):
        self._port.write(KORAD_ISET_CMD(ch,current))
    
    def set_output(self,enable:bool):
        enable = 1 if enable else 0 
        self._port.write(KORAD_OUTPUT_CMD(enable))
    
    def save_settings(self,loc:int):
        self._port.write(KORAD_SAVE_CMD(loc))
    
    def recall_settings(self,loc:int):
        self._port.write(KORAD_RECALL_CMD(loc))
    
    def set_ocp(self,enable:bool):
        enable = 1 if enable else 0
        self._port.write(KORAD_OCP_CMD(enable))
    
    def __del__(self):
        self._port.close()



# Function Interface

def korad_set_voltage(addr:str,ch:int,voltage:_Real):
    with _serial.Serial(addr,baudrate=KORAD_BAUD,parity=KORAD_PARITY,rtscts=KORAD_DATA_FLOW_CTRL,
                        dsrdtr=KORAD_DATA_FLOW_CTRL,timeout=KORAD_MAX_TIMEOUT) as port:
        port.write(KORAD_VSET_CMD(ch,voltage))

def korad_set_current(addr:str,ch:int,current:_Real):
    with _serial.Serial(addr,baudrate=KORAD_BAUD,parity=KORAD_PARITY,rtscts=KORAD_DATA_FLOW_CTRL,
                        dsrdtr=KORAD_DATA_FLOW_CTRL,timeout=KORAD_MAX_TIMEOUT) as port:
        port.write(KORAD_ISET_CMD(ch,current))

def korad_get_desired_voltage(addr:str,ch:int):
    with _serial.Serial(addr,baudrate=KORAD_BAUD,parity=KORAD_PARITY,rtscts=KORAD_DATA_FLOW_CTRL,
                        dsrdtr=KORAD_DATA_FLOW_CTRL,timeout=KORAD_MAX_TIMEOUT) as port:
        port.write(KORAD_VREAD_CMD(ch))

def korad_get_desired_current(addr:str,ch:int):
    with _serial.Serial(addr,baudrate=KORAD_BAUD,parity=KORAD_PARITY,rtscts=KORAD_DATA_FLOW_CTRL,
                        dsrdtr=KORAD_DATA_FLOW_CTRL,timeout=KORAD_MAX_TIMEOUT) as port:
        port.write(KORAD_IREAD_CMD(ch))

def korad_get_actual_voltage(addr:str,ch:int):
    with _serial.Serial(addr,baudrate=KORAD_BAUD,parity=KORAD_PARITY,rtscts=KORAD_DATA_FLOW_CTRL,
                        dsrdtr=KORAD_DATA_FLOW_CTRL,timeout=KORAD_MAX_TIMEOUT) as port:
        port.write(KORAD_VMEAS_CMD(ch))


def korad_get_actual_current(addr:str,ch:int):
    with _serial.Serial(addr,baudrate=KORAD_BAUD,parity=KORAD_PARITY,rtscts=KORAD_DATA_FLOW_CTRL,
                        dsrdtr=KORAD_DATA_FLOW_CTRL,timeout=KORAD_MAX_TIMEOUT) as port:
        port.write(KORAD_IMEAS_CMD(ch))


def korad_set_output(addr:str,enable:bool):
    with _serial.Serial(addr,baudrate=KORAD_BAUD,parity=KORAD_PARITY,rtscts=KORAD_DATA_FLOW_CTRL,
                        dsrdtr=KORAD_DATA_FLOW_CTRL,timeout=KORAD_MAX_TIMEOUT) as port:
        enable = 1 if enable else 0
        port.write(KORAD_OUTPUT_CMD(enable))


def korad_set_ocp(addr:str,enable:bool):
    with _serial.Serial(addr,baudrate=KORAD_BAUD,parity=KORAD_PARITY,rtscts=KORAD_DATA_FLOW_CTRL,
                        dsrdtr=KORAD_DATA_FLOW_CTRL,timeout=KORAD_MAX_TIMEOUT) as port:
        enable = 1 if enable else 0
        port.write(KORAD_OCP_CMD(enable))


def korad_identify(addr:str):
    with _serial.Serial(addr,baudrate=KORAD_BAUD,parity=KORAD_PARITY,rtscts=KORAD_DATA_FLOW_CTRL,
                        dsrdtr=KORAD_DATA_FLOW_CTRL,timeout=KORAD_MAX_TIMEOUT) as port:
        port.write(KORAD_ID_CMD)
        return port.readline().rstrip().decode('utf-8')

def korad_status(addr:str):
    with _serial.Serial(addr,baudrate=KORAD_BAUD,parity=KORAD_PARITY,rtscts=KORAD_DATA_FLOW_CTRL,
                        dsrdtr=KORAD_DATA_FLOW_CTRL,timeout=KORAD_MAX_TIMEOUT) as port:
        port.write(KORAD_STATUS_CMD)
        status = ord(port.readline().rstrip().decode('utf-8'))
        status_dict = {'output':bool(status&(1<<6)),
                       'mode':'CV' if status&1 else 'CC',
                       'ocp':bool(status&(1<<5)),
                       }

def korad_save_settings(addr:str,loc:int):
    with _serial.Serial(addr,baudrate=KORAD_BAUD,parity=KORAD_PARITY,rtscts=KORAD_DATA_FLOW_CTRL,
                        dsrdtr=KORAD_DATA_FLOW_CTRL,timeout=KORAD_MAX_TIMEOUT) as port:
        port.write(KORAD_SAVE_CMD(loc))

def korad_load_settings(addr:str,loc:int):
    with _serial.Serial(addr,baudrate=KORAD_BAUD,parity=KORAD_PARITY,rtscts=KORAD_DATA_FLOW_CTRL,
                        dsrdtr=KORAD_DATA_FLOW_CTRL,timeout=KORAD_MAX_TIMEOUT) as port:
        port.write(KORAD_RECALL_CMD(loc))
