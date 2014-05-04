#!/usr/bin/env python
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
from Config import Config
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

class Key():

    pin = 0

    def __init__(self, pin):
        self.pin = pin
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def reading(self):
        input_value = GPIO.input(self.pin)
        if input_value == 0:
            return True
        else:
            return False


class Keyboard():

    buttons = []

    def __init__(self):
        self.buttons = {
            'alarm': Key(Config.BTN_ALARM),
            #'scan': Key(Config.BTN_SCAN),
            #'mode': Key(Config.BTN_MODE),
            'info': Key(Config.BTN_INFO),
            'presets': Key(Config.BTN_PRESETS),
            'menu': Key(Config.BTN_MENU),
            'exit': Key(Config.BTN_EXIT),
            'select': Key(Config.BTN_SELECT)}

    def reading(self, name):
        if name in self.buttons:
            return self.buttons[name].reading() == 0
        else:
            return 0

    def reading_all(self):
        for name in self.buttons:
            if self.reading(name):
                return name
        return None
