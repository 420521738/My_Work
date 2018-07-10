#!/usr/bin/env python
#coding:utf-8

from django.conf.urls import patterns, include, url
from django.contrib import admin
from app01 import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'pager.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    # 首页，默认页参数是1，第一页
    url(r'index/$', views.index,{'page':1}),
    # 非首页，带参数随机
    url(r'index/(?P<page>\d*)/$', views.index),
)
