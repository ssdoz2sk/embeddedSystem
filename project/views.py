# Create your views here.
from rest_framework import views, status, permissions
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.response import Response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from project.models import Project, Device
from project.serializer import ProjectSerializer, DeviceSerializer, DeviceReadSerializer

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
        """
        Return a list of all the user's projects.
        ---

        parameters:
        """
        projects = Project.objects.filter(creater=request.user.id)
        for project in projects:
            project.device_count = project.devices.all().count()
            project.sensor_count = 0
            for device in project.devices.all():
                project.sensor_count += device.sensors.all().count()

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

    serializer_class = ProjectSerializer

    def get(self, request, pk):
        project = Project.objects.filter(pk=pk).first()

        serializer = self.serializer_class(project, many=False)

        return Response(serializer.data)

    def put(self, request, pk):
        project = Project.objects.filter(pk=pk).first()
        serializer = self.serializer_class(project, data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    def patch(self, request, pk):
        project = Project.objects.filter(pk=pk).first()
        serializer = self.serializer_class(project, partial=True, data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    def delete(self, request, pk):
        project = Project.objects.filter(pk=pk).first()
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class DeviceList(views.APIView):
    throttle_classes = ()
    permission_classes = (permissions.IsAuthenticated, )
    authentication_classes = (TokenAuthentication, JSONWebTokenAuthentication)

    serializer_class = DeviceSerializer

    def get(self, request):
        project_id = request.GET['p_id']
        devices = Device.objects.filter(project=project_id).all()

        for device in devices:
            device.sensor_count = device.sensors.all().count()
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
        project = Device.objects.filter(pk=pk).first()
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# class DataView(views.APIView):
#     throttle_classes = ()
#     permission_classes = ()
#     authentication_classes = (TokenAuthentication, )
#
#     serializer_class = DataSerializer
#
#     def post(self, request, token):
#         serializer = self.serializer_class(data=request.data, context={'token': token})
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#
#         return Response(status=status.HTTP_201_CREATED)

