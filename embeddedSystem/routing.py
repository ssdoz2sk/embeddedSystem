from channels import route_class

from project.consumers import DataConsumer, SensorConsumer, DeviceConsumer, ProjectConsumer

channel_routing = [
    route_class(DataConsumer, path=r'^/ws/data/(?P<token>[^/.]+)/$'),
    route_class(SensorConsumer, path=r'^/ws/sensor/(?P<pk>[^/.]+)/$'),
    route_class(DeviceConsumer, path=r'^/ws/device/(?P<pk>[^/.]+)/$'),
    route_class(ProjectConsumer, path=r'^/ws/project/(?P<pk>[^/.]+)/$'),
]
