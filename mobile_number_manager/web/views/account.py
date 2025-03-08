from io import BytesIO

from django import forms
from django.core.validators import RegexValidator
from django.shortcuts import render, HttpResponse, redirect

from utils.check_code import check_code
from utils.encrypt import sha256
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
    )
    password = forms.CharField(
        label='密码',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': '请输入密码',
            },
            render_value=True  # 保留密码
        ),
    )
    code = forms.CharField(
        label="验证码",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "输入验证码",
                "maxlength": "5",
            },
        ),
        validators=[
            RegexValidator(
                regex="^[A-Za-z0-9]{5}$",
                message="验证码必须为5位字母或数字"
            )
        ],
        error_messages={
            "required": "验证码不能为空",
            "max_length": "验证码不得超过5个字符"
        }
    )


def login(request):
    """用户登陆"""
    if request.method == 'GET':
        return render(request, 'login.html', {"form": LoginForm()})

    form = LoginForm(data=request.POST)
    if not form.is_valid():
        return render(request, 'login.html', {"form": form})
    # 1. 判断验证码是否正确
    check_code_image = request.session.get('image_code')
    if not check_code_image:
        form.add_error('code', '验证码已过期')
    if check_code_image.upper() != form.cleaned_data['code'].upper():
        form.add_error('code', '验证码错误')
        return render(request, 'login.html', {"form": form})

    # 验证码正确，去数据库校验用户名和密码
    username = form.cleaned_data['username']
    password = form.cleaned_data['password']
    # 密码加密
    encrypt_password = sha256(password)
    admin_object = models.Admin.objects.filter(username=username, password=encrypt_password).first()
    if not admin_object:
        return render(request, 'login.html', {"form": form, "error": "用户名或密码错误"})
    else:
        request.session['info'] = {"id": admin_object.id, "username": admin_object.username}
        request.session.set_expiry(60 * 60 * 24 * 7)  # 保存7天登陆信息
        return redirect("/home/")


def image_code(request):
    # 1.生成图片
    img_object, code_str = check_code()
    # 2.图片的内容返回
    stream = BytesIO()
    # 将图片写入stream中
    img_object.save(stream, 'png')
    # 3. 将图片的内容写入Session中，超时时间：60s
    request.session['image_code'] = code_str
    request.session.set_expiry(60)
    return HttpResponse(stream.getvalue())


def home(request):
    return render(request, 'home.html')


def logout(request):
    request.session.clear()
    return redirect("/login/")
