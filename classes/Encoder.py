#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Config import Config
import smbus
import time


class Encoder():

    DEVICE_CMD_SET = 0x01
    DEVICE_CMD_READ = 0x02
    DEVICE_CMD_MIN = 0x03
    DEVICE_CMD_MAX = 0x04

    bus = smbus.SMBus(Config.i2c_bus)
    i2c_address = 0x00
    min_value = 0
    max_value = 255
    value = 0
    debug = False

    def __init__(self, address, min_value, max_value, value):
        self.i2c_address = address
        self.set_min_value(min_value)
        self.set_max_value(max_value)
        self.set_value(value)

    def set_min_value(self, value):
        self.min_value = value
        try:
            self.bus.write_byte_data(self.i2c_address, self.DEVICE_CMD_MIN, value)
            time.sleep(0.01)

        except IOError:
            self.debug("set_min_value error")
            self.set_min_value(value)

    def set_max_value(self, value):
        self.max_value = value
        try:
            self.bus.write_byte_data(self.i2c_address, self.DEVICE_CMD_MAX, value)
            time.sleep(0.01)
        except IOError:
            self.debug("set_max_value error")
            self.set_max_value(value)

    def set_value(self, value):
        self.value = value
        try:
            self.bus.write_byte_data(self.i2c_address, self.DEVICE_CMD_SET, value)
            time.sleep(0.01)
        except IOError:
            self.debug("set_value error")
            self.set_value(value)

    def get_value(self):
        try:
            self.value = self.bus.read_byte(self.i2c_address)
            time.sleep(0.01)
        except IOError:
            self.debug("get_value error")
            return self.value

        return self.value

    def debug(self, msg):
        if self.debug:
            print msg
