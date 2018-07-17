class HTTPServer(object):
	#非阻塞单线程的HTTP服务器
    def __init__(self, request_callback, no_keep_alive=False, io_loop=None,
                 xheaders=False, ssl_options=None):
        self.request_callback = request_callback
        self.no_keep_alive = no_keep_alive
        self.io_loop = io_loop
        self.xheaders = xheaders
        self.ssl_options = ssl_options
        self._sockets = {}  # fd -> socket object
        self._started = False

    def listen(self, port, address=""):
        self.bind(port, address)
        self.start(1)

    def bind(self, port, address=None, family=socket.AF_UNSPEC):
        if address == "":
            address = None
		#获取要监听的那个地址和端口的信息
        for res in socket.getaddrinfo(address, port, family, socket.SOCK_STREAM,0, socket.AI_PASSIVE | socket.AI_ADDRCONFIG):
            af, socktype, proto, canonname, sockaddr = res
            sock = socket.socket(af, socktype, proto) #创建一个socket对象
            flags = fcntl.fcntl(sock.fileno(), fcntl.F_GETFD)
            flags |= fcntl.FD_CLOEXEC
            fcntl.fcntl(sock.fileno(), fcntl.F_SETFD, flags)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            if af == socket.AF_INET6:
                if hasattr(socket, "IPPROTO_IPV6"):
                    sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 1)
            sock.setblocking(0)
            sock.bind(sockaddr)
            sock.listen(128)
            self._sockets[sock.fileno()] = sock
            if self._started:
                self.io_loop.add_handler(sock.fileno(), self._handle_events,ioloop.IOLoop.READ)

    def start(self, num_processes=1):
        assert not self._started
        self._started = True
        if num_processes is None or num_processes <= 0:
            num_processes = _cpu_count()
        if num_processes > 1 and ioloop.IOLoop.initialized():
            logging.error("Cannot run in multiple processes: IOLoop instance "
                          "has already been initialized. You cannot call "
                          "IOLoop.instance() before calling start()")
            num_processes = 1
        if num_processes > 1:
            logging.info("Pre-forking %d server processes", num_processes)
            for i in range(num_processes):
                if os.fork() == 0:
                    import random
                    from binascii import hexlify
                    try:
                        # If available, use the same method as
                        # random.py
                        seed = long(hexlify(os.urandom(16)), 16)
                    except NotImplementedError:
                        # Include the pid to avoid initializing two
                        # processes to the same value
                        seed(int(time.time() * 1000) ^ os.getpid())
                    random.seed(seed)
                    self.io_loop = ioloop.IOLoop.instance()
                    for fd in self._sockets.keys():
                        self.io_loop.add_handler(fd, self._handle_events,ioloop.IOLoop.READ)
                    return
            os.waitpid(-1, 0)
        else:
            if not self.io_loop:
                self.io_loop = ioloop.IOLoop.instance()
            for fd in self._sockets.keys():
                self.io_loop.add_handler(fd, self._handle_events,ioloop.IOLoop.READ)

    def stop(self):
        for fd, sock in self._sockets.iteritems():
            self.io_loop.remove_handler(fd)
            sock.close()

	#处理请求的入口
    def _handle_events(self, fd, events):
        while True:
            try:
				#当有请求进入时，
                connection, address = self._sockets[fd].accept()
            except socket.error, e:
                if e.args[0] in (errno.EWOULDBLOCK, errno.EAGAIN):
                    return
                raise
            if self.ssl_options is not None:
                assert ssl, "Python 2.6+ and OpenSSL required for SSL"
                try:
					
                    connection = ssl.wrap_socket(connection,server_side=True,do_handshake_on_connect=False,**self.ssl_options)
                except ssl.SSLError, err:
                    if err.args[0] == ssl.SSL_ERROR_EOF:
                        return connection.close()
                    else:
                        raise
                except socket.error, err:
                    if err.args[0] == errno.ECONNABORTED:
                        return connection.close()
                    else:
                        raise
            try:
				#把客户端连接的socket对象封装到 SSLIOStream或IOStream中，之后会再把XXStream封装到 HTTPConnection 中。（猜想就是通过他来返回对象）
                if self.ssl_options is not None:
                    stream = iostream.SSLIOStream(connection, io_loop=self.io_loop)
                else:
                    stream = iostream.IOStream(connection, io_loop=self.io_loop)
				#执行HTTPConnection的构造函数，参数分别是：
				#stream  不知道是什么
				#address IP地址
				#self.request_callback    包含正则表达式和handler的集合
				
                HTTPConnection(stream, address, self.request_callback,self.no_keep_alive, self.xheaders)
            except:
                logging.error("Error in connection callback", exc_info=True)


				
				
				
