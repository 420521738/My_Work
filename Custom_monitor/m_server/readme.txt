m_server 结构：
└── m_server
    ├── conf
    │   ├── hosts.py
    │   ├── __init__.py
    │   ├── services
    │   │   ├── generic.py
    │   │   ├── __init__.py
    │   │   └── linux.py
    │   └── templates.py
    ├── core
    │   ├── global_setting.py
    │   ├── main_server.py
    │   └── redis_connector.py
    └── __init__.py

主程序是main_server.py：
主程序直接import程序redis_connector用于redis的连接；
import程序global_setting用于设定环境变量，也就是代码的家目录在哪里；
主程序间接import程序hosts客户端主机定义程序；

hosts程序直接import程序templates,用于定义基础服务类;
templates程序间接从services中import程序linux,用于定义基础监控类;
linux程序直接从generic中import程序DefaultService类,用于定义基础监控类中的基本监控类
