#!/usr/bin/env python
#coding:utf-8

from django.conf.urls import patterns, include, url
from django.contrib import admin
#import web.urls
from web.views import AccountView
from web.views import HomeView

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'UserManage.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    
    # 先设定url的入口，以xxx/admin/进来的，都交给web下面的url去处理
    # 以下这个是需要写的，如果使用了需要登录的装饰器，没有登录的话，默认会跳到login.html
    
    #url(r'^admin/', include(web.urls)),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login',{'template_name':'Account/Login.html'}),
    url(r'^admin/', include(admin.site.urls)),
    # 用户登录页
    url(r'^login/$', AccountView.Login),
    url(r'^acc_login/$', AccountView.Acc_login),
    url(r'^logout/$', AccountView.Logout_view),
    # 使用django的form进行登录验证，登录页的另一种更快捷的写法，这种写法的效果和上面的这种login写法效果一样
    url(r'^loginform/$', AccountView.LoginByForm),
    # 用户登录后的首页
    url(r'^index/$', HomeView.Index),
    # 用户列表页
    url(r'^userlist/$', HomeView.UserList),
    # 用户详情页
    url(r'^userdetail/(?P<id>\d*)/$', HomeView.UserDetail),
    # 增加用户页
    url(r'^adduser/$', HomeView.AddUser),
    # 删除用户页
    url(r'^deluser/$', HomeView.DelUser),
)
