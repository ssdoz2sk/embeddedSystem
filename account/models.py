import binascii

import os
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from six import python_2_unicode_compatible


@python_2_unicode_compatible
class Token(models.Model):
    """
    This is a mongoengine adaptation of DRF's default Token.
    The default authorization token model.
    """
    key = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super(Token, self).save(*args, **kwargs)

    def generate_key(self):
        return binascii.hexlify(os.urandom(20)).decode()

    def __str__(self):
        return self.key