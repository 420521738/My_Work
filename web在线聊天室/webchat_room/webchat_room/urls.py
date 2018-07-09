#!/usr/bin/env python
#coding:utf-8

from django.conf.urls import patterns, include, url
from django.contrib import admin
from app01 import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'webchat_room.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    
    # 使用django auth装饰器所需要配置的一条默认url
    url(r'^accounts/login/$', 'django.contrib.auth.views.login',{'template_name':'login.html'}),
    url(r'^admin/', include(admin.site.urls)),
    
    # 登录程序
    url(r'^login/$', views.login),
    
    # 退出账号程序
    url(r'^logout/$', views.logout),
    
    # 退出房间程序
    #url(r'^logoutroom/$', views.logoutroom),
    
    # 删除房间在线用户程序
    url(r'^delroomuser/(\d+)/$', views.delroomuser),
    
    # 默认首页程序
    url(r'^$', views.index),
    
    # 首页程序
    url(r'^index/$', views.index),
    
    # 进入房间程序
    url(r'^room/(\d+)/$', views.room),
    
    # 保存用户在房间发表的消息的程序
    url(r'^savemsg/$', views.savemsg),
    
    # 定时器获取房间聊天内容的程序
    url(r'^getmsg/$', views.getmsg),
    
    # 获取实时房间在线用户的程序
    url(r'^getuserlist/$', views.getuserlist),
)
