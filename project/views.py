# Create your views here.
from django.http import Http404
from rest_framework import views, status, permissions
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.response import Response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from project.models import Project, Device, Sensor
from project.serializer import ProjectSerializer, DeviceSerializer, DeviceReadSerializer, ProjectReadSerializer, \
    SensorSerializer, SensorReadSerializer, DataSerializer, DataReadSerializer

import logging

logger = logging.Logger(__name__)
logger.level = logging.DEBUG

class ProjectList(views.APIView):
    """
        schema_url: /api/project

        post:
            Create a new project.
   """
    throttle_classes = ()
    permission_classes = (permissions.IsAuthenticated, )
    authentication_classes = (TokenAuthentication, JSONWebTokenAuthentication)

    serializer_class = ProjectSerializer

    def get(self, request):
        projects = Project.objects.filter(creater=request.user.id)
        for project in projects:
            project.device_count = project.devices.all().count()

        serializer = ProjectSerializer(projects, many=True)

        return Response(serializer.data)

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request':request})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)


class ProjectDetail(views.APIView):
    throttle_classes = ()
    permission_classes = (permissions.IsAuthenticated, )
    authentication_classes = (TokenAuthentication, JSONWebTokenAuthentication)

    serializer_class = ProjectReadSerializer

    def get_object(self, pk):
        try:
            return Project.objects.get(pk=pk)
        except Project.DoesNotExist:
            raise Http404


    def get(self, request, pk):
        project = self.get_object(pk)
        serializer = self.serializer_class(project, many=False)

        return Response(serializer.data)

    def put(self, request, pk):
        project = self.get_object(pk)
        serializer = self.serializer_class(project, data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    def patch(self, request, pk):
        project = self.get_object(pk)
        serializer = self.serializer_class(project, partial=True, data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    def delete(self, request, pk):
        project = self.get_object(pk)
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class DeviceList(views.APIView):
    throttle_classes = ()
    permission_classes = (permissions.IsAuthenticated, )
    authentication_classes = (TokenAuthentication, JSONWebTokenAuthentication)

    serializer_class = DeviceSerializer

    def get(self, request):
        project_id = request.GET.get('project', None)
        devices = Device.objects.filter(project=project_id).all()

        serializer = self.serializer_class(devices, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request':request})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

class DeviceDetail(views.APIView):
    throttle_classes = ()
    permission_classes = (permissions.IsAuthenticated, )
    authentication_classes = (TokenAuthentication, JSONWebTokenAuthentication)

    serializer_class = DeviceSerializer
    serializer_readonly_class = DeviceReadSerializer

    def get(self, request, pk):
        device = Device.objects.filter(pk=pk).first()
        serializer = self.serializer_readonly_class(device, many=False)
        return Response(serializer.data)

    def put(self, request, pk):
        device = Device.objects.filter(pk=pk).first()
        serializer = self.serializer_class(device, data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    def patch(self, request, pk):
        device = Device.objects.filter(pk=pk).first()
        serializer = self.serializer_class(device, partial=True, data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    def delete(self, request, pk):
        device = Device.objects.filter(pk=pk).first()
        device.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SensorList(views.APIView):
    throttle_classes = ()
    permission_classes = (permissions.IsAuthenticated, )
    authentication_classes = (TokenAuthentication, JSONWebTokenAuthentication)

    serializer_class = SensorSerializer

    def get(self, request):
        device_id = request.GET.get('device', None)
        project_id = request.GET.get('project', None)
        if device_id:
            sensors = Sensor.objects.filter(device=device_id).all()
        elif project_id:
            sensors = Sensor.objects.filter(device__project=project_id)
        else:
            sensors = []

        serializer = self.serializer_class(sensors, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)


class SensorDetail(views.APIView):
    throttle_classes = ()
    permission_classes = (permissions.IsAuthenticated, )
    authentication_classes = (TokenAuthentication, JSONWebTokenAuthentication)

    serializer_class = SensorSerializer
    serializer_readonly_class = SensorReadSerializer

    def get(self, request, pk):
        sensor = Sensor.objects.filter(pk=pk).first()
        serializer = self.serializer_readonly_class(sensor, many=False)
        return Response(serializer.data)

    def put(self, request, pk):
        sensor = Sensor.objects.filter(pk=pk).first()
        serializer = self.serializer_class(sensor, data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    def patch(self, request, pk):
        sensor = Sensor.objects.filter(pk=pk).first()
        serializer = self.serializer_class(sensor, partial=True, data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    def delete(self, request, pk):
        sensor = Sensor.objects.filter(pk=pk).first()
        sensor.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class DataView(views.APIView):
    throttle_classes = ()
    permission_classes = ()
    # authentication_classes = (TokenAuthentication, )

    serializer_class = DataSerializer
    serializer_read_class = DataReadSerializer

    def get(self, request):
        sensor = request.GET.get('sensor', None)
        serializer = self.serializer_read_class(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_201_CREATED)
