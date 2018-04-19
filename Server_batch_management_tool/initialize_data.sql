create database manager_system default charset utf8;
use manager_system;
create table users( id int(10) unsigned not null primary key auto_increment, username char(20) not null, password char(20) not null, real_name char(20) not null );
create table manager1_server( id int(10) unsigned not null primary key auto_increment, ip char(20) not null, username char(20) not null, password char(20) not null, port int(11) not null, server_type char(20) not null );
insert into users values(null,'manager1','123456','zhangsan');
insert into users values(null,'manager2','123456','lisi');
insert into manager1_server values(null,'192.168.1.71','ihavecar','x+y-z=71',22612,'Test Server1');
insert into manager1_server values(null,'192.168.1.74','ihavecar','x+y-z=74',22612,'Test Server2');
insert into manager2_server values(null,'192.168.1.19','ihavecar','x+y-z=19',22,'Product Server1');
insert into manager2_server values(null,'192.168.1.37','ihavecar','x+y-z=37',22612,'Backup Server1');





