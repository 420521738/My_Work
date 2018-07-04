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
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required

# Create your views here.

class UserForm(forms.Form):
    username = forms.CharField(label='用户名')
    password = forms.CharField(label='密   码',widget=forms.PasswordInput())

# 修改密码的表单
class ChangeForm(forms.Form):
    username = forms.CharField(label='用户名')
    old_password = forms.CharField(label='原密码',widget=forms.PasswordInput())
    new_password = forms.CharField(label='新密码',widget=forms.PasswordInput())

# 先写登录处理程序
def Login(request):
    next=request.GET.get('next','/')
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

# 跳转到注册页
def regist_pub(request):
    return render_to_response('regist_pub.html',context_instance=RequestContext(request))

# 注册页面返回来的数据处理
def regist_sub(request):
    if request.method == 'POST':
        signature = request.POST.get('signature')
        your_first_pass = request.POST.get('password')
        your_second_pass = request.POST.get('password2')
        form = UserForm(request.POST)
        if form.is_valid():
            #获得表单数据
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            if your_first_pass == your_second_pass:
                # 判断用户是否存在
                user = auth.authenticate(username = username,password = password)
                if user:
                    #添加到session
                    request.session['username'] = username
                    #调用auth登录
                    auth.login(request, user)
                    #重定向到首页
                    return HttpResponseRedirect('/')
                else:
                    #添加到数据库（还可以加一些字段的处理）
                    user = User.objects.create_user(username=username, password=password)
                    user_id = User.objects.get(username=username).id
                    bbs_user = models.BBS_user.objects.create(user_id=user_id,signature=signature)
                    user.save()
                    bbs_user.save()
                    #重定向到首页
                    return HttpResponseRedirect('/acc_login/')
            else:
                return render_to_response('regist_pub.html',context_instance=RequestContext(request))
    else:
        return render_to_response('regist_pub.html',context_instance=RequestContext(request))

# 用户中心页面
@login_required
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

@login_required
def article(request):
    user_id = request.user.id
    author_id = models.BBS_user.objects.get(user_id=user_id).id
    this_user_article = models.BBS.objects.filter(author__id=author_id)
    return render_to_response('myarticle.html',{'article_list':this_user_article,'user':request.user})

@login_required
def delarticle(request,delarticle_id):
    article_id = delarticle_id
    models.BBS.objects.filter(id=article_id).delete()
    return HttpResponse("删除成功!<a href='/myarticle/'>文章管理</a>")
    
@login_required
def change_pass(request):
    if request.method == 'POST':
        uf = ChangeForm(request.POST)
        if uf.is_valid():
            username = uf.cleaned_data['username']
            old_password = uf.cleaned_data['old_password']
            new_password = uf.cleaned_data['new_password']
 
            ##判断用户原密码是否匹配
            UserResult = authenticate(username = username , password = old_password)
            if UserResult is not None:
                if UserResult.is_active:
                    UserResult.set_password(new_password)
                    UserResult.save()
                    user = auth.authenticate(username = username,password = new_password)
                    auth.login(request, user)
                    info = "密码修改成功!<a href='/user/'>用户中心</a>"
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
    bbs_category = models.Category.objects.all()
    return render_to_response('bbs_detail.html',{'bbs_obj':bbs,'current_path':request.path,'user':request.user,'bbs_category':bbs_category,'cate_id':0},context_instance=RequestContext(request))

@login_required
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

@login_required
def bbs_pub(request):
    return render_to_response('bbs_pub.html',context_instance=RequestContext(request))

@login_required
def bbs_sub(request):
    #print '=========>',request.POST.get('content')
    content = request.POST.get('content')
    title = request.POST.get('title')
    summary = request.POST.get('summary')
    category_id = request.POST.get('category_id')
    author = models.BBS_user.objects.get(user__username=request.user)
    models.BBS.objects.create(
            title = title,
            summary = summary,
            content = content,
            author = author,
            category_id = category_id,
            view_count = 1,
            ranking = 2,
        )
    bbs_id = models.BBS.objects.get(title=title,author=author).id
    return HttpResponseRedirect('/detail/%s/' % bbs_id,{'context_instance':RequestContext(request)}) 

