from django.apps import AppConfig

from project.mqtt import register_project_mqtt


class ProjectConfig(AppConfig):
    name = 'project'

    def ready(self):
        register_project_mqtt()