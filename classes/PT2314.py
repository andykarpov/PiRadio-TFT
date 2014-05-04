#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Class for controlling PT2314 via i2c
# 4-channel input audo processor
# Ronald Diaz ronald@ronalddiaz.net

import smbus
from Config import Config


class PT2314:
    def __init__(self):

        self.i2c = smbus.SMBus(Config.i2c_bus)

        self.i2c_address = 0x44
        self.volume = 0x20  # volume = minimum
        self.attenuation_l = 0  # (-x -> x ? )
        self.attenuation_r = 0  # (-x -> x ? )
        self.mute = False  # mute on
        self.loudness = True  # loudness on
        self.channel = 0  # channel 0 selected [ 0 > 3 ]
        self.bass = 0x0F  # bass = 0
        self.treble = 0x0F  # treble = 0
        self._updateAll()  # Initialise all

        # Tone lookup values
        self.tone_values = [(-14, 0x00), (-12, 0x01), (-10, 0x02), (-8, 0x03), (-6, 0x04), (-4, 0x05), (-2, 0x06),
                            (0, 0x07), (2, 0x0E), (4, 0x0D), (6, 0x0C), (8, 0x0B), (10, 0x0A), (12, 0x09), (14, 0x08)]

    # High Level Commands

    def powerOff(self):
        self.mute = True
        self._updateAttenuation()

    def volume_to_pt2314(self, vol):
        return 63 - ((vol * 63) / 100)

    def setVolume(self, volume):
        self.volume = self.volume_to_pt2314(volume)
        self._updateVolume()

    def muteOn(self):
        self.mute = True
        self._updateAttenuation()

    def muteOff(self):
        self.mute = False
        self._updateAttenuation()

    def selectChannel(self, ch):
        self.channel = ch
        self._updateAudioSwitch()

    def loudnessOn(self):
        self.loudness = True
        self._updateAudioSwitch()

    def loudnessOff(self):
        self.loudness = False
        self._updateAudioSwitch()

    def setAttenuation(self, l, r):
        self.attenuation_l = l
        self.attenuation_r = r
        self._updateAttenuation()

    def setBass(self, bass):
        self.bass = self._lookupTone(int(bass))
        self._updateBass()
        return self._lookupToneReverse(self.bass)

    def setTreble(self, treble):
        self.treble = self._lookupTone(int(treble))
        self._updateTreble()
        return self._lookupToneReverse(self.treble)

    # Low Level Commands

    def _updateVolume(self):
        self._sendByte(self.volume)

    def _updateAttenuation(self):
        if self.mute == True:
            self._sendByte(0xDF)
            self._sendByte(0xFF)
        else:
            self._sendByte(0xC0 | self.attenuation_l)
            self._sendByte(0xE0 | self.attenuation_r)

    def _updateAudioSwitch(self):
        audioByte = 0x58  # Audio Switch Byte
        if self.loudness == True:  # Loudness
            audioByte |= 0x00
        else:
            audioByte |= 0x04
        audioByte |= self.channel  # Select Channel
        self._sendByte(audioByte)  # Send Byte

    def _updateBass(self):
        self._sendByte(0x60 | self.bass)

    def _updateTreble(self):
        self._sendByte(0x70 | self.treble)

    def _lookupTone(self, value):
        try:
            return next(x for x in self.tone_values if x[0] == value)[1]
        except StopIteration:
            return 0x0F

    def _lookupToneReverse(self, value):
        try:
            return next(x for x in self.tone_values if x[1] == value)[0]
        except StopIteration:
            return 0

    def _updateAll(self):
        self._updateVolume()
        self._updateAttenuation()
        self._updateAudioSwitch()
        self._updateBass()
        self._updateTreble()

    def _sendByte(self, b):
        #print "data: %x" % b
        try:
            self.i2c.write_byte(self.i2c_address, b)  # send data via i2c
        except Exception:
            pass