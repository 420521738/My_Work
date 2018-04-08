#!/usr/bin/env python
# -*- coding: utf-8 -*-

class person:			###定义一个人的类
	assets = 0		###定义资产
	school_name = None	###学校的名称
	attraction = 0		###魅力值，满分是100分
	skills = []		###有什么技能
	love_status = None	###恋爱状态
	lover = None		###爱人是人
	job = None		###是做什么工作的
	company = None		###公司名称
	
	def __init__(self,name,sex,role):	###定义基类的初始化函数
		self.name = name
		self.sex = sex
		self.role = role
		print '\033[32;1m-\033[0m'*60
		if self.role == '富人':
			self.assets += 10000000
			self.attraction += 80
			print '\033[32;1m我的名字叫 %s ,我是一个 %s ,我有 ￥%s ,有钱的感觉真的很好！\033[0m' % (self.name,self.role,self.assets)
		elif self.role == '穷人':
			self.assets += 5000
			self.attraction += 40
			print '\033[32;1m我的名字叫 %s ,我是一个 %s ,我有 ￥%s ,我真的很讨厌我现在贫穷的生活，但是我却拿这无奈的生活没办法！\033[0m' % (self.name,self.role,self.assets)
		elif self.role == '美女':
			self.assets += 5000
			self.attraction += 90
			print '\033[32;1m我的名字叫 %s ,我是一个 %s ,我没有很多的钱，但是我长得很漂亮，美丽的容颜让我快乐和自信，但是我也不想永远的贫穷！\033[0m' % (self.name,self.role)
	
	def talk(self,msg,tone='正常'):	###这个方法的作用是：打印你想要说的话
		if tone == '正常':
			print '\033[32;1m%s:%s\033[0m' % (self.name,msg)
		elif tone == '生气':
			print '\033[31;1m%s:%s\033[0m' % (self.name,msg)
			
	def assets_balance(self,amount,action):		###资产剩余值，包括收入和支出
		if action == '挣钱':			###如果你挣了钱
			self.assets += amount		###amount是你赚到的钱
			print '\033[33;1m%s 赚了 ￥%s，现在你的剩余资产为 ￥%s!\033[0m' % (self.name,amount,self.assets)
		elif action == '花钱':			###如果你花了钱
			self.assets -= amount		###amount是你花的钱
			print '\033[34;1m%s 花了 ￥%s，现在你的剩余资产为 ￥%s!\033[0m' % (self.name,amount,self.assets)
	
###定义以下三个角色
###角色1
p1 = person('张三','男','富人')
p1.talk('哈哈 哈哈，大家好，我是本村土豪张三！')
p1.assets_balance(50000,'挣钱')
###角色2
p2 = person('李四','男','穷人')
p2.assets_balance(3000,'花钱')
###角色3
p3 = person('王昭君','女','美女')

###三个角色的状态
p2.love_status = '非单身'
p2.lover = p3
p2.talk('我是一个穷人，但是我有一个很漂亮的女朋友，我很爱她，她也很爱我，她的名字叫 %s!' % p2.lover.name) 

p3.love_status = '非单身'
p3.lover = p2
p3.talk(('我是一个很漂亮的女孩，但是我并不是很有钱，我有一个很爱我的男朋友，他的名字叫 %s，他并不是很有钱，反而有点穷，他长得也不帅，但是我很爱他，我相信靠我们的努力，我们的生活一定会好起来的!' % p3.lover.name),'生气')

###p2角色准备修改名字
print '%s 准备改他的名字！' % p2.name
p2.name = '赵五'
print '改成了',p2.name
print '%s 的爱人是 %s' % (p3.name,p3.lover.name)

####p1和p3角色发生了jian情
print "*"*50 + '\n %s 邂逅了 %s...' % (p3.name,p1.name)
print 'XXOOXXOOXXOOXXOO....'

###这两个bitch在一起了
p1.lover = p3
p3.lover = p1

###p2发现自己带了绿帽
print '%s 发现了这对狗男女，非常的伤心....' % p2.name
p2.lover = None

print '现在 %s 的男朋友由 %s 换成了 %s....' % (p3.name,p3.lover.name,p1.name)

###准备去培训技能
school_list = ['360','QQ','OldBOy']

def study():
	print school_list
	school = raw_input('请选择你要去的学校：')
	print '%s 在 %s 学习了几个月之后...' % (p2.name,school)
	return (school,'Python')
###从study函数返回中获取学习以及技能
school_name,skill = study()
p2.school_name = school_name
p2.skills.append(skill)

print '现在 %s 拥有了技能 %s，准备去腾讯面试!' % (p2.name,p2.skills)
