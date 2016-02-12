#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import codecs
from Config import Config


class PlaylistItem:

    def __init__(self):
        self.name = None
        self.url = None
        self.payload = []


class Playlist:

    playlist = []
    filename = ""
    debug_enabled = False

    def __init__(self, filename=Config.playlist):
        self.filename = filename
        self.load(filename)

    def load(self, filename):
        try:
            fsrc = codecs.open(filename, mode="r", encoding="utf-8")
            self.parse(fsrc)
            fsrc.close()
        except Exception as e:
            self.debug("Error while loading playlist: " + e.message)

    def parse(self, infile):
        ln = None
        self.playlist = []

        while ln != "" and ln != u"#EXTM3U\n":
            ln = infile.readline()

        ln = infile.readline()
        while ln != "":
            while ln != "" and ln.find(u"#EXTINF") == -1:
                ln = infile.readline()
            match = re.search(ur"#EXTINF:.*,(.*)", ln)
            name = match.group(1)
            nitem = PlaylistItem()
            nitem.name = name
            ln = infile.readline()
            while ln != "" and ln.find(u"#EXTINF") == -1:
                nitem.payload.append(ln)
                ln = infile.readline()
            nitem.url = nitem.payload[-1].strip()
            self.playlist.append(nitem)

    def debug(self, msg):
        if self.debug_enabled:
            print msg
