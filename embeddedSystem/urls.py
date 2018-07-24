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
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.documentation import include_docs_urls

import account
from account.views import ObtainJWTFromSocialProvider, UserList, UserDetail, UserRegister, UserLogin, UserGetMe, \
    UserChangePassword
from project.views import ProjectList, ProjectDetail, DeviceList, DeviceDetail


urlpatterns = [
    path('admin/', admin.site.urls),
    path('social-auth/', include('social_django.urls', namespace='social')),
    re_path('api/token/?', ObtainJWTFromSocialProvider.as_view(), name='rest_social_auth'),
    re_path('api/user/?', include('account.urls')),
    re_path('api/register/?', UserRegister.as_view()),
    re_path('api/login/?', UserLogin.as_view()),
    re_path('api/changepassword/?', UserChangePassword.as_view()),
    re_path('api/get-me/?', UserGetMe.as_view()),
    re_path('api/project/?', ProjectList.as_view()),
    re_path('api/project/<pk>/?', ProjectDetail.as_view()),
    re_path('api/device/?', DeviceList.as_view()),
    re_path('api/device/<pk>/?', DeviceDetail.as_view()),
    # url(r'^api/', include(router.urls)),
]
