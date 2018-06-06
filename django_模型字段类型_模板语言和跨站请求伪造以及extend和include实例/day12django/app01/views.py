# --*-- coding: utf-8 --*--
from django.shortcuts import render, render_to_response, redirect
from django.http import HttpResponse

# Create your views here.

data = ['张三','李四','ccc','ddd']

def List(request,id):
    if id:
        id = int(id)
        if id>=0 and id<len(data):
            result = data[int(id)]
            return HttpResponse("<h1>"+result+"</h1>")
           
    result = '</br>'.join(data)
    return HttpResponse("<h1>"+result+"</h1>") 

from app01.models import *

def Model(request):
    #model = ColorDic.objects.filter(ColorNmae__contains='e').count()
    #model = ColorDic.objects.filter(ColorNmae__contains='e')[2:4]
    model = ColorDic.objects.values('ColorNmae')
    return HttpResponse(model)
    
def Temp(request):
    return render_to_response('template.html',{'key1':'Chen Qiufei. ','key2':'How old are you ?','key3':'Nice to Meet you.'})

def ModelLoop(request):
    namelist = ['chenqiufei','zhangsan','lisi','wangwu','zhaoliu','wangqi']
    return render_to_response('template.html',{'key1':'Chen Qiufei. ','key2':'How old are you ?','key3':'Nice to Meet you.','names':namelist})

from django.template.context import RequestContext

def Login(request):
    data = {'LoginStatus':''}
    if request.method == 'POST':
        postData = request.POST
        username = postData.get('username')
        password = postData.get('password')
        if username == 'chenqiufei' and password == '123':
            return redirect('/temp/$')
        else:
            data['LoginStatus'] = 'username or password is wrong'
    return render_to_response('login.html',data,context_instance=RequestContext(request))

def Son(request):
    return render_to_response('son.html')   

