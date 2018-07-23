from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from rest_framework import viewsets
import serializers 
import models
import json
import time,random
from rest_framework.decorators import api_view
# Create your views here.



class ConfigurationViewSet(viewsets.ModelViewSet):
    queryset =  models.Host.objects.all()
    serializer_class = serializers.HostSerializer 
    
def monitor_data(request):
    print request.POST 
    
    return HttpResponse('service sends status report success!!')


def graph(request):
    return render_to_response('index.htm')


def graph_data(request):
    '''fake_data = [[1230771600000, -5.8, 0.1],
        [1230858000000, -4.1, 1.4],
        [1230944400000, -0.5, 4.1],
        [1231030800000, -8.9, -0.7],
        [1231117200000, -9.7, -3.7],
        [1231203600000, -3.4, 3.2]]
    '''
    fake_data = []
    start_num = 86400
    for i in range(86400):
        point = [(time.time() -start_num)*1000, random.randrange(100) ]
        fake_data.append(point)
        start_num -=1
        
    
    return HttpResponse(json.dumps(fake_data))
    