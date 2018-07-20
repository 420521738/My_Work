#!/usr/bin/env python
#coding:utf-8

from django.conf.urls import patterns, include, url
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
import views

version = 'v1.0'


# Routers provide an easy way of automatically determining the URL conf.
# 把类变成实例化
router = routers.DefaultRouter()
# 调用register方法，赋一个url叫做users
router.register(r'user', views.UserViewSet)
#router.register(r'group', views.GroupViewSet)
router.register(r'view_asset' , views.AssetViewSet)
router.register(r'cmdb_user' , views.UserProfileViewSet)
router.register(r'business_unit', views.BusinessUnitViewSet)
router.register(r'manufactory', views.ManufactoryViewSet)
router.register(r'product_version', views.ProductVersionViewSet)
router.register(r'contract', views.ContractViewSet)
router.register(r'idc', views.IDCViewSet)
router.register(r'server', views.ServerViewSet)
router.register(r'network_device', views.NetworkDeviceViewSet)
router.register(r'software', views.SoftwareViewSet)
router.register(r'cpu', views.CPUViewSet)
router.register(r'monitor', views.MonitorViewSet)
router.register(r'nic', views.NICViewSet)
router.register(r'disk', views.DiskViewSet)
router.register(r'memory', views.MemoryViewSet)
router.register(r'maintainence', views.MaintainenceViewSet)


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'auto_cmdb.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    # 以/api/v1.0/进来的任何请求，都使用router.urls去解析，也就是上面的router.register里面的url
    url(r'^', include(router.urls)),
    (r'add_asset/$', views.add_asset),
    #(r'asset/(\d+)/$', views.submit_asset),
    (r'asset/(\d+)/$', views.asset),
    (r'asset/([\w\.]+)/asset_id/$', views.fetch_asset_id),
    (r'asset_list/$' , views.asset_list),
    (r'asset_list/(\d+)/(\d+)/$', views.asset_list),
    (r'asset_detail/(\d+)/$', views.asset_detail),
    #(r'view_asset/get_detail/(\w+)/(\d+)/$', views.get_asset_detail),
    (r'asset_filter/$', views.asset_filter),
    (r'getsn_api/$', views.asset_api_for_oa),  
    (r'get_assets_summary/$',views.get_assets_summary),
    (r'api_test/$', views.api_test),
)
