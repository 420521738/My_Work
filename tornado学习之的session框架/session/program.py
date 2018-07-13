#!/usr/bin/env python
#coding:utf-8

import tornado.ioloop
import tornado.web
from session.session_factory import MySession

# 登录页面
class LoginHandler(tornado.web.RequestHandler):
    # 登录页首先需要执行的函数get，返回login.html页面
    def get(self):
        MySession(self)
        self.render('login.html')
    # login.html页面提交数据，假设数据
    def post(self):
        name = 'chenqiufei'
        pwd = '123'
        if name == 'chenqiufei' and pwd == '123':
            # 把用户的账号和密码存在列表li中
            li = [name,pwd]
            # 检验用户名密码，假设验证通过
            # 把session实例化
            session = MySession(self)
            # 调用MySession的set_session函数，传入的参数有两个，一个是key，一个是value
            session.set_session('logininfo',li)
            # 将用户的信息保存好后，返回index首页
            self.redirect('/index')
            #self.write('Post Success!')
        else:
            self.redirect('/login')

# 登录成功之后的后台管理页面
class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        session = MySession(self)
        # 先获取用户的logininfo信息，logininfo作为key
        se = session.get_session('logininfo')
        # 如果有数据，那么获取到的数据类似['chenqiufei', '123']
        if se:
            print se[0]
            self.write('Index:'+se[0])
        else:
            self.redirect('/login')

def make_app():
    return tornado.web.Application([
        # 正则表达式，访问/login则通过执行LoginHandler类去实现
        (r"/login", LoginHandler),
        # 访问/index则通过执行IndexHandler类去实现
        (r"/index", IndexHandler),
    ])

if __name__ == "__main__":
    print 'listening 8888'
    app = make_app()
    # 服务监听在8888端口
    app.listen(8888)
    tornado.ioloop.IOLoop.instance().start()