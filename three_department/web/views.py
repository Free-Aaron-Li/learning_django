from django.http import HttpResponse
from django.shortcuts import render, redirect
from web import models


def department(request):
    # ORM 操作
    # 1. 新增
    # 1.1 方式一：单条加入
    # models.Department.objects.create(title="开发部", count=10)
    # 1.2 方式二：字典加入
    # models.Department.objects.create(**{
    #     "title": "开发部",
    #     "count": 10
    # })

    # 2. 查询
    # 2.1 查询所有
    # queryset = models.Department.objects.all()
    # print(queryset)
    # for obj in queryset:
    #     print(obj.id, obj.title, obj.count)
    # 2.2 条件查询
    # queryset = models.Department.objects.filter(id__gt=1)  # id > 1
    # for obj in queryset:
    #     print(obj.id, obj.title, obj.count)
    # 2.3 查询单个对象
    # obj = models.Department.objects.filter(id=1).first()
    # print(obj.id, obj.title, obj.count)

    # 3. 删除
    # models.Department.objects.filter(id=1).delete()

    # 4. 更新
    # models.Department.objects.filter(id=2).update(count=20)

    # queryset = models.Department.objects.all().order_by("id") # asc 升序
    queryset = models.Department.objects.all().order_by("-id")  # desc 降序

    return render(request, 'department.html', {"queryset": queryset})


def add_department(request):
    """
    添加部门
    """
    # 显示添加部门页面
    if request.method == "GET":
        return render(request, 'add_department.html')
    # 提交部门的信息，新建
    title = request.POST.get("title")
    count = request.POST.get("count")
    models.Department.objects.create(title=title, count=count)
    # 跳转到部门列表页面
    return redirect("/department/")


def delete_department(request):
    """
    删除部门
    """
    department_id = request.GET.get('id')
    models.Department.objects.filter(id=department_id).delete()
    return redirect("/department/")


def edit_department(request):
    """
    编辑部门
    """
    # 从列表页面跳转过来的时候
    if request.method == "GET":
        department_id = request.GET.get('id')
        department_obj = models.Department.objects.filter(id=department_id).first()
        return render(request, 'edit_department.html', {'department_obj': department_obj})
    # 编辑并提交数据
    department_id = request.GET.get('id')
    title = request.POST.get('title')
    count = request.POST.get('count')
    models.Department.objects.filter(id=department_id).update(title=title, count=count)
    return redirect("/department/")
