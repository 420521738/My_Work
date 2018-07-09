#!/usr/bin/env python
#coding:utf-8

from django.shortcuts import render
from django.shortcuts import render_to_response,HttpResponse
from django.shortcuts import HttpResponse
from django.shortcuts import HttpResponseRedirect
from app01 import models
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core.context_processors import request
import json


msg_dic = {}

# 登录程序，判断请求的方式是不是POST，如果是，则使用django自带的auth认证去认证获取到的账号密码；如果请求的方式不是POST，那就直接返回登录页面
def login(request):
    if request.method == "POST":
        username,password = request.POST.get('username'),request.POST.get('password')
        user = auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request, user)
            # 如果验证通过了，返回首页
            return HttpResponseRedirect('/')
        else:
            # 如果账号密码验证不通过，也是返回登录页面，顺带把变量'login_error':'用户名或密码错误！'传到前端login.html页面上
            return render_to_response('login.html',{'login_error':'用户名或密码错误！'})
    return render_to_response('login.html')

# 退出登录的程序也很简单，直接使用django提供的auth.logout方法就可以退出了,退出后返回首页
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')

#@login_required
#def logoutroom(request):
#    # 点击房间页面内的“退出房间按钮，就会触发这个函数
#    return render_to_response('logoutroom.html',{'user':request.user})

# 首页程序
def index(request):
    # 使用django的数据库models查询chatroom这张表里的所有数据，返回房间数据以及当前登录用户数据给index.html页面
    rooms = models.ChatRoom.objects.all()
    return render_to_response('index.html',{'rooms':rooms,'user':request.user})

@login_required
def room(request,id):
    # 这是进入房间显示的页面，id是从前端index页面传回来的，是房间号
    room_obj = models.ChatRoom.objects.get(id=id)
    # 判断当前即将进入房间的用户是否已经记录到chataccount这个表了，这个表是用来记录用户是否在房间的依据
    record_count = models.ChatAccount.objects.filter(room=room_obj,user=request.user).count()
    # 如果用户没进入过这个房间，那就在数据库中插入一条记录
    if not record_count:
        record = models.ChatAccount.objects.create(room=room_obj,user=request.user)
        record.save()
    # 如果用户已经进入了该房间，则直接获取用户列表，member_list并不是真正的用户列表，如果要取到名字，需要member_list.user.username，传到前端后，前端就是这么获取想要的数据的
    member_list = models.ChatAccount.objects.filter(room=room_obj)
    return render_to_response('room.html',{'room_obj':room_obj,'member_list':member_list,'user':request.user})

@login_required
def delroomuser(request,id):
    # 用户点击“退出房间”的按钮时，会在确认退出之后执行这个函数
    user_id = request.user.id
    room_id = id
    # 删除掉这个用户在这个房间的数据库里的在线记录
    models.ChatAccount.objects.filter(room_id=room_id,user_id=user_id).delete()
    # 退出房间后，仍然是返回首页
    return HttpResponseRedirect('/')

@login_required
def savemsg(request):
    # 这个是从前端获取到信息并将信息保存到字典里的程序，字典的key是房间号，值是【id,roomid,msg,sendtime,name】
    id,roomid,msg,sendtime,name = request.POST.get('id'),request.POST.get('roomid'),request.POST.get('msg'),request.POST.get('sendtime'),request.POST.get('name')
    # 字典在本python文件最前面是空字典，这里先判断字典是否有房间号的key
    if msg_dic.has_key(int(roomid)):
        msg_dic[int(roomid)].append([id,msg,sendtime,name])
        print msg_dic
    else:
    # 如果没有，则创建字典
        msg_dic[int(roomid)] = [[id,msg,sendtime,name]]
        #print msg_dic
    # 这个保存前端返回来的聊天信息的程序不需要往后端再返回数据，所以无须返回
    return HttpResponse('OK')

@login_required
def getmsg(request):
    # 这个是前端的定时器定时获取聊天池里面的信息的程序，客户端是多个的，你不获取聊天池信息，你就看不到别人发的消息
    # 前端页面发了一个字典过来，key是roomid
    roomid = request.GET.get('roomid')
    # 先把指定房间的聊天池信息用空来表示，防止字典里没有这个房间号的key而取值出现错误
    msglist = []
    # 如果有前端页面传过来的roomid为key对应的信息
    if msg_dic.has_key(int(roomid)):
        # 这里记得需要int，不然会出现编码错误，前端传过来的数据，到了后端已经变成字符串了，需要进行int转换
        msglist = msg_dic[int(roomid)]
        #print msglist
    # 将指定房间的聊天池信息用json进行包装，前端页面拿到数据化也需要json反序列化
    return HttpResponse(json.dumps(msglist))

@login_required
def getuserlist(request):
    # 这是一个房间页面左上角获取在线实时用户的程序
    # 前端页面传回一个字典，keyi是roomid
    id = request.GET.get('roomid')
    room_obj = models.ChatRoom.objects.get(id=id)
    member_list = []
    member_list_obj = models.ChatAccount.objects.filter(room=room_obj)
    for i in member_list_obj:
        #print i.user.username
        # 注意这个地方，获取到的member_list只是一个用户id，要取名字，仍需要id.user.username，这个需要看user表的源码
        member_list.append(i.user.username)
    #print member_list[0],member_list[1]
    return HttpResponse(json.dumps(member_list))
