class Application(object):
    def __init__(self, handlers=None, default_host="", transforms=None,wsgi=False, **settings):
		#设置响应的编码和返回方式，对应的http相应头：Content-Encoding和Transfer-Encoding
		#Content-Encoding:gzip 表示对数据进行压缩，然后再返回给用户，从而减少流量的传输。
		#Transfer-Encoding:chunck 表示数据的传送方式通过一块一块的传输。
        if transforms is None:
            self.transforms = []
            if settings.get("gzip"):
                self.transforms.append(GZipContentEncoding)
            self.transforms.append(ChunkedTransferEncoding)
        else:
            self.transforms = transforms
        self.handlers = [] #---------成员变量handlers，并非参数
        self.named_handlers = {}
        self.default_host = default_host
        self.settings = settings
		#设置默认UI模块，和页面js、css、xsrf、template有关
		#_linkify、_xsrf_form_html和TemplateModule都是继承UIModule的子类，将该类保存在  self.ui_modules  字段中
        self.ui_modules = {'linkify': _linkify,
                           'xsrf_form_html': _xsrf_form_html,
                           'Template': TemplateModule,
                           }
        self.ui_methods = {}
        self._wsgi = wsgi
		#从参数settings中读取url模块和方法，如果没有设置的默认参数为空的字典
		#ui_modules的内容需要时 UIModule 类的子类
        self._load_ui_modules(settings.get("ui_modules", {}))
        self._load_ui_methods(settings.get("ui_methods", {}))
		#从settings中获取key为static_path的值，用于设置静态文件路径
		#静态文件的设置方式有两种：写的settings中或者在构造函数后面设置
        if self.settings.get("static_path"):
            path = self.settings["static_path"]
            handlers = list(handlers or []) #可以用，如果handler内容为空或者是None类型，则返回后面的默认赋值
			#设置静态文件路径，如果存在settings字典中不存在key = static_url_prefix，那默认返回值：/static/
            static_url_prefix = settings.get("static_url_prefix","/static/")
			#默认添加处理静态文件的StaticFileHandler，并将该handler添加到参数中传入的handlers的前面
            handlers = [
                (re.escape(static_url_prefix) + r"(.*)", StaticFileHandler,dict(path=path)),
                (r"/(favicon\.ico)", StaticFileHandler, dict(path=path)),
                (r"/(robots\.txt)", StaticFileHandler, dict(path=path)),
            ] + handlers
		#此时，handlers是一个列表，列表的元素是元祖，元祖包括：url正则、处理该url的handler。对于静态文件还有一个站点的相对路径
			#所以，看到这里就可以通过两种方式为tornado添加静态文件的路径，1、直接设置。2、设置settings使用默认的设置
		#所有的请求让这个handlers处理
        if handlers: self.add_handlers(".*$", handlers)

        # Automatically reload modified modules
		#如果settings中设置了 debug 模式，那么就使用自动加载重启
        if self.settings.get("debug") and not wsgi:
            import autoreload
            autoreload.start()