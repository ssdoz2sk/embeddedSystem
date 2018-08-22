from django.contrib import admin

# Register your models here.
from mqtt.models import MqttUser, Acl


class MqttUserAdmin(admin.ModelAdmin):
    list_display = [f.name for f in MqttUser._meta.fields]


class AclAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Acl._meta.fields]


admin.site.register(MqttUser, MqttUserAdmin)
admin.site.register(Acl, AclAdmin)