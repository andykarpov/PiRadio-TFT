#!/usr/bin/env python
# -*- coding: utf-8 -*-

from libs.fenix.program import Program
from libs.fenix.program import Process


class VolumeBar(Process):

    main = None
    value = 50
    bar_height = 10
    max_value = 100
    offset_x = 0
    offset_y = 0

    def begin(self, main, offset_x, offset_y, value, max_value, height, color):

        self.main = main
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.value = value
        self.max_value = max_value
        self.bar_height = height

        self.y = self.offset_y + self.bar_height/2
        self.x = self.offset_x + ((self.main.screen_size[0] - self.offset_x*2) * self.value / self.max_value)/2
        self.size = 100

        while True:

            self.x = self.offset_x + ((self.main.screen_size[0] - self.offset_x*2) * self.value / self.max_value)/2
            if self.x <= self.offset_x:
                self.x = self.offset_x+1
            w = round(((self.main.screen_size[0] - self.offset_x*2) * self.value) / self.max_value - self.offset_x)
            if w <= 0:
                w = 0
            self.graph = Program.new_map(w, self.bar_height)
            self.alpha = 255
            Program.map_clear(self.graph, color)

            yield

