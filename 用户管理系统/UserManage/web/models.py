#!/usr/bin/env python
#coding:utf-8

from django.db import models

# Create your models here.

# 创建数据库模型，在这里创建模型后，会在数据库（settings.py文件中设定的db）中穿件一个web_userinfo的表，表里会有下面几个字段，以及每个字段的属性
class UserInfo(models.Model):
    Nid = models.AutoField(primary_key=True)
    UserName = models.CharField(max_length=50)
    PassWord = models.CharField(max_length=256)
    RealName = models.CharField(max_length=256)
    Gender = models.NullBooleanField()
    Email = models.EmailField(max_length=256)