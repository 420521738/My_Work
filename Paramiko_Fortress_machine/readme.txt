本工具基于Paramiko的demo模块进行修改。实现以下需求：
需求
1、保垒机有一个公共账号，所有人都是用这个账号登陆保垒机，root用户只能由堡垒机管理员有权限可以登陆；
2、公共账号登陆保垒机->选择主机组->选择主机->选择你的普通用户->输入你的后端服务器的密码登陆；
3、登陆的后端服务器所操作过的命令要记录到文件。


此次代码结构介绍（3个目录，7个文件）
├── hosts_user
│   ├── qqandroid.txt       #qqandroid服的ip
│   ├── qqios.txt         #qqios服的ip
│   └── users.txt         #有权限登陆的用户
├── record_comm
│   └── record.txt           #记录用户操作过的命令文件
└── script
    ├── demo.py             #主程序文件
    ├── interactive.py        #被调用的记录用户操作过的命令的脚本
    └── zj.py              #登陆菜脚本