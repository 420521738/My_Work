from django.db import models

class UserInfo(models.Model):
    Name = models.CharField(max_length=40)
    Email = models.CharField(max_length=40)
    Phone = models.CharField(max_length=40)
