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
    # 用户账号密码验功能
    url(r'^acc_login/$', views.Acc_login),
    # 用户退出登录功能
    url(r'^logout/$', views.Logout_view),
    # 用户注册页
    url(r'^regist/$', views.regist_pub),
    # 用户注册写入数据库功能
    url(r'^regist_sub/$', views.regist_sub),
    # 其他的url规则去app01.urls里处理
    url(r'', include(app01.urls)),
)
