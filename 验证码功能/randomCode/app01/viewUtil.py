#!/usr/bin/env python
#coding:utf-8

from django.http import HttpResponse

#引入绘图模块
from PIL import Image, ImageDraw, ImageFont

#引入随机函数模块
import random
from io import BytesIO

def verifycode(request):
    #定义变量，用于画面的背景色、宽、高
    bgcolor = (random.randrange(20,100), random.randrange(20,100), 255)
    width = 100
    height = 35
    
    #创建画面对象
    im = Image.new('RGB', (width, height), bgcolor)
    
    #创建画笔对象
    draw = ImageDraw.Draw(im)
    
    #调用画笔的point()函数绘制噪点
    for i in range(0, 250):
        xy = (random.randrange(0, width), random.randrange(0, height))
        fill = (random.randrange(0, 255), 255, random.randrange(0, 255))
        draw.point(xy, fill=fill)
    
    #定义验证码的备选值
    str1 = 'ABCD123EFGHIJK456LMNOPQRS789TUVWXYZ0'
    
    #随机选取4个值作为验证码
    rand_str = ''
    for i in range(0, 4):
        rand_str += str1[random.randrange(0, len(str1))]
    
    #print '---------->',rand_str
    
    #构造字体颜色
    fontcolor = (255, random.randrange(0, 255), random.randrange(0, 255))
    
    #构造字体对象，这里需要注意，有很多地方说直接在这里写字体，但是直接写字体，不写绝对路径的话，程序会报错
    ft = ImageFont.truetype("C:\Windows\Fonts\STZHONGS.TTF", 23)
    
    #绘制4个字符
    draw.text((5, 2), rand_str[0], font=ft, fill=fontcolor)
    draw.text((25, 2), rand_str[1], font=ft, fill=fontcolor)
    draw.text((50, 2), rand_str[2], font=ft, fill=fontcolor)
    draw.text((75, 2), rand_str[3], font=ft, fill=fontcolor)
    
    #释放画笔
    del draw
    
    #将验证码存入session，用于做进一步验证
    request.session['verifycode'] = rand_str
    
    #内存文件操作
    buf = BytesIO()
    
    #将图片保存在内存中，文件类型为png
    im.save(buf, 'png')
    
    #将内存中的图片数据返回给客户端，MIME类型为图片png
    return HttpResponse(buf.getvalue(),content_type="image/png")
    

    #im.save(open('test2.png', 'wb'), 'png')
    #image_data = open('test2.png', 'rb').read()
    #return HttpResponse(image_data,content_type="image/png")
