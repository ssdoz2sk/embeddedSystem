import uuid
from datetime import datetime

import json

import secrets
from bson import ObjectId
from django.contrib.auth.models import User
from django.utils import timezone

from djongo import models

import logging

logger = logging.Logger(__name__)
logger.level = logging.DEBUG


class Project(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=False)
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
