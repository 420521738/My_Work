#!/usr/bin/env python
#coding:utf-8

from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response
# Create your views here.
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from app01.serializers import *
from models import *
import models 
import sys,uuid
# 这个api_view是装饰器的一种，属于rest_framework的，可以让django使用put、get、delete、post方法
# django默认只有post和get方法
from rest_framework.decorators import api_view
from rest_framework.renderers import JSONRenderer
import json
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework.decorators import detail_route, list_route
from rest_framework import status
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist,MultipleObjectsReturned
import assets
import data_filter
from django.db.models import Sum
import traceback
import api_auth
import asset_summary


divice_types_dic = {
    'server': (models.Server,ServerSerializer),
    'switch': (models.NetworkDevice,NetworkDeviceSerializer),
    'router': (models.NetworkDevice,NetworkDeviceSerializer),
    'firewall': (models.NetworkDevice,NetworkDeviceSerializer),
    'storage' : (models.NetworkDevice,NetworkDeviceSerializer),
    'acc_cpu' : (models.CPU,CPUSerializer),
    'acc_memory' : (models.Memory,MemorySerializer),
    'acc_network_adapter' : (models.NIC,NICSerializer),
    'acc_disk' : (models.Disk,DiskSerializer),
    'acc_monitor' : (models.Monitor,MonitorSerializer),
}
def ultimate_catch(func):
    def __wrapper(arg):
        try:
            print 'in decro'
            func(arg)
            print 'out decro'

        except BaseException as e:
            print e 
    return __wrapper 
    
import linecache


def PrintException():
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    msg= 'EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj)
    return msg
class ultimate_catch2(object):
    def __init__(self,f):
        #print 'inside __init__()'
        self.f = f
        #print self.f.__name
    def __call__(self, request_obj,asset_id):
        try:
            #print '\033[41;1minside call__\033[0m',request_obj,asset_id
            
            #print '\033[41;1margs self.f--------\033[0m ',asset_id
            return self.f(request_obj,asset_id)
        except:
            #print 'err::',e
            err = traceback.format_exc()
            return HttpResponse(err)
            
#@api_view(['GET', 'PUT','POST'])            
class token_required(object):
    def __init__(self,func):
        self.f = func
    
    def __call__(self, request_obj,asset_id):
        print '-------in decroragtor...', dir(request_obj)
        ass_data = request_obj._get_request()
        #data = request_obj.read()
        #print data
        user = ass_data.get('username')
        time_stamp = ass_data.get('time_stamp')
        hash_val = ass_data.get('hash_val')
        token_auth = api_auth.Auth()
        if token_auth.auth(time_stamp,user,hash_val,request_obj.method) is not True: # invalid user 
            return ResponseData(data=token_auth.errors,http_status=400)
        
        return self.f(request_obj,asset_id)
def auth_token(ass_data,request_obj):
    user = ass_data.get('username')
    time_stamp = ass_data.get('time_stamp')
    hash_val = ass_data.get('hash_val')
    token_auth = api_auth.Auth()
    if token_auth.auth(time_stamp,user,hash_val,request_obj.method) is not True: # invalid user 
        
        return token_auth.errors
    else:
        return True
        
def custom_exception_handler(exc):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc)

    # Now add the HTTP status code to the response.
    if response is not None:
        response.data['status_code'] = response.status_code

    return response

def error_response(data,status=400,message='bad request'):
    format_dic = {
        'status': status,
        'message': message,
        'errors': [],
        'help_url': '',
        'request_id':'',
    }
    if type(data) is dict:
        for i in data:
            msg = i.values()[0][0]
            #print '__________>',type(msg),msg,i
            error_msg = {
                'code' : 1002,
                'field': i.keys()[0],
                'message': msg #.encode('utf-8')
            }
            format_dic['errors'].append(error_msg)
    return format_dic

def record_error(request_id, err_data, request_data=''):   
    EventLog.objects.create(
        uuid = request_id,
        post_data= request_data,
        detail = err_data
    )
        
