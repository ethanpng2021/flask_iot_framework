from datetime import datetime
import socketio
from config import SocketIOConfig

# socket io
# standard Python
if __name__ == '__main__':
    sio = socketio.Client()
    sio.connect(SocketIOConfig['url'])
    msg = "Hello World"
    data = {'source': 'SockeIO Client', 'message': msg}
    print(f'[{datetime.now()}]Send: {msg}')
    sio.emit('on_broadcast_to_ui', data, callback = (lambda cb: print(f'[{datetime.now()}]Receive: {cb}')))