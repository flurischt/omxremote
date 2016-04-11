import os
import json
import hashlib
from flask import Flask, Response, request, jsonify
from omxremote.dbus_connection import OmxRemote


app = Flask(__name__)

# TODO
SUPPORTED_COMMANDS = ('pause', 'togglesubtitles', 'volumeup', 'volumedown', 'stop', 'seek_forward', 'seek_backward')
VIDEO_FILE_EXTENSIONS = ('.avi', '.mkv', '.mp4')
MOVIES_DIR = os.environ.get('OMXREMOTE_MOVIE_DIR', 'movies_dir/')


# memoize this...
def __find_movie_files():
    data = []
    for path, dirs, files in os.walk(MOVIES_DIR, topdown=True):
        # ignore directories starting with a .
        if dirs > 0:
            i = len(dirs) - 1
            while i >= 0:
                if dirs[i][0] == '.':
                    del(dirs[i])
                i = i - 1
        for f in files:
            if os.path.splitext(f)[1].lower() in VIDEO_FILE_EXTENSIONS:
                absolute = os.path.join(path, f)
                hash = hashlib.sha256(absolute.encode('utf-8')).hexdigest()
                data.append({'filename': f, 'hash': hash, 'absolute': absolute})
    return sorted(data, key=lambda movie: movie['filename'].lower())


@app.route('/')
def index():
    return app.send_static_file('index.html')


@app.route('/api/status')
def status():
    progress, duration, playback = OmxRemote().status()
    # TODO filename...
    # dbus sends in microseconds. just return seconds to the UI
    data = {'filename': '', 'progress': int(progress / 1e6), 'duration': int(duration / 1e6), 'playback': playback}
    return jsonify(data)


@app.route('/api/list')
def list():
    data = __find_movie_files()
    return Response(json.dumps(data), mimetype='application/json')


@app.route('/api/exec/<string:cmd>', methods=['POST'])
def command(cmd):
    assert cmd in SUPPORTED_COMMANDS
    OmxRemote().send_command(cmd)
    print('got command: ' + cmd)
    return jsonify({'status': 'OK'})


@app.route('/api/changeMovie', methods=['POST'])
def change_movie():
    hash = request.form['hash']
    data = __find_movie_files()
    for f in data:  # TODO comparing with every file is obviously stupid...
        if f['hash'] == hash:
            OmxRemote().play_movie(f['absolute'])
            return jsonify({'status': 'OK'})
    return jsonify({'status': 'FAIL'})