def ResponseData(data,http_status=400,message='bad request',content_type='plain', request_data='not provided'):
    request_id = ''
    if http_status == 400:
        #print '---lin116>',http_status,type(http_status)
        request_id = uuid.uuid4()
        request_id = str(request_id)

    format_dic = {
        'status': http_status,
        'message': message,
        'errors': [],
        'help_url': '',
        'request_id':request_id,
    }

    if type(data) is dict:
        #print data 
        data = data['error_list']
        
        for i in data:
            #print '----82>',i
            if len(i) > 1:
                err_obj,mod_name = i
                field = err_obj.errors.keys()[0]
                msg = err_obj.errors.values()[0][0]
            else:
                mod_name = i.keys()[0]
                field = ''
                msg = i.values()
            error_msg = {
                
                'code' : 1002,
                'mod_name': mod_name,
                'field': field,
                'message': msg, 
            }
            format_dic['errors'].append(error_msg)


    elif type(data) is list:
        for i in data:
            error_msg = {
                'code': 1003,
                'mod_name': '',
                'field': i.keys()[0],
                'message': i.values(),

            }
            format_dic['errors'].append(error_msg)
    
    #return format_dic
    if http_status == 400:
        record_error(request_id, json.dumps(format_dic), json.dumps(request_data) )
    if content_type.startswith('application/json'):
        return HttpResponse(format_dic, status=http_status)
    else:
        #return Response(format_dic,status=status.HTTP_400_BAD_REQUEST)
        return Response(format_dic,status=http_status)
        
                
def add_asset(request):
    #print request.POST
    
    return render_to_response('asset_test.html', context_instance=RequestContext(request))
    
def partial_update(table_name,table_obj, data):
    print '===>',table_name, getattr(models,table_name), data
    table_obj = getattr(models,table_name)
    records = table_obj.objects.filter(sn=data['sn'])
    for item in records:
        for key,value in data.items():
            table_field = getattr(item, key)
            print table_field , value
def validation_check(obj,err_dic,mod_name,data):
    #print '-----------------------------------',obj, err_dic
    if obj.is_valid():
        return err_dic
    else:
        #print obj._name,obj.errors,obj.fields
        for k,err in obj.errors.items():
            if 'already exists' in err[0]:
                #print '--->>>',k,err
                err_dic['exist_list'].append([obj,mod_name,data])  
            else:
                err_dic['error_list'].append([obj,mod_name,data])
            return err_dic
            
@api_view(['GET', 'PUT', 'DELETE','POST']) 
def api_test(request):
    user = request.GET.get('username')
    time_stamp = request.GET.get('time_stamp')
    hash_val = request.GET.get('hash_val')
    token_auth = api_auth.Auth()
    if token_auth.auth(request.build_absolute_uri(), time_stamp,user,hash_val,request.method) is not True: # invalid user 
        return ResponseData(data=token_auth.errors,http_status=400)
    return HttpResponse('done')              
     
#@ultimate_catch2         
@api_view(['GET', 'PUT', 'DELETE','POST']) 
def asset(request,asset_id=1):
    print '--->',request.build_absolute_uri()
    
    if request.method == 'PUT' or request.method == 'POST':
        ass_data = request.DATA
        #print ass_data
        if not request.content_type.startswith('application/json'):
            try:
                ass_data = json.loads(ass_data['data'])
                #ass_data = json.loads(ass_data)
                #print ass_data
            except ValueError,e:
                return ResponseData(data='',http_status=400 ,message="invalid data provided.. Err:%s" %e,request_data=ass_data)

            if type(ass_data) is dict and len(ass_data) > 0:
                pass
                #ass_data = ass_data #first item stores all the asset data 
            else:
                print len(ass_data), type(ass_data)
                return ResponseData(data=ass_data,http_status=400,request_data=ass_data)
                print '--------------------------------------------------'
        # user validation part 
        '''user = ass_data.get('username')
        time_stamp = ass_data.get('time_stamp')
        hash_val = ass_data.get('hash_val')
        token_auth = api_auth.Auth()
        if token_auth.auth(time_stamp,user,hash_val,request.method) is not True: # invalid user 
            return ResponseData(data=token_auth.errors,http_status=400,request_data=ass_data)
        '''
        #end user validation part     
        acc_handle = assets.Asset(ass_data)
        response_data = acc_handle.data_handle()
        if  acc_handle.is_valid(): #check whether there's error in all the components 
            #print 'no error in components'
            if acc_handle.has_exist_component():
                acc_handle.update_component()
            
            acc_handle_result = acc_handle.create_server()
            
            #print ':::|acc_handle result',acc_handle.update_server_succeess
            if acc_handle.update_server_succeess is True: #no error 
                print '---sever has been create or updated successfully..'
                acc_handle.record_changes_new_server()
                return ResponseData(data=acc_handle_result,http_status=200 ,message='sever has been created or updated successfully..',request_data=ass_data)
            else:
                #print '---line 193'
                #print '---line 194',acc_handle.validation_check_dic['error_list']
                #return ResponseData(data=acc_handle.validation_check_dic['error_list'],http_status=400 ,message='server is not created...')
                return ResponseData(data=acc_handle.validation_check_dic,http_status=400 ,message='server is not created...',request_data=ass_data)
        elif acc_handle.update_server_succeess is False:
            return ResponseData(data=acc_handle.validation_check_dic['error_list'],http_status=400,request_data=ass_data )
        else:
            print '++++++++++++>error needs to be fixed'
            return ResponseData(data=acc_handle.errors,http_status=400 ,request_data=ass_data)
        return HttpResponse('dd')
