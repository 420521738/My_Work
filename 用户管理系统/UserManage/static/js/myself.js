(function(arg){
	//定义扩展函数
	arg.extend({
		//函数名叫做validate,参数是Login.html页面传进来的form id
		'validate':function(form){
			//针对form表单，找到出属性是submit的键，只要点击submit按钮，就触发以下的函数
			$(form).find(':submit').click(function(){
				//先设定初始标志为真
				var flag = true;
				//针对form表单，找出属性是text或者password的键，并进行轮询
				$(form).find(':text,:password').each(function(){
					//获取找到的text或者password属性的键的html中的name值
					var name = $(this).attr('name');
					//获取这个键是否有获取到值，也就是是否有输入信息
					var val = $(this).val();
					//如果text或者password属性的键的值为空
					if(!val || val.trim() == ''){
						flag = false;
						font = name+'不能为空!';
						html = "<span style='color:red;'>" + font + "</span>";
						//如果为空，那么遍历将键的值情况
						$(this).next().remove();
						//在键的后面打印html的信息，也就是上面拼接的span信息
						$(this).after(html);
					}else{
						//如果不为空
						html = "<span sytle='color:green;'>OK</span>"
						$(this).next().remove();
						$(this).after(html);
					}
				});
				return flag;
			});
		}
	});
})(jQuery)