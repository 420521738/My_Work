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
    # 用户登录页
    #url(r'^login/', AccountView.Login),
    # 使用django的form进行登录验证，登录页的另一种更快捷的写法，这种写法的效果和上面的这种login写法效果一样
    #url(r'^loginform/', AccountView.LoginByForm),
    # 用户登录后的首页
    #url(r'^index/', HomeView.Index),
    # 用户列表页
    #url(r'^userlist/$', HomeView.UserList),
    # 用户详情页
    #url(r'^userdetail/(?P<id>\d*)/$', HomeView.UserDetail),
    # 增加用户页
    #url(r'^adduser/', HomeView.AddUser),
    # 删除用户页
    #url(r'^deluser/', HomeView.DelUser),
)