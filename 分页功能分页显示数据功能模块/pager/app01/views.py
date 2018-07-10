#!/usr/bin/env python
#coding:utf-8

from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse
from app01.models import UserInfo
from htmlhelper import pagerhelper

# Create your views here.

# page参数是前端url进来的
def index(request,page):
    # 以下这段注释是产生测试数据使用
    '''
    for i in range(315):
        userinfo = UserInfo(Name='chenqiufei'+str(i),Email='chenqiufei@126.com'+str(i),Phone='110110110'+str(i))
        userinfo.save()
    '''
    # page是str类型，需要现将page变量int为整形，才能进行加减乘除操作
    page = int(page)
    # 根据id来进行计算，因为数据库中数据id是从101开始的，所以会加上100，计算每页20条数据，计算出大于和小于的值
    ltpage = 100 + 20*(page-1) +1
    gtpage = 100 + page*20
    # 计算出总的数据条数
    totalnum = UserInfo.objects.all().count()
    # 取出当前页的数据
    page_data = UserInfo.objects.filter(id__lt=gtpage, id__gt=ltpage).all()
    # 调用pagerhelper.page函数去处理，返回的p是一些html标签，具体是什么则需要去pagerhelper.page中查看
    p = pagerhelper.page('/index/',totalnum,page)
    return render_to_response('index.html',{'page':p, 'page_data':page_data, 'current_page':page})