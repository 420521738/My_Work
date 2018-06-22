#!/usr/bin/env python
#coding:utf-8

from django.shortcuts import render_to_response,redirect
from django.http import HttpResponse,HttpResponseRedirect   
from django.template.context import RequestContext
from web.models import *
from web.forms.AccountForm import LoginForm
from django.contrib import auth
from django.contrib.auth.decorators import login_required

# 先写登录处理程序
def Login(request):
    return render_to_response('Account/Login.html',context_instance=RequestContext(request))

# 账户验证方法
def Acc_login(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    # auth.authenticate是用户的认证方法
    user = auth.authenticate(username=username,password=password)
    print username,password
    if user is not None:    #意思是用户是活跃的
        # 正确的账号密码，用户就会别标记为“active”，活跃的
        auth.login(request,user)
        return HttpResponseRedirect('/index/')
    else:
        # 如果验证失败了，就跳转到login.html页面，还把错误信息返回
        return render_to_response('Account/Login.html',{'LoginStatus':'Wrong username or password.'},context_instance=RequestContext(request))

def Logout_view(request):
    user = request.user    
    auth.logout(request)
    return HttpResponse("<b>%s</b> logged out! <br/><a href='/login/'>Re-login</a>" % user)

# 登录处理程序的另一种实现方法
def LoginByForm(request):
    if request.method == 'POST':
        data = request.POST
        # 实例化函数LoginForm到loginForm
        # LoginForm(data)是获取到的数据进行表单合组
        loginForm = LoginForm(data)
        #loginForm.as_table
        # 对loginForm的内容开始验证
        if loginForm.is_valid():
            # loginForm.cleaned_data是组成的那一个table里的数据关系，比如username与其值，password与其值等
            da = loginForm.cleaned_data
            #return HttpResponse('OK')
            username = da.get('username')
            password = da.get('password')
            # 如果账号和密码不为空
            if username and password:
                # UserInfo为数据库模型，UserInfo.objects.filter就是到数据库中过滤web_userinfo这张表里是否有这个用户名和密码，并统计条数
                result = UserInfo.objects.filter(UserName=username,PassWord=password).count()
                # 如果查询数据库得出的结果条数为1，那就是账号密码验证正确
                if result == 1:
                    # 账号密码验证通过后，跳转到url：/admin/index，这个url是做什么的，可以到web下的urls文件中去查
                    return redirect('/index')
        else:
            return render_to_response('Account/LoginForm.html',{'model':loginForm},context_instance=RequestContext(request))
    loginForm = LoginForm()
    return render_to_response('Account/LoginForm.html',{'model':loginForm},context_instance=RequestContext(request))



