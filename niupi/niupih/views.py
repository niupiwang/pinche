from django.http import HttpResponse
from django.shortcuts import render, redirect
# Create your views here.
from django.urls import reverse

from App.models import User, Userdetail
from niupih.forms import AdminForm


def index(request):
    id = request.session.get('uid')
    print(id, 111111111)
    admin = Userdetail.objects.filter(user_uid=id).first()
    # print(admin.user_uid.username)
    return render(request, 'niupih/index.html', locals())


def login(request):
    if request.method == 'POST':
        admin = request.POST.get('admin')
        password = request.POST.get('password')
        admin = User.objects.filter(username=admin).first()
        print(admin, password)
        # print(admin.username, admin.password)
        if admin.password == password:
            request.session['uid'] = admin.uid
            return redirect(reverse('myadmin:index'), locals())
    return render(request, 'niupih/login-2.html', locals())


def logout(request):
    request.session.delete()
    return render(request, 'niupih/login-2.html', locals())


def order_list(request):
    return render(request, 'niupih/order_list.html', locals())


def user_list(request):
    id = request.session.get('uid')
    admin = Userdetail.objects.filter(user_uid=id).first()
    userdetail = Userdetail.objects.all()
    return render(request, 'niupih/user_list.html', locals())


def user_detail(request, uid=0):
    id = request.session.get('uid')
    admin = Userdetail.objects.filter(user_uid=id).first()
    userdetail = Userdetail.objects.filter(user_uid=uid).first()
    print(userdetail)
    return render(request, 'niupih/user_detail.html', locals())


# 不需要, 不修改用户信息
def user_update(request, uid=0):
    id = request.session.get('uid')
    admin = Userdetail.objects.filter(user_uid=id).first()
    return render(request, 'niupih/user_detail.html', locals())


def admin_add(request):
    id = request.session.get('uid')
    admin = Userdetail.objects.filter(user_uid=id).first()
    if request.method == 'POST':
        admin_name = request.POST.get('username')
        password = request.POST.get('password')
        re_password = request.POST.get('confirm_password')
        email = request.POST.get('email')
        if User.objects.filter(username=admin_name).first():
            res = '该管理员已经存在'
            return redirect(reverse('myadmin:admin_add'), locals())
        if password != re_password:
            return HttpResponse('密码不一致')
        print(request.POST, 111111)
        admin = User()
        admin.username = admin_name
        admin.password = password
        admin.type = 1
        admin.is_active = 1
        admin.phone = None
        # print(admin.username, admin.password)
        # user.save()
        # admin = User(username=admin_name, password=password)
    return render(request, 'niupih/admin_add.html', locals())


def admin_detail(request, uid=0):
    admin = Userdetail.objects.filter(user_uid=uid).first()
    return render(request, 'niupih/admin_detail.html', locals())


def admin_update(request, uid=0):
    id = request.session.get('uid')
    admin = Userdetail.objects.filter(user_uid=id).first()
    if request.method == 'POST':
        print(request.POST)
        admin.real_name = request.POST.get('real_name')
        admin.id_num = request.POST.get('id_num')
        admin.age = request.POST.get('age')
        admin.birthday = request.POST.get('birthday')
        admin.address = request.POST.get('address')
        admin.user_uid.phone = request.POST.get('phone')
        admin.save()
    return render(request, 'niupih/admin_detail.html', locals())


def car_list(request):
    id = request.session.get('uid')
    admin = Userdetail.objects.filter(user_uid=id).first()
    return render(request, 'niupih/car_list.html', locals())


def bus_list(request):
    id = request.session.get('uid')
    admin = Userdetail.objects.filter(user_uid=id).first()
    return render(request, 'niupih/bus_list2.html', locals())


def bus_detail(request):

    id = request.session.get('uid')
    admin = Userdetail.objects.filter(user_uid=id).first()
    return None


def bus_add(request):

    id = request.session.get('uid')
    admin = Userdetail.objects.filter(user_uid=id).first()
    return render(request, 'niupih/bus_add.html', locals())


def bus_delete(request, bid=0):

    id = request.session.get('uid')
    admin = Userdetail.objects.filter(user_uid=id).first()
    return render(request, 'niupih/bus_list3.html', locals())


def bus_update(request):

    id = request.session.get('uid')
    admin = Userdetail.objects.filter(user_uid=id).first()
    return None


