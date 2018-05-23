#!/usr/bin/env python
#coding:utf-8

def RunServer(environ,start_response):
	start_response('200 ok',[('Content-Type','application/x-javascript')])
	data = 'callback({name:'chenqiufei',age:27});'
	return data