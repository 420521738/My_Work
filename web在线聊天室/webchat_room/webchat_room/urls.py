#!/usr/bin/env python
#coding:utf-8

from django.conf.urls import patterns, include, url
from django.contrib import admin
from app01 import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'webchat_room.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login',{'template_name':'login.html'}),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/$', views.login),
    url(r'^logout/$', views.logout),
    url(r'^logoutroom/$', views.logoutroom),
    url(r'^delroomuser/(\d+)/$', views.delroomuser),
    url(r'^$', views.index),
    url(r'^index/$', views.index),
    url(r'^room/(\d+)/$', views.room),
    url(r'^savemsg/$', views.savemsg),
    url(r'^getmsg/$', views.getmsg),
)
