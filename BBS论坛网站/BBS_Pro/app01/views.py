#!/usr/bin/env python
#coding:utf-8

from django.shortcuts import render,render_to_response
from django.http import HttpResponse,HttpResponseRedirect
import models
from django.template.context import RequestContext
from django.contrib import auth
from django.contrib import comments

# Create your views here.

# 先写登录处理程序
def Login(request):
    return render_to_response('login.html',context_instance=RequestContext(request))

# 账户验证方法
def Acc_login(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    # auth.authenticate是用户的认证方法
    user = auth.authenticate(username=username,password=password)
    #print username,password
    if user is not None:    #意思是用户是活跃的
        # 正确的账号密码，用户就会别标记为“active”，活跃的
        auth.login(request,user)
        return HttpResponseRedirect('/')
    else:
        # 如果验证失败了，就跳转到login.html页面，还把错误信息返回
        return render_to_response('login.html',{'LoginStatus':'Wrong username or password.'},context_instance=RequestContext(request))

def Logout_view(request):
    user = request.user    
    auth.logout(request)
    bbs_list = models.BBS.objects.all()
    return render_to_response('index.html',{'bbs_list':bbs_list})
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
    return render_to_response('bbs_detail.html',{'bbs_obj':bbs,'user':request.user},context_instance=RequestContext(request))

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

