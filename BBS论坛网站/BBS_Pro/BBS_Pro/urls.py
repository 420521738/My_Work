#!/usr/bin/env python
#coding:utf-8

from django.conf.urls import patterns, include, url
from django.contrib import admin
import app01.urls
from app01 import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'BBS_Pro.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login',{'template_name':'login.html'}),
    # 用户登录页
    url(r'^login/$', views.Login),
    url(r'^acc_login/$', views.Acc_login),
    url(r'^logout/$', views.Logout_view),
    url(r'', include(app01.urls)),
)
