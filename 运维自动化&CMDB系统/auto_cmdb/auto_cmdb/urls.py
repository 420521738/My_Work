#!/usr/bin/env python
#coding:utf-8

from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.models import User
import app01
from app01 import views

version = 'v1.0'

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'auto_cmdb.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    #url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/%s/' % version, include('app01.urls')),
)
