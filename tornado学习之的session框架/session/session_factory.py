#!/usr/bin/env python
#coding:utf-8

import hashlib
import time

session_container = {}

class MySession(object):
    # 执行构建函数
    def __init__(self,request):
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
        
    # LoginHandler的post函数调用此方法，传入了两个参数，一个是key，在这里是logininfo，一个是value，在这里是['chenqiufei', '123']
    def set_session(self,key,session_val):
        # 将LoginHandler的post函数传入的两个参数组成一个字典，类似：{'logininfo': ['chenqiufei', '123']}
        temp = {key:session_val}
        print temp
        # 将用户的sessionid的md5值作为key，再将上述的temp作为value，再传入字典session_container中
        # 类似 {'8e47b98d26d0ecd801669d3b74a107ad': {'logininfo': ['chenqiufei', '123']}}
        session_container[self.__id] = temp
        print session_container
    
    # IndexHandler的get传入参数logininfo
    def get_session(self,name):
        # val获取的是{'8e47b98d26d0ecd801669d3b74a107ad': {'logininfo': ['chenqiufei', '123']}}
        # 8e47b98d26d0ecd801669d3b74a107ad是self.__id，logininfo是name，那么获取到的数据是['chenqiufei', '123']
        val = session_container[self.__id][name]
        return val