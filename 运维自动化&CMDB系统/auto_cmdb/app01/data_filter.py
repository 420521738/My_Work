#!/usr/bin/env python
#_*_coding:utf-8_*_

from django.contrib.auth.models import User, Group
from app01 import models

from django.core.exceptions import ObjectDoesNotExist
import django_filters

from django.db.models import Q
import operator

class AssetFilter(object):
    '''
    format_dic = {
        'idc': ['BJ,SJZ', 'contains'],
        'update_at' : ['2014-12-01,2014-12-11', 'lt'],
        'manufactory' : ['DELL', 'contains'],
        'page_navi': [2,20],
        
    }
    '''
    def __init__(self, query_set):
        self.query_set = query_set
        self.error_list = []
        
    para_dic = {
        #'Asset':['id','name','hostname','contract','trade_time','business_unit','admin','client','idc','cabinet_num','cabinet_order','status',],
        'Server':['sn', 'manufactory' , 'model' , 'cpu_count' , 'cpu_core_count' , 'cpu_model' , 'raid_type' , 'ram_size' , 'create_at' , 'update_at','nic__ipaddr' ],
        'NetworkDevice':['sn','firmware','port_num','create_at' , 'update_at' ],
    }
    
    logics = ['gt', 'in', 'month', 'endswith', 'week_day', 'year', 'gte', 'lte','contains', 'lt', 'startswith', 'day', 'search',  'range']
    
    def __validate_field(self):
        print type(self.query_set)
        for key,val in self.query_set.items():
            has_count = 0 #means query key is not valid 
            val_error_count = 0 #means no err
            for table_name,field_list in self.para_dic.items():
            
                if key in field_list or key.startswith('asset__') or key.startswith('nic__') : #not valid key or key.startswith('ram__') or key.startswith('physical_disk_driver__')
                    has_count +=1
                    if type(val) is list and len(val) == 2: #not valid like ['DELL', 'contains'],
                        if val[-1] not in self.logics:
                            #print 'logic:',val[-1]
                            val_error_count +=1
                    else:
                       print 'else46....',type(field_list), len(field_list), field_list
                       val_error_count +=1 
            if has_count !=0 and val_error_count ==0: #means this condition is valid 
                pass
            else:
                if key != 'page_navi':
                    self.error_list.append({key:[val,'not valid']})
        
        if len(self.error_list) >0:
            return False
        else:
            return True
    def filter(self):
        #print self.query_set
        query_dic = {
            #'Asset':{},
            'Server': {},
            'NetworkDevice':{},
        
        }
        if self.__validate_field() is True: 
            #print 'validate pass-68'
            for filter_key, val in self.query_set.items():
                if filter_key != 'page_navi':
                    #print '-->filter key 72:',filter_key
                    for table in self.para_dic.keys():
                        
                        if filter_key in self.para_dic[table] or filter_key.startswith('asset__'): 
                            filter_value = val[0]
                            logic_operator = val[1]
                            if logic_operator in ('in','range'):
                                filter_value = filter_value.split(',') # need to be tuple for in and range logic  
                            elif logic_operator == 'contains' and len(filter_value.split(',')) >1:  #use special operator
                                query_dic[table]['contains_or::%s' %filter_key] = filter_value.split(',')
                                continue   #do not execute below part in this round 
                            else:
                                filter_value = val[0]
                            filter_key_str = '%s__%s' %(filter_key, logic_operator)
                            query_dic[table][filter_key_str] = filter_value
     
                #print '-------------------------'
            #print query_dic    
            result_list = []
            contains_or_list =[]
            
            for table_name, query_conditions in query_dic.items():
                print 'condition:--->', table_name, query_conditions
                table_obj = getattr(models, table_name)
                for key,query_val in query_conditions.items():
                    if key.startswith('contains_or::'): #special logic 
                        query_key ='%s__contains' %( key.split('::')[1] ) 
                        
                        print 'line99-->',query_key, query_val 
                        condition = reduce(operator.or_,(Q(**{query_key: x})for x in query_val ))
                        result = table_obj.objects.filter(condition)
                        print 'line101-->', len(result )
                        for i in result:contains_or_list.append(i.asset)
                        
                        
                        del query_conditions[key]
                print 'len query dic : 106',query_conditions
                if len(query_conditions) >0: #{} will cause error 
                    result = table_obj.objects.filter(**query_conditions)
                    print 'len result:--->',len(result)
                    for i in result:
                        #print i
                        result_list.append(i.asset)

            print '\033[32;1m----%s----\033[0m' % len(result_list)
            if len(result_list) >0 and len(contains_or_list) >0:
                result_list = list( set(result_list) & set(contains_or_list) )
            else :
                result_list = result_list + contains_or_list
                
            total_item = len(result_list)
            #page_navi
            #result_list.sort()
            if self.query_set.has_key('page_navi'):
                page_num, num_per_page = self.query_set['page_navi']
                total_pages = len(result_list) /num_per_page
                last_page_start  = None 
                if len(result_list) > num_per_page * page_num : #only works when result list has more items than one page required. 
                    
                    if num_per_page - 1 !=0: # page num bigger than 1 
                        item_start = (page_num - 1) * num_per_page
                        
                        item_end =  item_start + num_per_page
                        print 'line 114 -here----', item_start,item_end
                        result_list = result_list[item_start:item_end]
                    else: #first page 
                        pass
                else: # last page
                    item_start =  (page_num - 1) * num_per_page  
                    result_list =  result_list[item_start:]                     
                #elif total_pages  > 0: #result length is bigger than num_per_page
                #    last_page_items = len(result_list) % num_per_page  # 95%10 = 5, that means 5 items left in the 10th page
                #    if last_page_items ==0: # 90%10 = 0, means total page is last page as well
                #        last_page_start  = (total_pages -1) * num_per_page 
                #    else:
                #        last_page_start   = last_page_items    
                #        
                #     
                #    item_start =  (page_num - 1) * num_per_page  
                #    result_list =  result_list[item_start:]    
                    
            print '\033[31;1m----%s----\033[0m' % len(result_list)    
            
            result_list.append(total_item)
            return  result_list
        else:
            print 'here.....line125',self.error_list
            
        
        
        