# 三、Django 进阶

## 3.1 Cookie 和 Session

项目登陆相关。

## 3.2 中间件

本质上中间件是一个类。

所有的请求都会经过中间件。

对于静态文件，在低版本或其他框架会因为中间件阻止🚫。

## 3.3 母板

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>布局</title>
    {% block css %}{% endblock %} <!-- 占位符 -->
</head>
<body>
<div style="height: 48px; background-color: pink"></div>
<div class="container"></div>
{% block content %}{% endblock %}
{% block js %}{% endblock %}
</body>
</html>
```

## 3.4 连表操作

```python
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

```

### 3.4.1 创建

```python
models.User.objects.create(name="张三", age=18, salary=10000, depart_id=1)

# 或者
depart_object = models.Department.objects.filter(id=1).first()
models.User.objects.create(name="张三", age=18, salary=10000, depart=depart_object)
```

### 3.4.2 查询

```python
# 构建条件
models.User.objects.filter(name='xx')
models.User.objects.filter(salary=xx)
models.User.objects.filter(depart_id=1)
models.User.objects.filter(depart__title='xx') # 连表查询，查询时通过“__”

# 获取数据
queryset = models.User.objects.all()
for row in queryset:
	row.id row.name row.age row.salary row.depart_id row.depart.title # 获取数据通过“.”跨表
```

