from django.utils import timezone
from rest_framework import serializers

from project.models import Project, Device, Sensor, SensorData
import logging

from project.utils import mongoClient

logger = logging.Logger(__name__)
logger.level = logging.DEBUG


class ProjectSerializer(serializers.ModelSerializer):
    creater = serializers.CharField(default=serializers.CurrentUserDefault())
    device_count = serializers.IntegerField(read_only=True)
    # Use this method for the custom field
    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'creater', 'device_count', 'created_at', 'updated_at']

    def create(self, validated_data):
        project = Project.create_project(name=validated_data['name'],
                                         creater=validated_data['creater'],
                                         description=validated_data['description'])

        return project

    def update(self, instance, validated_data):
        project = Project.update_project(instance,
                                         name=validated_data['name'],
                                         description=validated_data['description'])

        return project

class ProjectReadSerializer(serializers.ModelSerializer):
    creater = serializers.CharField(default=serializers.CurrentUserDefault())
    device_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'creater', 'device_count', 'created_at', 'updated_at']

class DeviceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Device
        fields = ['id', 'name', 'description', 'project']

    def create(self, validated_data):
        device = Device.create_device(name=validated_data['name'],
                                      project=validated_data['project'],
                                      description=validated_data['description'])

        return device

    def update(self, instance, validated_data):
        device = Device.update_device(instance,
                                      name=validated_data['name'],
                                      description=validated_data['description'])

        return device


class DeviceReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ['id', 'name', 'description', 'project', 'access_token']


class SensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensor
        fields = ['id', 'name', 'showname', 'device', 'data_type', 'updated_at', 'last_upload']

    def create(self, validated_data):
        sensor = Sensor.create_sensor(name=validated_data['name'],
                                      showname=validated_data['showname'],
                                      device=validated_data['device'],
                                      data_type=validated_data['data_type'])

        return sensor

    def update(self, instance, validated_data):
        sensor = Sensor.update_sensor(instance,
                                      name=validated_data['name'],
                                      showname=validated_data['showname'])

        return sensor


class SensorReadSerializer(serializers.ModelSerializer):
    sensor_data = serializers.ListField(read_only=True, default=[])

    class Meta:
        fields = ['id', 'name', 'showname', 'device', 'last_upload']


class DataSerializer(serializers.Serializer):
    token = serializers.CharField(required=True)
    data = serializers.DictField()

    def save(self):
        validated_data = self.validated_data
        data = validated_data['data']

        mongo_client = mongoClient()
        collection = mongo_client.sensor_data

        for key, value in data.items():
            sensor = Sensor.objects.get(device=validated_data['device'], name=key)
            if not collection.find_one({'sensor': sensor.pk}):
                collection.insert({'sensor': sensor.pk, 'data': []})
            if sensor:
                collection.update({'sensor': sensor.pk}, {'$push': {'data': {key: value, '_upload': timezone.now()}}})
        return

    def validate(self, data):
        device = Device.objects.get(access_token=data['token'])
        data['device'] = device

        if not device:
            raise serializers.ValidationError("sensor or token error")
        return data


class DataMqttSerializer(serializers.Serializer):
    device = serializers.CharField(required=True)
    sensor_name = serializers.CharField(required=True)
    value = serializers.CharField(required=True)

    def save(self):
        device = Device.objects.get(pk=self.validated_data['device'])
        sensor = Sensor.objects.get(device=device, name=self.validated_data['sensor_name'])
        value = self.validated_data['value']

        double_value, int_value, bool_value, string_value = None, None, None, None
        try:
            if sensor.data_type == 'double':
                double_value = float(value)
            elif sensor.data_type == 'int':
                int_value = int(value)
            elif sensor.data_type == 'bool':
                bool_value = bool(value)
            elif sensor.data_type == 'string':
                string_value = value
        except ValueError:
            pass
        data = SensorData(sensor=sensor, double_data=double_value, int_data=int_value, bool_data=bool_value, string_data=string_value)
        data.save()


class DataReadSerializer(serializers.Serializer):
    sensor = serializers.UUIDField()
    offset = serializers.IntegerField(required=False)
    sensor_data = serializers.DictField(read_only=True)
    data = serializers.ListField(read_only=True)

    def create(self, validated_data):
        sensor = validated_data['sensor']
        offset = validated_data.get('offset', 0)

        data = SensorData.objects.filter(sensor=sensor).order_by("-datetime")[offset:100+offset]

        if not data:
            data = {}
        return {'sensor': sensor, 'data': data.get('data', [])}
