#!/usr/bin/env python
#coding:utf-8

from django.conf.urls import patterns, include, url
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
import views

# Routers provide an easy way of automatically determining the URL conf.
# 把类变成实例化
router = routers.DefaultRouter()
# 调用register方法，赋一个url叫做users
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'auto_cmdb.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    # 以/cmdb/进来的任何请求，都使用router.urls去解析，也就是上面的router.register里面的url
    url(r'^', include(router.urls)),
)
