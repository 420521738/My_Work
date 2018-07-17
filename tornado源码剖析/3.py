def listen(self, port, address="", **kwargs):
	#创建一个Http服务器，用来监听某个端口，接收客户端发来的请求。要启动这个服务器还需要执行IOLoop.instance().start()方法。
	#最好不要是使用还个listen方法，而是直接使用HTTPServer对象的bind和start方法
	
	from tornado.httpserver import HTTPServer
	server = HTTPServer(self, **kwargs)
	server.listen(port, address) #穿件socket对象，并将该方法接收请求的函数封装添加到 ioloop.IOLoop.instance() 对象的 self._handlers[fd]中
	
#到目前为止，socket对象，将处理请求的函数 【_handle_events】 封装添加到 ioloop.IOLoop.instance() 对象的 self._handlers[fd]中，在 HTTPServer 的Start方法中
#执行 【_handle_events】方法处理请求。