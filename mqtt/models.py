import logging

from django.contrib.auth.hashers import make_password
from django.db import models

# Create your models here.
logger = logging.Logger(__name__)
logger.level = logging.DEBUG

# Set by
# https://github.com/jpmens/mosquitto-auth-plug#mysql

class MqttUser(models.Model):
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    super_user = models.BooleanField(default=False)

    def __str__(self):
        return self.username

    @classmethod
    def create_user(cls, username, password):
        user = cls(username=username, password=make_password(password))
        user.save()

        return user


class Acl(models.Model):
    username = models.CharField(max_length=200)
    topic = models.TextField()
    rw = models.SmallIntegerField(default=1)  # 1: read only;  2: read-write

    @classmethod
    def create_acl(cls, username, topic, rw=2):
        acl = cls(username=username, topic=topic, rw=rw)
        acl.save()

        return acl

