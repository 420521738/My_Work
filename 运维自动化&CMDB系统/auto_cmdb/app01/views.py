#!/usr/bin/env python
#coding:utf-8

from django.shortcuts import render
from rest_framework import viewsets
from django.contrib.auth.models import User, Group
from serializers import *
from app01 import models

# ViewSets define the view behavior.
# 逻辑处理层，把数据取出来之后，需要做什么，跟django里面views里面的功能差不多的
class UserViewSet(viewsets.ModelViewSet):
    # 取出你要的数据
    queryset = User.objects.all()
    # 将取出的数据使用UserSerializer进行序列化
    serializer_class = UserSerializer
    
class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
