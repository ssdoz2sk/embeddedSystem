from mqtt.event import Event

import logging

logger = logging.getLogger('web-logger')


def on_connect(client, userdata, flags, rc):
    logger.info("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    # client.subscribe("project/#")
    client.subscribe("device/#")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    topic = msg.topic.split('/')

    if len(topic) == 3:
        if topic[0] == 'device':
            from project.serializer import DataMqttSerializer

            device_id = topic[1]
            sensor_name = topic[2]
            value = msg.payload.decode('UTF-8')
            serializer = DataMqttSerializer(data={'device': device_id, 'sensor_name': sensor_name, 'value': value})
            serializer.is_valid(raise_exception=True)
            serializer.save()




def register_project_mqtt():
    Event.register('on_connect', on_connect)
    Event.register('on_message', on_message)