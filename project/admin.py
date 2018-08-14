from django.contrib import admin
from .models import Project, Device, Sensor
# Register your models here.


class ProjectAdmin(admin.ModelAdmin):
    pass


class DeviceAdmin(admin.ModelAdmin):
    pass


class SensorAdmin(admin.ModelAdmin):
    list_display = ('name', 'showname', 'updated_at')


admin.site.register(Project, ProjectAdmin)
admin.site.register(Device, DeviceAdmin)
admin.site.register(Sensor, SensorAdmin)