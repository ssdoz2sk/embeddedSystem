from channels.generic.websocket import JsonWebsocketConsumer, WebsocketConsumer

from project.models import Device

import logging

logger = logging.Logger(__name__)
logger.level = logging.DEBUG


class DataConsumer(JsonWebsocketConsumer):
    strict_ordering = False

    def connection_groups(self, **kwargs):
        return ['data-{}'.format(kwargs['token'])]


    def websocket_connect(self, message, **kwargs):
        if Device.check_access_token_is_valid(kwargs['token']):
            message.reply_channel.send({"accept": True})
        else:
            message.reply_channel.send({"accept": False})
            self.close()

    def websocket_receive(self, content, **kwargs):
        # action = content['action']
        # if action == 'create':
        #     if isinstance(content['data'], list):
        #         serializer = DataSerializer(data=content['data'], many=True, context={'token': kwargs['token']})
        #         serializer.is_valid(raise_exception=True)
        #         serializer.save()
        #     elif isinstance(content['data'], dict):
        #         serializer = DataSerializer(data=content['data'], context={'token': kwargs['token']})
        #         serializer.is_valid(raise_exception=True)
        #         serializer.save()
        self.send({"status": "ok"})

    def websocket_disconnect(self, message, **kwargs):
        pass


class SensorConsumer(JsonWebsocketConsumer):
    http_user = True

    strict_ordering = False

    def connection_groups(self, **kwargs):
        return ['sensor-{}'.format(kwargs['pk'])]

    def websocket_connect(self, message, **kwargs):
        self.message.reply_channel.send({"accept": True})

    def websocket_receive(self, text=None, bytes=None, **kwargs):
        pass

    def websocket_disconnect(self, message, **kwargs):
        pass

class DeviceConsumer(JsonWebsocketConsumer):
    http_user = True

    strict_ordering = False

    def connection_groups(self, **kwargs):
        return ['device-{}'.format(kwargs['pk'])]

    def websocket_connect(self, message, **kwargs):
        self.message.reply_channel.send({"accept": True})

    def websocket_receive(self, text=None, bytes=None, **kwargs):
        http_user = True
        # 設定觸發器

    def websocket_disconnect(self, message, **kwargs):
        pass


class ProjectConsumer(JsonWebsocketConsumer):
    http_user = True

    strict_ordering = False

    def connection_groups(self, **kwargs):
        return ['project-{}'.format(kwargs['pk'])]

    def websocket_connect(self, message, **kwargs):
        pass

    def websocket_receive(self, text=None, bytes=None, **kwargs):
        pass

    def websocket_disconnect(self, message, **kwargs):
        pass


class EchoConsumer(WebsocketConsumer):
    counter = 0
    def connect(self):
        return ['test']

    def connection_groups(self, **kwargs):
        self.counter += 1
        return ['echo-{}'.format(self.counter)]

    def chat_message(self, event):
        self.send(text_data=event.get('text'))

    def disconnect(self, code):
        pass