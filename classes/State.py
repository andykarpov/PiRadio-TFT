#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs
from Config import Config


class State:

    filename = ""
    volume = 0
    channel = 0
    alarm_hours = 0
    alarm_minutes = 0
    alarm_on = False
    debug_enabled = False

    def __init__(self, filename=Config.state):
        self.filename = filename
        self.load()

    def load(self):
        try:
            handle = codecs.open(self.filename, mode="r", encoding="utf-8")
            ln = handle.readline().strip()
            if ln != "":
                parts = ln.split(":")
                self.channel = int(parts[0])
                self.volume = int(parts[1])
                self.alarm_hours = int(parts[2])
                self.alarm_minutes = int(parts[3])
                if parts[4] == '1':
                    self.alarm_on = True
            handle.close()
            return True
        except Exception as e:
            self.debug("Unable to load state: " + e.message)
            return False

    def save(self):
        try:
            handle = codecs.open(self.filename, mode="w", encoding="utf-8")
            handle.write(str(self.channel))
            handle.write(':')
            handle.write(str(self.volume))
            handle.write(':')
            handle.write(str(self.alarm_hours))
            handle.write(':')
            handle.write(str(self.alarm_minutes))
            handle.write(':')
            if self.alarm_on:
                handle.write('1')
            else:
                handle.write('0')
            handle.close()
        except Exception as e:
            self.debug("Unable to store state: " + e.message)

    def debug(self, msg):
        if self.debug_enabled:
            print msg
