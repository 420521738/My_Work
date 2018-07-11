#!/usr/bin/env python
#coding:utf-8

from django.conf.urls import patterns, include, url
from django.contrib import admin
from app01 import views
from app01 import viewUtil

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'randomCode.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    
    # 登录程序
    url(r'^verifycode/$', viewUtil.verifycode),
    
    # 验证码程序
    url(r'^login/$', views.login),
    
    # 退出账号程序
    url(r'^logout/$', views.logout),
    
    # 首页程序
    url(r'^$', views.index),
    url(r'^index/$', views.index),
)
