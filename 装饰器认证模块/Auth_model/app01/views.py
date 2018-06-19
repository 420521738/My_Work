#!/usr/bin/env python
#coding:utf-8
from django.shortcuts import render,render_to_response
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse,HttpResponseRedirect

# Create your views here.

# 登录执行方法，返回页面login.html
def Login(request):
    return render_to_response('login.html')

# 账户验证方法
def acc_login(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    # auth.authenticate是用户的认证方法
    user = auth.authenticate(username=username,password=password)
    print username,password
    if user is not None:    #意思是用户是活跃的
        # 正确的账号密码，用户就会别标记为“active”，活跃的
        auth.login(request,user)
        content = ''' 
            Welcome %s !!!
            <a href='/logout/'>Logout</a>
         ''' % user.username
        # 如果认证通过了，就跳转到/下，也就是什么也不加
        return HttpResponseRedirect('/')
    else:
        # 如果验证失败了，就跳转到login.html页面，还把错误信息返回
        return render_to_response('login.html',{'login_err':'Wrong username or password.'})
    
def logout_view(request):
    user = request.user    
    auth.logout(request)
    return HttpResponse("<b>%s</b> logged out! <br/><a href='/index/'>Re-login</a>" % user)

#启用装饰器，用户什么也不加，直接访问的时候，需要先正确登录
@login_required
def Index(request):
    # 确认用户登录后，返回index.html页面，并将用户名返回
    return render_to_response('index.html',{'user':request.user})
