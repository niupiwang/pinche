import datetime

from django.contrib.auth import authenticate
from django.http import HttpResponse
from django.shortcuts import render, redirect
# Create your views here.
from django.urls import reverse

from App import form
from App.form import RegisterForm
from App.models import User, Userdetail, Car, Bus
from niupih.forms import AdminForm, BusForm


def index(request):
    id = request.session.get('uid')
    if id:
        admin = Userdetail.objects.filter(user_uid=id).first()
        return render(request, 'niupih/index.html', locals())
    return redirect(reverse('myadmin:login'), locals())


def login(request):
    if request.method == 'POST':
        admin_name = request.POST.get('admin')
        password = request.POST.get('password')
        admin = authenticate(request, username=admin_name, password=password, type=1)
        if admin:
            request.session['uid'] = admin.uid
            return redirect(reverse('myadmin:index'), locals())
    return render(request, 'niupih/login-2.html', locals())


def logout(request):
    request.session.delete()
    return redirect(reverse('myadmin:login'), locals())
    # return render(request, 'niupih/login-2.html', locals())


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
        # print(request.POST)
        form = AdminForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            admin_name = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            phone = form.cleaned_data.get('phone')
            print(admin_name, password, 11111)
            admin = User.objects.create_user(username=admin_name, password=password, phone=phone, type=1)
            # login(request, admin)
            admin_detail = Userdetail.objects.get_or_create(user_uid=admin)
            # admin_detail.save()
            return redirect(reverse('myadmin:admin_list'), locals())
            # return render(request, 'niupih/admin_add.html', locals())
        # return render(request, 'niupih/admin_add.html', locals())
    else:
        form = RegisterForm()
        return render(request, 'niupih/admin_add.html', locals())
    # if request.method == 'POST':
    #     admin_name = request.POST.get('username')
    #     password = request.POST.get('password')
    #     re_password = request.POST.get('confirm_password')
    #     admin = User.objects.create_user(a)
    #     email = request.POST.get('email')
    #     if User.objects.filter(username=admin_name).first():
    #         res = '该管理员已经存在'
    #         return redirect(reverse('myadmin:admin_add'), locals())
    #     if password != re_password:
    #         return HttpResponse('密码不一致')
    #     print(request.POST, 111111)
    #     admin = User()
    #     admin.username = admin_name
    #     admin.password = password
    #     admin.type = 1
    #     admin.is_active = 1
    #     admin.phone = None
        # print(admin.username, admin.password)
        # user.save()
        # admin = User(username=admin_name, password=password)
    return render(request, 'niupih/admin_add.html', locals())


def admin_lsit(request):
    id = request.session.get('uid')
    admin = Userdetail.objects.filter(user_uid=id).first()
    # admin = User.objects.filter(type=1)
    userdetail = Userdetail.objects.filter(user_uid__type=1)
    return render(request, 'niupih/user_list.html', locals())


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
        admin.birthday = request.POST.get('birthday').replace('年', '-').replace('月', '-').replace('日', '')
        # admin.birthday = datetime.datetime.strptime(request.POST.get('birthday'), '%Y-%m-%d')
        admin.address = request.POST.get('address')
        admin.user_uid.phone = request.POST.get('phone')
        admin.save()
    return render(request, 'niupih/admin_detail.html', locals())


def bus_list(request):
    id = request.session.get('uid')
    admin = Userdetail.objects.filter(user_uid=id).first()
    bus = Bus.objects.all().order_by('-bid')
    return render(request, 'niupih/bus_list2.html', locals())


def bus_detail(request, bid):
    id = request.session.get('uid')
    admin = Userdetail.objects.filter(user_uid=id).first()
    return render(request, 'niupih/bus_detail.html', locals())


def bus_add(request):
    id = request.session.get('uid')
    admin = Userdetail.objects.filter(user_uid=id).first()
    if request.method == 'POST':
        print(request.POST, 222222)
        bus = Bus()
        bus.num = request.POST.get('num')
        bus.bus_num = request.POST.get('bus_num')
        bus.start_city = request.POST.get('start_city')
        bus.end_city = request.POST.get('end_city')
        bus.start_station = request.POST.get('start_station')
        bus.end_station = request.POST.get('end_station')
        bus.start_time = (request.POST.get('start_time') + ' ' + request.POST.get('start_time1'))
        bus.ticket = request.POST.get('ticket')
        bus.price = request.POST.get('price')
        bus.standby_ticket = request.POST.get('ticket')
        hours = request.POST.get('hours')
        res = datetime.datetime.strptime(bus.start_time, "%Y-%m-%d %H:%M")
        bus.end_time = res + datetime.timedelta(hours=int(hours))
        bus.save()
        print(bus.end_time, bus.start_time)
        return redirect(reverse('myadmin:bus_list'), locals())
        # form = BusForm(request.POST)
        # if form.is_valid():
        #     print(form.cleaned_data, 11111111)
        #     bus = Bus()
        #     bus.num = form.cleaned_data.get('num')
        #     bus.bus_num = form.cleaned_data.get('bus_num')
        #     bus.start_city = form.cleaned_data.get('start_city')
        #     bus.end_city = form.cleaned_data.get('end_city')
        #     bus.start_station = form.cleaned_data.get('start_station')
        #     bus.end_station = form.cleaned_data.get('end_station')
        #     bus.start_time = (form.cleaned_data.get('start_time') + ' ' + form.cleaned_data.get('start_time1'))
        #     bus.price = form.cleaned_data.get('price')
        #     bus.ticket = form.cleaned_data.get('ticket')
        #     bus.standby_ticket = form.cleaned_data.get('ticket')
        #     hours = form.cleaned_data.get('hours')
        #     res = datetime.datetime.strptime(bus.start_time, "%Y-%m-%d %H:%M")
        #     bus.end_time = res + datetime.timedelta(hours=int(hours))
        #     print(bus.start_time, bus.end_time, 1111111)
        #     return redirect(reverse('myadmin:bus_list'), locals())
        # return render(request, 'niupih/bus_add.html', locals())
    else:
        form=BusForm()
        return render(request, 'niupih/bus_add.html', locals())


def bus_delete(request, bid=0):
    id = request.session.get('uid')
    admin = Userdetail.objects.filter(user_uid=id).first()
    bus = Bus.objects.all().order_by('-bid')
    bus_de = Bus.objects.filter(bid=bid).first()
    print(bus_de.num)
    bus_de.delete()
    return render(request, 'niupih/bus_list3.html', locals())


def bus_update(request):
    id = request.session.get('uid')
    admin = Userdetail.objects.filter(user_uid=id).first()
    return None


def car_list(request):
    id = request.session.get('uid')
    admin = Userdetail.objects.filter(user_uid=id).first()
    cars = Car.objects.all()
    return render(request, 'niupih/car_list.html', locals())


def car_detail(request, cid):
    return render(request, 'niupih/car_detail.html', locals())
