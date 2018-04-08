#!/usr/bin/env python
# -*- coding: utf-8 -*-

class SchoolMember:	###基类
	school_name = 'Oldboy Linux edu'
	def __init__(self,name,gender,nationality='CN'):	###基类有三个变量
		self.name = name
		self.gender = gender
		self.nation = nationality
	
	def tell(self):	###基类的方法
		print "Hi,my name is %s,I am from %s" % (self.name,self.nation)

class Student(SchoolMember):	###子类，继承父类SchoolMember
	def __init__(self,Name,Gender,Class,Score,Nationality='US'):	###子类有5个变量，默认参数Nationality放最后
		SchoolMember.__init__(self,Name,Gender,Nationality)	###子类继承父类的Name,Gender,Nationality变量
		self.Class = Class	###子类的self.Class变量
		self.Score = Score	###子类的self.Score变量
	def payTuition(self,amount):	###子类的方法
		if amount < 6499:
			print "Get the fuck off..."
		else:
			print "Welcome onboard..."

class Teacher(SchoolMember):
	def __init__(self,Name,Gender,Course,Salary,Nationality='FR'):
		SchoolMember.__init__(self,Name,Gender,Nationality)
		self.Course = Course
		self.Salary = Salary
	def teaching(self):
		print "I am teaching %s,I am making %s per month!" % (self.Course,self.Salary)

S1 = Student('陈秋飞','Male','Python','C+','JP')
S1.tell()		###子类调用基类中的tell方法
S1.payTuition(5000)	###子类调用自己的payTuition方法

S2 = Student('ShitTshirt','Male','Linux','B')
S2.tell()
S2.payTuition(6500)

T1 = Teacher('刘德华','Male','TeachingC++',5000)
T1.tell()
T1.teaching()
