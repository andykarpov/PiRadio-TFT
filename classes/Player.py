#!/usr/bin/env python
# -*- coding: utf-8 -*-

from mpd import MPDClient, MPDError

class Player:

    def __init__(self):
	self._client = MPDClient()
        try:
		self._client.timeout = 10
		self._client.idletimeout = None
		self._client.connect("localhost", 6600)
        except IOError as (errno, strerror):
		pass
        except MPDError as e:
		pass

    def load(self, playlist):
	self._client.command_list_ok_begin()
	self._client.stop()
	self._client.clear()
	self._client.load(playlist)
	self._client.command_list_end()

    def play(self, channel):
	self._client.command_list_ok_begin()
	self._client.stop()
	self._client.play(channel)
	self._client.command_list_end()

    def stop(self):
	self._client.stop()

    def currentsong(self):
	try:
		song = self._client.currentsong()
		if song['title']:
			return song['title']
	except Exception:
		return ''

