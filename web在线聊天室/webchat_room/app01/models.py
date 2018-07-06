#!/usr/bin/env python
#coding:utf-8

from django.db import models
from django.contrib.auth.models import User

class ChatRoom(models.Model):
    name = models.CharField(max_length=100,unique=True)
    
    def __unicode__(self):
        return self.name
    
class ChatAccount(models.Model):
    room = models.ForeignKey(ChatRoom)
    user = models.ForeignKey(User)
    
    def __unicode__(self):
        return self.room
    