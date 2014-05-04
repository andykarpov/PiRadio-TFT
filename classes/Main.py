#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time
from datetime import datetime
from classes.Playlist import Playlist
from classes.MPDWrapper import MPDWrapper
from classes.Config import Config
from classes.State import State
from classes.Encoder import Encoder
from classes.Keyboard import Keyboard
from classes.PT2314 import PT2314
from libs.fenix.program import Program
from libs.fenix.program import Process
import pygame
from pygame.locals import *
from libs.fenix.locals import *
from classes.AppRadio import AppRadio
import chardet


class Main(Process):

    playlist = None
    mpd = None
    state = None
    volume_encoder = None
    channel_encoder = None
    keyboard = None
    pt2314 = None

    channel = 0
    volume = 0
    key = None

    last_channel = 0
    last_played_channel = 0
    last_volume = 0
    last_key = None

    current_time = 0
    last_channel_changed_time = 0
    last_volume_changed_time = 0
    last_keyboard_changed_time = 0
    last_mpd_poll = 0
    need_save_state = False
    need_change_song = False

    screen_size = None
    fps = None
    full_screen = False

    scene = None

    def __init__(self):

        self.screen_size = Config.default_screen_size
        self.fps = Config.fps
        self.full_screen = Config.full_screen

        os.environ["SDL_FBDEV"] = Config.fb_dev

        super(Main, self).__init__()

    def begin(self):

        Program.set_mode(self.screen_size, self.full_screen, False)
        Program.set_fps(self.fps)
        pygame.mouse.set_visible(False)

        self.playlist = Playlist()

        self.mpd = MPDWrapper(Config.mpd_host, Config.mpd_port, Config.mpd_password)
        self.mpd.connect()
        self.mpd.load_playlist(self.playlist.playlist)

        # todo: add bass, treble support
        self.state = State()

        print "State volume: {0}".format(self.state.volume)
        print "State channel: {0}".format(self.state.channel)

        self.volume_encoder = Encoder(0x48, 0, 100, self.state.volume)
        time.sleep(0.1)
        self.channel_encoder = Encoder(0x47, 0, len(self.playlist.playlist) - 1, self.state.channel)
        time.sleep(0.1)

        self.pt2314 = PT2314()
        self.pt2314.setVolume(self.state.volume)
        self.pt2314.setBass(0)
        self.pt2314.setTreble(12)
        self.pt2314.selectChannel(0)
        self.pt2314.loudnessOn()
        self.pt2314.muteOff()
        time.sleep(0.1)

        self.last_volume = self.state.volume
        self.last_channel = self.state.channel

        self.keyboard = Keyboard()

        self.mpd.play(self.state.channel)

        self.scene = AppRadio(self)

        while True:

            micro = self.get_micro()

            self.volume = self.volume_encoder.get_value()
            if self.volume > 100:
                self.volume = 100
                self.volume_encoder.set_value(self.volume)
                self.volume_encoder.set_max_value(self.volume)

            self.channel = self.channel_encoder.get_value()
            if self.channel > len(self.playlist.playlist) - 1:
                self.channel = len(self.playlist.playlist) - 1
                self.channel_encoder.set_value(self.channel)
                self.channel_encoder.set_max_value(self.channel)

            self.key = self.keyboard.reading_all()

            if self.last_volume != self.volume:
                self.pt2314.setVolume(self.volume)
                #print "Volume: {0}".format(self.volume)
                self.last_volume = self.volume
                self.last_volume_changed_time = micro

            if self.last_channel != self.channel:
                #todo: play mpd, save state
                #print "Channel: {0}".format(self.channel)
                self.last_channel = self.channel
                self.last_channel_changed_time = micro

            if self.last_key != self.key:
                #todo: process keyboard press
                #print "Key: {0}".format(self.key)
                self.last_key = self.key
                self.last_keyboard_changed_time = micro

            if self.last_played_channel != self.channel and micro - self.last_channel_changed_time > 1000:
                self.need_change_song = True

            if self.state.volume != self.volume and micro - self.last_volume_changed_time > 5000:
                self.state.volume = self.volume
                self.need_save_state = True

            if self.state.channel != self.channel and micro - self.last_channel_changed_time > 5000:
                self.state.channel = self.channel
                self.need_save_state = True

            if self.need_change_song:
                self.need_change_song = False
                self.last_played_channel = self.channel
                self.mpd.play(self.channel)

            if self.need_save_state:
                self.need_save_state = False
                self.state.save()

            yield

    def get_micro(self):
        return int(round(time.time() * 1000))

    def get_current_time(self):
        return datetime.now().strftime("%H:%M")

    def unicodify(self, text, min_confidence=0.5):
        guess = chardet.detect(text)
        if guess["confidence"] < min_confidence:
            # chardet isn't confident enough in its guess, so:
            raise UnicodeDecodeError
        decoded = text.decode(guess["encoding"])
        return decoded

    def fetch_song_title(self):
        current_song = self.mpd.currentsong()
        if current_song is not None and current_song != '' and 'title' in current_song[0]:
            title = self.unicodify(current_song[0]['title'])
            return title.upper()
        else:
            return ''

    def fetch_station_title(self):
        station = self.playlist.playlist[self.channel]
        return station.name.upper()

