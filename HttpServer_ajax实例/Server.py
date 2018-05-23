#!/usr/bin/env python
#coding:utf-8

from wsgiref.simple_server import make_server
import Application

httpd = make_server('0.0.0.0',9090,Application.RunServer)
print 'Serving Http on port 9090...'
httpd.serve_forever()