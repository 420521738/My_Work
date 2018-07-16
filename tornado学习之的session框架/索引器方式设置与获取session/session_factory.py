#!/usr/bin/env python
#coding:utf-8

import hashlib
import time

session_container = {}

class MySession(object):
    # 执行构建函数
    def __init__(self,request):
        #self.msg = {}
        # 定义一个私有变量self.__request在类里使用
        self.__request = request
        # 再执行initialize初始函数
        self.initialize()
        
    def initialize(self):
        # 先获取当前操作的id
        id = self.__request.get_cookie('__my_sessionid')
        # 如果在内存中没有记录这个id，则新建
        if not id:
            hash_md5 = hashlib.md5()
            hash_md5.update(str(time.time()))
            val = hash_md5.hexdigest()
            self.__request.set_cookie('__my_sessionid', val,expires_days=1)
        # 再顶一个私有变量self.__id在类里使用
        self.__id = id
    
    # 索引器方式设置session；  __setitem__是固定写法
    def __setitem__(self,key,session_val):
        #self.msg[key] = session_val
        temp = {key:session_val}
        session_container[self.__id] = temp
    
    # 索引器方式获取session；__getitem__是固定写法
    def __getitem__(self,name):
        return session_container[self.__id][name]