import os
import json
import hashlib
from flask import Flask, Response, request, jsonify
from omxremote.dbus_connection import OmxRemote


app = Flask(__name__)

#TODO 
SUPPORTED_COMMANDS = ('pause', 'togglesubtitles', 'volumeup', 'volumedown', 'stop')
VIDEO_FILE_EXTENSIONS = ('.avi', '.mkv', '.mp4')
MOVIES_DIR = 'movies_dir/'


@app.route('/')
def index():
    return app.send_static_file('index.html')


@app.route('/api/status')
def status():
    progress, duration, playback = OmxRemote().status()
    #TODO filename...
    data = {'filename' : '', 'progress' : int(progress), 'duration' : int(duration), 'playback' : playback}
    return jsonify(data)


@app.route('/api/list')
def list():
    #TODO memoize os.walk and hashing...
    data = []
    for path,dirs,files in os.walk(MOVIES_DIR):
        for f in files:
            if os.path.splitext(f)[1].lower() in VIDEO_FILE_EXTENSIONS:
                absolute = os.path.join(path, f)
                hash = hashlib.sha256(absolute.encode('utf-8')).hexdigest()
                data.append({'filename' : f, 'hash' : hash})
    return Response(json.dumps(data),  mimetype='application/json')


@app.route('/api/exec/<string:cmd>', methods=['POST'])
def command(cmd):
    assert cmd in SUPPORTED_COMMANDS
    OmxRemote().send_command(cmd)
    print('got command: ' + cmd)
    return jsonify({'status' : 'OK'})


@app.route('/api/changeMovie', methods=['POST'])
def change_movie():
    print(request.form['hash'])
    return jsonify({'status' : 'OK'})


if __name__ == '__main__':
    app.run(debug=True)

