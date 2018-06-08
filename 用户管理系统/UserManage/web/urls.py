#!/usr/bin/env python
#coding:utf-8

from django.conf.urls import patterns,include,url
from django.contrib import admin
#from web import views
from web.views import AccountView
from web.views import HomeView

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'UserManage.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    #url(r'^admin/', include(admin.site.urls)),
    
    # 以下这些url规则都是带了前缀/admin/进来的，所以在访问的时候一定要先加上 /admin/
    url(r'^login/', AccountView.Login),
    url(r'^index/', HomeView.Index),
    url(r'^userlist/$', HomeView.UserList),
    url(r'^userdetail/(?P<id>\d*)/$', HomeView.UserDetail),
    url(r'^adduser/', HomeView.AddUser),
    url(r'^deluser/', HomeView.DelUser),
)