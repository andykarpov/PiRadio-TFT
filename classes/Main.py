#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time
import re
import subprocess
from datetime import datetime
from classes.Playlist import Playlist
from classes.Player import Player
from classes.Config import Config
from classes.State import State
from classes.EncodersBoard import EncodersBoard
from classes.PT2314 import PT2314
from libs.fenix.program import Program
from libs.fenix.program import Process
import pygame
from pygame.locals import *
from libs.fenix.locals import *
from classes.AppRadio import AppRadio
import chardet
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
import threading

ring_bell = False

class HttpProcessor(BaseHTTPRequestHandler):

    def do_GET(self):
        global ring_bell
        if self.path=="/":
            self.send_response(200)
            self.send_header('content-type','text/plain')
            self.end_headers()
            self.wfile.write("Ding-dong")
            ring_bell = True
        else:
            self.send_response(404)
            self.send_header('content-type','text/plain')
            self.end_headers()


class Main(Process):

    playlist = None
    player = None
    state = None
    pt2314 = None

    channel = 0
    volume = 0
    buttons = 0

    icy_current_song = None

    last_channel = 0
    last_played_channel = 0
    last_volume = 0
    last_buttons = 0

    current_time = 0
    last_channel_changed_time = 0
    last_volume_changed_time = 0
    last_buttons_changed_time = 0
    last_currentsong_time = 0
    last_mpd_poll = 0
    need_save_state = False
    need_change_song = False
    need_change_buttons = False

    screen_size = None
    fps = None
    full_screen = False

    scene = None

    def __init__(self):

        self.screen_size = Config.default_screen_size
        self.fps = Config.fps
        self.full_screen = Config.full_screen

        os.environ["SDL_FBDEV"] = Config.fb_dev

	self.serv = HTTPServer( ("0.0.0.0", 8000), HttpProcessor)
        thread = threading.Thread(target = self.serv.serve_forever)
        thread.daemon = True
        thread.start()

        super(Main, self).__init__()

    def begin(self):

        Program.set_mode(self.screen_size, self.full_screen, False)
        Program.set_fps(self.fps)
        pygame.mouse.set_visible(False)

        self.playlist = Playlist()

        self.player = Player()

        self.state = State()

        #print "State volume: {0}".format(self.state.volume)
        #print "State channel: {0}".format(self.state.channel)

        self.encoders_board = EncodersBoard(0x40, 0, 20, self.state.volume, 0, len(self.playlist.playlist) - 1, self.state.channel);

        self.pt2314 = PT2314()
        self.pt2314.setVolume(self.state.volume*5)
	#self.pt2314.setAttenuation(0)
        self.pt2314.setBass(0)
        self.pt2314.setTreble(12)
        self.pt2314.selectChannel(0)
        self.pt2314.loudnessOn()
        self.pt2314.muteOff()
        time.sleep(0.1)

        self.last_volume = self.state.volume
        self.last_channel = self.state.channel
        self.last_played_channel = self.last_channel

        station_url = self.playlist.playlist[self.state.channel].url
        self.player.load("radio")
	self.player.play(self.state.channel)

        self.scene = AppRadio(self)

        while True:
            try:
                micro = self.get_micro()
                
                self.encoders_board.read()

                self.volume = self.encoders_board.get_value1()
                if self.volume > 20:
                    self.volume = 20
                    self.encoders_board.set_value1(self.volume)
                    self.encoders_board.set_max_value1(self.volume)
                    self.encoders_board.write()

                self.channel = self.encoders_board.get_value2()
                if self.channel > len(self.playlist.playlist) - 1:
                    self.channel = len(self.playlist.playlist) - 1
                    self.encoders_board.set_value2(self.channel)
                    self.encoders_board.set_max_value2(self.channel)
                    self.encoders_board.write()

                self.buttons = self.encoders_board.get_buttons()

                if self.last_volume != self.volume:
                    self.pt2314.setVolume(self.volume*5)
                    self.last_volume = self.volume
                    self.last_volume_changed_time = micro

                if self.last_channel != self.channel:
                    self.last_channel = self.channel
                    self.last_channel_changed_time = micro

                if self.last_buttons != self.buttons and micro - self.last_buttons_changed_time > 100:
                    self.last_buttons = self.buttons
                    self.last_buttons_changed_time = micro
                    self.need_change_buttons = True

                if self.last_played_channel != self.channel and micro - self.last_channel_changed_time > 1000:
                    self.need_change_song = True

                if self.state.volume != self.volume and micro - self.last_volume_changed_time > 5000:
                    self.state.volume = self.volume
                    self.need_save_state = True

                if self.state.channel != self.channel and micro - self.last_channel_changed_time > 5000:
                    self.state.channel = self.channel
                    self.need_save_state = True

		if micro - self.last_currentsong_time > 1000:
		    self.icy_current_song = self.player.currentsong()
		    #print self.icy_current_song
		    self.last_currentsong_time = micro

                global ring_bell
                if ring_bell:
                    #print "Doorbell detected";
                    ring_bell = False
                    self.player.stop()
                    self.pt2314.setVolume(95)
		    os.system('mplayer ' + Config.bell)
                    time.sleep(0.5)
                    self.pt2314.setVolume(self.volume*5)
                    self.need_change_song = True

                if self.need_change_song:
                    self.need_change_song = False
                    self.last_played_channel = self.channel
		    time.sleep(0.5)
		    self.player.play(self.channel)

                if self.need_save_state:
                    self.need_save_state = False
                    self.state.save()

		if self.need_change_buttons:
		    self.need_change_buttons = False
		    if (self.last_buttons & Config.BTN_POWER):
			subprocess.call(["poweroff"])
		    if (self.last_buttons & Config.BTN_ALARM):
			subprocess.call(["reboot"])

            except Exception:
                pass

            yield

    def get_micro(self):
        return int(round(time.time() * 1000))

    def get_current_time(self):
        return datetime.now().strftime("%H:%M")

    def unicodify(self, text, min_confidence=0.5):
        guess = chardet.detect(text)
        if guess["confidence"] < min_confidence:
            raise UnicodeDecodeError
        decoded = text.decode(guess["encoding"])
        return decoded

    def fetch_song_title(self):

        if self.icy_current_song is not None and self.icy_current_song != '':
	    try:
                title = self.unicodify(self.icy_current_song)
		#title = self.icy_current_song
                return title.upper()
            except Exception as e:
                return ''
        else:
            return ''

    def fetch_station_title(self):
        station = self.playlist.playlist[self.channel]
        return station.name.upper()

