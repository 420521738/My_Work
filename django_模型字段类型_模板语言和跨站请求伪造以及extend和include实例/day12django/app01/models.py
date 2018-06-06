from django.db import models
from django.db.models.fields import BooleanField
from django.template.defaultfilters import default

# Create your models here.
class FirstModel(models.Model):
    UserName = models.CharField(max_length=20)
    
class ThirdModel(models.Model):
    Nid = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=20,default='qiufei')
    Cname = models.CharField(max_length=20,default='chen')
    Gender = models.NullBooleanField()
    Age = models.IntegerField(default=1)
    CaiPiao = models.CommaSeparatedIntegerField(max_length=256,null=True,help_text="Don't dubo")
    #Date = models.DateField(auto_now_add=True)
    #DateTime = models.DateTimeField(auto_now=True,default='2017-06-04')
    
class FourthModel(models.Model):
    Price = models.DecimalField(max_digits=10,decimal_places=2)
    IP = models.IPAddressField()
    #IP2 = models.GenericIPAddressField()
    
class ColorDic(models.Model):
    ColorNmae = models.CharField(max_length=20)
    def __unicode__(self):
        return self.ColorNmae
    
class Person(models.Model):
    Name = models.CharField(max_length=20)
    Gender = models.BooleanField(default=False)
    Color = models.ForeignKey(ColorDic)
    
class AuthorList(models.Model):
    Name = models.CharField(max_length=10)
    
    
class Book(models.Model):
    BookName = models.CharField(max_length=10)
    Author = models.ManyToManyField(AuthorList)
    

    




    