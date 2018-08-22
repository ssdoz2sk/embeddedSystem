from django.apps import AppConfig
import paho.mqtt.client as mqtt

from mqtt.event import Event
from django.conf import settings

import logging

logger = logging.getLogger('mqtt-logger')



def on_connect(client, userdata, flags, rc):
    logger.info("Connected with result code "+str(rc))
    Event.notify('on_connect', client=client, userdata=userdata, flags=flags, rc=rc)


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    Event.notify('on_message', client=client, userdata=userdata, msg=msg)


class MqttConfig(AppConfig):
    name = 'mqtt'

    def ready(self):
        client = mqtt.Client()
        client.on_connect = on_connect
        client.on_message = on_message

        mqtt_server_ip = "localhost"
        mqtt_server_port = 1883

        if hasattr(settings, 'MQTT_IP'):
            mqtt_server_ip = settings.MQTT_IP

        if hasattr(settings, 'MQTT_PORT'):
            mqtt_server_port = settings.MQTT_PORT

        client.connect(mqtt_server_ip, mqtt_server_port, 60)

        # Blocking call that processes network traffic, dispatches callbacks and
        # handles reconnecting.
        # Other loop*() functions are available that give a threaded interface and a
        # manual interface.
        client.loop_start() # loop_forever()

