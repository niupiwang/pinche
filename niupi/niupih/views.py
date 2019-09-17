from django.http import HttpResponse
from django.shortcuts import render, redirect
# Create your views here.
from django.urls import reverse
from niupih.forms import AdminForm


def index(request):
    return render(request, 'niupih/base.html', locals())


def login(request):
    if request.method == 'POST':
        form = AdminForm()
        print(22222)
        if form.is_valid():
            print(11111)
            res = form.cleaned_data
            print(res, 2222)
        # admin = request.POST.get('admin')
        # password = request.POST.get('password')
        # if admin == 'king' and password == '123456':
        #     return redirect(reverse('niupih:index'))
        # print(request.POST, 111)
    return render(request, 'niupih/login-2.html', locals())


def logout(request):
    return render(request, 'niupih/login-2.html', locals())


def order_list(request):
    return render(request, 'niupih/order_list.html', locals())


def user_list(request):
    return render(request, 'niupih/user_list.html', locals())


def user_detail(request):
    return render(request, 'niupih/user_detail.html', locals())


def update_user(request, uid=0):
    return render(request, 'niupih/user_detail.html', locals())


def admin_add(request):
    return render(request, 'niupih/admin_add.html', locals())


def bus_list(request):
    return render(request, 'niupih/bus_list.html', locals())


def admin_detail(request):
    return render(request, 'niupih/user_detail.html', locals())


def car_list(request):
    return render(request, 'niupih/car_list.html', locals())