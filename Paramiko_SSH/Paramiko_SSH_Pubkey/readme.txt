paramiko的使用，通过密钥的方式。

如果没有key，则执行以下：
# ssh-keygen -t rsa
# ssh-copy-id -p 22612 -i ~/.ssh/id_rsa.pub ihavecar@192.168.1.71
ssh认证的过程是加密的，只要认证过后，通讯的数据都是明文传输的。

脚本执行方式：
# python paramiko_pkey.py 192.168.1.71 'free -m'