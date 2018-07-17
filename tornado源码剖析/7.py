class RequestHandler(object):
    SUPPORTED_METHODS = ("GET", "HEAD", "POST", "DELETE", "PUT", "OPTIONS")

    def __init__(self, application, request, **kwargs):
        self.application = application
        self.request = request
        self._headers_written = False
        self._finished = False
        self._auto_finish = True
        self._transforms = None  # will be set in _execute
		#获取在application中设置的 ui_modules 和ui_method
        self.ui = _O((n, self._ui_method(m)) for n, m in
                     application.ui_methods.iteritems())
        self.ui["modules"] = _O((n, self._ui_module(n, m)) for n, m in
                                application.ui_modules.iteritems())
        self.clear() #设置服务器、内容类型编码和连接
        # Check since connection is not available in WSGI
		#检查连接是否可用，应该是长短连接有关。
        if hasattr(self.request, "connection"):
            self.request.connection.stream.set_close_callback(self.on_connection_close)
        self.initialize(**kwargs)

    def initialize(self):
        pass
		
    def prepare(self):
        pass
    def _execute(self, transforms, *args, **kwargs):
        """Executes this request with the given output transforms."""
        self._transforms = transforms
        with stack_context.ExceptionStackContext(self._stack_context_handle_exception):
            if self.request.method not in self.SUPPORTED_METHODS:
                raise HTTPError(405)
            # If XSRF cookies are turned on, reject form submissions without
            # the proper cookie
            if self.request.method not in ("GET", "HEAD", "OPTIONS") and self.application.settings.get("xsrf_cookies"):
                self.check_xsrf_cookie()
            self.prepare()
            if not self._finished:
                args = [self.decode_argument(arg) for arg in args]
                kwargs = dict((k, self.decode_argument(v, name=k)) for (k,v) in kwargs.iteritems())
				#执行handler中定义的get、post等方法...（一般我们在这个方法内部使用 self.write来给客户端返回数据）
                #self.request.method.lower() 字符串的形式
                getattr(self, self.request.method.lower())(*args, **kwargs)
                if self._auto_finish and not self._finished:
                    self.finish()
	#----- 执行完之后，请求就会返回。
					
    def write(self, chunk):
		#把要返回给客户端的数据添加到一个 _write_buffer 列表中。
        assert not self._finished
        if isinstance(chunk, dict):
            chunk = escape.json_encode(chunk)
            self.set_header("Content-Type", "application/json; charset=UTF-8")
        chunk = utf8(chunk)
        self._write_buffer.append(chunk)
					
					
					
    def finish(self, chunk=None):
        """Finishes this response, ending the HTTP request."""
        assert not self._finished
        if chunk is not None: self.write(chunk)

        # Automatically support ETags and add the Content-Length header if
        # we have not flushed any content yet.
        if not self._headers_written:
            if (self._status_code == 200 and self.request.method in ("GET", "HEAD") and "Etag" not in self._headers):
                etag = self.compute_etag()
                if etag is not None:
                    inm = self.request.headers.get("If-None-Match")
                    if inm and inm.find(etag) != -1:
                        self._write_buffer = []
                        self.set_status(304)
                    else:
                        self.set_header("Etag", etag)
            if "Content-Length" not in self._headers:
                content_length = sum(len(part) for part in self._write_buffer)
                self.set_header("Content-Length", content_length)

        if hasattr(self.request, "connection"):
            # Now that the request is finished, clear the callback we
            # set on the IOStream (which would otherwise prevent the
            # garbage collection of the RequestHandler when there
            # are keepalive connections)
            self.request.connection.stream.set_close_callback(None)

        if not self.application._wsgi:
            self.flush(include_footers=True)
            self.request.finish() #执行HTTPRequest的finish方法，执行HTTPConnection的finish的方法，执行 xxstream 的close方法，
            self._log()
        self._finished = True

		
		
    def flush(self, include_footers=False):
        """Flushes the current output buffer to the network."""
        if self.application._wsgi:
            raise Exception("WSGI applications do not support flush()")

        chunk = b("").join(self._write_buffer)
        self._write_buffer = []
        if not self._headers_written:
            self._headers_written = True
            for transform in self._transforms:
                self._headers, chunk = transform.transform_first_chunk(
                    self._headers, chunk, include_footers)
            headers = self._generate_headers()
        else:
            for transform in self._transforms:
                chunk = transform.transform_chunk(chunk, include_footers)
            headers = b("")

        # Ignore the chunk and only write the headers for HEAD requests
        if self.request.method == "HEAD":
            if headers: self.request.write(headers)
            return

        if headers or chunk:
            self.request.write(headers + chunk)