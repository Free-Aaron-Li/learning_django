from django.shortcuts import render, redirect
from web import models


# Create your views here.
def login(request):
    """
    用户登陆
    """
    if request.method == 'GET':
        return render(request, 'login.html')
    username = request.POST.get('username')
    password = request.POST.get('password')

    # 1. 数据库校验
    #   1.1 MySQL
    #   1.2 SqlLite （Django 默认数据库）
    user_object = models.UserInfo.objects.filter(username=username, password=password).first()
    if user_object:
        # 2. 校验成功
        #   2.1 生成随机字符串
        #   2.2 返回到用户浏览器的cookie中
        #   2.3 存储到网站的session中，随机字符串+用户独有标识
        request.session["info"] = {"name": user_object.username, "id": user_object.id}
        return redirect("/home/")
        # 3. 校验失败
    else:
        return render(request, 'login.html', {'error': '用户名或密码错误'})


def home(request):
    # 中间件处理登陆问题
    return render(request, 'home.html', {"info_dict": request.info_dict})
