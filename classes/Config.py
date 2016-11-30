#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Config:

    debug = False

    default_screen_size = (320, 240)
    fps = 10
    full_screen = True
    fb_dev = "/dev/fb1"

    playlist = "/home/pi/PiRadio-TFT/data/radio.m3u"
    state = "/home/pi/PiRadio-TFT/data/state.txt"

    bell = "/home/pi/PiRadio-TFT/data/doorbell.mp3"

    menu_font = "/home/pi/PiRadio-TFT/gfx/zxspb___.ttf"
    menu_font_bold = "/home/pi/PiRadio-TFT/gfx/zxspb___.ttf"

    font_size_big = 14
    font_size_small = 10
    font_size_digits = 52

    color_white = (255, 255, 255)
    color_black = (0, 0, 0)
    color_green = (127,255,127)
    color_blue = (127,127,255)

    color_bg = (0, 25, 77)
    color_station = (255, 255, 255)
    color_song = (255, 255, 255)
    color_bar_text = (255, 255, 255)
    color_bar_outer = (255, 255, 255)
    color_bar_inner = (0, 0, 0)
    color_bar_volume = (58, 215, 255)
    color_bar_channel = (58, 215, 255)
    color_clock = (58, 215, 255)
    color_debug = (127, 127, 127)

    state_save_timeout = 10000
    mpd_poll_timeout = 2000

    init_delay = 1
    write_delay = 0.2
    read_delay = 0.2

    i2c_bus = 1

    BTN_ALARM = 128
    BTN_SCAN = 64
    BTN_MODE = 1
    #BTN_INFO = 2
    #BTN_PRESETS = 4
    #BTN_MENU = 8
    BTN_POWER = 16
    BTN_SELECT = 32
