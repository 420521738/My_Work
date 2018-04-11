#!/usr/bin/env python
# --*-- coding: utf-8 --*--

import socket
import sys
### this line is Latest revision by qiufei ###
### 加载时间模块 ###
import time	

# windows does not have termios...
try:
    import termios
    import tty
    has_termios = True
except ImportError:
    has_termios = False


def interactive_shell(chan):
    if has_termios:
        posix_shell(chan)
    else:
        windows_shell(chan)


def posix_shell(chan):
    import select
    
    oldtty = termios.tcgetattr(sys.stdin)
    ### this line is Latest revision by qiufei ###
    ### 打开命令记录文件 ###
    f = file('/home/chenqiufei/Fortress_machine/record_comm/record.txt','a+')
    try:
        tty.setraw(sys.stdin.fileno())
        tty.setcbreak(sys.stdin.fileno())
        chan.settimeout(0.0)
    	### this line is Latest revision by qiufei ###
    	### 定义一个空的列表 ###
	records = []

        while True:
            r, w, e = select.select([chan, sys.stdin], [], [])
            if chan in r:
                try:
                    x = chan.recv(1024)
                    if len(x) == 0:
                        print '\r\n*** EOF\r\n',
                        break
                    sys.stdout.write(x)
                    sys.stdout.flush()
                except socket.timeout:
                    pass
    	    ### this line is Latest revision by qiufei ###
    	    ### 这段为主要的修改代码 ###
            if sys.stdin in r:		###屏幕接收的输入
                x = sys.stdin.read(1)	###每次只接收一个字符
		records.append(x)	###将接收到的字符串追加到records列表中
		if x == '\r':		###如果输入是回车键，回车键是\r
		    c_time = time.strftime('%Y-%m-%d %H:%M:%S')	###定义命令时间的格式
		    cmd = ''.join(records).replace('\r','\n')	###将records列表里的元素直接连接起来，如果有windows下的换行\r就替换成Linux下的\n换行
		    log = '%s %s' % (c_time,cmd)		###命令的记录为命令执行时间，空格，连接后的records列表，也就是整个命令，否则我们在输入命令时会出现一些tab符
		    f.write(log)	###将以时间-完整命令格式的操作记录写入命令记录文件
		    f.flush()		###将命令记录缓存刷到磁盘中
		    records = []	###将一条操作记录完整记录后，再清空records内容，继续下一条

                if len(x) == 0:
                    break
                chan.send(x)

    finally:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, oldtty)
    	### this line is Latest revision by qiufei ###
    	### 关闭打开的文件 ###
	f.close()

    
# thanks to Mike Looijmans for this code
def windows_shell(chan):
    import threading

    sys.stdout.write("Line-buffered terminal emulation. Press F6 or ^Z to send EOF.\r\n\r\n")
        
    def writeall(sock):
        while True:
            data = sock.recv(256)
            if not data:
                sys.stdout.write('\r\n*** EOF ***\r\n\r\n')
                sys.stdout.flush()
                break
            sys.stdout.write(data)
            sys.stdout.flush()
        
    writer = threading.Thread(target=writeall, args=(chan,))
    writer.start()
        
    try:
        while True:
            d = sys.stdin.read(1)
            if not d:
                break
            chan.send(d)
    except EOFError:
        # user hit ^Z or F6
        pass
