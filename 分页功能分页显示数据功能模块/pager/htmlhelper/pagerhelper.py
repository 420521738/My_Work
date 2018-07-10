#!/usr/bin/env python
#coding:utf-8
from django.utils.safestring import mark_safe

# url前缀 /index/
# 每页显示数据条数
# 总页数
# 总条数
# 显示N个页

# 传入3个参数，一个是url前缀，一个是总的条数,一个是当前页
def page(baseurl,totalnum,currentpage):
    # 每页显示的条数
    perpage = 20
    # 显示前面N个页，可点击的
    pagenum = 11
    # 总页数，取余后，如果有余数，则总页数加1
    temp = divmod(totalnum, 20)
    totalpage = temp[0]
    if temp[1]:
        totalpage +=1
    
    # 如果总页数小于等于11页，则全部显示    
    if totalpage <=11:
        start = 1
        end = totalpage
    # 如果总页数不小于11页
    else:
        # 如果当前页大于等于6
        if currentpage >= 6:
            start = currentpage - 5
            end = currentpage + 6
        # 当前页数小于6页
        else:
            start = 1
            end = 12
        # 根据上面的if else得出的结果再进行判断，如果得到的end页大于总页数，那么end就是最后一页，start则需要减去11页
        if end > totalpage:
            end = totalpage
            start = end - 11
    
    # html这个列表里面的内容就是需要返回给view中index程序的数据
    html = []
    # 根据计算出的start和end页数，进行循环
    for i in range(start,end):
        # url则为/index/页数
        url = baseurl + str(i)
        # 先判断是否为当前页，如果是当前页，则需要额外添加类selected，就会变成橙色
        if i == currentpage:
            html.append('<a class="selected" href="'+url+'">'+str(i)+'</a>')
        else:
            html.append('<a href="'+url+'">'+str(i)+'</a>')
    # django.forms.Form 里找_html_output函数，看django是怎么返回的
    return mark_safe(''.join(html))
