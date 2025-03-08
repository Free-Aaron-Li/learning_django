from django.db import models


class Department(models.Model):
    """部门表"""
    title = models.CharField(verbose_name='部门名称', max_length=32)


class Admin(models.Model):
    """员工表"""
    username = models.CharField(verbose_name='用户名', max_length=32)
    password = models.CharField(verbose_name='密码', max_length=64)
    age = models.IntegerField(verbose_name='年龄', null=True, blank=True)  # 允许为空
    gender = models.IntegerField(
        verbose_name='性别',
        choices=(
            (1, '男'),
            (2, '女')
        ),
    )
    department = models.ForeignKey(verbose_name='部门', to='Department', on_delete=models.CASCADE)


class MobileNumber(models.Model):
    """靓号表"""
    mobile = models.CharField(verbose_name='手机号', max_length=11)
    # 无符号表
    price = models.PositiveIntegerField(verbose_name='价格', default=0)
    level = models.SmallIntegerField(
        verbose_name='号码等级',
        choices=(
            (1, '1级'),
            (2, '2级'),
            (3, '3级'),
            (4, '4级'),
        ),
        default=1
    )
    status_choices = (
        (1, '未分配'),
        (2, '已分配'),
    )
    status = models.SmallIntegerField(verbose_name='号码状态', choices=status_choices, default=2)
    admin = models.ForeignKey(verbose_name='管理员', to='Admin', on_delete=models.CASCADE)