@api_view(['GET', 'PUT', 'DELETE','POST'])
@csrf_exempt
def submit_asset(request,asset_id):
    print '====|>', asset_id,request.method ,request.content_type
    if request.method == 'PUT' or request.method == 'POST':
        
        ass_data = request.DATA
        #print ass_data
        if not request.content_type.startswith('application/json'):
            try:
                ass_data = json.loads(ass_data['data'])
                #ass_data = json.loads(ass_data)
                print ass_data
            except ValueError:
                #error_obj = error_response(data='')
                #print error_obj
                #return HttpResponse(error_obj,status=400)
                return ResponseData(data='',http_status=400 ,message="invalid data provided..")

            if type(ass_data) is dict and len(ass_data) > 0:
                print '----->goes here--type '
                #ass_data = ass_data #first item stores all the asset data 
            else:

                #error_obj = error_response(data=ass_data, status =400, message="invalid data ")
                #print error_obj, '++++++++'
                #return HttpResponse(error_obj,status=400)
                print len(ass_data), type(ass_data)
                return ResponseData(data=ass_data,http_status=400 )
                print '--------------------------------------------------'
        
        validation_check_list = []
        validation_check_dic = {
            'error_list': [],
            'exist_list': [] # 灏嗗簱閲屽凡缁忓瓨鍦ㄧ殑绾綍鏀惧埌杩欓噷锛岀劧鍚庣粺涓�鏇存柊
        }
        print '----->goes here--cpu count '
        #if ass_data.has_key('modify_notify'): #server type
        if ass_data.has_key('cpu_count'): #server type
            #if ass_data['modify_notify'] == 1: # asset has no changes

            if ass_data.has_key('cpu_model'): #create cpu model foreign record 
                cpu_dic = {
                    'sn': ass_data.get('sn'),
                    'model': ass_data.get('cpu_model'),
                    'manufactory':'intel'    
                }
                cpu_model = CPUSerializer(data =cpu_dic ,partial=True)
                
                
                #validation_check_list.append([cpu_model, 'cpu_model'])
                validation_check(cpu_model,validation_check_dic, mod_name= 'cpu_model',data=cpu_dic)
            if ass_data.has_key('nic'): #create nic model foreign record  
                for eth_num,v in ass_data['nic'].items():
                    nic_dic = {
                        'name': eth_num,
                        'sn': ass_data.get('sn'),
                        'model': v.get('model'),
                        'ipaddr': v.get('ipaddress'),
                        'netmask': v.get('netmask'),
                        'mac': v.get('macaddress'),
                    
                    }
                    nic_model= NICSerializer(data = nic_dic,partial=True)
                    #validation_check_list.append([nic_model,'nic.%s' % eth_num])
                    validation_check(nic_model,validation_check_dic, mod_name= 'nic.%s' % eth_num,data=nic_dic)
            if ass_data.has_key('ram_size'): #create ram model foreign record 
                mem_dic =  {
                    "sn":ass_data.get('sn'), 
                    "model": "1", 
                    "manufactory": "", 
                    "slot": 0, 
                    "capacity": 500, 
                }
                ram_model = MemorySerializer(data = mem_dic,partial=True)
                #validation_check_list.append([ram_model, 'ram_size'])
                validation_check(ram_model,validation_check_dic, mod_name= 'ram_size',data=mem_dic)
            
            #make sure all the obj valid
            error_list = []
            
            
            #for k,v  in validation_check_dic.items():
            #    print k,v
                #obj,mod_name  = obj
                #if not obj.is_valid():
                #    print '\033[31;1m*\033[0m' * 30,obj.errors
                #    error_list.append([obj.errors, mod_name])
            if len(validation_check_dic['error_list']) >0: #鏈夐敊璇紝闇�杩斿洖鍓嶇
                return ResponseData(validation_check_dic['error_list'])
            if len(validation_check_dic['exist_list']) >0: #鏁版嵁宸茬粡瀛樺湪锛岄渶鍦ㄦ暟鎹簱閲屾洿鏂�
                print '\033[41;1mwill update list::::::::::::\033[0m'
                for i in validation_check_dic['exist_list']:
                    obj,mod_name,data_dic = i
                    fields = obj.fields.keys()#
                    print '##############-->',fields, mod_name, data_dic

                    partial_update('NIC', obj, data_dic)

            if len(error_list) > 0:
                #error_obj = error_response(error_list)
                #print error_obj
                #return Response(error_obj,status=status.HTTP_400_BAD_REQUEST)
                #return HttpResponse(error_obj)
                return ResponseData(error_list)
            else:
                for (obj,mod_name) in validation_check_list:
                    obj.save()
                #save the total record 
     
                #manytomany and foreign keys
                print '+++++',ass_data.get('sn')
                cpu_obj = CPU.objects.get(sn=ass_data.get('sn') )
                #nic
                nic_obj = NIC.objects.filter(sn=ass_data.get('sn'))
                nic_list = []
                for obj in nic_obj: #loop many to many
                    nic_list.append(obj.id)
                #disk 
                disk_obj = Disk.objects.filter(sn=ass_data.get('sn'))
                disk_list = []
                for obj in disk_obj:
                    disk_list.append( obj.id )
                #mem 
                mem_obj = Memory.objects.filter(sn=ass_data.get('sn'))
                mem_list = []
                for obj in mem_obj:
                    mem_list.append(obj.id)

                ass_data['cpu_model'] = cpu_obj.id
                ass_data['nic'] = nic_list
                ass_data['physical_disk_driver'] = disk_list
                ass_data['ram_slot'] = mem_list            
                
                serializer = ServerSerializer(data=ass_data,partial=True)  
                if serializer.is_valid():
                    serializer.save() 
                    return HttpResponse('Object has been created.')
                else:
                    print serializer.errors
                    return HttpResponse(serializer.errors.items())
        else:
            error_obj = error_response(data='',message='no valid info data detected.')
            return Response(error_obj,status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'GET':
        return HttpResponseRedirect('/api/v1.0/server/')    
class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


    
class AssetViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Asset.objects.all()
    serializer_class = AssetSerializer
    
    
    '''
    serializer_class = AssetSerializer2
    #return Response(serializer_class.data)
    
    
    def get_queryset(self):
        print '=====goes herer....'
        return self.queryset
    #@list_route()
    def get_asset(self, request): 
        qu = Asset.objects.all()

       
        serializer = AssetSerializer(data=qu)
        return Response(serializer.data)
    @list_route()
    def detail(self,request):
        device_type = request.GET.get('device_type')
        asset_id = request.GET.get('asset_id')
        device_obj = divice_types_dic.get(device_type)
        print device_type
        if device_obj is not None:
            try:
                table_obj,serializer_class = device_obj 
                table_data = table_obj.objects.get(asset_id=asset_id)
                print 'line 380..',table_data
                serializer_class.Meta.depth = 2
                serializer_obj = serializer_class(table_data, context={'request': request})
                
                #serializer_obj= AssetSerializer(data = table_data)
                print serializer_obj.data
                return Response(serializer_obj.data)
            except ObjectDoesNotExist,e:
                return ResponseData(data='',message=str(e))
        else:
            return ResponseData(data='',message="invalid device_type '%s' " % device_type)        
     '''   
        
#class get_asset_detail(viewsets.ModelViewSet)
'''        
@api_view(['GET', ]) 
def get_asset_detail(request,device_type,asset_id):
    print device_type,asset_id
    device_obj = divice_types_dic.get(device_type)
    if device_obj is not None:
        table_obj,serializer_class = device_obj 
        table_data = table_obj.objects.get(id=asset_id)
        print 'line 380..',table_data
        #serializer_obj = serializer_class(data =table_data)
        serializer_obj= AssetSerializer(data = table_data)
        print serializer_obj.data
        return Response(serializer_obj.data)
    else:
        print 'no device type found'
    
    return Response('test')
'''
@api_view(['GET', 'POST', ])        
def fetch_asset_id(request,hostname):
    #print 'line 418',hostname
    #print '==>',request.stream
    try:
        asset = Asset.objects.get(hostname__contains= hostname)
        data = {'asset_id': asset.id}
        return HttpResponse(json.dumps(data))
    except (ObjectDoesNotExist,MultipleObjectsReturned) as e:
        
        
        errors = [{'asset': str(e),
                   'request_hostname': hostname }]
        return ResponseData(errors)
       
@api_view(['GET','POST'])
def asset_list(request, page_navi=None,page_item=None):
    if request.method =='GET':
        queryset=[]
        if page_navi is None and page_item is None: #no page navigation, return all items
        
            queryset = Asset.objects.all()
        else:
            page_navi,page_item=int(page_navi), int(page_item)
            
            record_id_start = (page_navi - 1) 
            if record_id_start !=0:#get the first page 
               record_id_start =  record_id_start * page_item
            record_id_end = record_id_start + page_item
            #print 'line 436',record_id_start, record_id_end
            #queryset = Asset.objects.filter(id__range=(record_id_start, record_id_end  ))
            queryset = Asset.objects.all()[record_id_start:record_id_end]
            print queryset
        total_items =  len(Asset.objects.all())  
        
        serializer = AssetSerializer2(queryset, many=True,context={'request': request})
        serializer.data.append({'total_item': total_items})
        return Response(serializer.data,status=status.HTTP_300_MULTIPLE_CHOICES)

@api_view(['GET','POST'])
def asset_detail(request,asset_id):
    
    obj = Asset.objects.filter(id=asset_id)
    #obj = Asset.objects.all()
    print '---lin516:', asset_id, obj
    serializer = AssetSerializer2(obj,context={'request': request})
    return Response(serializer.data,status=status.HTTP_302_FOUND)    
    
        
class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
class BusinessUnitViewSet(viewsets.ModelViewSet):
    queryset = BusinessUnit.objects.all()
    serializer_class = BusinessUnitSerializer   

class ManufactoryViewSet(viewsets.ModelViewSet):
    queryset = Manufactory.objects.all()
    serializer_class = ManufactorySerializer    
class ProductVersionViewSet(viewsets.ModelViewSet):
    queryset =  ProductVersion.objects.all()
    serializer_class = ProductVersionSerializer   
class ContractViewSet(viewsets.ModelViewSet):
    queryset =  Contract.objects.all()
    serializer_class = ContractSerializer   
class IDCViewSet(viewsets.ModelViewSet):
    queryset =  IDC.objects.all()
    serializer_class = IDCSerializer   
class ServerViewSet(viewsets.ModelViewSet):
    queryset =  Server.objects.all()
    serializer_class = ServerSerializer   
class NetworkDeviceViewSet(viewsets.ModelViewSet):
    queryset =  NetworkDevice.objects.all()
    serializer_class = NetworkDeviceSerializer   
class SoftwareViewSet(viewsets.ModelViewSet):
    queryset =  Software.objects.all()
    serializer_class = SoftwareSerializer   
class CPUViewSet(viewsets.ModelViewSet):
    queryset =  CPU.objects.all()
    serializer_class = CPUSerializer   
class MonitorViewSet(viewsets.ModelViewSet):
    queryset =  Monitor.objects.all()
    serializer_class = MonitorSerializer   
class DiskViewSet(viewsets.ModelViewSet):
    queryset =  Disk.objects.all()
    serializer_class = DiskSerializer   
class NICViewSet(viewsets.ModelViewSet):
    queryset =  NIC.objects.all()
    serializer_class = NICSerializer 
class MaintainenceViewSet(viewsets.ModelViewSet):
    queryset =  Maintainence.objects.all()
    serializer_class = MaintainenceSerializer   

class MemoryViewSet(viewsets.ModelViewSet):
    queryset =  Memory.objects.all()
    serializer_class = MemorySerializer   



@api_view(['GET','POST'])
def asset_filter(request):
    '''
    format_dic = {
        #'idc': ['BJ,SJZ', 'contains'],
        'asset__id' : ['3,56,1009,198,65', 'in'],
        'update_at' : ['2014-12-08,2014-12-11', 'range'],
        'manufactory' : ['Dell Inc.', 'contains'],
        'cpu_count' : [2, 'gt'],
        'ram_size' : [128, 'gt'],
        'page_navi': [6,6],
        
    }
    '''
    format_dic = request.GET.get('query_dic')
    #print format_dic
    if format_dic is not None:
        
        Filter = data_filter.AssetFilter(json.loads(format_dic))
        #Filter = data_filter.AssetFilter(format_dic)
        print '----line 595',format_dic
        query_result = Filter.filter()
        
        total_item = ''
        if len(query_result)>0:
            total_item = query_result[-1]
            del query_result[-1]
        serializer = AssetSerializer2(query_result, many=True,context={'request': request})
        serializer.data.append({'total_item': total_item})
        
        return Response(serializer.data,status=status.HTTP_302_FOUND) 
    else:
        return ResponseData('',message='invalid query dic', http_status=status.HTTP_400_BAD_REQUEST) 

def asset_api_for_oa(request):
    
    '''return format  
    {"asset_servicetag":"JHLRD3X",
      "asset_mode":"R610",
      "asset_cpunumber":"2",
      "asset_memnumber":"8",
      "asset_mempersize":"64 GB",
      "asset_vendor":"Dell Inc.",
      "asset_disknum":"6",
      "asset_disksize":"279 GB*6",
      "asset_processor":"Intel(R) Xeon(R) CPU           L5640  @ 2.27GHz,Intel(R) Xeon(R) CPU           L5640  @ 2.27GHz",
      "asset_system":"Microsoft Windows Server 2008 R2 Enterprise",
      "asset_used":"\u6c7d\u8f66\u4e4b\u5bb6",
      "asset_cabinet":"\u77f3\u5bb6\u5e84",
      "asset_idc":"\u8054\u901a5\u5c42\uff08\u65e7\uff09",
      "asset_cabinetnumber":"E5",
      "asset_netnum":2}
    '''
    q_sn = request.GET.get('sn')
    #print '--->',q_sn
    q_callback_str = request.GET.get('jsoncallback')
    
    asset_info = {}
    if q_sn is not None:
        q_sn = q_sn.upper()
    try:
        server_obj = Server.objects.get(sn=q_sn)
        asset_info = {
            'asset_servicetag': server_obj.sn,
            'asset_model': server_obj.model,
            'asset_cpunumber': server_obj.cpu_count,
            'asset_memsize': '%sGB' %server_obj.ram_size,
            'asset_memnumber': Memory.objects.filter(parent_sn=server_obj.asset.id,capacity__gt=0).count() , 
            'asset_vendor': server_obj.manufactory,
            'asset_disknum': server_obj.physical_disk_driver.count(),
            'asset_disksize': '%s GB' % Disk.objects.filter(parent_sn=server_obj.asset.id ).aggregate(Sum('capacity'))['capacity__sum'],
            'asset_processor': server_obj.cpu_model.model,
            'asset_system': 'not valid for now',
            'asset_used': server_obj.asset.client.name,
            'asset_cabinet': server_obj.asset.cabinet_num,
            'asset_idc': server_obj.asset.idc.name,
            'asset_cabinetnumber': server_obj.asset.cabinet_order,
            'asset_netnum': server_obj.nic.count(),     
        
        }
        
        result = json.dumps([asset_info])  
        result_with_callback = '%s(%s)' % (q_callback_str,result) 
        return HttpResponse(result_with_callback)
    except BaseException as err:
        print 'Err:',err
        return HttpResponse(str(err))
    
    
@api_view(['GET','POST'])    
def get_assets_summary(request):
    ass_instance = asset_summary.AssSummary()
    ass_instance.collect()
    print ass_instance.data
    return HttpResponse(json.dumps(ass_instance.data))