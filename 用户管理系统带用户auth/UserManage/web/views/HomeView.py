#!/usr/bin/env python
#coding:utf-8

from django.shortcuts import render_to_response,redirect
from django.http.response import HttpResponse,HttpResponseRedirect
from django.template.context import RequestContext
from web.models import UserInfo
from web.Extensions.HtmlHelper import Pager
from django.contrib import auth
from django.contrib.auth.decorators import login_required

# 登录后的首页展示
#启用装饰器，用户什么也不加，直接访问的时候，需要先正确登录
@login_required
def Index(request):
    return render_to_response('Home/Index.html')

# 用户列表展示
@login_required
def UserList(request):
    # 先获取数据库中所有的用户
    result = UserInfo.objects.all()
    # Pager这个是自己写的页面进度条，格式参数可以看Pager函数怎么写的
    page = Pager("http://127.0.0.1:9002/userlist/",2,90,30,10)
    # 返回Home/UserList.html这个html页面，在python文件中，只能指定文件，在html文件中就可以返回url路径
    return render_to_response('Home/UserList.html',{'model':result,'page':page},context_instance=RequestContext(request))

@login_required
def UserDetail(request,id):
    # 函数有两个参数，request是/userdetail，id是{{item.Nid}}，首先获取这个Nid对应的用户信息，赋给result，result的值赋给key1
    result = UserInfo.objects.get(Nid=int(id))
    return render_to_response('Home/UserDetail.html',{'key1':result})
    
@login_required
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
    return redirect('/userlist')

@login_required
def DelUser(request):
    postData = request.POST
    nid = postData.get('delnid')
    nid = int(nid)
    UserInfo.objects.filter(Nid=nid).delete()
    return redirect('/userlist')