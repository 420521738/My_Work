class HTTPRequest(object):
    def __init__(self, method, uri, version="HTTP/1.0", headers=None,
                 body=None, remote_ip=None, protocol=None, host=None,
                 files=None, connection=None):
        self.method = method
        self.uri = uri
        self.version = version
        self.headers = headers or httputil.HTTPHeaders()
        self.body = body or ""
        if connection and connection.xheaders:
            # Squid uses X-Forwarded-For, others use X-Real-Ip
            self.remote_ip = self.headers.get(
                "X-Real-Ip", self.headers.get("X-Forwarded-For", remote_ip))
            # AWS uses X-Forwarded-Proto
            self.protocol = self.headers.get(
                "X-Scheme", self.headers.get("X-Forwarded-Proto", protocol))
            if self.protocol not in ("http", "https"):
                self.protocol = "http"
        else:
            self.remote_ip = remote_ip
            if protocol:
                self.protocol = protocol
            elif connection and isinstance(connection.stream, 
                                           iostream.SSLIOStream):
                self.protocol = "https"
            else:
                self.protocol = "http"
        self.host = host or self.headers.get("Host") or "127.0.0.1"
        self.files = files or {}
        self.connection = connection
        self._start_time = time.time()
        self._finish_time = None

        scheme, netloc, path, query, fragment = urlparse.urlsplit(native_str(uri))
        self.path = path
        self.query = query
        arguments = parse_qs_bytes(query)
        self.arguments = {}
        for name, values in arguments.iteritems():
            values = [v for v in values if v]
            if values: self.arguments[name] = values


    def write(self, chunk):
        """Writes the given chunk to the response stream."""
        assert isinstance(chunk, bytes_type)
		#客户端socket对象写数据，调用 HTTPConnection的 write 方法。
		#HTTPConnection的 write 方法又会调用 xxStream 的write方法（当完成后执行HTTPConnection的 _on_write_complete 方法，默认不执行，因为请求没有终止）
		#xxStream 的write方法会把数据添加到 xxStream 的_write_buffer变量里
        self.connection.write(chunk)

    def finish(self):
        """Finishes this HTTP request on the open connection."""
        self.connection.finish()  #调用socket的close关闭客户端socket
        self._finish_time = time.time()
