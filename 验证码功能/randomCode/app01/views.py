#!/usr/bin/env python
#coding:utf-8

from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.template.context import RequestContext

# 登录程序，判断请求的方式是不是POST，如果是，则使用django自带的auth认证去认证获取到的账号密码；如果请求的方式不是POST，那就直接返回登录页面
def login(request):
    if request.method == "POST":
        vcode = request.POST.get('vcode')
        session_code = request.session['verifycode']
        username,password = request.POST.get('username'),request.POST.get('password')
        user = auth.authenticate(username=username,password=password)
        # 判断用户的账号密码是否验证通过
        if user is not None:
            # 判断用户输入的验证码是否正确
            if vcode.upper() == session_code:
                auth.login(request, user)
                # 如果验证通过了，返回首页
                return HttpResponseRedirect('/')
            else:
                return render_to_response('login.html',{'verifycode_error':'验证码输入错误！'},context_instance=RequestContext(request))
        else:
            # 如果账号密码验证不通过，也是返回登录页面，顺带把变量'login_error':'用户名或密码错误！'传到前端login.html页面上
            return render_to_response('login.html',{'login_error':'用户名或密码错误！'})
    return render_to_response('login.html',context_instance=RequestContext(request))

# 退出登录的程序也很简单，直接使用django提供的auth.logout方法就可以退出了,退出后返回首页
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')


# 首页程序
def index(request):
    return render_to_response('index.html',{'user':request.user})