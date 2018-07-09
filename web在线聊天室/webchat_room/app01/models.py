#!/usr/bin/env python
#coding:utf-8

from django.db import models
from django.contrib.auth.models import User

# 创建表chatroom，房间列表
class ChatRoom(models.Model):
    name = models.CharField(max_length=100,unique=True)
    
    # 在这里定义返回函数，在django admin的web界面，你想看到这个表里展示的是什么数据，如果不写，就会显示object之类的东西
    def __unicode__(self):
        return self.name

# 创建表chataccount表，用户在这个房间里的记录
class ChatAccount(models.Model):
    room = models.ForeignKey(ChatRoom)
    user = models.ForeignKey(User)
    
    def __unicode__(self):
        return self.room
    