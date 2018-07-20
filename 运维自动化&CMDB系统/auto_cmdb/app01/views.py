#!/usr/bin/env python
#coding:utf-8

from django.shortcuts import render
from django.http.response import HttpResponse
from rest_framework import viewsets
from django.contrib.auth.models import User, Group
from serializers import *
from app01 import models
# 这个api_view是装饰器的一种，属于rest_framework的，可以让django使用put、get、delete、post方法
# django默认只有post和get方法
from rest_framework.decorators import api_view
from rest_framework.response import Response

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

@api_view(['GET', 'PUT', 'POST', 'DELETE'])
def DjangoUsers(request,id=None):
    # 这里为什么是大写的DATA，可以通过测试打断点，可以看到request里面有DATA这个字段包含了信息
    data = request.DATA
    # 创建一条新的记录,POST是创建
    if request.method == 'POST':
        # 序列化前端提交过来的数据，与数据库里的格式进行比较
        user_obj = UserSerializer(data=data)
        # 如果提交的信息是有效的
        if user_obj.is_valid():
            # 保存到数据库
            user_obj.save()
            return HttpResponse('Records is reated!')
        else:
            # 如果不符合，那么则调用rest_framework的Response进行标准格式的输出
            return Response(user_obj.errors,status=404)
    elif request.method == 'PUT':
        user_object = User.objects.get(id=id)
        user_obj = UserSerializer(user_object,data=data)
        if user_obj.is_valid():
            user_obj.save()
            return HttpResponse('Record is updated!')
        else:
            return Response(user_obj.errors,status=404)




