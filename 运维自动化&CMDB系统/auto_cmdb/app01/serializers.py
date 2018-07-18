#!/usr/bin/env python
#coding:utf-8

from rest_framework import routers, serializers, viewsets
from django.contrib.auth.models import User, Group

# Serializers define the API representation.
# 你要用Serializer去表现哪个表里的数据，跟我们的form是差不多的
# 把model里面的数据变成可序列化的，是在页面上显示的，不是我们平时说的pkile
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        # 只展现哪些数据
        fields = ('url', 'username', 'email', 'is_staff')
        
class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('name',)