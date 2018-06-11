#!/usr/bin/env python
#coding:utf-8

from django.shortcuts import render_to_response,redirect
from django.http import HttpResponse
from django.template.context import RequestContext
from web.models import *
from web.forms.AccountForm import LoginForm

# 先写登录处理程序
def Login(request):
    # 这个data是登录提示信息，账号密码错误的时候会提示该信息，正确的时候该信息为空的
    data = {'LoginStatus':''}
    # 先判断/admin/login 这个请求是get方式还是post方式
    # /admin/login 这个请求是post方式
    if request.method == 'POST':
        # 先将post过来的数据存下来
        postData = request.POST
        username = postData.get('username')
        password = postData.get('password')
        # 如果账号和密码不为空
        if username and password:
            # UserInfo为数据库模型，UserInfo.objects.filter就是到数据库中过滤web_userinfo这张表里是否有这个用户名和密码，并统计条数
            result = UserInfo.objects.filter(UserName=username,PassWord=password).count()
            # 如果查询数据库得出的结果条数为1，那就是账号密码验证正确
            if result == 1:
                # 账号密码验证通过后，跳转到url：/admin/index，这个url是做什么的，可以到web下的urls文件中去查
                return redirect('/admin/index')
        # 如果账号密码存在，但是数据库中查不到该账号密码，那就提示账号密码错误
        data['LoginStatus'] = '用户名或者密码错误！'
    # 如果不是post方式，就直接返回Account/Login.html这个页面
    # 其中context_instance=RequestContext(request) 这个是防止跨站请求伪造而写的，在html页面的form表单中也要添加{% csrf_token %}
    return render_to_response('Account/Login.html',data,context_instance=RequestContext(request))

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
                    return redirect('/admin/index')
        else:
            return render_to_response('Account/LoginForm.html',{'model':loginForm},context_instance=RequestContext(request))
    loginForm = LoginForm()
    return render_to_response('Account/LoginForm.html',{'model':loginForm},context_instance=RequestContext(request))



