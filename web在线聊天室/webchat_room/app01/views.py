#!/usr/bin/env python
#coding:utf-8

from django.shortcuts import render
from django.shortcuts import render_to_response,HttpResponse
from django.shortcuts import HttpResponse
from django.shortcuts import HttpResponseRedirect
from app01 import models
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core.context_processors import request
import json


msg_dic = {}

def login(request):
    if request.method == "POST":
        username,password = request.POST.get('username'),request.POST.get('password')
        user = auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request, user)
            return HttpResponseRedirect('/')
        else:
            return render_to_response('login.html',{'login_error':'用户名或密码错误！'})
    return render_to_response('login.html')

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')

def logoutroom(request):
    #return HttpResponseRedirect('/')
    return render_to_response('logoutroom.html',{'user':request.user})

def index(request):
    rooms = models.ChatRoom.objects.all()
    return render_to_response('index.html',{'rooms':rooms,'user':request.user})

@login_required
def room(request,id):
    room_obj = models.ChatRoom.objects.get(id=id)
    record_count = models.ChatAccount.objects.filter(room=room_obj,user=request.user).count()
    if not record_count:
        record = models.ChatAccount.objects.create(room=room_obj,user=request.user)
        record.save()
    member_list = models.ChatAccount.objects.filter(room=room_obj)
    return render_to_response('room.html',{'room_obj':room_obj,'member_list':member_list,'user':request.user})

@login_required
def delroomuser(request,id):
    user_id = request.user.id
    room_id = id
    models.ChatAccount.objects.filter(room_id=room_id,user_id=user_id).delete()
    return HttpResponseRedirect('/')

def savemsg(request):
    id,roomid,msg,sendtime = request.POST.get('id'),request.POST.get('roomid'),request.POST.get('msg'),request.POST.get('sendtime')
    
    if msg_dic.has_key(int(roomid)):
        msg_dic[int(roomid)].append([id,msg,sendtime])
    else:
        msg_dic[int(roomid)] = [[id,msg,sendtime]]
    return HttpResponse('OK')

def getmsg(request):
    roomid = request.GET.get('roomid')
    msglist = []
    if msg_dic.has_key(int(roomid)):
        msglist = msg_dic[int(roomid)]
    return HttpResponse(json.dumps(msglist))
