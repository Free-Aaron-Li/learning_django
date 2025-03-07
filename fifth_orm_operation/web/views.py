from django.shortcuts import render, redirect

from web import models


# Create your views here.
def user_list(request):
    # 从数据库中获取所有数据
    return render(request, 'user_list.html', {"queryset": models.User.objects.all()})


def user_add(request):
    if request.method == "GET":
        depart_queryset = models.Department.objects.all()
        return render(request, 'user_add.html', {"depart_queryset": depart_queryset})
    name = request.POST.get("name")
    age = request.POST.get("age")
    salary = request.POST.get("salary")
    depart_id = request.POST.get("depart")  # 得到的是选择项的ID
    models.User.objects.create(name=name, age=age, salary=salary, depart_id=depart_id)
    return redirect("/user/list/")
