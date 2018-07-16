#!/usr/bin/env python
#coding:utf-8

class mydict(object):
    
    def __init__(self):
        self.msg = {}
    
    def __getitem__(self,key):
        return self.msg[key]
    
    def __setitem__(self,key,value):
        self.msg[key] = value
        
    def __delitem__(self):
        pass
        
d = mydict()
d[1] = 'qiufei'
d[2] = 'chenqiufei'

print d.msg
print d[1]