from channels import route_class

from project.consumers import DataConsumer, SensorConsumer, DeviceConsumer, ProjectConsumer

channel_routing = [
    route_class(DataConsumer, path=r'^/data/(?P<token>[^/.]+)/$'),
    route_class(SensorConsumer, path=r'^/sensor/(?P<pk>[^/.]+)/$'),
    route_class(DeviceConsumer, path=r'^/device/(?P<pk>[^/.]+)/$'),
    route_class(ProjectConsumer, path=r'^/project/(?P<pk>[^/.]+)/$'),
]
