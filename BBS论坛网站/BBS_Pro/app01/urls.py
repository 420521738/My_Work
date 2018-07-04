#!/usr/bin/env python
#coding:utf-8

from django.conf.urls import patterns, include, url
import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'BBS_Pro.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    
    # 首页
    url(r'^$',views.index),
    # 文章详情页
    url(r'^detail/(\d+)/$',views.bbs_detail),
    # 评论提交功能
    url(r'^sub_comment/$',views.sub_comment),
    # 文章发表页面
    url(r'^bbs_pub/$',views.bbs_pub),
    # 文章发表提交页面
    url(r'^bbs_sub/$',views.bbs_sub),
    # 板块切换功能
    url(r'^category/(\d+)/$',views.category),
    # 用户中心
    url(r'^user/$',views.user),
    # 用户文章管理功能
    url(r'^myarticle/$',views.article),
    # 用户文章删除功能
    url(r'^delete_ariticle/(\d+)/$',views.delarticle),
    # 密码修改功能
    url(r'^changepass/$',views.change_pass),
)
