import uuid
from datetime import datetime

import json

import secrets
from bson import ObjectId
from channels import Group
from django.contrib.auth.models import User
from django.utils import timezone

from django.db import models
from mongoengine import Document, EmbeddedDocument, fields

import logging

logger = logging.Logger(__name__)
logger.level = logging.DEBUG


class Project(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=False)
    name = models.CharField(max_length=200)
    creater = models.ForeignKey(User, related_name='projects')
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now,
                                      verbose_name='date joined')
    updated_at = models.DateTimeField(default=timezone.now,
                                      verbose_name='date changed')

    def __str__(self):
        return self.name

    @classmethod
    def create_project(cls, name, creater, description=None):
        now = datetime.now()

        project = cls(name=name, creater=creater, description=description,
                      created_at=now, updated_at=now)
        project.save()

        return project

    def update_project(self, name, description=None):
        now = datetime.now()

        self.name = name
        self.description = description
        self.updated_at = now
        self.save()
        return self


class Device(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=False)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    project = models.ForeignKey(Project, related_name='devices', on_delete=models.CASCADE)
    access_token = models.CharField(max_length=50)
    created_at = models.DateTimeField(default=timezone.now,
                                      verbose_name='date joined')
    updated_at = models.DateTimeField(default=timezone.now,
                                      verbose_name='date changed')

    def __str__(self):
        return self.name

    @classmethod
    def create_device(cls, name, project, description=None):
        now = datetime.now()
        access_token = secrets.token_urlsafe(32)
        device = cls(name=name, project=project, description=description,
                     access_token = access_token,
                     created_at=now, updated_at=now)
        device.save()

        return device

    def update_device(self, name, description=None):
        now = datetime.now()

        self.name = name
        self.description = description
        self.updated_at = now
        self.save()

        return self

    @staticmethod
    def check_access_token_is_valid(token):
        return Device.objects.filter(access_token=token).count() != 0


class Sensor(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=False)
    name = models.CharField(max_length=200)
    device = models.ForeignKey(Device, related_name='sensors', on_delete=models.CASCADE)
    last_update = models.DateTimeField(null=True, blank=True, default=None)
    created_at = models.DateTimeField(default=timezone.now,
                                      verbose_name='date joined')
    updated_at = models.DateTimeField(default=timezone.now,
                                      verbose_name='date changed')

    def __str__(self):
        return self.name

    @classmethod
    def create_sensor(cls, name, device):
        now = datetime.now()

        sensor = cls(name=name, device=device,
                     created_at=now, updated_at=now)

        sensor.save()

        return sensor

    def update_sensor(self, name):
        now = datetime.now()

        self.name = name
        self.updated_at = now

        self.save()

        return self

    def ws_pass_created_data(self, data):
        from project.serializer import DataSerializer

        data_serializer = DataSerializer(data, many=False)
        message = {'data': data_serializer.data}
        sensor_group = 'sensor-{}'.format(self.id)
        Group(sensor_group).send({'text': json.dumps(message)})

    def update_last_data_update(self, **kwargs):
        now = datetime.now()
        self.last_update = now
        self.save()
        return self


class Data(Document):
    value = fields.DynamicField()
    created_at = fields.DateTimeField(default=timezone.now)
    updated_at = fields.DateTimeField(default=timezone.now)
    sensor = fields.StringField(required=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.value

    @classmethod
    def create_data(cls, sensor, value):
        now = datetime.now()
        data = cls(value=value, sensor=sensor, created_at=now, updated_at=now)
        data.save()

        sensor_u = Sensor.objects.filter(pk=sensor).first()
        Sensor.update_last_data_update(sensor_u)
        Sensor.ws_pass_created_data(sensor_u, data)

        return data
