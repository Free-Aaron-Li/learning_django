from django.shortcuts import render, redirect


# Create your views here.
def login(request):
    # 判断到底是post还是get请求
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        # 去请求体中获取数据，再校验
        username = request.POST.get('user')
        password = request.POST.get('pwd')

        # 校验
        if username == 'admin' and password == '123456':
            # 成功跳转到后台管理界面：index.html
            return redirect('/index/')
        else:
            # 失败返回登录页面
            return render(request, 'login.html', {'error': '用户名或密码错误'})


def index(request):
    # 1. 获取数据
    queryset = [
        {
            "id": 1,
            "phone": "+9112345678", "city": "上海",
        },
        {
            "id": 1,
            "phone": "+9112345678", "city": "北京",
        }, {
            "id": 1,
            "phone": "+9112345678", "city": "成都",
        }, {
            "id": 1,
            "phone": "+9112345678", "city": "武汉",
        }, {
            "id": 1,
            "phone": "+9112345678", "city": "深圳",
        },
    ]

    # 2. 通过页面渲染返回给用户（表格）
    return render(request, 'index.html', {'queryset': queryset})