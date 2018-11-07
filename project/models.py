import uuid
from datetime import datetime

import secrets
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

import logging

logger = logging.Logger(__name__)
logger.level = logging.DEBUG


class Project(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    creater = models.ForeignKey(User, related_name='projects', on_delete=models.CASCADE)
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
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    project = models.ForeignKey(Project, related_name='devices', on_delete=models.CASCADE)
    access_token = models.CharField(max_length=50, unique=True)
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
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    showname = models.CharField(max_length=200)
    device = models.ForeignKey(Device, related_name='sensors', on_delete=models.CASCADE)
    data_type = models.CharField(max_length=100, default='string')
    last_upload = models.DateTimeField(null=True, blank=True, default=None)
    created_at = models.DateTimeField(default=timezone.now,
                                      verbose_name='date joined')
    updated_at = models.DateTimeField(default=timezone.now,
                                      verbose_name='date changed')

    def __str__(self):
        return self.name

    @classmethod
    def create_sensor(cls, name, showname, data_type, device):
        now = datetime.now()
        sensor = cls(name=name, showname=showname, device=device, data_type=data_type,
                     created_at=now, updated_at=now)
        sensor.save()

        return sensor

    def update_sensor(self, name, showname):
        now = datetime.now()

        self.name = name
        self.showname = showname
        self.updated_at = now

        self.save()

        return self


class SensorData(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE, related_name='sensor_data')
    double_data = models.FloatField(null=True, blank=True, default=None)
    int_data = models.BigIntegerField(null=True, blank=True, default=None)
    bool_data = models.NullBooleanField(null=True, blank=True, default=None)
    string_data = models.TextField(null=True, blank=True, default=None)
    datetime = models.DateTimeField(auto_now_add=True)

    @property
    def timestamp(self):
        return int(self.datetime.timestamp())

    @property
    def data(self):
        if self.sensor.data_type == 'double':
            return self.double_data
        if self.sensor.data_type == 'int':
            return self.int_data
        if self.sensor.data_type == 'bool':
            return self.bool_data
        if self.sensor.data_type == 'string':
            return self.string_data
        return None
