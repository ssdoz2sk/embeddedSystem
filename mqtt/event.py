import json
import logging

logger = logging.getLogger('mqtt-logger')


class Event(object):
    _observers = []

    @classmethod
    def register(cls, event, observer):
        if observer not in cls._observers:
            cls._observers.append([event, observer])

    @classmethod
    def unregister(cls, event, observer):
        if observer in cls._observers:
            cls._observers.remove([event, observer])

    @classmethod
    def notify(cls, target, **kwargs):
        for (event, observer) in cls._observers:
            if target == event:
                observer(**kwargs)