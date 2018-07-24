from django.conf.urls import url
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from project.consumers import DataConsumer, SensorConsumer, DeviceConsumer, ProjectConsumer, EchoConsumer

channel_routing = [
    url(r'^ws/data/(?P<token>[^/.]+)/$', DataConsumer),
    url(r'^ws/sensor/(?P<pk>[^/.]+)/$', SensorConsumer),
    url(r'^ws/device/(?P<pk>[^/.]+)/$', DeviceConsumer),
    url(r'^ws/project/(?P<pk>[^/.]+)/$', ProjectConsumer),
    url(r'^ws/echo/$', EchoConsumer),
]

application = ProtocolTypeRouter({
    # (http->django views is added by default)
    'websocket': AuthMiddlewareStack(
        URLRouter(
            channel_routing
        )
    ),
})
