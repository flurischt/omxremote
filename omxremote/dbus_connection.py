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
    def __init__(self, movie=None, user='pi', forceRestart=False):
	#TODO document when a movie is needed an when not
        self.movie = movie
        self.user = user
        self.connect_to_dbus(forceRestart)

    def connect_to_dbus(self, restart):
        try:
            addr = self.get_dbus_address()
        except IOError:
            self.start_omx_player() 
            addr = self.get_dbus_address()
        try:
            bus = dbus.bus.BusConnection(addr)
            obj = bus.get_object('org.mpris.MediaPlayer2.omxplayer','/org/mpris/MediaPlayer2', introspect=False)
            self.properties = dbus.Interface(obj,'org.freedesktop.DBus.Properties')
            self.player = dbus.Interface(obj,'org.mpris.MediaPlayer2.Player')
            if restart:
                self.stop()
                time.sleep(1)
                self.connect_to_dbus(False)
        except DBusException:
            self.start_omx_player() 
            addr = self.get_dbus_address()
            bus = dbus.bus.BusConnection(addr)
            obj = bus.get_object('org.mpris.MediaPlayer2.omxplayer','/org/mpris/MediaPlayer2', introspect=False)
            self.properties = dbus.Interface(obj,'org.freedesktop.DBus.Properties')
            self.player = dbus.Interface(obj,'org.mpris.MediaPlayer2.Player')

    def get_dbus_address(self):
        with open('/tmp/omxplayerdbus.' + self.user, 'r') as f:
            addr = f.read().strip()
        return addr

    def start_omx_player(self):
        cmd = '/usr/bin/omxplayer -o hdmi -b %s' % self.movie
        p = Popen(shlex.split(cmd), stdout=file(os.devnull), env={'DISPLAY' : ':0', 'USER' : self.user})
        #p.communicate()
        time.sleep(2) # to make sure dbus is available TODO: necessary?

    def send_command(self, command):
        self.player.Action(dbus.Int32(str(DBUS_COMMANDS[command])))

    def status(self):
        return (
            self.properties.Duration(),
            self.properties.Position(),
            self.properties.PlaybackStatus() == 'Playing'
        )

    def pause(self):
        self.send_command('pause')

    def stop(self):
        self.send_command('stop')


