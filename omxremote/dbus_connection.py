import os
import time
import shlex
import dbus
import getpass
from dbus.exceptions import DBusException
from subprocess import Popen

# see https://raw.githubusercontent.com/popcornmix/omxplayer/master/dbuscontrol.sh
DBUS_COMMANDS = {
    'pause' : 16,
    'stop' : 15,
    'volumeup' : 18,
    'volumedown' : 17,
    'togglesubtitles' : 12,
    'hidesubtitles' : 30,
    'showsubtitles' : 31,
}


class OmxRemote(object):
    """remote control for omxplayer using dbus
       needs the path to a movie-file that should be played
       if omxplayer is already running we connect to it over dbus. 
       use forceRestart to kill any existing instances and restart with 
       the new video-file.
    """
    def __init__(self, user='pi'):
        self.user = user
        self.properties = None
        self.player = None
        self.connected = self.connect_to_dbus()

    def connect_to_dbus(self):
        try:
            addr = self.get_dbus_address()
            bus = dbus.bus.BusConnection(addr)
            obj = bus.get_object('org.mpris.MediaPlayer2.omxplayer','/org/mpris/MediaPlayer2', introspect=False)
            self.properties = dbus.Interface(obj,'org.freedesktop.DBus.Properties')
            self.player = dbus.Interface(obj,'org.mpris.MediaPlayer2.Player')
            return True
        except (IOError, DBusException):
            return False

    def get_dbus_address(self):
        with open('/tmp/omxplayerdbus.' + self.user, 'r') as f:
            addr = f.read().strip()
        return addr

    def start_omx_player(self, movie):
        cmd = '/usr/bin/omxplayer -o hdmi -b %s' % movie
        p = Popen(shlex.split(cmd), stdout=file(os.devnull), env={'DISPLAY' : ':0', 'USER' : self.user})
        time.sleep(2) # to make sure dbus is available TODO: necessary?

    def send_command(self, command):
        assert self.connected == True #TODO better raise a NotConnected exception?
        self.player.Action(dbus.Int32(str(DBUS_COMMANDS[command])))

    def status(self):
        if self.connected:
            return (
                self.properties.Position(),
                self.properties.Duration(),
                self.properties.PlaybackStatus() == 'Playing'
            )
        else:
            return (
                0,
                0,
                False
            )

    def playMovie(self, movie):
        self.connected = self.connect_to_dbus()
        if self.connected:
            self.stop()
        self.start_omx_player(movie)
        self.connected = self.connect_to_dbus()

    def pause(self):
        self.send_command('pause')

    def stop(self):
        self.send_command('stop')


