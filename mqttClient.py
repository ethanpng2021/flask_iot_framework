from paho.mqtt import client as mqtt
from datetime import datetime
from config import PahoMqttConfig

class PahoMqttClient:
    def __init__(self, broker, port, subscribe_topic, publish_topic, client_id):
        self.broker = broker
        self.port = port
        self.subscribe_topic = subscribe_topic
        self.publish_topic = publish_topic
        self.client_id = client_id

    def connect_and_subscribe(self, on_message):
        def on_connect(client, userdata, flags, rc):
            if rc != 0:
                print(f"[{datetime.now()}]Failed to connect, return code %d\n", rc)

        self.client = mqtt.Client(self.client_id)
        self.client.on_connect = on_connect
        self.client.connect(self.broker, self.port)
        self.client.subscribe(self.subscribe_topic)
        self.client.on_message = on_message

    def publish(self, msg):
        result = self.client.publish(self.publish_topic, msg)
        # result: [0, 1]
        status = result[0]
        if status == 0:
            print(f"[{datetime.now()}]Send `{msg}`")
        else:
            print(f"Failed to send message to topic {self.publish_topic}")

        self.client.on_publish

if __name__ == '__main__':
    def on_message(client, userdata, msg):
        print(f"[{datetime.now()}]Received: `{msg.payload.decode()}`")

    mqttClient = PahoMqttClient(PahoMqttConfig['broker'], PahoMqttConfig['port'], PahoMqttConfig['client_topic'],PahoMqttConfig['server_topic'], 'client')
    mqttClient.connect_and_subscribe(on_message)
    mqttClient.publish("Hello World")
    mqttClient.client.loop_forever()