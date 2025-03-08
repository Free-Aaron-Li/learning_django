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

## 3.5 Form 和 ModelForm

### 3.5.1 Form

Django 中的 Form 组件有 2 个重要作用：
1. 生成 HTML表单标签
2. 数据校验

快速上手：

```python
class MyForm(forms.Form):
	a1 = ...
	a2 = ...
```

在视图函数上：

```python
def xxx(request):
	if request.method == 'GET'
		form = MyForm()
		return render(request, "xxx.html",{"form":form})
		
	# 用户提交数据进行校验
	form = MyForm(data=request.POST)
	if form.is_valid(): 
		print("成功", form.clearned_data) # 提交成功的字典数据
	else:
		form.errors # 获取所有的错误信息
```

在 HTML 页面上：

```html
<form>
	{{form.a1}}
	{{form.a2}}
	<input type='submit' value=“提交” />
</form>
```

**示例**
 
**表单**：
```python
class RoleForm(forms.Form):  
    user = forms.CharField(  
        max_length=32,  
        label='用户名',  
        widget=forms.TextInput(  
            attrs={"class": "form-control"},  
        )  
    )  # 会生成一个input typ="text"标签  
    password = forms.CharField(  
        max_length=32,  
        label='密码',  
        widget=forms.PasswordInput(  
            attrs={"class": "form-control"},  
        ),  # 插件  
    )  
    # 方式一：  
    # email = forms.EmailField(label='邮箱')    email = forms.CharField(  
        label="邮箱",  
        # widget=forms.Textarea(), # 多行文本  
        widget=forms.EmailInput(  
            attrs={"class": "form-control"},  
        ),  
    )  
    city = forms.ChoiceField(  
        label='城市',  
        choices=(  
            ('bj', '北京'),  
            ('sh', '上海'),  
            ('sz', '深圳'),  
            ('cd', '成都'),  
        ),  
        widget=forms.Select(  
            attrs={"class": "form-control"},  
        )  
    )
```

HTML：

```html
{% extends 'layout.html' %}  
{% block title %}  
    <title>添加角色</title>  
{% endblock %}  
{% block content %}  
    <form>        {{ form.user }}  
        {{ form.password }}  
        {{ form.email }}  
        {{ form.city }}  
        <input type="submit" value="提交">  
    </form>  
{% endblock %}
```

初始化默认值：

```python
def add_role(request):  
    form = RoleForm(  
        initial={ # 表单初始化必须加上 CSRF TOKEN，否则无法渲染初始化项默认值  
            "user": "root",  
            "password": "123456",  
            "email": "123@qq.com",  
            "city": "bj",  
        }  
    )    return render(request, 'add_role.html', {"form": form})
```

初步校验：

```python
# POST请求，对用户提交数据进行校验  
form = RoleForm(data=request.POST)  
if form.is_valid():  
    print("成功", form.cleaned_data)  
    return HttpResponse("成功")  
else:  
    # form.errors 包含了所有的错误信息  
    print("失败：", form.errors)  
    return render(request, 'add_role.html', {"form": form})
```

```html
<form method="POST" novalidate>  
    {% csrf_token %}  
    <p>{{ form.user }}</p><span style="color: red;">{{ form.user.errors.0 }}</span>  
    <p>{{ form.password }}</p><span style="color: red;">{{ form.password.errors.0 }}</span>  
    <p>{{ form.email }}</p><span style="color: red;">{{ form.email.errors.0 }}</span>  
    <p>{{ form.city }}</p><span style="color: red;">{{ form.city.errors.0 }}</span>  
    <input type="submit" value="提交">  
</form>
```

自定义校验：

```python
user = forms.CharField(  
    max_length=32,  
    label='用户名',  
    widget=forms.TextInput(  
        attrs={"class": "form-control"},  
    ),  
    validators=[RegexValidator(r'^[0-9]+$', "请输入数字")]  # 正则表达式
)
```


### 3.5.2 ModelForm

```python
# models.py
class UserInfo(models.Model):  
    username = models.CharField(verbose_name="用户名", max_length=32)  
    password = models.CharField(verbose_name="密码", max_length=64)  
    age = models.IntegerField(verbose_name="年龄")
```

```python
# views.py
class LoginModelForm(forms.ModelForm):  
    class Meta:  
        model = models.UserInfo  
        # 方式一：  
        # fields = ['username', 'password']        # 方式二：自动拿去所有字段        fields = '__all__'  
        widgets = {  
            "username": forms.TextInput(  
                attrs={  
                    'class': 'form-control',  
                    'placeholder': '请输入用户名',  
                },  
            ),  
            "password": forms.PasswordInput(  
                attrs={  
                    'class': 'form-control',  
                    'placeholder': '请输入密码',},  
            ),  
        }
```

默认显示数据 + 保存数据

```python
# 保存数据
obj = LoginModelForm(data=request.POST)
obj.save() # 省去 models...create(...)


# 显示数据
obj = models.UserInfo.objects.filter(id=1).first()
obj = LoginModelForm(instance=obj)
```

## 3.6 总结

单独知识点需要知道是什么？
- Cookie 和 Session
- 中间件
- 母板
- 连表操作
- Form
- ModelForm