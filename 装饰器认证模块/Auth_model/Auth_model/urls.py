#!/usr/bin/env python
#coding:utf-8

from django.conf.urls import patterns, include, url
from django.contrib import admin
from app01 import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'Auth_model.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    
    # 以下这个是需要写的，如果使用了需要登录的装饰器，没有登录的话，默认会跳到login.html
    url(r'^accounts/login/$', 'django.contrib.auth.views.login',{'template_name':'login.html'}),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/$', views.Login),
    url(r'^acc_login/$', views.acc_login),
    url(r'^logout/$', views.logout_view),
    # 默认什么都不加的时候，执行views.Index方法
    url(r'^$', views.Index),
)
