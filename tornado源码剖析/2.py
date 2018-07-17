#设置主机模型，对应的handlers，默认是所有的请求 .* 
def add_handlers(self, host_pattern, host_handlers):
	#如果主机模型最后没有结尾符，那么就为他添加一个结尾符。
	if not host_pattern.endswith("$"):
		host_pattern += "$"
	handlers = []
	#如果当前成员变量 handlers 中有值（默认没有），并且handlers 的最后一个元祖的url正则是 .*$ ,那么将参数中设置的handler插入到原来成员变量中最后一个handler的元素的前面，模型还是 .*$
	if self.handlers and self.handlers[-1][0].pattern == '.*$':
		#注意第二个参数，他是一个引用类型，之后再对该handlers进行赋值。
		#这样就使得具体的主机模型正则在 .* 之前，使得请求先对具体的正则对url进行处理，最后再让 .* 做。
		self.handlers.insert(-1, (re.compile(host_pattern), handlers))
	else:
		#如果成员变量中的handlers的值为空 或 成员变量中的handlers的最后一个元素的模型不是 .*
		self.handlers.append((re.compile(host_pattern), handlers))
	#以上目的：使用主机先做一次路由，并且把具体的主机模型放在 .* 的前面。不要问我为什么，因为这样的话，才能保证正则表达式起作用
	
	#将参数中设置的handlers封装到 URLSpec 类中，然后添加 self.handlers中对应的主机模型对应的handlers中。
	for spec in host_handlers:
		if type(spec) is type(()):
			assert len(spec) in (2, 3)
			pattern = spec[0]
			handler = spec[1]
			if len(spec) == 3:
				kwargs = spec[2]
			else:
				kwargs = {}
			spec = URLSpec(pattern, handler, kwargs)
		handlers.append(spec)
		#用于主机模型下的具体handler进行命名规范，是否重复设置了handler，默认这个功能不启用。
		#如果想要启用，那就为URLSpec添加第四个参数就好了。再每个handler命一个名字
		if spec.name:
			if spec.name in self.named_handlers:
				logging.warning("Multiple handlers named %s; replacing previous value",spec.name)
			self.named_handlers[spec.name] = spec
			
			
#到目前为止 Application对象的成员变量有：
self.transforms #默认不设置，用于对返回数据方式和编码。
self.handlers	#按照主机模型首先区分，内容是：正则表达式对象和对应的handlers
self.settings	#配置文件 
self.ui_modules	#用于自定义模型展示，使用 {{ module Book(arg)}}，需要实现render方法
self.ui_methods #用于自定义模型展示，使用 {{ trim_string('a string that is too long............') }} 
self._wsgi