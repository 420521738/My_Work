#!/usr/bin/env python
#coding:utf-8

from django.contrib import admin
from app01 import models

# Register your models here.

# 在这个注册的数据库表，在django的admin的web页面里都可以看到与管理 
admin.site.register(models.ChatRoom)
admin.site.register(models.ChatAccount)
