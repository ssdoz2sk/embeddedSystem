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
from channels import route
from django.conf.urls import url, include
from django.contrib import admin

# We use a single global DRF Router that routes views from all apps in project
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.documentation import include_docs_urls

import account
from account.views import ObtainJWTFromSocialProvider, UserList, UserDetail, UserRegister, UserLogin, UserGetMe, \
    UserChangePassword
from embeddedSystem.routers import HybridRouter
from project.views import ProjectList, ProjectDetail, DeviceList, DeviceDetail, SensorList, SensorDetail, DataView

router = HybridRouter()

# app views and viewsets
router.add_api_view(r'user_register', url('^register/$', UserRegister.as_view(), name=r"register"))
router.add_api_view(r'user_login', url('^login/$', UserLogin.as_view(), name=r"login"))
router.add_api_view(r'user_changepassword', url('^changePassword/', UserChangePassword.as_view(), name=r"changePassowrd"))
router.add_api_view(r'user_getme', url('^getMe/$', UserGetMe.as_view(), name=r"getMe"))
router.add_api_view(r'project', url(r'^project/$', ProjectList.as_view(), name=r"project"))
router.add_api_view(r'project_detail', url(r'^project/(?P<pk>[^/.]+)/$', ProjectDetail.as_view(), name=r"project_detail"))
router.add_api_view(r'device', url(r'^device/$', DeviceList.as_view(), name=r"device"))
router.add_api_view(r'device_detail', url(r'^device/(?P<pk>[^/.]+)/$', DeviceDetail.as_view(), name=r"project_detail"))
router.add_api_view(r'sensor', url(r'^sensor/$', SensorList.as_view(), name=r"sensor"))
router.add_api_view(r'sensor_detail', url(r'^sensor/(?P<pk>[^/.]+)/$', SensorDetail.as_view(), name=r"sensor_detail"))
router.add_api_view(r'data', url(r'^data/(?P<token>[^/.]+)/$', DataView.as_view(), name=r"data"))

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^social-auth/', include('social_django.urls', namespace='social')),
    url(r'^api/token/', ObtainJWTFromSocialProvider.as_view(), name='rest_social_auth'),
    url(r'^api/user/$', include('account.urls')),
    url(r'^api/', include(router.urls, namespace='api')),
    url(r'^docs/', include('rest_framework_docs.urls')),
]
