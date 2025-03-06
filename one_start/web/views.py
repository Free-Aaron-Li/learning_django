from django.shortcuts import render, redirect


def login(request):
    # 三种不同的返回方式
    # 方式一：
    # return HttpResponse("登陆界面")
    # 方式二：
    return render(request, "login.html")
    # 方式三：
    # return redirect("https://www.baidu.com")


"""
案例1：号码列表
"""
def phone_list(request):
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
    return render(request, 'phone_list.html', {"data": queryset})
