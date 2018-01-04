

from django.conf.urls import url, include

from account.views import UserList, UserDetail

urlpatterns = [
    url('^$', UserList.as_view(), name=r"user"),
    url('^(?P<pk>[^/.]+)/$', UserDetail.as_view(), name=r"user")
]