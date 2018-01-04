from rest_framework import serializers
from rest_framework_mongoengine import serializers as mongo_serializers

from project.models import Project, Device, Sensor, Data
import logging

logger = logging.Logger(__name__)
logger.level = logging.DEBUG


class ProjectSerializer(serializers.ModelSerializer):
    creater = serializers.HiddenField(default=serializers.CurrentUserDefault())
    sensor_count = serializers.IntegerField(read_only=True)
    device_count = serializers.IntegerField(read_only=True)
    # Use this method for the custom field
    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'creater', 'sensor_count', 'device_count']

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

class DeviceSerializer(serializers.ModelSerializer):
    sensor_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Device
        fields = ['id', 'name', 'description', 'project', 'sensor_count']

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
        fields = ['id', 'name', 'device', 'last_update']

    def create(self, validated_data):
        sensor = Sensor.create_sensor(name=validated_data['name'],
                                      device=validated_data['device'])

        return sensor

    def update(self, instance, validated_data):
        sensor = Sensor.update_sensor(instance,
                                      name=validated_data['name'])

        return sensor


class DataSerializer(mongo_serializers.DocumentSerializer):
    class Meta:
        model = Data
        fields = ['id', 'sensor', 'value', 'created_at']

    def create(self, validated_data):
        sensor = validated_data['sensor']
        value = validated_data['value']
        try:
            value = float(value)
        except ValueError:
            pass

        data = Data.create_data(sensor=sensor, value=value)

        return data

    def validate(self, data):
        sensor_c = Sensor.objects.filter(id=data['sensor'], device__access_token=self.context['token']).count()
        if sensor_c == 0:
            raise serializers.ValidationError("sensor or token error")
        return data
