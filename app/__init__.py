import json
import requests

URL = 'http://0.0.0.0:5000/'

from flask import Flask
app = Flask(__name__)

import logging
logging.basicConfig(filename='error.log',level=logging.DEBUG)

from flask_socketio import SocketIO, emit
async_mode = None
socketio = SocketIO(app, async_mode=async_mode)

script = '''
<script src='/static/socket.io.min.js'></script>
<script>
namespace = 'main';
var socket = io.connect("''' + URL + '''" + namespace);

socket.on('answer', function(mes) {
    console.log(mes);
});

window.setInterval(function() {
    socket.emit('online', {id: 'Hi!'});
    console.log('!');
}, 500);
</script>
'''

@app.route("/", methods=["GET"])
def get():
    return "<h1 style='color:blue'>Hello There!</h1>" + script

@app.route("/post", methods=["GET"])
def post():
    res = requests.post(URL + 'sys').text
    return res

@app.route("/sys", methods=["POST"])
def sys():
    return json.dumps({'123': 456, '789': 'str'})

@socketio.on('online', namespace='/main')
def sockio(mes):
    print(mes)
    socketio.emit('answer', {'id': 'Hoba'}, namespace='/main')

if __name__ == '__main__':
	socketio.run(app, debug=True)