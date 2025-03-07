from django.db import models


class UserInfo(models.Model):
    username = models.CharField(verbose_name="用户名", max_length=32)
    password = models.CharField(verbose_name="密码", max_length=64)
    age = models.IntegerField(verbose_name="年龄")
    phone_number = models.CharField(verbose_name="手机号", max_length=11)


class Department(models.Model):
    title = models.CharField(verbose_name="部门名称", max_length=32)


class User(models.Model):
    name = models.CharField(verbose_name="姓名", max_length=12)
    age = models.IntegerField(verbose_name="年龄")
    salary = models.DecimalField(verbose_name="工资")

    # 外键约束
    # 会自动生成为depart_id字段
    # on_delete=models.CASCADE: 级联删除（当部门被删除时，关联的字段全部都会被删除）
    # on_delete=models.SET_NULL: 置空（当部门被删除时，关联的字段置空）
    # on_delete=models.SET_DEFAULT: 置默认（当部门被删除时，关联的字段置为默认值）
    # on_delete=models.PROTECT: 防护（当部门被删除时，关联的字段报错）
    depart = models.ForeignKey(verbose_name="部门", to="Department", on_delete=models.CASCADE)
