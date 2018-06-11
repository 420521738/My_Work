#!/usr/bin/env python
#coding:utf-8

from django.shortcuts import render_to_response,redirect
from django.http.response import HttpResponse
from django.template.context import RequestContext
from web.models import UserInfo
from web.Extensions.HtmlHelper import Pager

# 登录后的首页展示
def Index(request):
    return render_to_response('Home/Index.html')

# 用户列表展示
def UserList(request):
    # 先获取数据库中所有的用户
    result = UserInfo.objects.all()
    # Pager这个是自己写的页面进度条，格式参数可以看Pager函数怎么写的
    page = Pager("http://127.0.0.1:9002/admin/userlist/",2,90,30,10)
    # 返回Home/UserList.html这个html页面，在python文件中，只能指定文件，在html文件中就可以返回url路径
    return render_to_response('Home/UserList.html',{'model':result,'page':page},context_instance=RequestContext(request))

def UserDetail(request,id):
    # 函数有两个参数，request是/admin/userdetail，id是{{item.Nid}}，首先获取这个Nid对应的用户信息，赋给result，result的值赋给key1
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