from django.core.validators import RegexValidator
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django import forms

from web import models


class LoginForm(forms.Form):
    username = forms.CharField(
        label='用户名',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': '请输入用户名',
            }
        ),
        validators=[RegexValidator(r'^\w{6,}$', '用户名格式错误')]
    )
    password = forms.CharField(
        label='密码',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': '请输入密码',
            }
        ),
    )


class LoginModelForm(forms.ModelForm):
    class Meta:
        model = models.UserInfo
        # 方式一：
        # fields = ['username', 'password']
        # 方式二：自动拿去所有字段
        fields = '__all__'
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
                    'placeholder': '请输入密码', },
            ),
        }


def login(request):
    if request.method == 'GET':
        return render(request, 'login.html', {'form': LoginForm()})
    form = LoginForm(request.POST)
    if form.is_valid():
        # 得到校验成功的字典
        # 进行数据库校验
        # 方式一：
        # user_object = models.UserInfo.objects.filter(username=form.cleaned_data['username'],
        #                                              password=form.cleaned_data['password']).first()
        # 方式二：
        user_object = models.UserInfo.objects.filter(**form.cleaned_data).first()
        if user_object:
            return HttpResponse("校验成功")
        else:
            return render(request, 'login.html', {'form': form, "error": "用户名或密码错误"})
    else:
        return render(request, 'login.html', {'form': form})


def department_list(request):
    queryset = models.Department.objects.all()
    return render(request, 'department_list.html', {'queryset': queryset})


class DepartmentModelForm(forms.ModelForm):
    class Meta:
        model = models.Department
        fields = '__all__'


def add_department(request):
    if request.method == 'GET':
        return render(request, 'department_form.html', {'form': DepartmentModelForm()})
    form = DepartmentModelForm(request.POST)
    if form.is_valid():
        form.save()  # 数据库保存
        return redirect('/department/list/')
    else:
        return render(request, 'department_form.html', {'form': DepartmentModelForm()})


def delete_department(request):
    did = request.GET.get('did')
    models.Department.objects.filter(id=did).delete()
    return redirect('/department/list/')


def edit_department(request):
    did = request.GET.get('did')
    department_object = models.Department.objects.filter(id=did).first()
    if request.method == 'GET':
        return render(request, 'department_form.html', {'form': DepartmentModelForm(instance=department_object)})

    form = DepartmentModelForm(data=request.POST, instance=department_object)
    if form.is_valid():
        form.save()  # 更新数据，而非新建数据，通过instance确定。
        return redirect('/department/list/')
    else:
        return render(request, 'department_form.html', {'form': form})
