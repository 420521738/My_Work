#_*_coding:utf-8_*_

from app01 import models
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count

class AssSummary:
    def __init__(self):
        self.data = {
                'idc':  {},
                'device_type':  {},
                'business_unit':  {},
                'admin':  {},
                'os':  {},
                'manufactory':  {},
                'status':  {},
                'expires':{},
                   
                     }
    
    def collect(self):
        self.__get_idc()
        self.__get_business_unit()
        self.__get_device_type()
        self.__get_manufactory()
        self.__get_device_status()
    def __get_idc(self):
        idcs = models.IDC.objects.all()
        for idc in idcs:    
            server_num = models.Asset.objects.filter(idc__id= idc.id, device_type='server').count()
            switch_num = models.Asset.objects.filter(idc__id= idc.id,device_type='switch').count()
            router_num = models.Asset.objects.filter(idc__id= idc.id,device_type='router').count()
            firewall_num = models.Asset.objects.filter(idc__id= idc.id,device_type='firewall').count()
            storage_num = models.Asset.objects.filter(idc__id= idc.id,device_type='storage').count()   
            idc_info = {
                        'servers':server_num,
                        'switchs':switch_num,
                        'routers':router_num,
                        'firewalls':firewall_num,
                        'storages':storage_num}
            self.data['idc'][idc.id] = { 'data': idc_info,  'idc_name':idc.name  }
 
    def __get_device_type(self):
        assets = models.Asset.objects.all()
        server_num = models.Asset.objects.filter( device_type='server').count()
        switch_num = models.Asset.objects.filter(device_type='switch').count()
        router_num = models.Asset.objects.filter(device_type='router').count()
        firewall_num = models.Asset.objects.filter(device_type='firewall').count()
        storage_num = models.Asset.objects.filter(device_type='storage').count()         
        others =  models.Asset.objects.filter().exclude(device_type__in=['server','switch','router','firewall','storage']).count() 
        
        device_type_info = {
                        'servers':server_num,
                        'switchs':switch_num,
                        'routers':router_num,
                        'firewalls':firewall_num,
                        'storages':storage_num,
                        'others':  others
                            }
        self.data['device_type']['data'] = device_type_info
    def __get_business_unit(self):
        business_units= models.BusinessUnit.objects.all()
        unit_info = {}
        for unit in business_units:
            unit_num = models.Asset.objects.filter(business_unit__id=unit.id).count()
            unit_info[unit.id] = {'data': unit_num, 'unit_name': unit.name} 
        self.data['business_unit']['data'] = unit_info
        
        
    def __get_manufactory(self):
        server_list =list(models.Server.objects.values('manufactory').annotate(ServerCount=Count('manufactory'))  ) 
        network_list =list(models.NetworkDevice.objects.values('manufactory').annotate(NetworkDeviceCount=Count('manufactory')))  
        for i in network_list:
            has_count = 0
            for index,s in enumerate(server_list):    
                if s['manufactory'] == i['manufactory']: #save network data into server list 
                    server_list[index].update(i)
                    has_count +=1
            if has_count == 0: #server list doesn't contain same manufctory for this item ,need to create a new record in server list 
                server_list.append(i)        
        self.data['manufactory'] = {'data': server_list}        
    def __get_device_status(self):
        status_list = list(models.Asset.objects.values('status').annotate(st=Count('id')) ) 
        for i in models.Asset.status_choice:
            for index,item in enumerate(status_list):   
                if item['status'] ==  i[0]:
                        status_list[index]['name'] = i[1]
                        
        self.data['status']['data'] = status_list
        
  