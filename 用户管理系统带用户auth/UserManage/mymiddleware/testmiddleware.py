#!/usr/bin/env python
#coding:utf-8

'''
Created on 2018年6月22日

@author: Chenqiufei
'''

class TestMiddleware1(object):
    def process_request(self,request):
        pass
    def process_view(self, request, callback, callback_args, callback_kwargs):
        pass
    def process_exception(self, request, exception):
        pass  
    def process_response(self, request, response):
        return response
    
class TestMiddleware2(object):
    def process_request(self,request):
        pass
    def process_view(self, request, callback, callback_args, callback_kwargs):
        pass
    def process_exception(self, request, exception):
        pass  
    def process_response(self, request, response):
        return response
    