from django.db import models


class Department(models.Model):
    title = models.CharField(verbose_name="部门名称", max_length=32)
    count = models.IntegerField(verbose_name="部门人数", default=1)
