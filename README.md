# omxremote
omxremote is a mobile friendly webinterface to remote control omxplayer.bin on your raspberry pi. connect the pi to a tv/beamer, and use omxremote with your mobile phone to control video playback.

##STATUS
Currently under development. I'd say it's in beta phase.
What works:
 - chose video and start playback
 - play/pause and stop
 - volume and subtitle control

##TODO
 - implement skip forward/backward, skip to movie-position
 - bugfixes
 - create debian apt repository for raspbian 

##INSTALL
```
apt-get install python-dbus
git clone https://github.com/flurischt/omxremote.git
cd omxremote/
python setup.py install
```
##RUN
Do NOT expose gunicorn to the internet. Use nginx. (TODO: document this)

```OMXREMOTE_MOVIE_DIR=/PATH/TO/YOUR/MOVIES gunicorn -w 2 -b 127.0.0.1:5000 omxremote:app```