class IOLoop(object):
    """A level-triggered I/O loop.

    We use epoll (Linux) or kqueue (BSD and Mac OS X; requires python
    2.6+) if they are available, or else we fall back on select(). If
    you are implementing a system that needs to handle thousands of
    simultaneous connections, you should use a system that supports either
    epoll or queue.

    Example usage for a simple TCP server::

        import errno
        import functools
        import ioloop
        import socket

        def connection_ready(sock, fd, events):
            while True:
                try:
                    connection, address = sock.accept()
                except socket.error, e:
                    if e.args[0] not in (errno.EWOULDBLOCK, errno.EAGAIN):
                        raise
                    return
                connection.setblocking(0)
                handle_connection(connection, address)

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.setblocking(0)
        sock.bind(("", port))
        sock.listen(128)

        io_loop = ioloop.IOLoop.instance()
        callback = functools.partial(connection_ready, sock)
        io_loop.add_handler(sock.fileno(), callback, io_loop.READ)
        io_loop.start()

    """
    # Constants from the epoll module
    _EPOLLIN = 0x001
    _EPOLLPRI = 0x002
    _EPOLLOUT = 0x004
    _EPOLLERR = 0x008
    _EPOLLHUP = 0x010
    _EPOLLRDHUP = 0x2000
    _EPOLLONESHOT = (1 << 30)
    _EPOLLET = (1 << 31)

    # Our events map exactly to the epoll events
    NONE = 0
    READ = _EPOLLIN
    WRITE = _EPOLLOUT
    ERROR = _EPOLLERR | _EPOLLHUP | _EPOLLRDHUP

    def __init__(self, impl=None):
        self._impl = impl or _poll()
        if hasattr(self._impl, 'fileno'):
            self._set_close_exec(self._impl.fileno())
        self._handlers = {}
        self._events = {}
        self._callbacks = []
        self._timeouts = []
        self._running = False
        self._stopped = False
        self._blocking_signal_threshold = None

        # Create a pipe that we send bogus data to when we want to wake
        # the I/O loop when it is idle
        if os.name != 'nt':
            r, w = os.pipe()
            self._set_nonblocking(r)
            self._set_nonblocking(w)
            self._set_close_exec(r)
            self._set_close_exec(w)
            self._waker_reader = os.fdopen(r, "rb", 0)
            self._waker_writer = os.fdopen(w, "wb", 0)
        else:
            self._waker_reader = self._waker_writer = win32_support.Pipe()
            r = self._waker_writer.reader_fd
        self.add_handler(r, self._read_waker, self.READ)

    def add_handler(self, fd, handler, events):
        """Registers the given handler to receive the given events for fd."""
        self._handlers[fd] = stack_context.wrap(handler)
        self._impl.register(fd, events | self.ERROR)
		
		
    @classmethod
    def instance(cls):
        """Returns a global IOLoop instance.

        Most single-threaded applications have a single, global IOLoop.
        Use this method instead of passing around IOLoop instances
        throughout your code.

        A common pattern for classes that depend on IOLoops is to use
        a default argument to enable programs with multiple IOLoops
        but not require the argument for simpler applications::

            class MyClass(object):
                def __init__(self, io_loop=None):
                    self.io_loop = io_loop or IOLoop.instance()
        """
		#单例模式，创建一个该类的实例，并把实例添加到私有静态字段 _instance
        if not hasattr(cls, "_instance"):
            cls._instance = cls()
        return cls._instance
		
    def start(self):
        """Starts the I/O loop.

        The loop will run until one of the I/O handlers calls stop(), which
        will make the loop stop after the current event iteration completes.
        """
        if self._stopped:
            self._stopped = False
            return
        self._running = True
        while True:
            # Never use an infinite timeout here - it can stall epoll
            poll_timeout = 0.2

            # Prevent IO event starvation by delaying new callbacks
            # to the next iteration of the event loop.
            callbacks = self._callbacks
            self._callbacks = []
            for callback in callbacks:
                self._run_callback(callback)

            if self._callbacks:
                poll_timeout = 0.0

            if self._timeouts:
                now = time.time()
                while self._timeouts:
                    if self._timeouts[0].callback is None:
                        # the timeout was cancelled
                        heapq.heappop(self._timeouts)
                    elif self._timeouts[0].deadline <= now:
                        timeout = heapq.heappop(self._timeouts)
                        self._run_callback(timeout.callback)
                    else:
                        milliseconds = self._timeouts[0].deadline - now
                        poll_timeout = min(milliseconds, poll_timeout)
                        break

            if not self._running:
                break

            if self._blocking_signal_threshold is not None:
                # clear alarm so it doesn't fire while poll is waiting for
                # events.
                signal.setitimer(signal.ITIMER_REAL, 0, 0)

            try:
                event_pairs = self._impl.poll(poll_timeout)
            except Exception, e:
                # Depending on python version and IOLoop implementation,
                # different exception types may be thrown and there are
                # two ways EINTR might be signaled:
                # * e.errno == errno.EINTR
                # * e.args is like (errno.EINTR, 'Interrupted system call')
                if (getattr(e, 'errno', None) == errno.EINTR or
                    (isinstance(getattr(e, 'args', None), tuple) and
                     len(e.args) == 2 and e.args[0] == errno.EINTR)):
                    continue
                else:
                    raise

            if self._blocking_signal_threshold is not None:
                signal.setitimer(signal.ITIMER_REAL,
                                 self._blocking_signal_threshold, 0)

            # Pop one fd at a time from the set of pending fds and run
            # its handler. Since that handler may perform actions on
            # other file descriptors, there may be reentrant calls to
            # this IOLoop that update self._events
            self._events.update(event_pairs)
            while self._events:
                fd, events = self._events.popitem()
                try:
                    self._handlers[fd](fd, events)   #---------------------------执行 HTTPServer的_handle_events
                except (KeyboardInterrupt, SystemExit):
                    raise
                except (OSError, IOError), e:
                    if e.args[0] == errno.EPIPE:
                        # Happens when the client closes the connection
                        pass
                    else:
                        logging.error("Exception in I/O handler for fd %d",
                                      fd, exc_info=True)
                except:
                    logging.error("Exception in I/O handler for fd %d",
                                  fd, exc_info=True)
        # reset the stopped flag so another start/stop pair can be issued
        self._stopped = False
        if self._blocking_signal_threshold is not None:
            signal.setitimer(signal.ITIMER_REAL, 0, 0)
				