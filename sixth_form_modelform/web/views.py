from django.core.validators import RegexValidator
from django.http import HttpResponse
from django.shortcuts import render
from django import forms


class RoleForm(forms.Form):
    user = forms.CharField(
        max_length=32,
        label='用户名',
        widget=forms.TextInput(
            attrs={"class": "form-control"},
        ),
        validators=[RegexValidator(r'^[0-9]+$', "请输入数字")]
    )  # 会生成一个input typ="text"标签
    password = forms.CharField(
        max_length=32,
        label='密码',
        widget=forms.PasswordInput(
            attrs={"class": "form-control"},
            render_value=True,  # 密码在render初始化时不会默认显示，必须显式声明
        ),  # 插件
    )
    # 方式一：
    # email = forms.EmailField(label='邮箱')
    email = forms.EmailField(
        label="邮箱",
        required=False,  # 允许为空
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


# Create your views here.
def add_role(request):
    if request == 'GET':
        form = RoleForm(
            initial={  # 表单初始化必须加上 CSRF TOKEN，否则无法渲染初始化项默认值
                "user": "root",
                "password": "123456",
                "email": "123@qq.com",
            }
        )
        return render(request, 'add_role.html', {"form": form})

    # POST请求，对用户提交数据进行校验
    form = RoleForm(data=request.POST)
    if form.is_valid():
        print("成功", form.cleaned_data)
        return HttpResponse("成功")
    else:
        # form.errors 包含了所有的错误信息
        print("失败：", form.errors)
        return render(request, 'add_role.html', {"form": form})
