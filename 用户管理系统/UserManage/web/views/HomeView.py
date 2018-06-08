#!/usr/bin/env python
#coding:utf-8

from django.shortcuts import render_to_response,redirect
from django.http.response import HttpResponse
from django.template.context import RequestContext
from web.models import UserInfo
from web.Extensions.HtmlHelper import Pager

def Index(request):
    return render_to_response('Home/Index.html')

def UserList(request):
    result = UserInfo.objects.all()
    page = Pager("http://127.0.0.1:9002/admin/userlist/",2,90,30,10)
    return render_to_response('Home/UserList.html',{'model':result,'page':page},context_instance=RequestContext(request))

def UserDetail(request,id):
    result = UserInfo.objects.get(Nid=int(id))
    return render_to_response('Home/UserDetail.html',{'key1':result})
    

def AddUser(request):
    postData = request.POST
    username = postData.get('username')
    name = postData.get('name')
    gender2 = postData.get('gender2')
    password = postData.get('password')
    email = postData.get('email')
    if username and name and password and email:
        userInfo = UserInfo(UserName=username,PassWord=password,RealName=name,Email=email,Gender=gender2)
        userInfo.save()
    return redirect('/admin/userlist')

def DelUser(request):
    postData = request.POST
    nid = postData.get('delnid')
    nid = int(nid)
    UserInfo.objects.filter(Nid=nid).delete()
    return redirect('/admin/userlist')