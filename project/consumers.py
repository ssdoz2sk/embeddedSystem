from channels.generic.websockets import JsonWebsocketConsumer, WebsocketConsumer

from project.models import Device
from project.serializer import DataSerializer

import logging

logger = logging.Logger(__name__)
logger.level = logging.DEBUG


class DataConsumer(JsonWebsocketConsumer):
    strict_ordering = False

    def connection_groups(self, **kwargs):
        return ['data-{}'.format(kwargs['token'])]

    def connect(self, message, **kwargs):
        if Device.check_access_token_is_valid(kwargs['token']):
            self.message.reply_channel.send({"accept": True})
        else:
            self.message.reply_channel.send({"accept": False})
            self.close()

    def receive(self, content, **kwargs):
        action = content['action']
        if action == 'create':
            if isinstance(content['data'], list):
                serializer = DataSerializer(data=content['data'], many=True, context={'token': kwargs['token']})
                serializer.is_valid(raise_exception=True)
                serializer.save()
            elif isinstance(content['data'], dict):
                serializer = DataSerializer(data=content['data'], context={'token': kwargs['token']})
                serializer.is_valid(raise_exception=True)
                serializer.save()
        self.send({"status": "ok"})

    def disconnect(self, message, **kwargs):
        pass


class SensorConsumer(JsonWebsocketConsumer):
    http_user = True

    strict_ordering = False

    def connection_groups(self, **kwargs):
        return ['sensor-{}'.format(kwargs['pk'])]

    def connect(self, message, **kwargs):
        self.message.reply_channel.send({"accept": True})

    def receive(self, text=None, bytes=None, **kwargs):
        pass

    def disconnect(self, message, **kwargs):
        pass

class DeviceConsumer(JsonWebsocketConsumer):
    http_user = True

    strict_ordering = False

    def connection_groups(self, **kwargs):
        return ['device-{}'.format(kwargs['pk'])]

    def connect(self, message, **kwargs):
        self.message.reply_channel.send({"accept": True})

    def receive(self, text=None, bytes=None, **kwargs):
        http_user = True
        # 設定觸發器

    def disconnect(self, message, **kwargs):
        pass

class ProjectConsumer(JsonWebsocketConsumer):
    http_user = True

    strict_ordering = False

    def connection_groups(self, **kwargs):
        return ['project-{}'.format(kwargs['pk'])]

    def connect(self, message, **kwargs):
        pass

    def receive(self, text=None, bytes=None, **kwargs):
        pass

    def disconnect(self, message, **kwargs):
        pass

