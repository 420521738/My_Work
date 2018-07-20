#!/usr/bin/env python
#_*_coding:utf-8_*_

#import db_conn
#import django
#django.setup()
from django.contrib.auth.models import User, Group
from app01 import models
import json,sys,datetime
import MySQLdb
import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone

from django.core import serializers as JsonSerializer

class Asset(object):
    def __init__(self,data):
        self.validation_check_dic = {
            'error_list': [],
            'exist_list': [] # �������Ѿ����ڵļ�¼�ŵ����Ȼ��ͳһ����
        }
        self.data = data 
        self.update_server_succeess = None
        
        #create a dic contains all m2m fields, this dic will be useing to compare with data from db 
        self.server_m2m_dic = {}
        for field in models.Server._meta.get_m2m_with_model():
            field_name = str(field[0]).split('.')[-1]
            #print '====>',field_name
            self.server_m2m_dic[field_name] = []
        #self.server_update_errors = {}
    def catch_db_exceptions(func):
        def __wrapper(self,arg):
            try:
                func(self,arg)
            except MySQLdb.Warning,e:
                
                self.__gen_exception(arg[1],str(e))
            except ObjectDoesNotExist,e:
                self.__gen_exception(arg[1],str(e))
        return __wrapper
        
    def data_handle(self):

        try:
            asset_obj = models.Asset.objects.get(id = self.data.get('asset_id'))
            #print '111111111111111111111111',self.data.get('asset_id')
            #print dir(asset_obj)
            if self.data.get('not_modify') == 0:
                #check whether this server exists in table Server
                
                server_obj = models.Server.objects.filter(sn=self.data.get('sn'))
                if len(server_obj) == 0: #no records , need create a new one
                    cpu_obj = self.__validate_cpu()
                    nic_obj = self.__validate_nic()
                    ram_obj = self.__validate_ram()
                    raid_obj = self.__validate_raid_adaptor()
                    disk_obj = self.__validate_disk()


                elif len(server_obj) == 1: #server obj already exist,only need to update 
                    cpu_obj = self.__validate_cpu()
                    nic_obj = self.__validate_nic()
                    ram_obj = self.__validate_ram()
                    raid_obj = self.__validate_raid_adaptor()
                    disk_obj = self.__validate_disk()
                else: #more than one returned , abnormal
                    #return self.__gen_exception('server','found more than 1 records in Server table with the same SN number...please check.' )
                    cpu_obj = self.__validate_cpu()
                    nic_obj = self.__validate_nic()
                    ram_obj = self.__validate_ram()
                    raid_obj = self.__validate_raid_adaptor()
                    disk_obj = self.__validate_disk()                
                
                
            else:#device didn't update, only need to update the timestamp of this asset 
                return self.__gen_exception('server',"field 'not_modify' is required... "  % self.data.get('asset_id'))
        except ObjectDoesNotExist:          
            return self.__gen_exception('server','asset id %s not found in db'  % self.data.get('asset_id'))
    def __gen_exception(self,key,message):
        error = {key: message}
        self.validation_check_dic['error_list'].append(error)
        self.update_server_succeess = False
        return self.update_server_succeess       
            
    def update_component(self):
        '''can only run this after run has_exist_component function  '''
        if self.exist_list:
            for i in self.exist_list:
                mod_obj, mod_name, mod_data = i
                #print mod_name, mod_data
                if mod_name == 'cpu_model':
                    self.__update_cpu(i)
                if mod_name.startswith('nic.'):
                    self.__update_nic(i)
                if mod_name.startswith('ram.'):
                    self.__update_ram(i)
                if mod_name.startswith('raid.'):
                    self.__update_raid_adaptor(i)
                if mod_name.startswith('disk.'):
                    self.__update_disk(i)
                if mod_name.startswith('server_obj'):
                    #print '\033[34;1m %s \033[0m\n ' % mod_obj.errors
                    self.__update_server(i)
                    break #server obj only need to loop once 
        self.exist_list = [] #clear exist list 
    @catch_db_exceptions
    def __update_cpu(self,data):
        mod_obj, mod_name, mod_data = data
        print '---line109--- parent_sn : %s'  % mod_data['parent_sn']
        mod_record = models.CPU.objects.get(parent_sn= mod_data['parent_sn'] )
        
        for field, val in mod_data.items(): #compare each field one by one 
            db_val = getattr(mod_record,field)
            if val != db_val: #not same , need to update and record it
                db_field = mod_record._meta.get_field(field) # get field instance out from db 
                db_field.save_form_data(mod_record, val)
                #need to record this change later 
                self.record_changes(mod_data['parent_sn'],field,db_val,val)
        
        mod_record.save()
    @catch_db_exceptions     
    def __update_nic(self,data):
        mod_obj, mod_name, mod_data = data 
        #mod_record = models.NIC.objects.get(parent_sn= mod_data['parent_sn'] ,name=mod_data['name'])
        mod_record = models.NIC.objects.filter(mac= mod_data['mac'])
        mod_record=mod_record[0]
        
        for field, val in mod_data.items(): #compare each field one by one 
            db_val = getattr(mod_record,field)
            #print 'db_val:[%s]==>val:[%s]' %(db_val, val), type(db_val), type(val)
            if val != db_val: #not same , need to update and record it
                db_field = mod_record._meta.get_field(field) # get field instance out from db 
                db_field.save_form_data(mod_record, val)
                #need to record this change later 
                self.record_changes(mod_data['parent_sn'],field,db_val,val)
        
        mod_record.save()  
    @catch_db_exceptions
    def __update_disk(self,data):
        mod_obj, mod_name, mod_data = data 
        #print 'line 126--->',data
        mod_name = mod_name.split('.')[1]
        mod_record = models.Disk.objects.get(parent_sn= mod_data['parent_sn'], slot=mod_name)
        for field, val in mod_data.items(): #compare each field one by one 
            db_val = getattr(mod_record,field)
            if type(db_val) is float:val = float(val)
            elif  type(db_val) is unicode: val = unicode(val)
            #print '==>',db_val, val, 'db_val:',type(db_val), type(val)
            if val != db_val: #not same , need to update and record it
                db_field = mod_record._meta.get_field(field) # get field instance out from db 
                db_field.save_form_data(mod_record, val)
                #need to record this change later 
                self.record_changes(mod_data['parent_sn'],field,db_val,val)
        
        mod_record.save()         
    @catch_db_exceptions     
    def __update_raid_adaptor(self,data):
        mod_obj, mod_name, mod_data = data 
        #print 'raid:::', mod_data, mod_name
        mod_name = mod_name.split('.')[1]
        mod_record = models.RaidAdaptor.objects.get(parent_sn= mod_data['parent_sn'], name=mod_name)
        #print mod_name,'--',mod_record
        for field, val in mod_data.items(): #compare each field one by one 
            db_val = getattr(mod_record,field)
            #print '==>',db_val, val
            if val != db_val: #not same , need to update and record it
                db_field = mod_record._meta.get_field(field) # get field instance out from db 
                db_field.save_form_data(mod_record, val)
                #need to record this change later 
                self.record_changes(mod_data['parent_sn'],field,db_val,val)
        
        mod_record.save()  

        
    @catch_db_exceptions         
    def __update_ram(self,data):
        mod_obj, mod_name, mod_data = data 
        mod_record = models.Memory.objects.get(parent_sn= mod_data['parent_sn'], slot=mod_data['slot'] )
        #print data, '==>', mod_record
        for field, val in mod_data.items(): #compare each field one by one 
            db_val = getattr(mod_record,field)
            #print '==>',db_val, val
            if val != db_val: #not same , need to update and record it
                #print type(val), type(db_val)
                db_field = mod_record._meta.get_field(field) # get field instance out from db 
                db_field.save_form_data(mod_record, val)
                #need to record this change later 
                self.record_changes(mod_data['parent_sn'],field,db_val,val)
        
        mod_record.save()  
        
    def __compare_asset(self,data):
        
        mod_data = data
        db_fields_name =['asset', 'cpu_core_count', 'cpu_count', 'cpu_model', 'created_by',
                         'nic', 'physical_disk_driver',u'raid_adaptor','manufactory','model',
                         'raid_type', 'ram_size', 'ram', 'sn', 'update_at']

        server_record = models.Server.objects.get(asset__id=mod_data['asset_id'])
            
        for db_field in db_fields_name:
            field_obj = server_record._meta.get_field(db_field)
            field_type = str( type(field_obj) )
            if 'ManyToMany' in  field_type:
                new_data_list = []
                m2m_target_model = getattr(models, field_obj.rel.to.__name__)
                mod_data_from_client = self.server_m2m_dic[field_obj.name]
                if field_obj.name == 'physical_disk_driver' or field_obj.name == 'ram':
                    #print '\033[45;1m--%s--\033[0m' % self.server_m2m_dic[field_obj.name]
                    for item in mod_data_from_client: #pull data out from db by puppet sent data 
                        data_in_db = m2m_target_model.objects.get(parent_sn= item['parent_sn'],  slot=item['slot'])
                        #print '---data_in_db', data_in_db
                        new_data_list.append(data_in_db.id)
                elif field_obj.name == 'nic':
                    #print '\033[45;1m--%s--\033[0m' % self.server_m2m_dic[field_obj.name]
                    for item in mod_data_from_client:
                        #print '------>=', item
                        data_in_db = m2m_target_model.objects.get(parent_sn= item['parent_sn'], name= item['name'],  mac=item['mac'])
                        #print '---data_in_db', data_in_db
                        new_data_list.append(data_in_db.id)      
                elif field_obj.name == 'raid_adaptor':
                    #print '\033[45;1m--%s--\033[0m' % self.server_m2m_dic[field_obj.name]
                    for item in mod_data_from_client:
                        data_in_db = m2m_target_model.objects.get(parent_sn= item['parent_sn'],  name=item['name'])
                        #print '---data_in_db', data_in_db
                        new_data_list.append(data_in_db.id)      
                                             
                old_data_list = map(lambda x:x.id, field_obj.value_from_object(server_record))
                #print '-->mod_data[%s] -- [%s]' % (field_obj.name, mod_data.get(field_obj.name) )
                old_data_list = set(old_data_list)
                new_data_list = set(new_data_list)

                #print '\033[45;1mFromPuppet--%s--\033[0m' % new_data_list
                #print '\033[35;1mFromMysql---%s--\033[0m' % old_data_list
                
                if old_data_list != new_data_list: # update many to many to new list  
                    field_obj.save_form_data(server_record, new_data_list)
                    deprecated_list = old_data_list - new_data_list
                    print '==============need to delete :', deprecated_list
                    db_table = getattr(models, field_obj.rel.to.__name__) 
                    deprecated_data = db_table.objects.filter(id__in=deprecated_list)
                    print deprecated_data
                    msg = '''id_list: %s , below data will be deleted right now:  %s 
                    ''' %(new_data_list, JsonSerializer.serialize('json', deprecated_data))
                    self.record_changes(server_record.asset.id,None, field_obj.name,old_data_list, msg)
                    deprecated_data.delete()
            elif 'ForeignKey' in  field_type or 'OneToOneField' in field_type:
                old_val = field_obj.value_from_object(server_record)
                new_val = mod_data[field_obj.name]
                new_val_instance = getattr(models, field_obj.rel.to.__name__)
                if old_val != new_val: #save new value into this foreign field 
                    field_obj.save_form_data(server_record,new_val_instance.objects.get(id=new_val) ) 
                    self.record_changes(server_record.asset.id,None,field_obj.name,old_val, new_val)
            elif 'DateTimeField' in field_type:
                field_obj.save_form_data(server_record,timezone.now())
            else :
                old_val = getattr(server_record, db_field)
                new_val = mod_data.get(field_obj.name)
                if new_val is not None:
                    if 'IntegerField' in field_type:new_val = int(new_val)   
                    #print '------>got herer old:[%s]  new:[%s]' %( old_val, new_val) 
                    if old_val != new_val:
                        
                        field_obj.save_form_data(server_record, new_val)
                        self.record_changes(server_record.asset.id,None, field_obj.name,old_val, new_val)
                else:pass     
        server_record.save()
        
        self.update_server_succeess= True 
        return self.update_server_succeess        
    def __update_server(self,data):
        mod_obj, mod_name, mod_data = data
        db_fields_name =['asset', 'cpu_core_count', 'cpu_count', 'cpu_model', 'created_by',
                         'nic', 'physical_disk_driver',u'raid_adaptor','manufactory','model',
                         'raid_type', 'ram_size', 'ram', 'sn', 'update_at']
        if mod_obj.errors.has_key('asset'):

            server_record = models.Server.objects.get(asset__id=mod_data['asset_id'])
                
            for db_field in db_fields_name:
                field_obj = server_record._meta.get_field(db_field)
                field_type = str( type(field_obj) )
                #print '\033[42;1m%s %s %s \033[0m' %(field_type, field_obj, field_obj.name)
                if 'ManyToMany' in  field_type:
                    new_data_list = []
                    m2m_target_model = getattr(models, field_obj.rel.to.__name__)
                    mod_data_from_client = self.server_m2m_dic[field_obj.name]
                    if field_obj.name == 'physical_disk_driver' or field_obj.name == 'ram':
                        #print '\033[45;1m--%s--\033[0m' % self.server_m2m_dic[field_obj.name]
                        for item in mod_data_from_client: #pull data out from db by puppet sent data 
                            data_in_db = m2m_target_model.objects.get(parent_sn= item['parent_sn'],  slot=item['slot'])
                            #print '---data_in_db', data_in_db
                            new_data_list.append(data_in_db.id)
                    elif field_obj.name == 'nic':
                        #print '\033[45;1m--%s--\033[0m' % self.server_m2m_dic[field_obj.name]
                        for item in mod_data_from_client:
                            print '==>'
                            data_in_db = m2m_target_model.objects.get(parent_sn= item['parent_sn'],  mac=item['mac'])
                            #print '---data_in_db', data_in_db
                            new_data_list.append(data_in_db.id)      
                    elif field_obj.name == 'raid_adaptor':
                        #print '\033[45;1m--%s--\033[0m' % self.server_m2m_dic[field_obj.name]
                        for item in mod_data_from_client:
                            data_in_db = m2m_target_model.objects.get(parent_sn= item['parent_sn'],  name=item['name'])
                            #print '---data_in_db', data_in_db
                            new_data_list.append(data_in_db.id)      
                                                 
                    old_data_list = map(lambda x:x.id, field_obj.value_from_object(server_record))
                    #print '-->mod_data[%s] -- [%s]' % (field_obj.name, mod_data.get(field_obj.name) )
                    old_data_list = set(old_data_list)
                    new_data_list = set(new_data_list)

                    #new_data_list_bak = mod_data[field_obj.name] # collect from client 
                    print '\033[45;1mFromPuppet--%s--\033[0m' % new_data_list
                    print '\033[35;1mFromMysql---%s--\033[0m' % old_data_list
                    #print '\033[46;1m--%s--\033[0m' % new_data_list_bak
                    
                    if old_data_list != new_data_list: # update many to many to new list  
                        field_obj.save_form_data(server_record, new_data_list)
                        self.record_changes(server_record.sn,field_obj.name,old_data_list, new_data_list)
                elif 'ForeignKey' in  field_type or 'OneToOneField' in field_type:
                    old_val = field_obj.value_from_object(server_record)
                    new_val = mod_data[field_obj.name]
                    new_val_instance = getattr(models, field_obj.rel.to.__name__)
                    if old_val != new_val: #save new value into this foreign field 
                        field_obj.save_form_data(server_record,new_val_instance.objects.get(id=new_val) ) 
                        self.record_changes(server_record.sn,field_obj.name,old_val, new_val)
                elif 'DateTimeField' in field_type:
                    field_obj.save_form_data(server_record,timezone.now())
                else :
                    old_val = getattr(server_record, db_field)
                    new_val = mod_data[field_obj.name]
                    if new_val is not None:
                        if 'IntegerField' in field_type:new_val = int(new_val)    
                        if old_val != new_val:
                            field_obj.save_form_data(server_record, new_val)
                            self.record_changes(server_record.sn, field_obj.name,old_val, new_val)
                    else:pass     
            server_record.save()
            
            self.update_server_succeess= True 
        else:
            print '\033[41;1mAre you sure this servr obj has record in Asset table?\033[0m'
            print mod_obj.errors
            return self.__gen_exception('server',"server with sn '%s' bind with another asset id already.err:" % (mod_data.get('sn'),mod_obj.errors ) )
        return self.update_server_succeess
    def __validate_cpu(self):
        if self.data.has_key('cpu_model'): #create cpu model's foreign record 
            cpu_dic = {
                'sn': self.data.get('sn'), #should put the component own sn in here ,instead of it's parent 
                'parent_sn': self.data.get('asset_id'),
                'model': self.data.get('cpu_model'),
                'manufactory':'INTEL>'    
            }
            cpu_model = serializers.CPUSerializer(data =cpu_dic)
            
            if cpu_model.is_valid():
                print 'creating cpu .....'
                cpu_model.save()
                self.record_changes(cpu_dic['parent_sn'], 'cpu', field=None, old=None, new='model:%s' % cpu_dic['model'], event_type=2)
            else:
                self.__update_table(serializers.CPUSerializer, cpu_dic, mod_name= 'cpu_model', table_obj=models.CPU, 
                                    filters={'parent_sn':cpu_dic.get('parent_sn')} )                  
        else:
            print 'not found cpu ....'
    def __validate_nic(self):
        if self.data.has_key('nic'): #create nic model foreign record  
            for eth_num,v in self.data['nic'].items():
                if eth_num.startswith('bond') or eth_num.startswith('vir') or eth_num.startswith('br'): #stands for vip
                    #macaddress = v.get('macaddress') + '_' + eth_num
                    
                    self.data['nic'][eth_num]['macaddress'] = str(v.get('macaddress')) + '_' + eth_num
                    #print self.data['nic']
                nic_dic = {
                    'name': eth_num,
                    'parent_sn': self.data.get('asset_id'),
                    'model': v.get('model'),
                    'ipaddr': v.get('ipaddress'),
                    'netmask': v.get('netmask'),
                    'mac': v.get('macaddress'),
                }
                nic_model= serializers.NICSerializer(data = nic_dic)
                
                if nic_model.is_valid():
                    nic_model.save()
                    self.record_changes(nic_dic['parent_sn'], 'nic', field=None, old=None, new='name:%s' % nic_dic['name'], event_type=2)
                else:
                    self.__update_table(serializers.NICSerializer, nic_dic, mod_name= 'nic.%s' % eth_num, table_obj=models.NIC, 
                                        filters={'mac':nic_dic.get('mac'), 'name': nic_dic.get('name')
                                                                                                                                            
                                                 })                                  
                self.server_m2m_dic['nic'].append( nic_dic  )
 
    def __validate_disk(self):
        if self.data.has_key('physical_disk_driver'):
            for item in self.data['physical_disk_driver']:
                disk_dic = {
                    'sn': item.get('sn') or '',
                    'parent_sn': self.data.get('asset_id'),
                    'model': item.get('model'),
                    'slot': item.get('slot'),
                    'manufactory': item.get('manufactory') or '',
                    'iface_type': item.get('iface_type'),                    
                    'capacity': item.get('capacity'),                    
                
                }
                disk_model = serializers.DiskSerializer(data=disk_dic)
                
                if disk_model.is_valid():
                    disk_model.save()
                    self.record_changes(disk_dic['parent_sn'], 'disk', field=None, old=None, new='slot:%s' % disk_dic['slot'], event_type=2)
                else:
                    self.__update_table(serializers.DiskSerializer, disk_dic, mod_name= 'disk.%s' % item.get('slot'), table_obj=models.Disk, 
                                        filters={'slot':disk_dic.get('slot'),
                                                  'parent_sn': disk_dic.get('parent_sn')                                                                                              
                                                 })  
                self.server_m2m_dic['physical_disk_driver'].append( disk_dic  )
    def __validate_disk_bak(self):
        if self.data.has_key('physical_disk_driver'):
            for key,item in self.data['physical_disk_driver'].items():
                disk_dic = {
                    'sn': item.get('sn') or '',
                    'parent_sn': self.data.get('asset_id'),
                    'model': item.get('model'),
                    'slot': item.get('slot'),
                    'manufactory': item.get('manufactory') or '',
                    'iface_type': item.get('iface_type'),                    
                    'capacity': item.get('capacity'),                    
                
                }
                disk_model = serializers.DiskSerializer(data=disk_dic)
                self.__validation_check(disk_model,mod_name= 'disk.%s' % item.get('slot'),ass_data=disk_dic)
                if disk_model.is_valid():
                    disk_model.save()
                self.server_m2m_dic['physical_disk_driver'].append( disk_dic  )
    def __validate_raid_adaptor(self):
        if self.data.has_key('raid_adaptor'): #create nic model foreign record  
            for adapter_num,v in self.data['raid_adaptor'].items():
                adapter_dic = {
                    'name': adapter_num,
                    'sn': v.get('sn'),
                    'parent_sn': self.data.get('asset_id'),
                    'model': v.get('model'),
                    'memo': str(v.get('memory_size')),
                }
                #print 'raid::',adapter_dic
                adaptor_model= serializers.RaidAdaptorSerializer(data = adapter_dic)
                
                if adaptor_model.is_valid():
                    adaptor_model.save()
                    self.record_changes(adapter_dic['parent_sn'], 'raid_adaptor', field=None, old=None, new='name:%s' % adapter_dic['name'], event_type=2)
                else:
                    self.__update_table(serializers.RaidAdaptorSerializer, adapter_dic, mod_name='raid.%s' % adapter_num, table_obj=models.RaidAdaptor, 
                                        filters={'name':adapter_dic.get('name'),
                                                  'parent_sn': adapter_dic.get('parent_sn')                                                                                              
                                                 })  
                    
                        
                self.server_m2m_dic['raid_adaptor'].append( adapter_dic  )                        
    def __validate_ram(self): 
        if self.data.has_key('ram'): #create ram model foreign record 
            for each_slot,v in self.data['ram'].items():
                
                mem_dic =  {
                    "parent_sn":self.data.get('asset_id'), 
                    "model": v.get('model'), 
                    "manufactory":v.get('manufactory'), 
                    "slot": each_slot, 
                    "capacity": v.get('capacity'), 
                }
                ram_model = serializers.MemorySerializer(data = mem_dic)
                
                if ram_model.is_valid():
                    ram_model.save()
                    self.record_changes(mem_dic['parent_sn'], 'ram', field=None, old=None, new='slot:%s' % mem_dic['slot'], event_type=2)
                else:   
                    self.__update_table(serializers.MemorySerializer, mem_dic, mod_name='ram.%s' % each_slot, table_obj=models.Memory, 
                                        filters={'slot':mem_dic.get('slot'),
                                                  'parent_sn': mem_dic.get('parent_sn')                                                                                              
                                                 })  

                self.server_m2m_dic['ram'].append( mem_dic  )  
    def __update_table(self,serializer_mod, component_data , mod_name, table_obj, filters={}):
        #print '---->', serializer_mod, component_data , mod_name, table_obj, filters
        try:
            component_obj = table_obj.objects.get(**filters)
            component_update = serializer_mod(component_obj,data=component_data)
            
            #print dir(component_update)
            if component_update.is_valid():
                self.__compare_data(component_obj, client_data=component_data)
                component_update.save()
                #print '-0--->%s updated...' % mod_name
        except Exception,e:
            print 'Error:',e  
    def __compare_data(self,table_obj,client_data):
        '''table_obj is the object of table in db, client_data is the data for this component which sent from client ,such as cpu,or ram'''
        #print table_obj,client_data
        
        for key,value in client_data.items(): #compare data changes
            #print '-----503key:', key, value 
            db_val = getattr(table_obj, key) #get val out of this table for this field 
            if db_val != value:
                self.record_changes(table_obj.parent_sn,table_obj._meta.model_name,key,db_val,value)
                #print "DataChange::: obj [%s] --- parent_sn:[%s] ---key[%s]  has changed from [%s] to [%s]" %(table_obj._meta.model_name,table_obj.parent_sn,key,db_val,value)

    def __validation_check(self,obj,mod_name,ass_data):
        if not obj.is_valid():
            #print obj._name,obj.errors,obj.fields
            for k,err in obj.errors.items():
                if 'already exists' in err[0]:
                    self.validation_check_dic['exist_list'].append([obj,mod_name,ass_data])  
                else:
                    self.validation_check_dic['error_list'].append([obj,mod_name])
    def is_valid(self):
        if len(self.validation_check_dic['error_list']) >0: #�д����践��ǰ��
            self.errors = self.validation_check_dic
            #print self.errors
            return False
        else:
            return True
    def has_exist_component(self):
        if len(self.validation_check_dic['exist_list']) >0: #���Ѿ����ڵ�
            self.exist_list = self.validation_check_dic['exist_list']
            return True
        else:
            self.exist_list = []
            return False
    def create_server(self):
        #print self.validation_check_dic
        if len(self.exist_list) > 0:
            print '\033[31;1mError needs to be fixed before saveing server record, call update_component() \033[0m' #return ResponseData(error_list)
            print self.exist_list
            
            return self.__gen_exception('server','Error needs to be fixed before saveing server record, call update_component()' )
            
        else:
            server_asset_id = self.data.get('asset_id')
            #manytomany and foreign keys
            
            cpu_obj = models.CPU.objects.get(parent_sn=server_asset_id )
            #nic
            nic_obj = models.NIC.objects.filter(parent_sn=server_asset_id)
            nic_list = []
            for obj in nic_obj: #loop many to many
                nic_list.append(obj.id)
            #disk 
            disk_obj = models.Disk.objects.filter(parent_sn=server_asset_id)
            disk_list = []
            for obj in disk_obj:
                disk_list.append( obj.id )
            #raid_adaptor
            raid_obj = models.RaidAdaptor.objects.filter(parent_sn=server_asset_id)
            #print '328 raid_ada::::', raid_obj
            raid_adaptor_list = []
            for obj in raid_obj:
                raid_adaptor_list.append( obj.id)
                #print '332-->', type(obj.id)
                
            #mem 
            mem_obj = models.Memory.objects.filter(parent_sn=server_asset_id)
            mem_list = []
            for obj in mem_obj:
                mem_list.append(obj.id)

            self.data['cpu_model'] = cpu_obj.id
            #self.data['cpu_model_id'] = cpu_obj.pk
            self.data['nic'] = nic_list
            self.data['physical_disk_driver'] = disk_list
            self.data['ram'] = mem_list            
            self.data['raid_adaptor'] = raid_adaptor_list            
            
            #get asset oneToOne
            asset_obj = models.Asset.objects.get(id = self.data['asset_id'])
            self.data['asset'] = asset_obj.id
            server_obj =  serializers.ServerSerializer(data=self.data)  
            if server_obj.is_valid():
                server_obj.save()
                self.update_server_succeess =True
            else:
                try:
                    this_server_obj = models.Server.objects.get(asset__id=server_asset_id) 
                    server_update = serializers.ServerSerializer(this_server_obj,data=self.data)
                    #print dir(server_update)
                    #print '-->585',self.data
                    if server_update.is_valid():
                        self.__compare_asset(self.data)
                        #self.__compare_server_static_data(this_server_obj, self.data)
                        server_update.save()
                        
                        self.update_server_succeess =True
                        print 'server updated...'
                    else:
                        print server_update.errors
                except Exception,e:
                    print e  
                    self.__validation_check(server_obj, mod_name= 'server_obj',ass_data=self.data)
                #print self.validation_check_dic
                if self.is_valid(): #no err but the server may exist already
                    
                    if self.has_exist_component(): # server exist already, 
                        print 'server exist already,'
                        #return self.update_component()
                else:
                    print  '360 ---still has error in servr obj'
                    
    def record_changes(self,parent_asset_id,model_name, field,old,new,event_type=1):
        #print "DataChange::: obj [%s] --- parent_sn:[%s] ---key[%s]  has changed from [%s] to [%s]" %(model_name,parent_asset_id,field,old,new)
        
        if event_type==1: #device change
            message = "AssetID:[%s], model:[%s], field:[%s], value has changed from [%s] to [%s] " %(parent_asset_id,model_name,field, old,new)
        
        elif event_type ==2: #new device
            message = "AssetID:[%s], has found new hardware [%s], key:[%s]" %(parent_asset_id,model_name,new)
        print message 
        models.Maintainence.objects.create(
            name='AssetChangeWarning',
            maintain_type = event_type,
            description = message, 
            device_sn = parent_asset_id,
            event_start = datetime.datetime.now(),
            event_end = datetime.datetime.now(),
            applicant = models.UserProfile.objects.get(pk=1),
            performer = models.UserProfile.objects.get(pk=1),
        )
        print 'hello'
    def record_changes_new_server(self):
        
        #print '%s  -->Field\033[31;1m %s \033[0m has changed from \033[31;1m %s \033[0m to \033[32;1m%s\033[0m' %( parent_sn,field, old,new)
        try:
            models.Maintainence.objects.get(name='NewServerOnLine',device_sn=self.data.get('sn') )
        except ObjectDoesNotExist: #only create record when it doesn't exist in thsi table 
            models.Maintainence.objects.create(
                name='NewServerOnLine',
                maintain_type = 4,
                description = "NewDevice SN:%s has been inserted by Puppet agent " %( self.data.get('sn')) ,
                device_sn = self.data.get('sn'),
                event_start = datetime.datetime.now(),
                event_end = datetime.datetime.now(),
                applicant = models.UserProfile.objects.get(pk=1),
                performer = models.UserProfile.objects.get(pk=1),
            )
            
if __name__ == '__main__':
    from backend import asset_insert
    test_data = asset_insert.temp_asset
    #print test_data
    a = Asset(test_data)
    a.data_handle()