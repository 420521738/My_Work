#!/usr/bin/env python
#coding:utf-8

from django.contrib import admin
from app01 import models

# Register your models here.

admin.site.register(models.ChatRoom)
admin.site.register(models.ChatAccount)
