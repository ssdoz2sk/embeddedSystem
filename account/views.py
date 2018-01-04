from django.contrib.auth.models import User
from django.shortcuts import render

# Create your views here.
from rest_framework import mixins, permissions, views, status
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.settings import api_settings

from account.serializer import UserSerializer, UserRegisterSerializer, UserUpdateSerializer, AuthTokenSerializer

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class UserList(views.APIView):
    throttle_classes = ()
    permission_classes = (permissions.IsAuthenticated, permissions.IsAdminUser)  # IsAdminUser?
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    serializer_class = UserSerializer

    def get(self, request):
        users = User.objects.all()
        serializer = self.serializer_class(users, many=True)
        return Response(serializer.data)


    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request':request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class UserDetail(views.APIView):
    throttle_classes = ()
    permission_classes = (permissions.IsAuthenticated, )
    authentication_classes = (TokenAuthentication, SessionAuthentication)

class UserRegister(views.APIView):
    throttle_classes = ()
    permission_classes = ()
    authentication_classes = ()
    serializer_class = UserRegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_201_CREATED)


class UserChangePassword(views.APIView):
    throttle_classes = ()
    permission_classes = ()
    authentication_classes = (JSONWebTokenAuthentication, )
    serializer_class = UserUpdateSerializer

    def post(self, request):
        user = request.user
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        user.set_password(serializer.data.get('password'))
        user.save()

        return Response(status=status.HTTP_200_OK)


class UserLogin(views.APIView):
    throttle_classes = ()
    permission_classes = ()
    authentication_classes = ()
    serializer_class = AuthTokenSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request':request})
        if serializer.is_valid():
            user = serializer.validated_data['user']
            payload = jwt_payload_handler(user)
            return Response(
                {'token': jwt_encode_handler(payload), 'username': user.username})

        return Response({'message': '帳號或密碼錯誤'}, status=status.HTTP_403_FORBIDDEN)

class UserGetMe(views.APIView):
    throttle_classes = ()
    permission_classes = (permissions.IsAuthenticated, )
    authentication_classes = (TokenAuthentication, JSONWebTokenAuthentication)
    serializer_class = UserSerializer

    def get(self, request):
        serializer = self.serializer_class(request.user)
        return Response(serializer.data)

class ObtainJWTFromSocialProvider(APIView):
    throttle_classes = ()
    permission_classes = ()

    def get(self, request):
        if request.user.is_authenticated:
            payload = jwt_payload_handler(request.user)
            return Response({'token': jwt_encode_handler(payload), 'username': request.user.username}) # 回傳JWT token及使用者帳號
        return Response(status=status.HTTP_401_UNAUTHORIZED)
