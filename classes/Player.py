import pygst
pygst.require('0.10')
import gst
import time

class Player(object):
    def __init__(self, channel):
        self.pipeline = gst.Pipeline("RadioPipe")
        self.player = gst.element_factory_make("playbin", "player")
        pulse = gst.element_factory_make("pulsesink", "pulse")
        fakesink = gst.element_factory_make("fakesink", "fakesink")

        self.player.set_property("audio-sink", pulse)
        self.player.set_property("video-sink", fakesink)
	self.channel(channel)
	self.play()

    def channel(self, channel):
	self.player.set_property('uri', channel)

    def play(self):
        self.pipeline.set_state(gst.STATE_PLAYING)

    def stop(self):
        self.pipeline.set_state(gst.STATE_NULL)

    def playnew(self, channel):
	self.stop()
	self.channel(channel)
	self.play()

