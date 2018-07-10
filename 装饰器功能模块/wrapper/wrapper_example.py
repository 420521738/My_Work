#!/usr/bin/env python
#coding:utf-8

# 在Fliter装饰器中，该函数是首先需要执行的，arg1和arg2是Excute函数传入的
def wrapper_before(arg1,arg2):
    if arg1 > 2:
        return None
    else:
        return arg1*arg2

# 在Fliter装饰器中，该函数是最后需要执行的，arg1和arg2是Excute函数传入的
# 该函数也有可能不执行，如果前面的wrapper_before函数以及Excute函数执行结果为None的话
def wrapper_after(arg1,arg2):
    return 100

# 执行装饰器，传入两个参数，这两个参数分别为函数wrapper_before和wrapper_after
def Filter(before_func,after_func):
    # main_func函数就是Excute 函数
    def outer(main_func):
        def wrapper(request,kargs):
            
            before_result = before_func(request,kargs)
            if(before_result != None):
                return before_result
            
            main_result = main_func(request,kargs)
            if(main_result != None):
                return main_result
            
            after_result = after_func(request,kargs)
            if(after_result != None):
                return after_result
            
        return wrapper
    return outer


# 主函数前使用装饰器，该装饰器执行是先执行wrapper_before函数，再执行Excute函数，最后执行wrapper_after函数
@Filter(wrapper_before, wrapper_after)
def Excute(arg1,arg2):
    return None

print Excute(3, 2)
