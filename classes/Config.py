#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Config:

    debug = True

    default_screen_size = (320, 240)
    fps = 15
    full_screen = True
    fb_dev = "/dev/fb1"

    playlist = "/home/pi/PiRadio-TFT/data/radio.m3u"
    state = "/home/pi/PiRadio-TFT/data/state.txt"

    menu_font = "/home/pi/PiRadio-TFT/gfx/zxspb___.ttf"
    menu_font_bold = "/home/pi/PiRadio-TFT/gfx/zxspb___.ttf"

    font_size_big = 14
    font_size_small = 10

    color_white = (255, 255, 255)
    color_blue = (153, 229, 255)
    color_black = (0, 0, 0)
    color_green = (127,255,127)
    color_blue = (127,127,255)

    state_save_timeout = 10000
    mpd_poll_timeout = 2000

    init_delay = 0.1
    write_delay = 0.1
    read_delay = 0.1

    i2c_bus = 1

    BTN_ALARM = 4
#    BTN_SCAN = 14
#    BTN_MODE = 15
    BTN_INFO = 22
    BTN_PRESETS = 21
    BTN_MENU = 23
    BTN_EXIT = 7
    BTN_SELECT = 17
