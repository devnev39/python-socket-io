import socketio

sio = socketio.Client()

@sio.event
def connect():
    print('client connected !')

sio.connect('http://localhost:3000')