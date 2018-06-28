#!/usr/bin/env python
#coding:utf-8

from django.conf.urls import patterns, include, url
import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'BBS_Pro.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$',views.index),
    url(r'^detail/(\d+)/$',views.bbs_detail),
    url(r'^sub_comment/$',views.sub_comment),
    url(r'^bbs_pub/$',views.bbs_pub),
    url(r'^bbs_sub/$',views.bbs_sub),
    url(r'^category/(\d+)/$',views.category),
)
