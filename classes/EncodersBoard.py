#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Config import Config
import smbus
import time
import sys


class EncodersBoard():

    bus = smbus.SMBus(Config.i2c_bus)
    i2c_address = 0x40

    min_value1 = 0
    max_value1 = 255
    value1 = 0

    min_value2 = 0
    max_value2 = 255
    value2 = 0

    buttons = 0

    debug = False

    def __init__(self, address, min_value1, max_value1, value1, min_value2, max_value2, value2):
        self.i2c_address = address
        self.min_value1 = min_value1
        self.min_value2 = min_value2
        self.max_value1 = max_value1
        self.max_value2 = max_value2
        self.value1 = value1
        self.value2 = value2
	self.write()

    def write(self):
        try:
            self.bus.write_i2c_block_data(self.i2c_address, 0x01, [self.min_value1, self.max_value1, self.value1, self.min_value2, self.max_value2, self.value2])
            time.sleep(0.1)
        except IOError:
            self.debug("i2c write error");

    def set_min_value1(self, value):
        self.min_value1 = value
        #self.write()

    def set_max_value1(self, value):
        self.max_value1 = value
        #self.write()

    def set_value1(self, value):
        self.value1 = value
        #self.write()

    def set_min_value2(self, value):
        self.min_value2 = value
        #self.write()

    def set_max_value2(self, value):
        self.max_value2 = value
        #self.write()

    def set_value2(self, value):
        self.value2 = value
        #self.write()

    def read(self):
        try:
            #print "try read i2c"
            values = self.bus.read_i2c_block_data(self.i2c_address, 0x02, 3)
            time.sleep(0.1)
            #print "values:"
            #print values
            self.value1 = values[0]
            self.value2 = values[1]
            self.buttons = values[2]
        except Exception as e:
            self.debug(sys.exc_info()[0])

    def get_value1(self):
        return self.value1

    def get_value2(self):
        return self.value2

    def get_buttons(self):
        return self.buttons

    def debug(self, msg):
        if self.debug == True:
            print msg
