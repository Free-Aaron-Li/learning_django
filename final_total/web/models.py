from django.db import models


class UserInfo(models.Model):
    username = models.CharField(verbose_name="用户名", max_length=32)
    password = models.CharField(verbose_name="密码", max_length=64)
    age = models.IntegerField(verbose_name="年龄")

class Department(models.Model):
    title= models.CharField(verbose_name="部门名称", max_length=32)
    count = models.IntegerField(verbose_name="部门人数")
