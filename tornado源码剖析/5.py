class HTTPConnection(object):
    """Handles a connection to an HTTP client, executing HTTP requests.

    We parse HTTP headers and bodies, and execute the request callback
    until the HTTP conection is closed.
    """
    def __init__(self, stream, address, request_callback, no_keep_alive=False,
                 xheaders=False):
        self.stream = stream
        self.address = address
        self.request_callback = request_callback
        self.no_keep_alive = no_keep_alive
        self.xheaders = xheaders
        self._request = None
        self._request_finished = False
        # Save stack context here, outside of any request.  This keeps
        # contexts from one request from leaking into the next.
		#执行 【_on_headers】 方法 --> 
		#从请求中获取数据，并根据请求数据通过 _on_headers 方法来做响应
        self._header_callback = stack_context.wrap(self._on_headers)
        self.stream.read_until(b("\r\n\r\n"), self._header_callback)
		
    def _on_headers(self, data):
        try:
			#data表示请求数据
            data = native_str(data.decode('latin1'))
            eol = data.find("\r\n")
			#获取请求的起始行数据，例如：GET / HTTP/1.1
            start_line = data[:eol]
            try:
				#请求方式、请求地址、http版本号
                method, uri, version = start_line.split(" ")
            except ValueError:
                raise _BadRequestException("Malformed HTTP request line")
            if not version.startswith("HTTP/"):
                raise _BadRequestException("Malformed HTTP version in HTTP Request-Line")
			#把请求头信息包装到一个字典中。（不包括第一行）
            headers = httputil.HTTPHeaders.parse(data[eol:])
			#把请求封装到一个tornadoHTTPRequest对象中。其中封装了 HTTPConnection 对象，该对象包含了客户端的 socket对象，使用它来返回对象。
            self._request = HTTPRequest(connection=self, method=method, uri=uri, version=version,headers=headers, remote_ip=self.address[0])
			#从请求头中获取 Content-Length
            content_length = headers.get("Content-Length")
            if content_length:
                content_length = int(content_length)
                if content_length > self.stream.max_buffer_size:
                    raise _BadRequestException("Content-Length too long")
                if headers.get("Expect") == "100-continue":
                    self.stream.write("HTTP/1.1 100 (Continue)\r\n\r\n")
                self.stream.read_bytes(content_length, self._on_request_body)
                return
			#**************** 执行Application对象的 __call__ 方法，也就是路由系统的入口 *******************
            self.request_callback(self._request)
        except _BadRequestException, e:
            logging.info("Malformed HTTP request from %s: %s",
                         self.address[0], e)
            self.stream.close()
            return
			
			
