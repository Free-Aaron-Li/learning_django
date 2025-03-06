from django.db import models


class UserInfo(models.Model):  # 必须继承models.Model
    # 默认生成id领域，自增，主键
    name = models.CharField(verbose_name="姓名", max_length=32)  # varchar
    # 额外添加列，需要对其判断是否可以为空
    # 1. 设置可以为空
    # pwd = models.CharField(verbose_name="密码", max_length=64, null=True, blank=True)  # varchar
    # 2. 设置默认值
    # pwd = models.CharField(verbose_name="密码", max_length=64, default="11111")  # varchar
    # 3. 终端提供默认值
    pwd = models.CharField(verbose_name="密码", max_length=64)  # varchar
    age = models.IntegerField(verbose_name="年龄")  # int
    email = models.EmailField(verbose_name="邮箱", max_length=32)  # varchar
