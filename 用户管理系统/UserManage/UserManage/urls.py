#!/usr/bin/env python
#coding:utf-8

from django.conf.urls import patterns, include, url
from django.contrib import admin
import web.urls

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'UserManage.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    #url(r'^admin/', include(admin.site.urls)),
    
    # 先设定url的入口，以xxx/admin/进来的，都交给web下面的url去处理
    url(r'^admin/', include(web.urls)),
)
