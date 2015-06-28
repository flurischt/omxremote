import json
from flask import Flask, Response
from flask import jsonify


app = Flask(__name__)


@app.route('/')
def index():
    return app.send_static_file('index.html')


@app.route('/api/status')
def status():
    #TODO get status via dbus
    data = {'filename' : 'test.avi', 'progress' : 15, 'duration' : 100}
    return jsonify(data)


@app.route('/api/list')
def list():
    #TODO get status via dbus
    data = [{'filename' : 'a.avi', 'hash' : 'asdf'}, {'filename' : 'b.avi', 'hash' : 'bsdf'}]
    return Response(json.dumps(data),  mimetype='application/json')


if __name__ == '__main__':
    app.run(debug=True)
