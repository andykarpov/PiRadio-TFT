#!/usr/bin/env python
# -*- coding: utf-8 -*-

from mpd import MPDClient, MPDError, CommandError


class PollerError(Exception):
    """Fatal error in poller."""


class MPDWrapper:

    def __init__(self, host="localhost", port="6600", password=None):
        self._host = host
        self._port = port
        self._password = password
        self._client = MPDClient()

    def connect(self):
        try:
            self._client.connect(self._host, self._port)

        except IOError as (errno, strerror):
            raise PollerError("Could not connect to '%s': %s" % (self._host, strerror))

        except MPDError as e:
            raise PollerError("Could not connect to '%s': %s" % (self._host, e))

        if self._password:
            try:
                self._client.password(self._password)

            except CommandError as e:
                raise PollerError("Could not connect to '%s': "
                                  "password command failed: %s" %
                                  (self._host, e))

            except (MPDError, IOError) as e:
                raise PollerError("Could not connect to '%s': "
                                  "error with password command: %s" %
                                  (self._host, e))

    def disconnect(self):
        try:
            self._client.close()

        except (MPDError, IOError):
            pass

        try:
            self._client.disconnect()

        except (MPDError, IOError):
            self._client = MPDClient()

    def currentsong(self):

        try:
            self._client.command_list_ok_begin()
            self._client.currentsong()
            song = self._client.command_list_end()

        except (MPDError, IOError):
            self.disconnect()

            try:
                self.connect()

            except PollerError as e:
                raise PollerError("Reconnecting failed: %s" % e)

            try:
                self._client.command_list_ok_begin()
                self._client.currentsong()
                song = self._client.command_list_end()

            except (MPDError, IOError) as e:
                raise PollerError("Couldn't retrieve current song: %s" % e)

        return song

    def load_playlist(self, playlist):
        try:
            self._client.command_list_ok_begin()
            self._client.stop()
            self._client.clear()
            for item in playlist:
                self._client.add(item.url)
            self._client.command_list_end()

        except (MPDError, IOError):
            self.disconnect()

            try:
                self.connect()

            except PollerError as e:
                raise PollerError("Reconnecting failed: %s" % e)

            try:
                self._client.command_list_ok_begin()
                self._client.stop()
                self._client.clear()
                for item in playlist:
                    self._client.add(item.url)
                self._client.command_list_end()

            except (MPDError, IOError) as e:
                raise PollerError("Couldn't load playlist: %s" % e)

    def play(self, idx):
        try:
            self._client.command_list_ok_begin()
            self._client.stop()
            self._client.play(idx)
            self._client.command_list_end()

        except (MPDError, IOError):
            self.disconnect()

            try:
                self.connect()

            except PollerError as e:
                raise PollerError("Reconnecting failed: %s" % e)

            try:
                self._client.command_list_ok_begin()
                self._client.stop()
                self._client.play(idx)
                self._client.command_list_end()

            except (MPDError, IOError) as e:
                raise PollerError("Couldn't play song: %s" % e)
