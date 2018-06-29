#!/usr/bin/env python
#coding:utf-8

from django.shortcuts import render,render_to_response
from django.http import HttpResponse,HttpResponseRedirect
import models
from django.template.context import RequestContext
from django.contrib import auth
from django.contrib import comments
from django.contrib.auth.models import User
from django import forms
from models import User
from django.contrib.auth import authenticate

# Create your views here.

class UserForm(forms.Form):
    username = forms.CharField(label='用户名')
    password = forms.CharField(label='密   码',widget=forms.PasswordInput())
    #last_login = forms.DateTimeField()

class ChangeForm(forms.Form):
    username = forms.CharField(label='用户名')
    old_password = forms.CharField(label='原密码',widget=forms.PasswordInput())
    new_password = forms.CharField(label='新密码',widget=forms.PasswordInput())

# 先写登录处理程序
def Login(request):
    next=request.GET.get('next','/')
    #print next
    return render_to_response('login.html',{'current_path':next},context_instance=RequestContext(request))

# 账户验证方法
def Acc_login(request):
    next=request.GET.get('next','/')
    username = request.POST.get('username')
    password = request.POST.get('password')
    # auth.authenticate是用户的认证方法
    user = auth.authenticate(username=username,password=password)
    #print username,password
    if user is not None:    #意思是用户是活跃的
        # 正确的账号密码，用户就会别标记为“active”，活跃的
        auth.login(request,user)
        return HttpResponseRedirect('%s' % next)
    else:
        # 如果验证失败了，就跳转到login.html页面，还把错误信息返回
        return render_to_response('login.html',{'LoginStatus':'Wrong username or password.','current_path':next},context_instance=RequestContext(request))

def user(request):
    user = request.user
    #print user
    userid = request.user.id
    #print userid
    userinfo = User.objects.get(username=user)
    signature = models.BBS_user.objects.get(user_id=userid)
    #print signature
    #print userinfo
    return render_to_response('UserDetail.html',{'UserInfo':userinfo,'user':request.user,'signature':signature})

def change_pass(request):
    if request.method == 'POST':
        uf = ChangeForm(request.POST)
        if uf.is_valid():
            username = uf.cleaned_data['username']
            print '11111',username
            old_password = uf.cleaned_data['old_password']
            print '22222',old_password
            new_password = uf.cleaned_data['new_password']
            print '33333',new_password
 
            ##判断用户原密码是否匹配
            UserResult = authenticate(username = username , password = old_password)
            if UserResult is not None:
                if UserResult.is_active:
                    UserResult.set_password(new_password)
                    UserResult.save()
                    info = '密码修改成功!'
                else:
                    info = '没有权限'
            else:
                info = '旧密码错误!'
 
        return HttpResponse(info)
    else:
        uf = ChangeForm()
    return render_to_response('change.html',{'uf':uf},context_instance=RequestContext(request))

def Logout_view(request):
    user = request.user    
    auth.logout(request)
    bbs_list = models.BBS.objects.all()
    bbs_category = models.Category.objects.all()
    return render_to_response('index.html',{'bbs_list':bbs_list,'user':request.user,'bbs_category':bbs_category,'cate_id':0})
    #return HttpResponse("<b>%s</b> logged out! <br/><a href='/login/'>Re-login</a>" % user)

def index(request):
    bbs_list = models.BBS.objects.all()
    bbs_category = models.Category.objects.all()
    #print bbs_category
    return render_to_response('index.html',{'bbs_list':bbs_list,'user':request.user,'bbs_category':bbs_category,'cate_id':0})

def category(request,cate_id):
    bbs_list = models.BBS.objects.filter(category__id=cate_id)
    bbs_category = models.Category.objects.all()
    return render_to_response('index.html',{'bbs_list':bbs_list,'user':request.user,'bbs_category':bbs_category,'cate_id':int(cate_id)})

def bbs_detail(request,bbs_id):
    bbs = models.BBS.objects.get(id=bbs_id)
    return render_to_response('bbs_detail.html',{'bbs_obj':bbs,'current_path':request.path,'user':request.user},context_instance=RequestContext(request))

def sub_comment(request):
    #print request.POST
    bbs_id = request.POST.get('bbs_id')
    comment = request.POST.get('comment_content')
    comments.models.Comment.objects.create(
        content_type_id = 7,
        object_pk = bbs_id,
        site_id = 1,
        user = request.user,
        comment = comment,
        )
    return HttpResponseRedirect('/detail/%s/' % bbs_id,{'context_instance':RequestContext(request)})

def bbs_pub(request):
    return render_to_response('bbs_pub.html',context_instance=RequestContext(request))

def bbs_sub(request):
    #print '=========>',request.POST.get('content')
    content = request.POST.get('content')
    title = request.POST.get('title')
    summary = request.POST.get('summary')
    author = models.BBS_user.objects.get(user__username=request.user)
    models.BBS.objects.create(
            title = title,
            summary = summary,
            content = content,
            author = author,
            view_count = 1,
            ranking = 2,
        )
    return HttpResponse('发布成功！') 

