"""embeddedSystem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
# from channels import route
from django.conf.urls import url, include
from django.contrib import admin

# We use a single global DRF Router that routes views from all apps in project
from django.urls import path, re_path

import account
from account.views import ObtainJWTFromSocialProvider, UserList, UserDetail, UserRegister, UserLogin, UserGetMe, \
    UserChangePassword
from project.views import ProjectList, ProjectDetail, DeviceList, DeviceDetail, SensorList, SensorDetail, DataView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('social-auth/', include('social_django.urls', namespace='social')),
    re_path(r'^api/token/?', ObtainJWTFromSocialProvider.as_view(), name='rest_social_auth'),
    re_path(r'^api/user/?', include('account.urls')),
    re_path(r'^api/register/?', UserRegister.as_view()),
    re_path(r'^api/login/?', UserLogin.as_view()),
    re_path(r'^api/changepassword/?', UserChangePassword.as_view()),
    re_path(r'^api/get-me/?', UserGetMe.as_view()),
    re_path(r'^api/projects/?', ProjectList.as_view()),
    re_path(r'^api/project/(?P<pk>\w{8}-\w{4}-\w{4}-\w{4}-\w{12})/?$', ProjectDetail.as_view()),
    re_path(r'^api/devices/?', DeviceList.as_view()),
    re_path(r'^api/device/(?P<pk>\w{8}-\w{4}-\w{4}-\w{4}-\w{12})/?$', DeviceDetail.as_view()),
    re_path(r'^api/sensors/?', SensorList.as_view()),
    re_path(r'^api/sensor/(?P<pk>\w{8}-\w{4}-\w{4}-\w{4}-\w{12})/?$', SensorDetail.as_view()),
    re_path(r'^api/data/?$', DataView.as_view()),
    # url(r'^api/', include(router.urls)),
]
