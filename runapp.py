from flask import Flask, render_template
from flask_socketio import SocketIO, emit, send
import paho.mqtt.client as mqtt
from datetime import datetime
import threading
from config import PahoMqttConfig
from mqttClient import PahoMqttClient

# Flask app and socket io
app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('on_broadcast_to_ui')
def on_broadcast_to_ui(data):
    messagePackage = create_return_dict(data['source'], data['message'])
    emit('ui_response', messagePackage, broadcast=True)
    return data['message']

def run_mqtt():
    def on_message(client, userdata, msg):
        messagePackage = create_return_dict('MQTT Client', msg.payload.decode())
        print(f"[{datetime.now()}]Server Received: `{messagePackage['message']}`")
        socketio.emit('ui_response', messagePackage, broadcast=True)
        mqttClient.publish("Hello World")

    mqttClient = PahoMqttClient(PahoMqttConfig['broker'], PahoMqttConfig['port'], PahoMqttConfig['server_topic'],PahoMqttConfig['client_topic'], 'server')
    mqttClient.connect_and_subscribe(on_message)
    mqttClient.client.loop_forever()

def create_return_dict(source, message):
    return {
        'source': source,
        'message': message
    }

if __name__ == '__main__':
    x = threading.Thread(target=run_mqtt)
    x.start()
    socketio.run(app)

    