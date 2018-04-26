#!/usr/bin/env python
# --*-- coding: utf-8 --*--

import redis
r = redis.Redis(host='192.168.1.234',port=6379,db=0)	### 实例化r,连接服务端的redis
